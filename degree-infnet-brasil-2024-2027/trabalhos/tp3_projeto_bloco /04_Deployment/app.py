import streamlit as st
import pandas as pd
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt

st.set_page_config(page_title="ConectaFood - TP3", page_icon="🌱", layout="wide")

# URL da API FastAPI (rodando localmente)
API_URL = "http://localhost:8000"
CAMINHO_CSV = '../02_Data_Ingestion_Understanding/projetos_sociais.csv'

# Menu de Navegação Lateral
st.sidebar.title("Navegação")
pagina = st.sidebar.radio("Ir para:", ["🏠 Home", "📊 Dashboard Analítico", "🔌 Integração API"])

# --- PÁGINA 1: HOME ---
if pagina == "🏠 Home":
    st.title("🌱 ConectaFood: Inteligência e Dados para Fome Zero")
    st.markdown("""
    Bem-vindo ao **ConectaFood**! Esta plataforma foi evoluída para utilizar múltiplas páginas, 
    integração via APIs (FastAPI) e coleta de dados dinâmicos (Selenium).
    
    **ODS Alinhados:** ODS 2 (Fome Zero) e ODS 12 (Consumo Responsável).
    """)
    st.image("https://images.unsplash.com/photo-1593113563332-f144cc7516d2?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80", use_container_width=True)

# --- PÁGINA 2: DASHBOARD ---
elif pagina == "📊 Dashboard Analítico":
    st.title("📊 Exploração de ONGs Parceiras")
    
    try:
        df = pd.read_csv(CAMINHO_CSV)
        
        # Filtros
        atuacoes = df['Atuação'].dropna().unique().tolist()
        filtro = st.multiselect("Filtre por Atuação:", options=atuacoes, default=atuacoes)
        df_filtrado = df[df['Atuação'].isin(filtro)]
        
        st.dataframe(df_filtrado, use_container_width=True)
        
        # Download
        st.download_button("📥 Baixar Dados Filtrados (CSV)", df_filtrado.to_csv(index=False), "filtrados.csv", "text/csv")
        
        # Estatísticas
        st.header("📈 Insights")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Por Atuação")
            st.bar_chart(df_filtrado['Atuação'].value_counts())
        with col2:
            st.subheader("Nuvem de Palavras")
            textos = " ".join(df_filtrado['Descrição'].dropna().tolist())
            if textos:
                wc = WordCloud(width=800, height=400, background_color='white', colormap='Greens').generate(textos)
                fig, ax = plt.subplots()
                ax.imshow(wc, interpolation='bilinear')
                ax.axis('off')
                st.pyplot(fig)
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")

# --- PÁGINA 3: INTEGRAÇÃO API ---
elif pagina == "🔌 Integração API":
    st.title("🔌 Interação com a API FastAPI")
    st.markdown("Nesta página, a aplicação não lê o CSV diretamente, ela faz requisições HTTP para a API FastAPI.")
    
    # GET - Buscar da API
    if st.button("Buscar Dados da API (GET)"):
        try:
            resposta = requests.get(f"{API_URL}/ongs")
            if resposta.status_code == 200:
                st.success("Dados recebidos da API!")
                st.dataframe(pd.DataFrame(resposta.json()))
            else:
                st.warning("API não encontrada. Você iniciou o servidor Uvicorn?")
        except requests.exceptions.ConnectionError:
            st.error("Falha na conexão. Verifique se o FastAPI está rodando na porta 8000.")
            
    st.divider()
    
    # POST - Enviar para a API
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
                else:
                    st.error("Erro ao registrar.")
            except:
                st.error("Erro de conexão com a API.")