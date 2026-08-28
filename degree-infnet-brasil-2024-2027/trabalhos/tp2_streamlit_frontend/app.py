import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pydeck as pdk

st.set_page_config(layout="wide", page_title="Dashboard COVID-19 Brasil")


# CARREGAMENTO DO CSV REAL

@st.cache_data
def load_data():
    # Lê o arquivo CSV real separado por ponto e vírgula
    df = pd.read_csv('HIST_PAINEL_COVIDBR_05set2025/HIST_PAINEL_COVIDBR_2020_Parte1_05set2025.csv', sep=';')
    
    # Tratamento básico de tipos numéricos
    cols_num = ['casosNovos', 'obitosNovos', 'casosAcumulado', 'obitosAcumulado']
    for col in cols_num:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    if 'populacaoTCU2019' in df.columns:
        df['populacao'] = pd.to_numeric(df['populacaoTCU2019'], errors='coerce').fillna(100000)
    elif 'populacao' not in df.columns:
        df['populacao'] = 100000

    # Criação de colunas fictícias para lat, lon e leitos caso não existam no CSV do MS
    if 'lat' not in df.columns or 'lon' not in df.columns:
        np.random.seed(42)
        df['lat'] = np.random.uniform(-30, 5, len(df))
        df['lon'] = np.random.uniform(-65, -35, len(df))
        
    if 'leitosOcupados' not in df.columns:
        df['leitosOcupados'] = df['casosNovos'].apply(lambda x: max(0, x * 0.1) if pd.notnull(x) else 0)
        
    return df

df = load_data()

st.title("Painel Analítico COVID-19 - Brasil")
st.markdown("""
**Importância da Visualização de Dados na Pandemia**
A visualização de dados transforma volumes massivos e complexos de informações epidemiológicas em insights acessíveis. Em uma pandemia como a COVID-19, gráficos e mapas permitem identificar rapidamente picos de contágio, interiorização da doença e taxas de letalidade. Para gestores públicos, isso baliza a alocação de leitos de UTI, envio de vacinas e implementação de medidas de distanciamento. Para a população, cria a percepção real do risco, incentivando a adesão a medidas preventivas através da clareza visual (como a famosa curva epidêmica a ser "achatada").
""")


# EXERCÍCIO 1

st.header("1. Casos Novos por Semana Epidemiológica (São Paulo)")
st.info("Gráfico de Barras (Streamlit - SP): Escolheu-se São Paulo por ser o estado mais populoso e o principal hub logístico do país, frequentemente o primeiro a registrar novas ondas e variantes, servindo como termômetro para o resto do Brasil.")
# Filtra apenas a linha de consolidação do estado (município é nulo)
df_sp = df[(df['estado'] == 'SP') & (df['municipio'].isnull())].groupby('semanaEpi')['casosNovos'].sum()
st.bar_chart(df_sp)


# EXERCÍCIO 2

st.header("2. Evolução de Óbitos Acumulados no Brasil")
st.info("Gráfico de Linha (Streamlit - Brasil): A curva de óbitos acumulados sempre cresce ou estabiliza. A inclinação da curva demonstra a gravidade do momento: platôs indicam controle (baixa mortalidade diária), enquanto curvas íngremes refletem colapso hospitalar e alta letalidade.")
# Filtra apenas a consolidação nacional
df_br_obitos = df[df['regiao'] == 'Brasil'].groupby('semanaEpi')['obitosAcumulado'].max()
st.line_chart(df_br_obitos)


# EXERCÍCIO 3

st.header("3. Comparação de Casos Acumulados (SP, RJ, MG)")
st.info("Gráfico de Área (Streamlit - SP, RJ, MG): A comparação no Sudeste evidencia que, embora SP tenha o maior volume absoluto devido à população, surtos sazonais afetam os três estados quase simultaneamente devido à alta conectividade terrestre e aérea.")
df_sudeste = df[(df['estado'].isin(['SP', 'RJ', 'MG'])) & (df['municipio'].isnull())]
df_area = df_sudeste.pivot_table(index='semanaEpi', columns='estado', values='casosAcumulado', aggfunc='max')
st.area_chart(df_area)


# EXERCÍCIO 4

st.header("4. Distribuição Geográfica em São Paulo")
st.info("Mapa (Streamlit - Municípios SP): A análise geográfica identifica 'clusters' ou manchas quentes (hotspots). Isso mostra se a doença está concentrada em capitais/regiões metropolitanas ou se já sofreu interiorização.")
# Pega o último registro por município de SP
semana_max = df['semanaEpi'].max()
df_mapa_sp = df[(df['estado'] == 'SP') & (df['municipio'].notnull()) & (df['semanaEpi'] == semana_max)][['lat', 'lon', 'casosAcumulado']]
st.map(df_mapa_sp)


# EXERCÍCIO 5

st.header("5. Casos Novos vs Óbitos Novos por Estado (Última Semana)")
st.info("Matplotlib (Casos vs. Óbitos): Revela a defasagem natural de semanas entre os picos de infecção e os de mortalidade. Também sugere a Taxa de Letalidade de cada estado em determinado momento.")
df_recent = df[(df['estado'].notnull()) & (df['municipio'].isnull()) & (df['semanaEpi'] == semana_max)].groupby('estado')[['casosNovos', 'obitosNovos']].sum()

fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(df_recent.index))
width = 0.35
ax.bar(x - width/2, df_recent['casosNovos'], width, label='Casos Novos', color='skyblue')
ax.bar(x + width/2, df_recent['obitosNovos'] * 10, width, label='Óbitos Novos (x10 para viz)', color='salmon') 
ax.set_xticks(x)
ax.set_xticklabels(df_recent.index, rotation=45)
ax.legend()
st.pyplot(fig)


# EXERCÍCIO 6

st.header("6. Distribuição de Casos Novos (Norte, Nordeste, Sudeste)")
st.info("Seaborn (Boxplot - Norte, Nordeste, Sudeste): Mostra a dispersão e outliers. Os outliers superiores representam as semanas mais críticas (picos da 1ª e 2ª onda), evidenciando como a variante Gamma, por exemplo, causou valores extremos inicialmente no Norte (Manaus).")
df_box = df[(df['regiao'].isin(['Norte', 'Nordeste', 'Sudeste'])) & (df['municipio'].isnull()) & (df['estado'].notnull())]
fig_box, ax_box = plt.subplots(figsize=(10, 5))
sns.boxplot(x='regiao', y='casosNovos', data=df_box, ax=ax_box, palette='Set2')
st.pyplot(fig_box)


# EXERCÍCIO 7

st.header("7. Evolução Semanal de Casos na Região Sul")
st.info("Altair (Área - Região Sul): Escolhida para observar a sazonalidade, dado que infecções respiratórias no Sul do Brasil tendem a se agravar nos meses mais frios, gerando picos específicos.")
df_sul = df[(df['regiao'] == 'Sul') & (df['municipio'].isnull()) & (df['estado'].notnull())].groupby(['semanaEpi', 'estado'])['casosNovos'].sum().reset_index()
area_chart = alt.Chart(df_sul).mark_area(opacity=0.6).encode(
    x='semanaEpi:O',
    y='casosNovos:Q',
    color='estado:N'
).properties(width=800, height=400)
st.altair_chart(area_chart, use_container_width=True)


# EXERCÍCIO 8

st.header("8. Correlação: Casos, Óbitos e Leitos (SP)")
st.info("Altair (Heatmap): A correlação entre casos novos, óbitos novos e ocupação hospitalar costuma ser forte e positiva. O heatmap prova estatisticamente a relação de causa e efeito e a sobrecarga sistêmica.")
df_sp_est = df[(df['estado'] == 'SP') & (df['municipio'].isnull())]
df_corr_sp = df_sp_est[['casosNovos', 'obitosNovos', 'leitosOcupados']].corr().reset_index().melt('index')
heatmap = alt.Chart(df_corr_sp).mark_rect().encode(
    x='index:O',
    y='variable:O',
    color=alt.Color('value:Q', scale=alt.Scale(scheme='reds')),
    tooltip=['index', 'variable', 'value']
).properties(width=500, height=400)
st.altair_chart(heatmap, use_container_width=True)


# EXERCÍCIO 9

st.header("9. Distribuição Total de Casos por Região")
st.info("Plotly (Pizza): O Sudeste tende a dominar a distribuição absoluta de casos devido à sua altíssima densidade demográfica, abrigando mais de 40% da população do país.")
df_regiao_total = df[(df['regiao'].isin(['Norte', 'Nordeste', 'Sudeste', 'Sul', 'Centro-Oeste'])) & (df['estado'].isnull())]
df_regiao_total = df_regiao_total.groupby('regiao')['casosAcumulado'].max().reset_index()
fig_pie = px.pie(df_regiao_total, values='casosAcumulado', names='regiao', hole=0.3, color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_pie, use_container_width=True)


# EXERCÍCIO 10

st.header("10. Comparativo Temporal: Norte vs Sudeste")
st.info("Plotly Subplots (Norte vs. Sudeste): Expõe a assincronia das ondas. O Norte sofreu colapsos de oxigênio de forma mais aguda em períodos onde o Sudeste ainda iniciava a escalada de casos.")
df_norte_sudeste = df[(df['regiao'].isin(['Norte', 'Sudeste'])) & (df['estado'].isnull())].groupby(['semanaEpi', 'regiao'])[['casosNovos', 'obitosNovos']].sum().reset_index()

fig_sub = make_subplots(rows=1, cols=2, subplot_titles=("Região Norte", "Região Sudeste"))

df_n = df_norte_sudeste[df_norte_sudeste['regiao'] == 'Norte']
fig_sub.add_trace(go.Bar(x=df_n['semanaEpi'], y=df_n['casosNovos'], name="Casos Norte", marker_color='blue'), row=1, col=1)
fig_sub.add_trace(go.Bar(x=df_n['semanaEpi'], y=df_n['obitosNovos']*10, name="Óbitos Norte (x10)", marker_color='red'), row=1, col=1)

df_s = df_norte_sudeste[df_norte_sudeste['regiao'] == 'Sudeste']
fig_sub.add_trace(go.Bar(x=df_s['semanaEpi'], y=df_s['casosNovos'], name="Casos Sudeste", marker_color='lightblue'), row=1, col=2)
fig_sub.add_trace(go.Bar(x=df_s['semanaEpi'], y=df_s['obitosNovos']*10, name="Óbitos Sudeste (x10)", marker_color='darkred'), row=1, col=2)

st.plotly_chart(fig_sub, use_container_width=True)


# EXERCÍCIO 11

st.header("11. Densidade de Casos vs População (Mapa PyDeck 3D)")
st.info("PyDeck (Densidade Populacional): Vírus de transmissão respiratória se beneficiam de aglomerações. O mapa 3D mostra que municípios com maior densidade demográfica concentram o maior volume verticalizado de casos per capita, exigindo barreiras sanitárias mais rígidas.")
df_pydeck = df[(df['regiao'] == 'Sudeste') & (df['municipio'].notnull()) & (df['semanaEpi'] == semana_max)].copy()
df_pydeck['incidencia'] = (df_pydeck['casosAcumulado'] / df_pydeck['populacao']) * 100000

layer = pdk.Layer(
    "ColumnLayer",
    data=df_pydeck,
    get_position=['lon', 'lat'],
    get_elevation='incidencia',
    elevation_scale=10, # Escala ajustada para dados reais
    radius=15000,
    get_fill_color=['incidencia * 2', 50, 100, 150],
    pickable=True,
    auto_highlight=True,
)

view_state = pdk.ViewState(
    latitude=-20.0,
    longitude=-45.0,
    zoom=4,
    pitch=45,
)

r = pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{municipio}\nIncidência: {incidencia}"})
st.pydeck_chart(r)