import re
import unicodedata
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

st.set_page_config(
    page_title="ConectaFood — Dashboard",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://localhost:8000"
CAMINHO_CSV = (
    Path(__file__).resolve().parent.parent
    / "02_Data_Ingestion_Understanding"
    / "projetos_sociais.csv"
)

TEMAS = [
    ("Alimentação e combate à fome", ["alimento", "refeic", "fome", "comida", "nutri"]),
    ("Infância", ["crianca", "adolescente", "infanc"]),
    ("Educação", ["educa", "escola", "leitura", "vestibular"]),
    ("Mulheres e equidade de gênero", ["mulher", "genero", "femin"]),
    ("Pessoas em situação de rua", ["situacao de rua"]),
    ("Povos indígenas", ["indigen"]),
    ("Meio ambiente e clima", ["meio ambiente", "clima", "conserv", "biodivers", "agroecolog"]),
    ("Saúde e inclusão", ["saude", "deficien", "psicolog", "reabilit", "alcool", "paralis", "droga"]),
    ("Refúgio e migração", ["refug", "migrant", "imigrant"]),
    ("Pessoas idosas", ["idos", "velho"]),
    ("Proteção animal", ["animal", "caes", "gatos", "canil", "gatil"]),
]

PERFIS = [
    "Investidor social",
    "Voluntário",
    "Empresa (agenda ESG)",
    "Doador de alimentos",
    "Gestor público",
]


def _sem_acento(texto: str) -> str:
    base = unicodedata.normalize("NFD", str(texto).lower())
    return "".join(caractere for caractere in base if unicodedata.category(caractere) != "Mn")


def _carregar_csv() -> pd.DataFrame:
    df = pd.read_csv(CAMINHO_CSV).fillna("")
    for coluna in ["Nome", "Atuação", "Site", "Descrição"]:
        if coluna not in df.columns:
            df[coluna] = ""
        df[coluna] = df[coluna].astype(str).str.strip()
    return df


def _base_analitica(df: pd.DataFrame) -> pd.DataFrame:
    nome = df["Nome"].map(_sem_acento)
    atuacao = df["Atuação"].map(_sem_acento)
    teste = nome.isin({"teste", "test", "xxx"}) | atuacao.str.startswith("teste")
    return df.loc[~teste & df["Nome"].ne("")].copy()


def _temas_da_linha(nome: str, descricao: str) -> list[str]:
    texto = _sem_acento(f"{nome} {descricao}")
    achados = [rotulo for rotulo, chaves in TEMAS if any(chave in texto for chave in chaves)]
    return achados or ["Outros"]


def _contagem_temas(df: pd.DataFrame) -> pd.Series:
    contagem: dict[str, int] = {}
    for _, linha in df.iterrows():
        for tema in _temas_da_linha(linha["Nome"], linha["Descrição"]):
            contagem[tema] = contagem.get(tema, 0) + 1
    serie = pd.Series(contagem, dtype="int64").sort_values(ascending=False)
    return serie


def _cobertura(valor: str) -> str:
    texto = str(valor).strip()
    baixo = _sem_acento(texto)
    if not texto or baixo in {"nan", "none"}:
        return "Não informado"
    if any(p in baixo for p in ["mundial", "paises", "incluindo o brasil"]):
        return "Internacional"
    if any(p in baixo for p in ["todo o pais", "em todo o pais", "brasil"]):
        return "Nacional"
    if texto.count(",") >= 2:
        return "Vários estados"
    parte = re.sub(r"(?i)^sede em\s+", "", texto.split(",")[0]).strip()
    if len(parte) > 40:
        return parte[:37] + "..."
    return parte or "Não informado"


def _detalhe_http(resposta: requests.Response) -> str:
    try:
        corpo = resposta.json()
    except ValueError:
        return resposta.text or f"HTTP {resposta.status_code}"
    detalhe = corpo.get("detail", corpo) if isinstance(corpo, dict) else corpo
    if isinstance(detalhe, list):
        return "; ".join(str(item) for item in detalhe)
    if isinstance(detalhe, dict):
        return str(detalhe.get("mensagem") or detalhe)
    return str(detalhe)


def _exibir_recomendacao(dados: dict) -> None:
    st.caption(
        f"Modelo `{dados.get('modelo', 'n/d')}` · "
        f"{dados.get('ongs_no_contexto', 0)} organizações no contexto · "
        f"perfil: {dados.get('perfil', '')}"
    )
    st.markdown(dados.get("resumo") or "")

    recomendacoes = dados.get("recomendacoes") or []
    if not recomendacoes:
        st.warning("O agente não confirmou organizações do catálogo para este interesse.")
    for indice, item in enumerate(recomendacoes, start=1):
        st.markdown("---")
        st.subheader(f"{indice}. {item.get('nome', 'Organização')}")
        colunas = st.columns(3)
        colunas[0].markdown(f"**Cobertura**  \n{item.get('atuacao') or '—'}")
        colunas[1].markdown(f"**Pilar ESG**  \n{item.get('pilar_esg') or '—'}")
        site = item.get("site") or ""
        if site.startswith("http"):
            colunas[2].markdown(f"**Site**  \n[{site}]({site})")
        else:
            colunas[2].markdown(f"**Site**  \n{site or '—'}")
        ods = item.get("ods") or []
        if ods:
            st.markdown("**ODS:** " + " · ".join(ods))
        st.write(item.get("justificativa") or "")

    impacto = dados.get("impacto_ods") or ""
    if impacto:
        st.markdown("#### Impacto na Agenda 2030")
        st.write(impacto)
    passos = dados.get("proximos_passos") or []
    if passos:
        st.markdown("#### Próximos passos")
        for passo in passos:
            st.markdown(f"- {passo}")


def pagina_dashboard() -> None:
    st.title("Dashboard de Ciência de Dados")
    st.markdown(
        """
        Os dados das organizações foram coletados no Observatório do 3º Setor
        (BeautifulSoup e Selenium) e ficam em `projetos_sociais.csv`.
        A primeira aba explora esse catálogo. A segunda envia o mesmo arquivo
        como contexto para o agente ESG da Groq (gpt-oss-120b, com fallback), que recomenda com quem se conectar
        e explica o efeito da parceria nos ODS.
        """
    )

    try:
        df = _carregar_csv()
    except FileNotFoundError:
        st.error(f"CSV não encontrado em `{CAMINHO_CSV}`.")
        return
    except Exception as exc:
        st.error(f"Não foi possível ler o CSV: {exc}")
        return

    aba_dados, aba_agente = st.tabs(["Visão geral e dados", "Agente inteligente ESG"])

    with aba_dados:
        analitico = _base_analitica(df)
        temas = _contagem_temas(analitico)
        cobertura = analitico["Atuação"].map(_cobertura).value_counts()
        raras = cobertura[cobertura < 2]
        if not raras.empty:
            cobertura = cobertura[cobertura >= 2].copy()
            cobertura.loc["Outras localidades"] = int(raras.sum())
            cobertura = cobertura.sort_values(ascending=False)
        excluidos = len(df) - len(analitico)

        c1, c2, c3 = st.columns(3)
        c1.metric("Registros no CSV", len(df))
        c2.metric("Usados nos gráficos", len(analitico))
        c3.metric("Tema mais citado", temas.index[0] if not temas.empty else "—")
        if excluidos:
            st.caption(
                f"{excluidos} registro(s) sem nome ou de teste ficam na tabela e saem dos gráficos."
            )

        st.dataframe(df, width="stretch", hide_index=True)
        st.download_button(
            "Baixar catálogo (CSV)",
            df.to_csv(index=False).encode("utf-8"),
            "projetos_sociais.csv",
            "text/csv",
        )

        st.subheader("Leitura do catálogo")
        grafico_tema, grafico_cobertura = st.columns(2)
        with grafico_tema:
            st.markdown("**Organizações por área temática**")
            st.bar_chart(temas, height=360)
            st.caption("Uma organização pode entrar em mais de um tema. A regra é por palavras da descrição.")
        with grafico_cobertura:
            st.markdown("**Organizações por cobertura**")
            st.bar_chart(cobertura, height=360)
            st.caption(
                "A coluna Atuação descreve onde a organização atua. "
                "Localidades com uma única organização entram em Outras localidades."
            )

        with st.expander("Como estes gráficos foram calculados"):
            st.markdown(
                """
                A fonte não traz uma coluna de causa social: `Atuação` é a cobertura geográfica.
                O gráfico temático procura termos nas colunas Nome e Descrição
                (educação, fome, mulheres, clima, e outros). Isso é uma leitura exploratória,
                separada do modelo de sentimento e do agente.

                O sentimento do TP4 classifica um texto sob demanda e não fica gravado no CSV,
                então não há distribuição de estrelas para plotar.
                """
            )

    with aba_agente:
        st.subheader("Matchmaker ESG")
        st.markdown(
            """
            Descreva o apoio que você quer oferecer. A API lê o CSV, monta o contexto
            e pede ao modelo uma decisão: quais organizações fazem sentido e quais ODS
            essa conexão fortalece. Cada consulta é independente.
            """
        )

        with st.form("form_agente"):
            interesse = st.text_area(
                "Qual é o seu interesse?",
                value="Quero investir em projetos de educação para crianças",
                height=120,
            )
            coluna_perfil, coluna_limite = st.columns(2)
            perfil = coluna_perfil.selectbox("Perfil de quem decide", PERFIS)
            limite = coluna_limite.slider("Quantidade de recomendações", 1, 5, 3)
            enviar = st.form_submit_button("Pedir recomendação")

        if enviar:
            texto = interesse.strip()
            if len(texto) < 10:
                st.warning("Descreva o interesse com pelo menos 10 caracteres.")
            else:
                payload = {"interesse": texto, "perfil": perfil, "limite": int(limite)}
                try:
                    with st.spinner("Consultando o agente ESG..."):
                        resposta = requests.post(
                            f"{API_URL}/agente_recomendacao",
                            json=payload,
                            timeout=90,
                        )
                    if resposta.status_code == 200:
                        dados = resposta.json()
                        st.session_state["ultima_recomendacao"] = dados
                    else:
                        st.error(f"A API retornou HTTP {resposta.status_code}.")
                        st.write(_detalhe_http(resposta))
                except requests.exceptions.ConnectionError:
                    st.error(
                        "Sem conexão com a API. Na raiz do projeto, com o venv ativo: "
                        "`uvicorn --app-dir 04_Deployment api:app --reload`"
                    )
                except requests.exceptions.Timeout:
                    st.error("A consulta passou de 90 segundos. Tente de novo.")

        ultima = st.session_state.get("ultima_recomendacao")
        if ultima:
            _exibir_recomendacao(ultima)


def pagina_sentimento() -> None:
    st.title("Análise de sentimento")
    st.markdown(
        """
        Classifica o tom de uma descrição em **1 a 5 estrelas** com o modelo local
        `nlptown/bert-base-multilingual-uncased-sentiment`, via `POST /processar_texto`.
        O resultado não é gravado no CSV.
        """
    )
    exemplo = (
        "Organização sem fins lucrativos que redistribui alimentos excedentes "
        "para comunidades em situação de vulnerabilidade, promovendo dignidade e sustentabilidade."
    )
    with st.form("form_sentimento"):
        descricao = st.text_area("Descrição da ONG", value=exemplo, height=180)
        enviar = st.form_submit_button("Analisar sentimento")

    if not enviar:
        return
    if len(descricao.strip()) < 10:
        st.warning("Informe pelo menos 10 caracteres de texto.")
        return

    payload = {"texto": descricao.strip(), "tipo_analise": "sentimento"}
    try:
        with st.spinner("Processando com o modelo local..."):
            resposta = requests.post(f"{API_URL}/processar_texto", json=payload, timeout=120)
        if resposta.status_code == 200:
            dados = resposta.json()
            st.success(dados.get("resultado", "Análise concluída."))
            st.metric("Estrelas", f"{dados.get('estrelas', 0)} / 5")
            confianca = dados.get("confianca")
            if confianca is not None:
                st.metric("Confiança do modelo", f"{confianca:.1%}")
            st.caption(f"Modelo: `{dados.get('modelo', 'N/A')}`")
        else:
            st.error(f"Erro da API (HTTP {resposta.status_code}).")
            st.write(_detalhe_http(resposta))
    except requests.exceptions.ConnectionError:
        st.error("Falha na conexão. Inicie a API na porta 8000.")
    except requests.exceptions.Timeout:
        st.error("Tempo esgotado. O modelo pode estar carregando na primeira execução.")


def pagina_cadastro() -> None:
    st.title("Cadastro via API")
    st.markdown("Estas ações falam com o FastAPI. A listagem e o cadastro alteram o mesmo CSV do dashboard.")

    if st.button("Buscar organizações (GET /ongs)"):
        try:
            resposta = requests.get(f"{API_URL}/ongs", timeout=15)
            if resposta.status_code == 200:
                st.dataframe(pd.DataFrame(resposta.json()), width="stretch", hide_index=True)
            else:
                st.error(_detalhe_http(resposta))
        except requests.exceptions.ConnectionError:
            st.error("Falha na conexão. Verifique se o FastAPI está na porta 8000.")

    st.divider()
    st.subheader("Adicionar organização (POST /ongs)")
    with st.form("form_api"):
        nome = st.text_input("Nome da ONG")
        atuacao = st.text_input("Cobertura ou área de atuação")
        site = st.text_input("Site ou contato")
        descricao = st.text_area("Descrição")
        enviar = st.form_submit_button("Enviar para a API")
        if enviar:
            payload = {"Nome": nome, "Atuação": atuacao, "Site": site, "Descrição": descricao}
            try:
                resposta = requests.post(f"{API_URL}/ongs", json=payload, timeout=15)
                if resposta.status_code == 200:
                    st.success("Organização registrada no CSV.")
                else:
                    st.error(_detalhe_http(resposta))
            except requests.exceptions.ConnectionError:
                st.error("Erro de conexão com a API.")


st.sidebar.title("ConectaFood")
st.sidebar.caption("Versão final · TP5")
pagina = st.sidebar.radio(
    "Ir para",
    ["Dashboard", "Análise de sentimento", "Cadastro via API"],
    label_visibility="collapsed",
)
st.sidebar.markdown("---")
st.sidebar.markdown("**Agenda 2030 no catálogo**")
st.sidebar.caption(
    "ODS 2 Fome Zero, 4 Educação, 5 Igualdade de gênero, "
    "10 Redução das desigualdades, 12 Consumo responsável e 13 Ação climática."
)
try:
    saude = requests.get(f"{API_URL}/", timeout=1.5)
    if saude.ok:
        st.sidebar.success("API online")
    else:
        st.sidebar.warning("API respondeu com erro")
except requests.RequestException:
    st.sidebar.info("API offline. A visão geral lê o CSV direto. O agente precisa da API.")

if pagina == "Dashboard":
    pagina_dashboard()
elif pagina == "Análise de sentimento":
    pagina_sentimento()
else:
    pagina_cadastro()
