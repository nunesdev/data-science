"""
Coleta dinâmica (Selenium) do Observatório do 3º Setor e integração ao CSV principal.

Os registros extraídos são acrescentados em `projetos_sociais.csv`, usado pela API e pelo Streamlit.
"""
from __future__ import annotations

import re
import time
from pathlib import Path

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

URL_OBSERVATORIO = (
    "https://observatorio3setor.org.br/lista-conheca-projetos-sociais-de-15-causas-diferentes/"
)
DIR_BASE = Path(__file__).resolve().parent
CSV_PRINCIPAL = DIR_BASE / "projetos_sociais.csv"
CSV_AUDITORIA = DIR_BASE / "dados_coletados_selenium.csv"
COLUNAS = ["Nome", "Atuação", "Site", "Descrição"]


def _normalizar_site(site: str) -> str:
    site = site.strip()
    if site and not site.startswith(("http://", "https://")):
        return f"https://{site}"
    return site


def extrair_projetos_dos_paragrafos(paragrafos) -> list[dict]:
    """Mesma lógica de blocos do coleta_dados.py, adaptada aos elementos Selenium."""
    projetos: list[dict] = []
    projeto_atual: dict[str, str] = {}

    for p in paragrafos:
        texto = (p.text or "").strip()
        if not texto:
            continue

        if texto.startswith("Atuação:"):
            projeto_atual["Atuação"] = texto.replace("Atuação:", "").strip()
            try:
                nome = p.find_element(By.TAG_NAME, "strong").text.strip()
                if nome:
                    projeto_atual["Nome"] = nome
            except NoSuchElementException:
                pass

        elif texto.startswith("Site:"):
            try:
                link = p.find_element(By.TAG_NAME, "a")
                href = link.get_attribute("href")
                projeto_atual["Site"] = _normalizar_site(href or texto.replace("Site:", "").strip())
            except NoSuchElementException:
                projeto_atual["Site"] = _normalizar_site(texto.replace("Site:", "").strip())

        elif texto.startswith("O que faz:"):
            projeto_atual["Descrição"] = texto.replace("O que faz:", "").strip()
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


def _chave_dedup(registro: dict) -> str:
    nome = re.sub(r"\s+", " ", registro.get("Nome", "").lower()).strip()
    site = registro.get("Site", "").lower().strip()
    return f"{nome}|{site}"


def apendar_ao_csv_principal(novos: list[dict]) -> tuple[int, int]:
    """Retorna (total_apos_merge, quantidade_inserida_nesta_execucao)."""
    if not novos:
        return 0, 0

    if CSV_PRINCIPAL.exists():
        df_existente = pd.read_csv(CSV_PRINCIPAL).fillna("")
    else:
        df_existente = pd.DataFrame(columns=COLUNAS)

    for col in COLUNAS:
        if col not in df_existente.columns:
            df_existente[col] = ""

    existentes_chaves = {_chave_dedup(row) for _, row in df_existente.iterrows()}

    apenas_novos = []
    for reg in novos:
        reg = {col: str(reg.get(col, "")).strip() for col in COLUNAS}
        if not reg["Nome"]:
            continue
        chave = _chave_dedup(reg)
        if chave not in existentes_chaves:
            apenas_novos.append(reg)
            existentes_chaves.add(chave)

    if not apenas_novos:
        df_existente.to_csv(CSV_PRINCIPAL, index=False, encoding="utf-8")
        return len(df_existente), 0

    df_novos = pd.DataFrame(apenas_novos, columns=COLUNAS)
    df_final = pd.concat([df_existente, df_novos], ignore_index=True)
    df_final.to_csv(CSV_PRINCIPAL, index=False, encoding="utf-8")

    df_novos.to_csv(CSV_AUDITORIA, index=False, encoding="utf-8")
    return len(df_final), len(apenas_novos)


def coletar_dados_dinamicos() -> None:
    print("Iniciando o Selenium WebDriver...")
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument("--headless=new")
    opcoes.add_argument("--no-sandbox")
    opcoes.add_argument("--disable-dev-shm-usage")

    servico = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servico, options=opcoes)

    try:
        print(f"Acessando: {URL_OBSERVATORIO}")
        driver.get(URL_OBSERVATORIO)
        time.sleep(3)

        paragrafos = driver.find_elements(By.TAG_NAME, "p")
        print(f"Parágrafos encontrados na página: {len(paragrafos)}")

        projetos = extrair_projetos_dos_paragrafos(paragrafos)
        print(f"Projetos estruturados na coleta Selenium: {len(projetos)}")

        total, inseridos = apendar_ao_csv_principal(projetos)
        print(
            f"Integração concluída: {inseridos} novo(s) registro(s) "
            f"acrescentado(s) a '{CSV_PRINCIPAL.name}' (total {total} linhas)."
        )
        if inseridos:
            print(f"Snapshot dos novos registros salvo em '{CSV_AUDITORIA.name}'.")
        else:
            print("Nenhum registro inédito (base já continha os itens ou página sem blocos novos).")
    finally:
        driver.quit()


if __name__ == "__main__":
    coletar_dados_dinamicos()