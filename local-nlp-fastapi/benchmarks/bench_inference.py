"""Benchmark local: RAM peak and POST /processar_texto latency on real NGO descriptions."""
from __future__ import annotations

import json
import platform
import statistics
import sys
import threading
import time
from pathlib import Path

import pandas as pd

try:
    import psutil
except ImportError:
    exe = sys.executable
    print(
        "Missing dependency: psutil for this interpreter:\n"
        f"  {exe}\n"
        "Install into the same environment:\n"
        f"  {exe} -m pip install -r requirements.txt\n"
        "If you use a venv, confirm: which python  →  .../local-nlp-fastapi/venv/bin/python",
        file=sys.stderr,
    )
    raise SystemExit(1)

import torch
from fastapi.testclient import TestClient

from api.main import app

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "projetos_sociais.csv"
OUT_PATH = Path(__file__).resolve().parent / "results.json"
WARMUP_REQUESTS = 1
REPETICOES_POR_TEXTO = 3


def selecionar_amostras(csv_path: Path, k: int = 5) -> list[dict]:
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["Descrição", "Nome"])
    df = df[df["Nome"].astype(str).str.strip() != ""]
    df["Descrição"] = df["Descrição"].astype(str)
    df = df[df["Descrição"].str.len() >= 30]
    df["len_chars"] = df["Descrição"].str.len()
    df = df.sort_values("len_chars")
    if len(df) < k:
        raise ValueError("CSV com poucas descrições para o benchmark.")

    indices = [0, len(df) // 4, len(df) // 2, (3 * len(df)) // 4, len(df) - 1]
    amostras = []
    for idx in indices[:k]:
        row = df.iloc[idx]
        amostras.append(
            {
                "nome_ong": str(row["Nome"]),
                "tamanho_chars": int(row["len_chars"]),
                "texto": row["Descrição"],
            }
        )
    return amostras


def monitorar_memoria(stop: threading.Event, pico_mb: list[float]) -> None:
    proc = psutil.Process()
    while not stop.is_set():
        rss_mb = proc.memory_info().rss / (1024**2)
        pico_mb[0] = max(pico_mb[0], rss_mb)
        time.sleep(0.05)


def main() -> int:
    proc = psutil.Process()
    baseline_mb = proc.memory_info().rss / (1024**2)
    pico_mb = [baseline_mb]

    stop = threading.Event()
    thread = threading.Thread(target=monitorar_memoria, args=(stop, pico_mb), daemon=True)
    thread.start()

    amostras = selecionar_amostras(CSV_PATH)
    latencias_por_texto: list[dict] = []

    device_note = (
        "CUDA" if torch.cuda.is_available() else "CPU (pipeline device=-1 when CUDA unavailable)"
    )

    t_carga_inicio = time.perf_counter()
    with TestClient(app) as client:
        t_carga_fim = time.perf_counter()
        tempo_carga_s = t_carga_fim - t_carga_inicio

        health = client.get("/")
        if health.status_code != 200:
            print("Falha no GET /", file=sys.stderr)
            return 1
        if not health.json().get("nlp_disponivel"):
            print("Modelo NLP não carregou (503). Verifique torch/transformers.", file=sys.stderr)
            return 1

        for _ in range(WARMUP_REQUESTS):
            client.post(
                "/processar_texto",
                json={"texto": amostras[0]["texto"][:200], "tipo_analise": "sentimento"},
            )

        for amostra in amostras:
            tempos_ms: list[float] = []
            ultima_resposta = None
            for _ in range(REPETICOES_POR_TEXTO):
                t0 = time.perf_counter()
                resp = client.post(
                    "/processar_texto",
                    json={"texto": amostra["texto"], "tipo_analise": "sentimento"},
                )
                elapsed_ms = (time.perf_counter() - t0) * 1000
                tempos_ms.append(elapsed_ms)
                if resp.status_code == 200:
                    ultima_resposta = resp.json()

            latencias_por_texto.append(
                {
                    "nome_ong": amostra["nome_ong"],
                    "tamanho_chars": amostra["tamanho_chars"],
                    "latencia_media_ms": round(statistics.mean(tempos_ms), 2),
                    "latencia_min_ms": round(min(tempos_ms), 2),
                    "latencia_max_ms": round(max(tempos_ms), 2),
                    "estrelas": ultima_resposta.get("estrelas") if ultima_resposta else None,
                    "confianca": ultima_resposta.get("confianca") if ultima_resposta else None,
                    "resultado": ultima_resposta.get("resultado") if ultima_resposta else None,
                    "truncado": ultima_resposta.get("truncado") if ultima_resposta else None,
                }
            )

    stop.set()
    thread.join(timeout=2)

    media_global_ms = round(statistics.mean([x["latencia_media_ms"] for x in latencias_por_texto]), 2)

    resultado = {
        "ambiente": {
            "python": platform.python_version(),
            "plataforma": platform.platform(),
            "processador": platform.processor() or platform.machine(),
            "nucleos_logicos": psutil.cpu_count(logical=True),
            "device_inferencia": device_note,
        },
        "memoria_mb": {
            "baseline_antes_carga": round(baseline_mb, 1),
            "pico_durante_teste": round(pico_mb[0], 1),
            "delta_aproximado": round(pico_mb[0] - baseline_mb, 1),
        },
        "tempo_carga_modelo_s": round(tempo_carga_s, 2),
        "repeticoes_por_texto": REPETICOES_POR_TEXTO,
        "amostras": latencias_por_texto,
        "latencia_media_global_ms": media_global_ms,
        "modelo": "nlptown/bert-base-multilingual-uncased-sentiment",
        "dataset_csv": str(CSV_PATH.relative_to(ROOT)),
        "linhas_dataset": len(pd.read_csv(CSV_PATH)),
    }

    OUT_PATH.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())