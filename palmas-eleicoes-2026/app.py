import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Configuração inicial da página
st.set_page_config(page_title="Apuração Eleitoral TSE", layout="wide")

st.title("📊 Painel de Apuração e Inteligência Eleitoral")
st.markdown("Consolidação de votos (BU) e análise estratégica (Dados Abertos TSE).")

# ==========================================
# CARREGAMENTO DE DADOS
# ==========================================
@st.cache_data
def load_votos():
    df = pd.read_csv("data/dados_palmas_completo.csv", sep=",", encoding="latin1", low_memory=False)
    cols_numericas = ['QT_VOTOS', 'QT_APTOS', 'QT_COMPARECIMENTO', 'QT_ABSTENCOES']
    for col in cols_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
            df.loc[df[col] == -1, col] = 0

    for col in ['NR_ZONA', 'NR_SECAO', 'NR_LOCAL_VOTACAO', 'NR_VOTAVEL', 'NR_PARTIDO']:
        if col in df.columns:
            df[col] = df[col].astype(str)
    return df

@st.cache_data
def load_perfil():
    df = pd.read_csv("data/dados_perfil_eleitorado_palmas.csv", sep=",", encoding="utf-8", low_memory=False)
    for col in ['NR_ZONA', 'NR_SECAO', 'NR_LOCAL_VOTACAO']:
        if col in df.columns:
            df[col] = df[col].astype(str)
    return df

try:
    df_votos = load_votos()
    df_perfil = load_perfil()
except FileNotFoundError as e:
    st.error(f"Ficheiro não encontrado: {e}. Certifique-se de que os dois arquivos CSV estão na mesma pasta.")
    st.stop()

# Criar dicionário global de mapeamento de escolas (Código -> Nome da Escola)
if 'NR_LOCAL_VOTACAO' in df_perfil.columns and 'NM_LOCAL_VOTACAO' in df_perfil.columns:
    mapa_escolas = df_perfil[['NR_LOCAL_VOTACAO', 'NM_LOCAL_VOTACAO']].drop_duplicates().set_index('NR_LOCAL_VOTACAO')['NM_LOCAL_VOTACAO'].to_dict()
else:
    mapa_escolas = {}

# ==========================================
# BARRA LATERAL (Filtros Compartilhados)
# ==========================================
st.sidebar.header("Filtros de Análise")

regioes_disponiveis = ["Todas as Regiões", "Taquarucu", "Taquaralto", "Aurenys", "Buritirana", "Plano Diretor Sul", "Plano Diretor Norte"]
regiao_selecionada = st.sidebar.selectbox("Região da Cidade:", options=regioes_disponiveis)

df_v_filtrado = df_votos.copy()
df_p_filtrado = df_perfil.copy()

if regiao_selecionada == "Taquarucu":
    secoes_taquarucu = ['10', '11', '12', '13', '61', '303', '512', '528']
    df_v_filtrado = df_v_filtrado[df_v_filtrado['NR_SECAO'].isin(secoes_taquarucu)]
    df_p_filtrado = df_p_filtrado[df_p_filtrado['NR_SECAO'].isin(secoes_taquarucu)]
    st.sidebar.success(f"📍 Exibindo apenas as {len(secoes_taquarucu)} secções de Taquaruçu.")
    
elif regiao_selecionada in ["Taquaralto", "Aurenys", "Buritirana", "Plano Diretor Sul", "Plano Diretor Norte"]:
    st.sidebar.info(f"🚧 Em construção: O mapeamento das secções de '{regiao_selecionada}' será inserido nas próximas versões.")
    df_v_filtrado = pd.DataFrame(columns=df_votos.columns)
    df_p_filtrado = pd.DataFrame(columns=df_perfil.columns)

if not df_v_filtrado.empty:
    zonas = sorted(df_v_filtrado['NR_ZONA'].unique())
    zona_selecionada = st.sidebar.multiselect("Zona Eleitoral:", options=zonas, default=zonas)
    df_v_filtrado = df_v_filtrado[df_v_filtrado['NR_ZONA'].isin(zona_selecionada)]
    df_p_filtrado = df_p_filtrado[df_p_filtrado['NR_ZONA'].isin(zona_selecionada)]

if not df_v_filtrado.empty:
    locais = sorted(df_v_filtrado['NR_LOCAL_VOTACAO'].unique())
    locais_selecionados = st.sidebar.multiselect("Local de Votação (Cód.):", options=locais, default=locais)
    df_v_filtrado = df_v_filtrado[df_v_filtrado['NR_LOCAL_VOTACAO'].isin(locais_selecionados)]
    df_p_filtrado = df_p_filtrado[df_p_filtrado['NR_LOCAL_VOTACAO'].isin(locais_selecionados)]

if not df_v_filtrado.empty:
    secoes = sorted(df_v_filtrado['NR_SECAO'].unique())
    secoes_selecionadas = st.sidebar.multiselect("Secções Específicas:", options=secoes, default=secoes)
    df_v_filtrado = df_v_filtrado[df_v_filtrado['NR_SECAO'].isin(secoes_selecionadas)]
    df_p_filtrado = df_p_filtrado[df_p_filtrado['NR_SECAO'].isin(secoes_selecionadas)]

if df_v_filtrado.empty:
    st.warning("Nenhum dado a ser exibido. Ajuste os filtros na barra lateral.")
    st.stop()

# ==========================================
# ESTRUTURA PRINCIPAL (Abas)
# ==========================================
# Renomeada a aba estratégica para "Desempenho e Locais"
aba_resultados, aba_desempenho, aba_perfil = st.tabs(["🗳️ Resultados da Eleição", "🏢 Desempenho e Locais", "👥 Perfil do Eleitorado"])

# ------------------------------------------
# ABA 1: RESULTADOS DA ELEIÇÃO
# ------------------------------------------
with aba_resultados:
    cargos = sorted(df_v_filtrado['DS_CARGO_PERGUNTA'].dropna().unique())
    cargos_selecionados = st.sidebar.multiselect("Cargos (Para Apuração):", options=cargos, default=cargos)
    
    st.sidebar.markdown("---")
    termo_busca = st.sidebar.text_input("Buscar Candidato (Ex: LULA, 22):")

    df_secoes_unicas = df_v_filtrado.drop_duplicates(subset=['NR_ZONA', 'NR_SECAO']).copy()
    aptos = df_secoes_unicas['QT_APTOS'].sum()
    comparecimento = df_secoes_unicas['QT_COMPARECIMENTO'].sum()
    abstencao = df_secoes_unicas['QT_ABSTENCOES'].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Eleitores Aptos", f"{aptos:,}".replace(',', '.'))
    if aptos > 0:
        col2.metric("Comparecimento", f"{comparecimento:,}".replace(',', '.'), f"{(comparecimento/aptos)*100:.1f}%")
        col3.metric("Abstenções", f"{abstencao:,}".replace(',', '.'), f"{(abstencao/aptos)*100:.1f}%", delta_color="inverse")
    st.divider()

    if cargos_selecionados:
        abas_cargos = st.tabs(cargos_selecionados)
        for sub_aba, cargo in zip(abas_cargos, cargos_selecionados):
            with sub_aba:
                st.subheader(f"Apuração Oficial - {cargo}")
                df_cargo = df_v_filtrado[df_v_filtrado['DS_CARGO_PERGUNTA'] == cargo]
                
                if termo_busca:
                    termo = termo_busca.upper()
                    df_cargo = df_cargo[
                        df_cargo['NM_VOTAVEL'].str.upper().str.contains(termo, na=False) | 
                        df_cargo['NR_VOTAVEL'].str.startswith(termo, na=False)
                    ]
                
                if df_cargo.empty:
                    st.info("Sem votos para exibir com os filtros atuais.")
                    continue
                
                df_agrupado = df_cargo.groupby(['NM_VOTAVEL', 'NR_VOTAVEL', 'DS_TIPO_VOTAVEL'])['QT_VOTOS'].sum().reset_index()
                df_candidatos = df_agrupado[~df_agrupado['DS_TIPO_VOTAVEL'].isin(['Branco', 'Nulo'])].sort_values(by='QT_VOTOS', ascending=True)
                
                col_grafico, col_tabela = st.columns([6, 4])
                with col_grafico:
                    df_top = df_candidatos.tail(20)
                    if not df_top.empty:
                        fig = px.bar(
                            df_top, x='QT_VOTOS', y='NM_VOTAVEL', orientation='h', text='QT_VOTOS',
                            title=f"Top 20 Mais Votados - {cargo}" if not termo_busca else f"Resultados da Busca",
                            color='QT_VOTOS', color_continuous_scale='Blues'
                        )
                        fig.update_layout(showlegend=False, yaxis_title="", xaxis_title="Votos", height=500)
                        st.plotly_chart(fig, use_container_width=True)
                
                with col_tabela:
                    st.markdown("**Detalhamento de Votos**")
                    df_exibicao = df_agrupado.sort_values(by='QT_VOTOS', ascending=False).reset_index(drop=True)
                    df_exibicao = df_exibicao.rename(columns={'NR_VOTAVEL': 'Nº', 'NM_VOTAVEL': 'Nome / Voto', 'DS_TIPO_VOTAVEL': 'Tipo', 'QT_VOTOS': 'Total'})
                    st.dataframe(df_exibicao, use_container_width=True, height=450)

# ------------------------------------------
# ABA 2: DESEMPENHO E LOCAIS
# ------------------------------------------
with aba_desempenho:
    st.subheader("Análise de Desempenho e Concentração de Votos")
    
    st.markdown("**📉 Desinteresse e Rejeição Eleitoral (Consolidado de todos os cargos)**")
    
    votos_brancos = df_v_filtrado[df_v_filtrado['DS_TIPO_VOTAVEL'] == 'Branco']['QT_VOTOS'].sum()
    votos_nulos = df_v_filtrado[df_v_filtrado['DS_TIPO_VOTAVEL'] == 'Nulo']['QT_VOTOS'].sum()
    
    col_abs, col_br, col_nul = st.columns(3)
    col_abs.metric("Faltosos (Abstenções)", f"{abstencao:,}".replace(',', '.'))
    col_br.metric("Votos em Branco", f"{votos_brancos:,}".replace(',', '.'))
    col_nul.metric("Votos Nulos", f"{votos_nulos:,}".replace(',', '.'))
    
    st.markdown("---")
    
    col_partidos, col_logistica = st.columns(2)
    
    # Ranking de Partidos
    with col_partidos:
        st.markdown("**🏆 Partidos Mais Votados (Soma de Cargos)**")
        df_validos = df_v_filtrado[~df_v_filtrado['DS_TIPO_VOTAVEL'].isin(['Branco', 'Nulo'])]
        df_partidos = df_validos[(df_validos['SG_PARTIDO'] != '#NULO#') & (~df_validos['SG_PARTIDO'].isna())]
        
        if not df_partidos.empty:
            ranking_partidos = df_partidos.groupby(['SG_PARTIDO', 'NR_PARTIDO'])['QT_VOTOS'].sum().reset_index()
            ranking_partidos = ranking_partidos.sort_values(by='QT_VOTOS', ascending=False).head(10)
            ranking_partidos = ranking_partidos.sort_values(by='QT_VOTOS', ascending=True)
            
            ranking_partidos['Partido_Rótulo'] = ranking_partidos['SG_PARTIDO'] + " (" + ranking_partidos['NR_PARTIDO'] + ")"
            
            fig_partidos = px.bar(
                ranking_partidos, x='QT_VOTOS', y='Partido_Rótulo', orientation='h',
                text='QT_VOTOS', color='QT_VOTOS', color_continuous_scale='Greens'
            )
            fig_partidos.update_layout(showlegend=False, yaxis_title="", xaxis_title="Total de Votos", height=400)
            st.plotly_chart(fig_partidos, use_container_width=True)
            
    # Concentração de Seções e Escolas
    with col_logistica:
        st.markdown("**🏫 Polos de Votação (Maiores Colégios)**")
        st.caption("Locais com maior quantidade de seções para organização logística.")
        
        locais_secoes = df_v_filtrado.drop_duplicates(subset=['NR_ZONA', 'NR_LOCAL_VOTACAO', 'NR_SECAO'])
        ranking_locais = locais_secoes.groupby('NR_LOCAL_VOTACAO')['NR_SECAO'].count().reset_index()
        ranking_locais.columns = ['Cód. Local', 'Seções']
        
        # Fazendo o cruzamento usando o dicionário gerado a partir do perfil do eleitor
        ranking_locais['Nome da Escola'] = ranking_locais['Cód. Local'].map(mapa_escolas).fillna('Nome não encontrado')
        
        # Reorganizar as colunas para o Nome da Escola ser o foco
        ranking_locais = ranking_locais[['Nome da Escola', 'Cód. Local', 'Seções']]
        ranking_locais = ranking_locais.sort_values(by='Seções', ascending=False).reset_index(drop=True)
        
        st.dataframe(ranking_locais, use_container_width=True, height=400)

# ------------------------------------------
# ABA 3: PERFIL DO ELEITORADO
# ------------------------------------------
with aba_perfil:
    st.subheader("Demografia das Seções Filtradas")
    
    total_eleitores_perfil = df_p_filtrado['QT_ELEITORES'].sum()
    st.markdown(f"**Total de registros processados:** {total_eleitores_perfil:,} eleitores".replace(',', '.'))
    
    if total_eleitores_perfil > 0:
        col_gen, col_ec = st.columns(2)
        with col_gen:
            df_gen = df_p_filtrado.groupby('DS_GENERO')['QT_ELEITORES'].sum().reset_index()
            fig_gen = px.pie(df_gen, values='QT_ELEITORES', names='DS_GENERO', title='Distribuição por Gênero', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_gen, use_container_width=True)
            
        with col_ec:
            df_ec = df_p_filtrado.groupby('DS_ESTADO_CIVIL')['QT_ELEITORES'].sum().reset_index()
            fig_ec = px.pie(df_ec, values='QT_ELEITORES', names='DS_ESTADO_CIVIL', title='Estado Civil', hole=0.4)
            st.plotly_chart(fig_ec, use_container_width=True)
            
        col_idade, col_esc = st.columns(2)
        with col_idade:
            df_idade = df_p_filtrado.groupby('DS_FAIXA_ETARIA')['QT_ELEITORES'].sum().reset_index()
            ordem_idade = sorted(df_idade['DS_FAIXA_ETARIA'].unique(), key=lambda x: int(re.search(r'\d+', x).group()) if re.search(r'\d+', x) else 999)
            fig_idade = px.bar(df_idade, x='DS_FAIXA_ETARIA', y='QT_ELEITORES', title='Faixa Etária', category_orders={"DS_FAIXA_ETARIA": ordem_idade}, color_discrete_sequence=['#4C78A8'])
            fig_idade.update_layout(xaxis_title="", yaxis_title="Eleitores")
            st.plotly_chart(fig_idade, use_container_width=True)
            
        with col_esc:
            df_esc = df_p_filtrado.groupby('DS_GRAU_ESCOLARIDADE')['QT_ELEITORES'].sum().reset_index()
            df_esc = df_esc.sort_values(by='QT_ELEITORES', ascending=True)
            fig_esc = px.bar(df_esc, x='QT_ELEITORES', y='DS_GRAU_ESCOLARIDADE', title='Grau de Escolaridade', orientation='h', color_discrete_sequence=['#F58518'])
            fig_esc.update_layout(xaxis_title="Eleitores", yaxis_title="")
            st.plotly_chart(fig_esc, use_container_width=True)