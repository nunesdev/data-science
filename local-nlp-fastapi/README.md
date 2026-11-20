# ConectaFood — Local NLP + FastAPI

Data platform for Brazilian NGOs and social projects: **FastAPI** backend, **Streamlit** dashboard (UI in **Portuguese**, matching the PT-BR dataset), **BeautifulSoup** ingestion, and **local sentiment analysis** (`nlptown/bert-base-multilingual-uncased-sentiment`).

Aligned with SDG 2 (Zero Hunger) and SDG 12 (Responsible Consumption).

## Prerequisites

- Python 3.9+
- ~670 MB Hugging Face model cache after the first successful model load

## Install

From this folder (`local-nlp-fastapi`):

```bash
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Optional: copy `.env.example` to `.env` and set `API_URL` for the Streamlit app.

## Run (two terminals)

Project root = this directory, venv activated.

**Terminal 1 — API**

```bash
uvicorn api.main:app --reload
```

Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

**Terminal 2 — Streamlit**

```bash
streamlit run app/dashboard.py
```

## Data ingestion

Append new NGOs from the [Observatório do 3º Setor](https://observatorio3setor.org.br/) list (deduplicated by name + site):

```bash
python -m ingestion.scrape
```

Canonical dataset: `data/projetos_sociais.csv` (49 rows after cleanup: removed blank names, trailing `Voltar` artifacts).

## API routes

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/ongs` | List NGOs from the CSV |
| `POST` | `/ongs` | Append an NGO (CSV locked) |
| `POST` | `/processar_texto` | Sentiment 1–5 stars; `truncado` if input exceeds 512 tokens |

## Project layout

```text
local-nlp-fastapi/
├── api/           # FastAPI + NLP service
├── app/           # Streamlit dashboard (PT-BR UI)
├── benchmarks/    # Local inference benchmark
├── data/          # projetos_sociais.csv
├── docs/          # Model notes
└── ingestion/     # scrape.py
```

## CPU benchmark (Nov 2026)

Reproduce:

```bash
python -m benchmarks.bench_inference
```

Output: `benchmarks/results.json` (and stdout). Environment: macOS 15.7.7 arm64, Python 3.9.6, 8 logical CPUs, **CPU** inference.

| Metric | Value |
|--------|------:|
| Dataset rows | 49 |
| Model load (TestClient lifespan) | 0.16 s |
| Peak RSS | 717.3 MB |
| Mean latency (across 5 samples × 3 runs) | **55.15 ms** |

| NGO (sample) | Chars | Mean latency (ms) | Stars |
|--------------|------:|------------------:|------:|
| Associação Antialcoólica do Estado de São Paulo | 148 | 49.29 | 4 |
| Projeto Eu Acredito | 240 | 47.46 | 5 |
| Consulado da mulher | 277 | 49.13 | 4 |
| Desaparecidos do Brasil | 345 | 56.32 | 4 |
| Organização Bem-Animal (OBA!) | 494 | 73.57 | 4 |

More detail: [docs/model.md](docs/model.md).

## Design notes

- Dashboard loads NGOs via `GET /ongs` when the API is up; falls back to `data/projetos_sociais.csv` with a caption.
- NLP inference and CSV writes use thread locks for safe concurrent access under uvicorn.
- Long inputs use `truncation=True, max_length=512` on the pipeline; `texto_original` remains the full stripped user text.

## License / portfolio

This project was refactored from a university block project into a standalone portfolio layout inside the `data-science` monorepo.