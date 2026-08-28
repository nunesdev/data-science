# Data Summary Report
**Projeto:** ConectaFood - Plataforma Inteligente de Redistribuição de Alimentos
**Fase TDSP:** 02 - Data Ingestion & Understanding

Este documento relaciona as fontes de dados que serão utilizadas ao longo do projeto, indicando os métodos de coleta, os tipos de dados e o objetivo de cada um dentro do fluxo da aplicação. Este é o primeiro esboço, elaborado como artefato inicial exigido no TP1.

## Tabela de Fontes de Dados

| Fonte de Dados | Método de Coleta | Tipo de Dado | Objetivo de Uso |
| :--- | :--- | :--- | :--- |
| **Observatório do 3º Setor** | Web Scraping (*BeautifulSoup / Requests*) | Texto / HTML Estruturado | Extrair nomes, causas e contatos de ONGs e projetos sociais para compor a base de possíveis receptores das doações. |
| **API de Mapas (OpenStreetMap / ViaCEP)** | Requisição via API Pública | JSON | Obter coordenadas geográficas (Latitude/Longitude) a partir de endereços para plotar doadores e ONGs no dashboard. |
| **Painel de Doações** | Input do Usuário via Interface Streamlit | Texto e Numérico (Inteiros / Floats) | Receber os dados informados pelo doador: descrição do alimento, quantidade em kg, data de validade e endereço de coleta. |
| **API de LLM (IA Generativa)** | Requisição via API (Engenharia de Prompts) | Texto (Retorno Estruturado) | Analisar a descrição do alimento doado para categorizá-lo automaticamente (perecível/não perecível) e sugerir cuidados no transporte. |

---
*Artefato desenvolvido de acordo com as metodologias ágeis de Ciência de Dados (CRISP-DM e TDSP).*