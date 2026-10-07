import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração inicial da página
st.set_page_config(page_title="Apuração Eleitoral TSE", layout="wide")

st.title("📊 Painel de Apuração - Base Oficial TSE")
st.markdown("Consolidação de votos utilizando o Boletim de Urna Web (Dados Abertos).")

@st.cache_data
def load_data():
    # Carrega os dados com o separador corrigido para vírgula
    df = pd.read_csv("dado_filtrado/dados_palmas_completo.csv", sep=",", encoding="latin1", low_memory=False)
    
    # Substituir os valores nulos oficiais do TSE (-1) por 0 nas colunas numéricas
    cols_numericas = ['QT_VOTOS', 'QT_APTOS', 'QT_COMPARECIMENTO', 'QT_ABSTENCOES']
    for col in cols_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            df.loc[df[col] == -1, col] = 0

    # Garantir que campos de identificação sejam strings para os filtros
    df['NR_ZONA'] = df['NR_ZONA'].astype(str)
    df['NR_SECAO'] = df['NR_SECAO'].astype(str)
    df['NR_LOCAL_VOTACAO'] = df['NR_LOCAL_VOTACAO'].astype(str)
    df['NR_VOTAVEL'] = df['NR_VOTAVEL'].astype(str)
    
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Ficheiro 'dados_palmas_completo.csv' não encontrado. Extraia o ficheiro do TSE na mesma pasta deste script.")
    st.stop()

# ==========================================
# BARRA LATERAL (Filtros)
# ==========================================
st.sidebar.header("Filtros de Análise")

# 1. NOVO: Filtro de Regiões
regioes_disponiveis = ["Todas as Regiões", "Taquarucu", "Taquaralto", "Aurenys", "Buritirana", "Plano Diretor Sul", "Plano Diretor Norte"]
regiao_selecionada = st.sidebar.selectbox("Região da Cidade:", options=regioes_disponiveis)

df_filtrado = df.copy()

# Aplica a lógica da Região Selecionada
if regiao_selecionada == "Taquarucu":
    secoes_taquarucu = ['10', '11', '12', '13', '61', '303', '512', '528']
    df_filtrado = df_filtrado[df_filtrado['NR_SECAO'].isin(secoes_taquarucu)]
    st.sidebar.success(f"📍 Exibindo apenas as {len(secoes_taquarucu)} secções de Taquaruçu.")

elif regiao_selecionada in ["Taquaralto","Aurenys", "Buritirana", "Plano Diretor Sul", "Plano Diretor Norte"]:
    st.sidebar.info(f"🚧 Em construção: O mapeamento das secções de '{regiao_selecionada}' será inserido nas próximas versões.")
    # Esvazia o dataframe para forçar o utilizador a aguardar ou mudar o filtro, ou mantém como está
    # Neste caso, deixaremos o dataframe vazio para evidenciar que ainda não há dados mapeados
    df_filtrado = pd.DataFrame(columns=df.columns)

# 2. Filtro de Zona Eleitoral
if not df_filtrado.empty:
    zonas = sorted(df_filtrado['NR_ZONA'].unique())
    zona_selecionada = st.sidebar.multiselect("Zona Eleitoral:", options=zonas, default=zonas)
    df_filtrado = df_filtrado[df_filtrado['NR_ZONA'].isin(zona_selecionada)]

# 3. Filtro de Local de Votação (Escola)
if not df_filtrado.empty:
    locais = sorted(df_filtrado['NR_LOCAL_VOTACAO'].unique())
    locais_selecionados = st.sidebar.multiselect("Local de Votação (Escola):", options=locais, default=locais)
    df_filtrado = df_filtrado[df_filtrado['NR_LOCAL_VOTACAO'].isin(locais_selecionados)]

# 4. Filtro de Secção (Atualizado dinamicamente)
if not df_filtrado.empty:
    secoes = sorted(df_filtrado['NR_SECAO'].unique())
    secoes_selecionadas = st.sidebar.multiselect("Secções Específicas:", options=secoes, default=secoes)
    df_filtrado = df_filtrado[df_filtrado['NR_SECAO'].isin(secoes_selecionadas)]

# 5. Filtro de Cargo
if not df_filtrado.empty:
    cargos = sorted(df_filtrado['DS_CARGO_PERGUNTA'].dropna().unique())
    cargos_selecionados = st.sidebar.multiselect("Cargos:", options=cargos, default=cargos)
else:
    cargos_selecionados = []

# 6. Busca Textual
st.sidebar.markdown("---")
st.sidebar.subheader("Busca Específica")
termo_busca = st.sidebar.text_input("Buscar Candidato ou Número (Ex: LULA, 22):")

if df_filtrado.empty:
    st.warning("Nenhum dado a ser exibido. Ajuste os filtros na barra lateral.")
    st.stop()

if not cargos_selecionados:
    st.warning("Selecione pelo menos um Cargo na barra lateral.")
    st.stop()

# ==========================================
# MÉTRICAS GERAIS (Estatísticas de Comparecimento)
# ==========================================
# Remove os duplicados por Zona e Secção para somar corretamente os aptos e faltosos
df_secoes_unicas = df_filtrado.drop_duplicates(subset=['NR_ZONA', 'NR_SECAO']).copy()

aptos = df_secoes_unicas['QT_APTOS'].sum()
comparecimento = df_secoes_unicas['QT_COMPARECIMENTO'].sum()
abstencao = df_secoes_unicas['QT_ABSTENCOES'].sum()

col1, col2, col3 = st.columns(3)
col1.metric("Eleitores Aptos (Filtro Atual)", f"{aptos:,}".replace(',', '.'))
if aptos > 0:
    col2.metric("Comparecimento", f"{comparecimento:,}".replace(',', '.'), f"{(comparecimento/aptos)*100:.1f}%")
    col3.metric("Abstenções", f"{abstencao:,}".replace(',', '.'), f"{(abstencao/aptos)*100:.1f}%", delta_color="inverse")

st.divider()

# ==========================================
# EXIBIÇÃO POR CARGO (Gráficos e Tabelas)
# ==========================================
abas = st.tabs(cargos_selecionados)

for aba, cargo in zip(abas, cargos_selecionados):
    with aba:
        st.subheader(f"Apuração - {cargo}")
        
        df_cargo = df_filtrado[df_filtrado['DS_CARGO_PERGUNTA'] == cargo]
        
        # Filtro Textual
        if termo_busca:
            termo = termo_busca.upper()
            df_cargo = df_cargo[
                df_cargo['NM_VOTAVEL'].str.upper().str.contains(termo, na=False) | 
                df_cargo['NR_VOTAVEL'].str.startswith(termo, na=False)
            ]
        
        if df_cargo.empty:
            st.info("Sem votos para exibir com os filtros atuais.")
            continue
        
        # Agrupamento da votação
        df_agrupado = df_cargo.groupby(['NM_VOTAVEL', 'NR_VOTAVEL', 'DS_TIPO_VOTAVEL'])['QT_VOTOS'].sum().reset_index()
        
        # Remove brancos e nulos do gráfico para não distorcer as barras dos candidatos
        df_candidatos = df_agrupado[~df_agrupado['DS_TIPO_VOTAVEL'].isin(['Branco', 'Nulo'])].sort_values(by='QT_VOTOS', ascending=True)
        
        col_grafico, col_tabela = st.columns([6, 4])
        
        with col_grafico:
            df_top = df_candidatos.tail(20)
            if not df_top.empty:
                titulo_grafico = f"Top 20 Mais Votados - {cargo}" if not termo_busca else f"Resultados da Busca"
                fig = px.bar(
                    df_top, 
                    x='QT_VOTOS', 
                    y='NM_VOTAVEL', 
                    orientation='h',
                    text='QT_VOTOS',
                    title=titulo_grafico,
                    color='QT_VOTOS',
                    color_continuous_scale='Blues'
                )
                fig.update_layout(showlegend=False, yaxis_title="", xaxis_title="Votos", height=500)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Sem candidatos nominais para o gráfico.")
        
        with col_tabela:
            st.markdown("**Detalhamento de Votos**")
            df_exibicao = df_agrupado.sort_values(by='QT_VOTOS', ascending=False).reset_index(drop=True)
            
            df_exibicao = df_exibicao.rename(columns={
                'NR_VOTAVEL': 'Nº',
                'NM_VOTAVEL': 'Nome / Voto',
                'DS_TIPO_VOTAVEL': 'Tipo',
                'QT_VOTOS': 'Total'
            })
            
            st.dataframe(df_exibicao, use_container_width=True, height=450)