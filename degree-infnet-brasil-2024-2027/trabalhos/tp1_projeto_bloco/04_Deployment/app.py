import streamlit as st
import pandas as pd
import os

# Configuração inicial da página
st.set_page_config(page_title="ConectaFood - TP1", page_icon="🌱", layout="wide")

# 1. Título do projeto
st.title("🌱 ConectaFood: Inteligência e Dados para Fome Zero")

# 2. Descrição do problema de negócio e dos objetivos
st.header("Sobre o Projeto")
st.markdown("""
**Problema de Negócio:** 
O alto índice de desperdício de alimentos em centros urbanos, que contrasta diretamente com a vulnerabilidade de milhares de pessoas em situação de insegurança alimentar.

**Objetivos do Projeto:** 
Criar uma plataforma analítica e inteligente que conecte estabelecimentos com excedente de alimentos (doadores) a ONGs e projetos sociais (receptores). 
Esta solução utiliza tecnologia (Web Scraping, APIs e IA Generativa) para criar impacto positivo, estando 100% alinhada às práticas ESG e aos seguintes Objetivos de Desenvolvimento Sustentável (Agenda 2030):
* **ODS 2:** Fome Zero e Agricultura Sustentável.
* **ODS 12:** Consumo e Produção Responsáveis.
""")

# 3. Links úteis
st.header("Links Úteis e Inspirações")
st.markdown("""
* [Observatório do 3º Setor (Fonte de Dados Base)](https://observatorio3setor.org.br/lista-conheca-projetos-sociais-de-15-causas-diferentes)
* [Agenda 2030 - Objetivos de Desenvolvimento Sustentável (ONU)](https://brasil.un.org/pt-br/sdgs)
* [Pacto Global da ONU no Brasil - Frente de Direitos Humanos](https://www.pactoglobal.org.br/)
""")

# 4. Tabela exibindo amostras dos dados
st.header("Amostra de Dados (Receptores/ONGs)")
st.markdown("Abaixo está uma amostra dos dados extraídos que comporão a nossa base de ONGs parceiras para o redirecionamento de alimentos:")

# Tenta carregar o CSV gerado no script anterior 
caminho_csv = '../02_Data_Ingestion_Understanding/projetos_sociais.csv'


try:
    df = pd.read_csv(caminho_csv)
    # Exibe as 10 primeiras linhas para não poluir a tela
    st.dataframe(df.head(10), use_container_width=True)
    st.success(f"Base carregada com sucesso! Total de registros disponíveis: {len(df)}")
except FileNotFoundError:
    st.warning("Arquivo de coleta não encontrado. Exibindo dados simulados de estrutura:")