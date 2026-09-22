import streamlit as st
import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io

# 1. Configuração inicial da página
st.set_page_config(page_title="ConectaFood - TP2", page_icon="🌱", layout="wide")

# 2. Implementação de Cache para ganho de performance
@st.cache_data
def carregar_dados_iniciais(caminho):
    try:
        return pd.read_csv(caminho)
    except FileNotFoundError:
        # Retorna um DataFrame vazio com as colunas esperadas caso o arquivo não exista
        return pd.DataFrame(columns=['Nome', 'Atuação', 'Site', 'Descrição'])

# Carrega os dados coletados via web scraping na TP1
caminho_csv = '../02_Data_Ingestion_Understanding/projetos_sociais.csv'
df_inicial = carregar_dados_iniciais(caminho_csv)

# 3. Gerenciamento de Estado de Sessão (Session State)
if 'dados' not in st.session_state:
    # Armazena o dataframe inicial na sessão para que não seja resetado a cada interação
    st.session_state['dados'] = df_inicial

# Interface - Título e Descrição
st.title("🌱 ConectaFood: Inteligência e Dados para Fome Zero")
st.markdown("""
Esta plataforma conecta estabelecimentos com excedente de alimentos a ONGs. 
**ODS Alinhados:** ODS 2 (Fome Zero) e ODS 12 (Consumo Responsável).
""")

# 4. Serviço de Upload de Arquivos na Barra Lateral (Interatividade)
st.sidebar.header("⚙️ Ferramentas de Dados")
arquivo_upload = st.sidebar.file_uploader("Adicionar novos dados (CSV)", type=["csv"])

if arquivo_upload is not None:
    try:
        df_novo = pd.read_csv(arquivo_upload)
        # Atualiza o estado de sessão concatenando os dados antigos com os novos
        st.session_state['dados'] = pd.concat([st.session_state['dados'], df_novo], ignore_index=True)
        st.sidebar.success("Novos dados incorporados com sucesso!")
    except Exception as e:
        st.sidebar.error(f"Erro ao ler o arquivo: {e}")

df_atual = st.session_state['dados']

# 5. Interface de Usuário Dinâmica (Filtros interativos)
st.header("Exploração de ONGs Parceiras")
if not df_atual.empty:
    atuacoes_disponiveis = df_atual['Atuação'].dropna().unique().tolist()
    filtro_atuacao = st.multiselect(
        "Filtre os projetos pela área de atuação:",
        options=atuacoes_disponiveis,
        default=atuacoes_disponiveis
    )
    
    # Aplica o filtro
    df_filtrado = df_atual[df_atual['Atuação'].isin(filtro_atuacao)]
    
    st.dataframe(df_filtrado, use_container_width=True)
    
    # 6. Serviço de Download de Arquivos
    csv_download = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar Dados Filtrados (CSV)",
        data=csv_download,
        file_name='projetos_filtrados.csv',
        mime='text/csv'
    )
    
    # 7. Exibição de Estatísticas e Nuvem de Palavras
    st.header("📈 Insights e Estatísticas")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Distribuição por Atuação")
        # Gráfico de barras simples usando st.bar_chart
        contagem_atuacao = df_filtrado['Atuação'].value_counts()
        st.bar_chart(contagem_atuacao)
        
    with col2:
        st.subheader("Nuvem de Palavras das Descrições")
        textos = " ".join(df_filtrado['Descrição'].dropna().tolist())
        
        if textos.strip():
            # Gera a nuvem de palavras
            wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='Greens').generate(textos)
            
            # Plota usando matplotlib
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
        else:
            st.info("Não há descrições suficientes para gerar a nuvem de palavras.")
            
else:
    st.warning("Nenhum dado encontrado. Por favor, verifique o arquivo original ou faça o upload de uma nova base.")