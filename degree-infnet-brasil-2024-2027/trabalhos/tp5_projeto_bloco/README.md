# ConectaFood — TP5 (Projeto de Bloco)

Plataforma de dados e APIs para organizações sociais, com **FastAPI**, **Streamlit**, coleta **Selenium**, **análise de sentimento** local (Hugging Face) e **agente ESG na Groq** que recomenda organizações a partir de `projetos_sociais.csv`.

O agente usa `openai/gpt-oss-120b`. Se a Groq responder que esse modelo não existe (HTTP 404), o serviço chama `models.list()` e refaz a recomendação com o primeiro modelo de texto ativo da conta. Nesta entrega, `qwen/qwen3.8-27b` já cumpriu esse papel.

## Pré-requisitos

- Python 3.9+
- Google Chrome (para o script Selenium)

## Instalação

Na **raiz** deste repositório:

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Na primeira execução da API, o modelo NLP é baixado para o cache local do Hugging Face (~670 MB).

O agente ESG lê a chave em `.env`, na raiz (o arquivo já está no `.gitignore`):

```bash
# edite .env e troque o placeholder pela chave real
GROQ_API_KEY=sua_chave_aqui
```

## Executar a aplicação

Use **dois terminais**, sempre com o ambiente virtual ativado e a **raiz do projeto** como diretório atual.

### Terminal 1 — API FastAPI

Na raiz do projeto (com o `venv` ativo):

```bash
uvicorn --app-dir 04_Deployment api:app --reload
```

É o equivalente funcional de `uvicorn 04_Deployment.api:app --reload`: o nome da pasta começa com `04`, o que impede importar o módulo exatamente nesse formato no Python.

Documentação: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Terminal 2 — App Streamlit

```bash
streamlit run 04_Deployment/app.py
```

## Coleta de dados (Selenium)

Enriquece o CSV usado pela API (`02_Data_Ingestion_Understanding/projetos_sociais.csv`):

```bash
cd 02_Data_Ingestion_Understanding
python coleta_selenium.py
```

## Estrutura principal

| Pasta | Conteúdo |
|-------|----------|
| `01_Business_Understanding/` | Project Charter |
| `02_Data_Ingestion_Understanding/` | CSV, Selenium, Data Summary Report |
| `03_Modeling/` | Justificativa do modelo NLP (TP4) |
| `04_Deployment/` | `api.py`, `app.py`, serviço NLP e agente ESG |

## Rotas úteis

- `GET /ongs` — lista ONGs do CSV
- `POST /ongs` — inclui ONG no CSV
- `POST /processar_texto` — sentimento 1–5 estrelas (modelo local)
- `POST /agente_recomendacao` — agente ESG: recomenda organizações para o interesse informado