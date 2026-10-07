import streamlit as st
import pandas as pd
import plotly.express as px
import re

# Configuração inicial da página
st.set_page_config(page_title="Apuração Eleitoral TSE", layout="wide")

st.title("📊 Painel de Apuração Eleitoral - Palmas 2026")
st.markdown("Consolidação de votos (BU) e análise (Dados Abertos TSE).")

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
    st.error(f"Ficheiro não encontrado: {e}. Certifique-se de que os dois ficheiros CSV estão na mesma pasta.")
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

regioes_disponiveis = [
    "Todas as Regiões", 
    "Plano Diretor Norte", 
    "Plano Diretor Sul", 
    "Aurenys", 
    "Taquaralto", 
    "Taquari",
    "Taquarucu", 
    "Buritirana e Zona Rural",
    "Bertaville e Acessos",
    "Outros Bairros / Sul Extremo"
]
regiao_selecionada = st.sidebar.selectbox("Região da Cidade:", options=regioes_disponiveis)

df_v_filtrado = df_votos.copy()
df_p_filtrado = df_perfil.copy()

# Aplicação da lógica de filtragem por Região Geográfica
if regiao_selecionada == "Plano Diretor Norte":
    secoes = ['275', '281', '286', '291', '298', '306', '313', '321', '516', '393', '394', '397', '416', '424', '455', '521', '694', '726', '194', '245', '265', '269', '552', '738', '158', '159', '160', '161', '162', '163', '164', '165', '166', '182', '517', '105', '117', '126', '136', '142', '221', '254', '332', '389', '526', '201', '204', '205', '207', '216', '231', '250', '257', '530', '150', '151', '152', '153', '154', '155', '156', '157', '187', '404', '422', '534', '637', '667', '109', '119', '127', '134', '143', '476', '544', '589', '140', '145', '146', '147', '148', '149', '546', '432', '441', '444', '457', '493', '550', '609', '640', '196', '234', '260', '352', '359', '403', '492', '556', '607', '626', '652', '371', '430', '462', '557', '600', '633', '663', '711', '733', '195', '230', '261', '437', '495', '562', '599', '622', '662', '710', '742', '203', '210', '247', '255', '448', '456', '486', '564', '189', '228', '271', '287', '308', '324', '496', '571', '354', '376', '406', '425', '452', '474', '574', '193', '215', '224', '248', '256', '266', '576', '623', '90', '91', '100', '101', '106', '325', '328', '337', '345', '361', '377', '577', '700', '715', '739']
    df_v_filtrado = df_v_filtrado[df_v_filtrado['NR_SECAO'].isin(secoes)]
    df_p_filtrado = df_p_filtrado[df_p_filtrado['NR_SECAO'].isin(secoes)]
    st.sidebar.success(f"📍 Exibindo {len(secoes)} secções do Plano Norte.")

elif regiao_selecionada == "Plano Diretor Sul":
    secoes = ['128', '129', '132', '137', '184', '186', '449', '466', '481', '520', '338', '360', '522', '592', '657', '188', '208', '223', '240', '264', '273', '523', '587', '612', '645', '651', '343', '362', '382', '391', '428', '524', '588', '344', '365', '426', '504', '525', '660', '87', '99', '103', '112', '125', '139', '477', '527', '653', '66', '78', '83', '102', '120', '133', '144', '529', '598', '4', '35', '41', '45', '49', '57', '63', '84', '274', '531', '595', '636', '722', '736', '671', '672', '673', '677', '681', '682', '683', '706', '717', '734', '349', '366', '392', '475', '536', '431', '446', '453', '458', '480', '548', '597', '642', '661', '192', '235', '262', '280', '301', '320', '405', '434', '436', '547', '190', '213', '219', '236', '249', '253', '503', '554', '197', '244', '272', '290', '310', '329', '502', '563', '610', '658', '92', '97', '107', '108', '110', '114', '464', '500', '566', '596', '656', '191', '252', '445', '567', '594', '5', '47', '50', '64', '65', '74', '82', '569', '277', '285', '292', '302', '312', '317', '407', '423', '447', '575', '463', '485', '499', '507', '578', '605', '617', '635', '659', '723', '52', '80', '95', '115', '364', '388', '410', '414', '533', '590', '608', '614', '627', '669', '684', '685', '705', '727', '487', '488', '489', '743', '744', '745', '746', '276', '282', '288', '297', '300', '305', '311', '318', '351', '390', '418', '454', '482', '581', '585', '655', '697', '707', '719', '731', '741', '34', '44', '58', '70', '135', '185', '429', '465', '538', '202', '211', '217', '229', '241', '331', '336', '408', '415', '478', '532', '720']
    df_v_filtrado = df_v_filtrado[df_v_filtrado['NR_SECAO'].isin(secoes)]
    df_p_filtrado = df_p_filtrado[df_p_filtrado['NR_SECAO'].isin(secoes)]
    st.sidebar.success(f"📍 Exibindo {len(secoes)} secções do Plano Sul.")

elif regiao_selecionada == "Aurenys":
    secoes = ['36', '43', '48', '56', '62', '69', '81', '98', '121', '373', '386', '519', '629', '648', '666', '696', '37', '53', '67', '96', '124', '232', '239', '295', '326', '568', '693', '730']
    df_v_filtrado = df_v_filtrado[df_v_filtrado['NR_SECAO'].isin(secoes)]
    df_p_filtrado = df_p_filtrado[df_p_filtrado['NR_SECAO'].isin(secoes)]
    st.sidebar.success(f"📍 Exibindo {len(secoes)} secções da região das Aurenys.")

elif regiao_selecionada == "Taquaralto":
    secoes = ['283', '293', '307', '315', '316', '319', '322', '468', '494', '518', '601', '628']
    df_v_filtrado = df_v_filtrado[df_v_filtrado['NR_SECAO'].isin(secoes)]
    df_p_filtrado = df_p_filtrado[df_p_filtrado['NR_SECAO'].isin(secoes)]
    st.sidebar.success(f"📍 Exibindo as {len(secoes)} secções do CEM Taquaralto.")

elif regiao_selecionada == "Taquari":
    secoes = ['401', '402', '451', '460', '471', '484', '490', '501', '513', '539', '604', '611', '619', '630', '639', '644', '650', '654']
    df_v_filtrado = df_v_filtrado[df_v_filtrado['NR_SECAO'].isin(secoes)]
    df_p_filtrado = df_p_filtrado[df_p_filtrado['NR_SECAO'].isin(secoes)]
    st.sidebar.success(f"📍 Exibindo as {len(secoes)} secções do Jd. Taquari.")

elif regiao_selecionada == "Taquarucu":
    secoes = ['10', '11', '12', '13', '61', '303', '512', '528']
    df_v_filtrado = df_v_filtrado[df_v_filtrado['NR_SECAO'].isin(secoes)]
    df_p_filtrado = df_p_filtrado[df_p_filtrado['NR_SECAO'].isin(secoes)]
    st.sidebar.success(f"📍 Exibindo apenas as {len(secoes)} secções de Taquaruçu.")

elif regiao_selecionada == "Buritirana e Zona Rural":
    secoes = ['304', '433', '470', '509', '510', '561']
    df_v_filtrado = df_v_filtrado[df_v_filtrado['NR_SECAO'].isin(secoes)]
    df_p_filtrado = df_p_filtrado[df_p_filtrado['NR_SECAO'].isin(secoes)]
    st.sidebar.success(f"📍 Exibindo as {len(secoes)} secções da região de Buritirana e Fazendas.")

elif regiao_selecionada == "Bertaville e Acessos":
    secoes = ['93', '130', '172', '173', '174', '175', '176', '177', '178', '179', '180', '181', '183', '330', '342', '357', '378', '411', '541', '675', '735']
    df_v_filtrado = df_v_filtrado[df_v_filtrado['NR_SECAO'].isin(secoes)]
    df_p_filtrado = df_p_filtrado[df_p_filtrado['NR_SECAO'].isin(secoes)]
    st.sidebar.success(f"📍 Exibindo {len(secoes)} secções do Bertaville e vias de acesso.")

elif regiao_selecionada == "Outros Bairros / Sul Extremo":
    secoes = ['2', '3', '15', '38', '39', '40', '42', '51', '55', '59', '68', '73', '76', '77', '79', '86', '88', '89', '94', '104', '113', '116', '123', '131', '138', '141', '167', '168', '169', '170', '171', '198', '199', '200', '206', '209', '212', '214', '218', '220', '222', '226', '227', '233', '237', '238', '242', '243', '258', '259', '267', '268', '270', '278', '279', '284', '289', '294', '296', '299', '309', '314', '327', '334', '335', '346', '347', '348', '355', '356', '358', '368', '370', '374', '379', '380', '381', '383', '385', '387', '396', '398', '399', '400', '417', '419', '421', '438', '440', '442', '443', '450', '467', '469', '472', '473', '508', '537', '540', '542', '543', '549', '551', '553', '560', '570', '572', '573', '579', '580', '586', '591', '593', '602', '603', '613', '616', '621', '625', '632', '634', '641', '646', '647', '649', '664', '668', '670', '674', '688', '690', '721']
    df_v_filtrado = df_v_filtrado[df_v_filtrado['NR_SECAO'].isin(secoes)]
    df_p_filtrado = df_p_filtrado[df_p_filtrado['NR_SECAO'].isin(secoes)]
    st.sidebar.success(f"📍 Exibindo {len(secoes)} secções de bairros periféricos e expansão sul.")

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
aba_resultados, aba_desempenho, aba_perfil = st.tabs(["🗳️ Resultados da Eleição", "🏢 Desempenho e Locais", "👥 Perfil do Eleitorado"])

# ------------------------------------------
# ABA 1: RESULTADOS DA ELEIÇÃO
# ------------------------------------------
with aba_resultados:
    cargos = sorted(df_v_filtrado['DS_CARGO_PERGUNTA'].dropna().unique())
    cargos_selecionados = st.sidebar.multiselect("Cargos (Para Apuração):", options=cargos, default=cargos)
    
    st.sidebar.markdown("---")
    termo_busca = st.sidebar.text_input("Buscar Candidato (Ex: LULA, 13):")

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
            
    with col_logistica:
        st.markdown("**🏫 Polos de Votação (Maiores Colégios)**")
        st.caption("Locais com maior quantidade de seções para organização logística.")
        
        locais_secoes = df_v_filtrado.drop_duplicates(subset=['NR_ZONA', 'NR_LOCAL_VOTACAO', 'NR_SECAO'])
        ranking_locais = locais_secoes.groupby('NR_LOCAL_VOTACAO')['NR_SECAO'].count().reset_index()
        ranking_locais.columns = ['Cód. Local', 'Seções']
        
        ranking_locais['Nome da Escola'] = ranking_locais['Cód. Local'].map(mapa_escolas).fillna('Nome não encontrado')
        
        ranking_locais = ranking_locais[['Nome da Escola', 'Cód. Local', 'Seções']]
        ranking_locais = ranking_locais.sort_values(by='Seções', ascending=False).reset_index(drop=True)
        
        st.dataframe(ranking_locais, use_container_width=True, height=400)

# ------------------------------------------
# ABA 3: PERFIL DO ELEITORADO E INCLUSÃO
# ------------------------------------------
with aba_perfil:
    st.subheader("Demografia e Inclusão Social")
    
    # 1. Cartões de Métricas (KPIs de Inclusão)
    total_eleitores_perfil = df_p_filtrado['QT_ELEITORES'].sum()
    total_pcd = df_p_filtrado['QT_ELEITORES_DEFICIENCIA'].sum()
    total_nome_social = df_p_filtrado['QT_ELEITORES_NOME_SOCIAL'].sum()
    total_quilombola = df_p_filtrado[df_p_filtrado['DS_QUILOMBOLA'] == 'SIM']['QT_ELEITORES'].sum()
    
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    col_t1.metric("Total de Eleitores", f"{total_eleitores_perfil:,}".replace(',', '.'))
    col_t2.metric("Eleitores PCD", f"{total_pcd:,}".replace(',', '.'))
    col_t3.metric("Uso de Nome Social", f"{total_nome_social:,}".replace(',', '.'))
    col_t4.metric("Eleitores Quilombolas", f"{total_quilombola:,}".replace(',', '.'))
    
    st.markdown("---")
    
    if total_eleitores_perfil > 0:
        # Linha 1: Gênero e Identidade de Gênero
        col_gen, col_idgen = st.columns(2)
        with col_gen:
            df_gen = df_p_filtrado.groupby('DS_GENERO')['QT_ELEITORES'].sum().reset_index()
            fig_gen = px.pie(df_gen, values='QT_ELEITORES', names='DS_GENERO', title='Distribuição por Gênero', hole=0.4, color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_gen, use_container_width=True)
        
        with col_idgen:
                    df_id_gen = df_p_filtrado.groupby('DS_IDENTIDADE_GENERO')['QT_ELEITORES'].sum().reset_index()
                    fig_idgen = px.pie(df_id_gen, values='QT_ELEITORES', names='DS_IDENTIDADE_GENERO', title='Identidade de Gênero', hole=0.4, color_discrete_sequence=px.colors.qualitative.Set3)
                    st.plotly_chart(fig_idgen, use_container_width=True)    
        
         # Linha 2: Raça/Cor e  Estado Civil
        col_raca, col_ec = st.columns(2)
        with col_raca:
            df_raca = df_p_filtrado.groupby('DS_RACA_COR')['QT_ELEITORES'].sum().reset_index()
            df_raca = df_raca.sort_values(by='QT_ELEITORES', ascending=True)
            fig_raca = px.bar(df_raca, x='QT_ELEITORES', y='DS_RACA_COR', title='Autodeclaração de Raça/Cor', orientation='h', color_discrete_sequence=['#54A24B'])
            fig_raca.update_layout(xaxis_title="Eleitores", yaxis_title="")
            st.plotly_chart(fig_raca, use_container_width=True)
            
        with col_ec:
                    df_ec = df_p_filtrado.groupby('DS_ESTADO_CIVIL')['QT_ELEITORES'].sum().reset_index()
                    fig_ec = px.pie(df_ec, values='QT_ELEITORES', names='DS_ESTADO_CIVIL', title='Estado Civil', hole=0.4)
                    st.plotly_chart(fig_ec, use_container_width=True)

        # Linha 3: Faixa Etária e Escolaridade
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

        st.markdown("---")
        