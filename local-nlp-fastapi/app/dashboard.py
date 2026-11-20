from __future__ import annotations

import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st
from wordcloud import WordCloud

st.set_page_config(page_title="ConectaFood", page_icon="🌱", layout="wide")

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000").rstrip("/")
ROOT = Path(__file__).resolve().parents[1]
CSV_FALLBACK = ROOT / "data" / "projetos_sociais.csv"

st.sidebar.title("Navegação")
pagina = st.sidebar.radio(
    "Ir para:",
    ["🏠 Home", "📊 Dashboard Analítico", "🔌 Integração API", "💬 Análise de Sentimento"],
)


@st.cache_data(ttl=30)
def carregar_ongs_via_api() -> tuple[pd.DataFrame | None, str | None]:
    try:
        resposta = requests.get(f"{API_URL}/ongs", timeout=15)
        if resposta.status_code == 200:
            return pd.DataFrame(resposta.json()), None
        return None, f"API respondeu HTTP {resposta.status_code}."
    except requests.exceptions.ConnectionError:
        return None, "API indisponível."


def carregar_ongs_fallback() -> pd.DataFrame:
    if not CSV_FALLBACK.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {CSV_FALLBACK}")
    return pd.read_csv(CSV_FALLBACK).fillna("")


def obter_dataframe_ongs() -> tuple[pd.DataFrame, str]:
    df_api, erro = carregar_ongs_via_api()
    if df_api is not None:
        return df_api, "api"
    df = carregar_ongs_fallback()
    fonte = "offline (CSV local)"
    if erro:
        fonte = f"{fonte} — {erro}"
    return df, fonte


if pagina == "🏠 Home":
    st.title("🌱 ConectaFood: Inteligência e Dados para Fome Zero")
    st.markdown(
        """
        Bem-vindo ao **ConectaFood**! Plataforma com múltiplas páginas,
        API FastAPI e coleta de dados de ONGs (Observatório do 3º Setor).

        **ODS alinhados:** ODS 2 (Fome Zero) e ODS 12 (Consumo Responsável).
        """
    )
    st.image(
        "https://images.unsplash.com/photo-1593113563332-f144cc7516d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        use_container_width=True,
    )

elif pagina == "📊 Dashboard Analítico":
    st.title("📊 Exploração de ONGs Parceiras")

    try:
        df, fonte = obter_dataframe_ongs()
        st.caption(f"Fonte dos dados: **{fonte}** (`{API_URL}/ongs` quando a API está no ar).")

        atuacoes = df["Atuação"].dropna().unique().tolist()
        filtro = st.multiselect("Filtre por Atuação:", options=atuacoes, default=atuacoes)
        df_filtrado = df[df["Atuação"].isin(filtro)]

        st.dataframe(df_filtrado, use_container_width=True)
        st.download_button(
            "📥 Baixar Dados Filtrados (CSV)",
            df_filtrado.to_csv(index=False),
            "filtrados.csv",
            "text/csv",
        )

        st.header("📈 Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Por Atuação")
            st.bar_chart(df_filtrado["Atuação"].value_counts())
        with col2:
            st.subheader("Nuvem de Palavras")
            textos = " ".join(df_filtrado["Descrição"].dropna().astype(str).tolist())
            if textos.strip():
                wc = WordCloud(
                    width=800,
                    height=400,
                    background_color="white",
                    colormap="Greens",
                ).generate(textos)
                fig, ax = plt.subplots()
                ax.imshow(wc, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")

elif pagina == "🔌 Integração API":
    st.title("🔌 Interação com a API FastAPI")
    st.markdown("Esta página consome apenas a API FastAPI (HTTP).")

    if st.button("Buscar Dados da API (GET)"):
        try:
            resposta = requests.get(f"{API_URL}/ongs")
            if resposta.status_code == 200:
                st.success("Dados recebidos da API!")
                st.dataframe(pd.DataFrame(resposta.json()))
            else:
                st.warning("API não encontrada. Você iniciou o servidor Uvicorn?")
        except requests.exceptions.ConnectionError:
            st.error("Falha na conexão. Verifique se o FastAPI está rodando.")

    st.divider()

    st.subheader("Adicionar nova ONG via API (POST)")
    with st.form("form_api"):
        nome = st.text_input("Nome da ONG")
        atuacao = st.text_input("Área de Atuação")
        site = st.text_input("Site ou Contato")
        desc = st.text_area("Descrição (O que faz)")
        submit = st.form_submit_button("Enviar para a API")

        if submit:
            payload = {"Nome": nome, "Atuação": atuacao, "Site": site, "Descrição": desc}
            try:
                res = requests.post(f"{API_URL}/ongs", json=payload)
                if res.status_code == 200:
                    st.success("ONG registrada via API com sucesso!")
                    carregar_ongs_via_api.clear()
                else:
                    st.error("Erro ao registrar.")
            except requests.exceptions.ConnectionError:
                st.error("Erro de conexão com a API.")

elif pagina == "💬 Análise de Sentimento":
    st.title("💬 Análise de Sentimento (modelo local)")
    st.markdown(
        """
        Digite a **descrição de uma ONG** (em português) para classificar o tom do texto
        em **1 a 5 estrelas**, via API FastAPI.
        """
    )

    exemplo = (
        "Organização sem fins lucrativos que redistribui alimentos excedentes "
        "para comunidades em situação de vulnerabilidade, promovendo dignidade e sustentabilidade."
    )

    with st.form("form_sentimento"):
        descricao = st.text_area(
            "Descrição da ONG",
            value=exemplo,
            height=180,
            help="Mínimo de 10 caracteres.",
        )
        enviar = st.form_submit_button("Analisar sentimento")

    if enviar:
        if len(descricao.strip()) < 10:
            st.warning("Informe pelo menos 10 caracteres de texto.")
        else:
            payload = {"texto": descricao.strip(), "tipo_analise": "sentimento"}
            try:
                with st.spinner("Processando com o modelo local..."):
                    res = requests.post(f"{API_URL}/processar_texto", json=payload, timeout=120)
                if res.status_code == 200:
                    dados = res.json()
                    estrelas = dados.get("estrelas", 0)
                    st.success(dados.get("resultado", "Análise concluída."))
                    st.metric("Estrelas", f"{estrelas} / 5")
                    conf = dados.get("confianca")
                    if conf is not None:
                        st.metric("Confiança do modelo", f"{conf:.1%}")
                    if dados.get("truncado"):
                        st.info("O texto excedeu 512 tokens; a inferência usou truncamento automático.")
                    st.caption(f"Modelo: `{dados.get('modelo', 'N/A')}`")
                elif res.status_code == 503:
                    st.error(
                        "Modelo indisponível (503). Verifique se a API carregou "
                        "`torch`/`transformers` na inicialização."
                    )
                    try:
                        st.json(res.json())
                    except Exception:
                        st.text(res.text)
                elif res.status_code == 422:
                    st.error("Dados inválidos (422).")
                    st.json(res.json())
                else:
                    st.error(f"Erro da API (HTTP {res.status_code}).")
                    try:
                        st.json(res.json())
                    except Exception:
                        st.text(res.text)
            except requests.exceptions.ConnectionError:
                st.error("Falha na conexão. Inicie a API: `uvicorn api.main:app --reload` (na raiz do projeto).")
            except requests.exceptions.Timeout:
                st.error("Tempo esgotado. O modelo pode estar baixando pesos na primeira execução.")