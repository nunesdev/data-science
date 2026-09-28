import streamlit as st
import pandas as pd
from statsbombpy import sb
from mplsoccer import Pitch
import matplotlib.pyplot as plt
import seaborn as sns
import io

# ==========================================
# Configuração da Página
# ==========================================
st.set_page_config(page_title="Football Analytics Dashboard", page_icon="⚽", layout="wide")

# ==========================================
# Funções de Carregamento de Dados (Cache)
# ==========================================
@st.cache_data(ttl=3600)
def carregar_competicoes():
    """Carrega as competições disponíveis na base aberta da StatsBomb"""
    return sb.competitions()

@st.cache_data(ttl=3600)
def carregar_partidas(comp_id, season_id):
    """Carrega as partidas de uma dada competição e temporada"""
    return sb.matches(competition_id=comp_id, season_id=season_id)

@st.cache_data(ttl=3600)
def carregar_eventos(match_id):
    """Carrega os eventos de uma partida específica"""
    return sb.events(match_id=match_id)

# ==========================================
# Gerenciamento de Estado (Session State)
# ==========================================
if 'match_id' not in st.session_state:
    st.session_state.match_id = None

# ==========================================
# Interface: Barra Lateral (Filtros Principais)
# ==========================================
st.sidebar.title("⚙️ Filtros da Partida")

with st.spinner("Carregando competições..."):
    df_comps = carregar_competicoes()

# Seletor de Competição e Temporada
comp_nomes = df_comps['competition_name'].unique()
sel_comp = st.sidebar.selectbox("Selecione o Campeonato:", comp_nomes)

# Filtrar temporadas baseadas no campeonato escolhido
temporadas = df_comps[df_comps['competition_name'] == sel_comp]['season_name'].unique()
sel_temp = st.sidebar.selectbox("Selecione a Temporada:", temporadas)

# Obter IDs para buscar as partidas
comp_id = df_comps[(df_comps['competition_name'] == sel_comp) & (df_comps['season_name'] == sel_temp)]['competition_id'].values[0]
season_id = df_comps[(df_comps['competition_name'] == sel_comp) & (df_comps['season_name'] == sel_temp)]['season_id'].values[0]

with st.spinner("Buscando partidas..."):
    df_matches = carregar_partidas(comp_id, season_id)

# Formatar o nome da partida para o dropdown
df_matches['match_label'] = df_matches['home_team'] + " vs " + df_matches['away_team'] + " (" + df_matches['match_date'] + ")"
sel_partida = st.sidebar.selectbox("Selecione a Partida:", df_matches['match_label'])

st.session_state.match_id = df_matches[df_matches['match_label'] == sel_partida]['match_id'].values[0]
detalhes_partida = df_matches[df_matches['match_id'] == st.session_state.match_id].iloc[0]

# ==========================================
# Carregamento de Eventos da Partida
# ==========================================
barra_progresso = st.progress(0)
with st.spinner("Baixando eventos da partida (Isso pode levar alguns segundos)..."):
    df_eventos = carregar_eventos(st.session_state.match_id)
    barra_progresso.progress(100)

# ==========================================
# Estrutura Principal do Dashboard (Tabs)
# ==========================================
st.title(f"⚽ {detalhes_partida['home_team']} {detalhes_partida['home_score']} x {detalhes_partida['away_score']} {detalhes_partida['away_team']}")
st.caption(f"**Campeonato:** {sel_comp} | **Temporada:** {sel_temp} | **Data:** {detalhes_partida['match_date']}")

tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "🗺️ Mapas Táticos", "🏃 Análise de Jogador", "📁 Dados Brutos"])

# --- TAB 1: VISÃO GERAL (Métricas) ---
with tab1:
    st.subheader("Indicadores da Partida")
    
    # Cálculos básicos
    total_gols = detalhes_partida['home_score'] + detalhes_partida['away_score']
    chutes = df_eventos[df_eventos['type'] == 'Shot']
    passes = df_eventos[df_eventos['type'] == 'Pass']
    
    taxa_conversao = (total_gols / len(chutes) * 100) if len(chutes) > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Gols", total_gols)
    col2.metric("Total de Chutes", len(chutes))
    col3.metric("Total de Passes", len(passes))
    col4.metric("Conversão de Chutes", f"{taxa_conversao:.1f}%")

    # Gráfico Seaborn: Passes por Equipe
    st.markdown("---")
    st.subheader("Volume de Passes por Equipe")
    fig_bar, ax_bar = plt.subplots(figsize=(8, 4))
    sns.countplot(data=passes, y='team', palette='viridis', ax=ax_bar)
    ax_bar.set_xlabel("Quantidade de Passes")
    ax_bar.set_ylabel("Equipe")
    st.pyplot(fig_bar)

# --- TAB 2: MAPAS TÁTICOS (mplsoccer) ---
with tab2:
    st.subheader("Mapas de Eventos Espaciais")
    tipo_mapa = st.radio("Selecione o tipo de visualização:", ["Mapa de Chutes", "Mapa de Passes (Assistências/Chances)"])
    
    pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
    fig, ax = pitch.draw(figsize=(10, 6))

    if tipo_mapa == "Mapa de Chutes":
        # Filtrar chutes e extrair coordenadas
        chutes_validos = chutes.dropna(subset=['location'])
        for _, row in chutes_validos.iterrows():
            x, y = row['location']
            gol = row.get('shot_outcome') == 'Goal'
            cor = 'green' if gol else 'red'
            marcador = '*' if gol else 'o'
            tamanho = 200 if gol else 100
            pitch.scatter(x, y, s=tamanho, c=cor, marker=marcador, ax=ax, edgecolors='white', zorder=2)
        st.caption("Verde (*) = Gol | Vermelho (o) = Chute não convertido")
        
    else:
        # Filtrar passes que geraram finalização
        passes_chave = passes[passes.get('pass_shot_assist') == True].dropna(subset=['location', 'pass_end_location'])
        for _, row in passes_chave.iterrows():
            x, y = row['location']
            end_x, end_y = row['pass_end_location']
            pitch.arrows(x, y, end_x, end_y, color='cyan', ax=ax, width=2, headwidth=4, alpha=0.8)
        st.caption("Setas azuis indicam passes que resultaram em finalizações.")

    st.pyplot(fig)

# --- TAB 3: ANÁLISE DE JOGADOR (Formulários) ---
with tab3:
    st.subheader("Filtragem de Desempenho Individual")
    
    jogadores = df_eventos['player'].dropna().sort_values().unique()
    
    with st.form("form_jogador"):
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            jogador_selecionado = st.selectbox("Selecione o Jogador:", jogadores)
        with col_form2:
            minutos = st.slider("Intervalo de Tempo (minutos):", 0, 120, (0, 90))
            
        tipos_evento = st.multiselect("Tipos de Eventos:", df_eventos['type'].unique(), default=['Pass', 'Shot', 'Dribble'])
        submit_btn = st.form_submit_button("Gerar Análise")

    if submit_btn:
        df_jogador = df_eventos[
            (df_eventos['player'] == jogador_selecionado) & 
            (df_eventos['minute'] >= minutos[0]) & 
            (df_eventos['minute'] <= minutos[1]) &
            (df_eventos['type'].isin(tipos_evento))
        ]
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric(f"Eventos Registrados", len(df_jogador))
        
        # Passes bem-sucedidos
        if 'Pass' in tipos_evento:
            passes_jog = df_jogador[df_jogador['type'] == 'Pass']
            passes_incompletos = passes_jog['pass_outcome'].notna().sum()
            passes_certos = len(passes_jog) - passes_incompletos
            col_m2.metric("Passes Bem-Sucedidos", passes_certos)

        st.dataframe(df_jogador[['minute', 'type', 'play_pattern', 'location']].head(15), use_container_width=True)

# --- TAB 4: DADOS BRUTOS & DOWNLOAD ---
with tab4:
    st.subheader("Base de Dados de Eventos")
    
    col_filtro, col_download = st.columns([3, 1])
    with col_filtro:
        equipe_filtro = st.selectbox("Filtrar Tabela por Equipe:", ["Ambas"] + list(df_eventos['team'].dropna().unique()))
    
    df_tabela = df_eventos if equipe_filtro == "Ambas" else df_eventos[df_eventos['team'] == equipe_filtro]
    
    # Exibir o dataframe
    st.dataframe(df_tabela[['minute', 'team', 'player', 'type', 'location', 'pass_outcome', 'shot_outcome']], use_container_width=True)
    
    # Serviço de Download
    csv = df_tabela.to_csv(index=False).encode('utf-8')
    with col_download:
        st.download_button(
            label="📥 Baixar Dados (CSV)",
            data=csv,
            file_name=f"eventos_{st.session_state.match_id}.csv",
            mime="text/csv",
        )