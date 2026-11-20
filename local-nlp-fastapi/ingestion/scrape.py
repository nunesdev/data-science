"""
Coleta de projetos sociais do Observatório do 3º Setor (BeautifulSoup) com append deduplicado.
"""
from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup

URL_OBSERVATORIO = (
    "https://observatorio3setor.org.br/lista-conheca-projetos-sociais-de-15-causas-diferentes/"
)
ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data" / "projetos_sociais.csv"
COLUNAS = ["Nome", "Atuação", "Site", "Descrição"]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
}


def _normalizar_site(site: str) -> str:
    site = site.strip()
    if site and not site.startswith(("http://", "https://")):
        return f"https://{site}"
    return site


def _limpar_descricao(desc: str) -> str:
    desc = desc.strip()
    for sufixo in ("Voltar", "voltar"):
        if desc.endswith(sufixo):
            desc = desc[: -len(sufixo)].strip()
    return desc


def extrair_projetos_do_html(soup: BeautifulSoup) -> list[dict]:
    projetos: list[dict] = []
    projeto_atual: dict[str, str] = {}

    for p in soup.find_all("p"):
        texto = p.get_text(strip=True)
        if not texto:
            continue

        if texto.startswith("Atuação:"):
            projeto_atual["Atuação"] = texto.replace("Atuação:", "").strip()
            strong = p.find("strong")
            if strong:
                projeto_atual["Nome"] = strong.get_text(strip=True)
            else:
                prev_p = p.find_previous_sibling("p")
                if prev_p and prev_p.find("strong"):
                    projeto_atual["Nome"] = prev_p.find("strong").get_text(strip=True)

        elif texto.startswith("Site:"):
            link = p.find("a")
            if link and link.has_attr("href"):
                projeto_atual["Site"] = _normalizar_site(str(link["href"]))
            else:
                projeto_atual["Site"] = _normalizar_site(texto.replace("Site:", "").strip())

        elif texto.startswith("O que faz:"):
            projeto_atual["Descrição"] = _limpar_descricao(texto.replace("O que faz:", ""))
            if projeto_atual.get("Nome"):
                projetos.append(
                    {
                        "Nome": projeto_atual.get("Nome", "").strip(),
                        "Atuação": projeto_atual.get("Atuação", "").strip(),
                        "Site": projeto_atual.get("Site", "").strip(),
                        "Descrição": projeto_atual.get("Descrição", "").strip(),
                    }
                )
            projeto_atual = {}

    return projetos


def coletar_dados_online(url: str = URL_OBSERVATORIO) -> list[dict]:
    print(f"Acessando: {url} ...")
    response = requests.get(url, headers=HEADERS, timeout=60)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    return extrair_projetos_do_html(soup)


def _chave_dedup(registro: dict) -> str:
    nome = re.sub(r"\s+", " ", registro.get("Nome", "").lower()).strip()
    site = registro.get("Site", "").lower().strip()
    return f"{nome}|{site}"


def apendar_ao_csv(novos: list[dict]) -> tuple[int, int]:
    """Retorna (total de linhas, inseridos nesta execução)."""
    if not novos:
        if CSV_PATH.exists():
            return len(pd.read_csv(CSV_PATH)), 0
        return 0, 0

    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    if CSV_PATH.exists():
        df_existente = pd.read_csv(CSV_PATH).fillna("")
    else:
        df_existente = pd.DataFrame(columns=COLUNAS)

    for col in COLUNAS:
        if col not in df_existente.columns:
            df_existente[col] = ""

    existentes_chaves = {_chave_dedup(row) for _, row in df_existente.iterrows()}

    apenas_novos: list[dict] = []
    for reg in novos:
        reg = {col: str(reg.get(col, "")).strip() for col in COLUNAS}
        reg["Descrição"] = _limpar_descricao(reg["Descrição"])
        if not reg["Nome"]:
            continue
        chave = _chave_dedup(reg)
        if chave not in existentes_chaves:
            apenas_novos.append(reg)
            existentes_chaves.add(chave)

    if not apenas_novos:
        df_existente.to_csv(CSV_PATH, index=False, encoding="utf-8")
        return len(df_existente), 0

    df_novos = pd.DataFrame(apenas_novos, columns=COLUNAS)
    df_final = pd.concat([df_existente, df_novos], ignore_index=True)
    df_final.to_csv(CSV_PATH, index=False, encoding="utf-8")
    return len(df_final), len(apenas_novos)


def main() -> None:
    projetos = coletar_dados_online()
    print(f"Projetos extraídos na página: {len(projetos)}")
    total, inseridos = apendar_ao_csv(projetos)
    print(f"CSV atualizado: {inseridos} novo(s) registro(s); total {total} linha(s) em {CSV_PATH.name}.")


if __name__ == "__main__":
    main()