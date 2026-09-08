import streamlit as st
import pandas as pd
import io
import time
import plotly.express as px

# Configuração inicial da página
st.set_page_config(page_title="Dashboard de Turismo - Data.Rio", layout="wide")

st.markdown("""
### Objetivo e Motivação
O dataset utilizado (**2676.xls**) foi escolhido a partir do portal **Data.Rio**. Ele apresenta dados históricos sobre a chegada mensal de turistas ao município do Rio de Janeiro via marítima, categorizados por continentes e países de residência permanente. 

A **motivação** por trás desta escolha é a importância do turismo marítimo (cruzeiros) para a economia carioca. O objetivo é analisar a sazonalidade do fluxo turístico ao longo do ano e identificar quais países são os maiores emissores de visitantes, permitindo direcionar campanhas turísticas e melhorar a infraestrutura portuária.

### Funcionalidades e Visualizações Implementadas
Para explorar esses dados, a aplicação conta com as seguintes ferramentas:
* **Funcionalidades:** Upload dinâmico de arquivos XLS, otimização de processamento via Cache, preservação de filtros do usuário com Session State, seletores interativos (Radio, Checkbox, Multiselect), personalização visual de cores (Color Picker) e exportação dos dados filtrados para CSV e Excel.
* **Métricas:** Cards numéricos indicando a quantidade de países listados, total acumulado de turistas e a média por região.
* **Visualizações Básicas:** Tabela de dados interativa, Gráfico de Barras (Top 10 Regiões), Gráfico de Linhas (Evolução Sazonal) e Gráfico de Pizza (Composição dos Top 5).
* **Visualizações Avançadas:** Histograma (Distribuição de volume) e Gráfico de Dispersão (Correlação de visitas entre meses específicos).
""")

st.sidebar.header("🎨 Personalização Visual")

#Recupera as cores da URL (se existirem), caso contrário, usa os padrões
default_bg = st.query_params.get("bg_color", "#45454A")
default_font = st.query_params.get("font_color", "#D7DAEC")

bg_color = st.sidebar.color_picker("Cor de fundo da aplicação", default_bg)
font_color = st.sidebar.color_picker("Cor das fontes principais", default_font)

st.query_params["bg_color"] = bg_color
st.query_params["font_color"] = font_color

st.markdown(f"""
    <style>
    /* Muda a cor de fundo do container principal */
    [data-testid="stAppViewContainer"] {{
        background-color: {bg_color} !important;
    }}
    
    /* Força a cor da fonte em todos os elementos de texto (títulos, parágrafos, labels, métricas) */
    h1, h2, h3, h4, h5, h6, p, span, label, div[data-testid="stMetricValue"] {{
        color: {font_color} !important;
    }}
    
    /* Opcional: Garante que os valores dentro dos inputs também fiquem visíveis */
    .st-bb, .st-at, .st-ae {{
        color: {font_color} !important;
    }}
    </style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data(file):
    """
    Função em cache para carregar e tratar os dados do arquivo XLS.
    """
    try:
        # Lê o excel.
        xls = pd.ExcelFile(file)
        sheet_to_load = xls.sheet_names[1] if len(xls.sheet_names) > 1 else xls.sheet_names[0]
        df = pd.read_excel(file, sheet_name=sheet_to_load, skiprows=4)
        
        # Mapeamento de colunas padronizado
        col_names = ["País", "Total", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", 
                     "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
        
        # Ajusta os nomes das colunas se o formato bater
        if len(df.columns) == 14:
            df.columns = col_names
            
        # Limpeza e Tratamento Básicos
        df = df.dropna(subset=['País', 'Total'])
        df = df[~df['País'].astype(str).str.contains('Fonte:|Nota:|Anuário', case=False, na=False)]
        df = df[df['País'] != 'Total']
        
        # Converte valores com hífen para 0 e tipa como numérico
        df = df.replace("-", 0).fillna(0)
        for col in col_names[1:]:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
        return df, col_names[2:] # retorna o df e a lista de meses
    except Exception as e:
        st.error(f"Erro ao processar a planilha. Verifique o formato do arquivo. Detalhe: {e}")
        return pd.DataFrame(), []


st.sidebar.header("📁 Upload de Dados")
uploaded_file = st.sidebar.file_uploader("Faça o upload do arquivo de turismo (Ex: 2676.xls)", type=["xls", "xlsx"])

if uploaded_file is not None:
    
    with st.spinner("Processando e limpando o arquivo..."):
        progress_bar = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress_bar.progress(i + 1)
            
        df, meses_lista = load_data(uploaded_file)
        progress_bar.empty()
        st.sidebar.success("Arquivo carregado com sucesso!")

    # Inicializando as variáveis no Session State para que os filtros não reiniciem
    if 'selected_months' not in st.session_state:
        st.session_state.selected_months = meses_lista
    if 'show_raw_data' not in st.session_state:
        st.session_state.show_raw_data = True
    if 'visit_filter' not in st.session_state:
        st.session_state.visit_filter = "Todos os Registros"


    st.divider()
    st.subheader("⚙️ Filtros e Controles de Exibição")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Checkbox
        st.session_state.show_raw_data = st.checkbox("Exibir tabela interativa de dados?", value=st.session_state.show_raw_data)
        
    with col2:
        # Radio
        st.session_state.visit_filter = st.radio("Filtrar países por tráfego:", 
                                                 ["Todos os Registros", "Apenas países com turistas (>0)"],
                                                 index=0 if st.session_state.visit_filter == "Todos os Registros" else 1)
        
    with col3:
        # Dropdowns (Multiselect)
        st.session_state.selected_months = st.multiselect(
            "Selecione os meses desejados:", 
            options=meses_lista, 
            default=st.session_state.selected_months
        )

    df_filtrado = df.copy()
    if st.session_state.visit_filter == "Apenas países com turistas (>0)":
        df_filtrado = df_filtrado[df_filtrado['Total'] > 0]
        
    colunas_finais = ["País", "Total"] + st.session_state.selected_months
    df_filtrado = df_filtrado[colunas_finais]


    st.divider()
    st.subheader("📊 Métricas de Resumo")
    m1, m2, m3 = st.columns(3)
    
    total_linhas = len(df_filtrado)
    total_turistas = df_filtrado['Total'].sum()
    media_turistas = df_filtrado['Total'].mean() if total_linhas > 0 else 0
    
    m1.metric(label="Países/Regiões Listados", value=total_linhas)
    m2.metric(label="Total de Turistas (Acumulado)", value=f"{total_turistas:,.0f}")
    m3.metric(label="Média de Turistas por Região", value=f"{media_turistas:,.2f}")


  
    if st.session_state.show_raw_data:
        st.divider()
        st.subheader("📋 Tabela Interativa")
        st.dataframe(df_filtrado, use_container_width=True, hide_index=True)


    st.markdown("### 📥 Exportação de Dados")
    down_col1, down_col2 = st.columns([1, 1])
    
    # Gera CSV
    csv_data = df_filtrado.to_csv(index=False).encode('utf-8')
    down_col1.download_button(
        label="Baixar Dados (Formato CSV)",
        data=csv_data,
        file_name="dados_turismo.csv",
        mime="text/csv",
    )
    
    # Gera Excel (XLSX)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df_filtrado.to_excel(writer, index=False, sheet_name='Filtrados')
    excel_data = output.getvalue()
    
    down_col2.download_button(
        label="Baixar Dados (Formato Excel/XLS)",
        data=excel_data,
        file_name="dados_turismo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    st.divider()
    st.subheader("📈 Gráficos Simples")
    c1, c2 = st.columns(2)
    
    with c1:
        st.markdown("**Top 10 Regiões**")
        top10 = df_filtrado.nlargest(10, 'Total')
        st.bar_chart(data=top10.set_index('País')['Total'])
        
    with c2:
        st.markdown("**Evolução Temporal Global**")
        if len(st.session_state.selected_months) > 0:
            soma_temporal = df_filtrado[st.session_state.selected_months].sum()
            st.line_chart(soma_temporal)
        else:
            st.info("Selecione os meses no filtro superior para visualizar a evolução temporal.")
            
    # Gráfico de Pizza simples 
    st.markdown("**Composição dos Top 5**")
    top5 = df_filtrado.nlargest(5, 'Total')
    fig_pie = px.pie(top5, values='Total', names='País', hole=0.3)
    st.plotly_chart(fig_pie, use_container_width=True)


    st.divider()
    st.subheader("📉 Gráficos Avançados")
    c3, c4 = st.columns(2)
    
    with c3:
        st.markdown("**Distribuição de Visitas**")
        fig_hist = px.histogram(df_filtrado[df_filtrado['Total'] > 0], x="Total", nbins=15, 
                                marginal="box", color_discrete_sequence=['#3b5998'])
        fig_hist.update_layout(xaxis_title="Volume de Turistas", yaxis_title="Contagem de Países")
        st.plotly_chart(fig_hist, use_container_width=True)
        
    with c4:
        st.markdown("**Correlação entre Meses**")
        if len(st.session_state.selected_months) >= 2:
            mes1 = st.session_state.selected_months[0]
            mes2 = st.session_state.selected_months[1]
            fig_scatter = px.scatter(df_filtrado, x=mes1, y=mes2, 
                                     hover_name='País', size='Total', size_max=40,
                                     color='Total', color_continuous_scale=px.colors.sequential.Viridis)
            fig_scatter.update_layout(xaxis_title=f"Turistas em {mes1}", yaxis_title=f"Turistas em {mes2}")
            st.plotly_chart(fig_scatter, use_container_width=True)
        else:
            st.warning("Para exibir o Gráfico de Dispersão (Scatter), selecione **pelo menos 2 meses** nos filtros acima.")

else:
    # Mensagem exibida enquanto o arquivo não é feito o upload
    st.info("👈 Por favor, faça o upload do arquivo XLS do portal Data.Rio na barra lateral esquerda para iniciar a aplicação.")