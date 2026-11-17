# Data Summary Report

| Campo | Valor |
|-------|--------|
| **Projeto** | ConectaFood — Plataforma Inteligente de Redistribuição de Alimentos |
| **Fase TDSP** | 02 — Data Ingestion & Understanding |
| **Versão** | **v3.0 — Integração de IA** |
| **Data da revisão** | **16 de novembro de 2026** |

Este documento consolida as fontes de dados do projeto após as entregas TP2–TP4: coleta estática (BeautifulSoup), coleta dinâmica (Selenium integrada ao CSV principal), API FastAPI e modelo NLP local.

## Tabela de fontes de dados

| Fonte de Dados | Método de Coleta | Tipo de Dado | Objetivo de Uso |
| :--- | :--- | :--- | :--- |
| **Observatório do 3º Setor** | Web Scraping (*BeautifulSoup / Requests*) | Texto / HTML estruturado | Base inicial de ONGs em `projetos_sociais.csv` (nome, atuação, site, descrição). |
| **Observatório do 3º Setor (dinâmico)** | Web Scraping (*Selenium / WebDriver*) | Texto estruturado → **append no CSV principal** | Atualizar a mesma base consumida pela API e pelo Streamlit (`coleta_selenium.py` → `projetos_sociais.csv`). |
| **API ConectaFood (FastAPI)** | Requisições HTTP (GET/POST) | JSON | Backend central: listagem/cadastro de ONGs e `POST /processar_texto` (sentimento). |
| **Painel Streamlit** | Input do usuário + chamadas HTTP | Texto / tabelas | Dashboard, integração com a API e testes de NLP na aba *Análise de Sentimento*. |
| **Modelo NLP local (Hugging Face)** | `transformers` em CPU (sem API na nuvem na inferência) | JSON (Pydantic) | Classificar descrições das ONGs em **1–5 estrelas** (`nlptown/bert-base-multilingual-uncased-sentiment`). |
| **API de Mapas (evolução)** | Requisição via API pública (planejado) | JSON | Geolocalização para mapas no dashboard (não implementado no MVP atual). |

## Fluxo de dados atual

```text
Observatório (BS4 / Selenium) → projetos_sociais.csv → FastAPI (/ongs) → Streamlit
Descrição de ONG → POST /processar_texto → modelo local → resposta JSON → Streamlit
```

## Artefatos relacionados

- `projetos_sociais.csv` — base principal da aplicação
- `dados_coletados_selenium.csv` — snapshot dos **últimos** registros novos inseridos via Selenium (auditoria)
- `03_Modeling/Justificativa_Modelo_TP4.md` — desempenho e custo computacional do NLP

---

*Artefato revisado conforme metodologias CRISP-DM e TDSP (entrega consolidada TP4).*