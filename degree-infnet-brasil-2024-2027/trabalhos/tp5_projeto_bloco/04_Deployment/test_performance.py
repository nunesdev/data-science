#!/usr/bin/env python3
"""
Benchmark temporário — TP4 ConectaFood
Mede pico de RAM e latência de POST /processar_texto com descrições reais do CSV.

Uso:
  cd 04_Deployment
  pip install psutil pandas
  python test_performance.py

Saída: JSON no stdout e arquivo test_performance_resultado.json na mesma pasta.
"""
from __future__ import annotations

import json
import platform
import statistics
import sys
import threading
import time
from pathlib import Path

import pandas as pd
import psutil
from fastapi.testclient import TestClient

from api import app

CSV_PATH = Path(__file__).resolve().parents[1] / "02_Data_Ingestion_Understanding" / "projetos_sociais.csv"
OUT_PATH = Path(__file__).resolve().parent / "test_performance_resultado.json"
WARMUP_REQUESTS = 1
REPETICOES_POR_TEXTO = 3


def selecionar_amostras(csv_path: Path, k: int = 5) -> list[dict]:
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["Descrição", "Nome"])
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
    detalhes_inferencias: list[dict] = []

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
                cpu_amostras: list[float] = []
                t0 = time.perf_counter()
                proc.cpu_percent(interval=None)
                resp = client.post(
                    "/processar_texto",
                    json={"texto": amostra["texto"], "tipo_analise": "sentimento"},
                )
                elapsed_ms = (time.perf_counter() - t0) * 1000
                cpu_amostras.append(proc.cpu_percent(interval=None))
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
                }
            )

    stop.set()
    thread.join(timeout=2)

    todas_latencias = [
        item["latencia_media_ms"] for item in latencias_por_texto for _ in range(REPETICOES_POR_TEXTO)
    ]
    # recalcular média global a partir das médias por texto (ponderação igual)
    media_global_ms = round(statistics.mean([x["latencia_media_ms"] for x in latencias_por_texto]), 2)

    resultado = {
        "ambiente": {
            "python": platform.python_version(),
            "plataforma": platform.platform(),
            "processador": platform.processor() or platform.machine(),
            "nucleos_logicos": psutil.cpu_count(logical=True),
            "device_inferencia": "CPU (device=-1 no pipeline; CUDA não utilizada)",
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
    }

    OUT_PATH.write_text(json.dumps(resultado, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(resultado, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())