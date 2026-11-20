# NLP model — ConectaFood

## Problem

ConectaFood lists Brazilian NGOs and social projects with free-text descriptions in Portuguese. A **1–5 star** sentiment score helps compare tone across organizations in the dashboard and API.

## Model

| Field | Value |
|-------|--------|
| Hugging Face ID | [`nlptown/bert-base-multilingual-uncased-sentiment`](https://huggingface.co/nlptown/bert-base-multilingual-uncased-sentiment) |
| Output | Five star classes |
| Weights (disk) | ~670 MB in the local HF cache after first download |

**Why not English-only DistilBERT?** Descriptions are in PT-BR; multilingual BERT keeps granularity (5 stars) without a translation step.

## API integration

- Model loads on FastAPI startup (`lifespan` in `api/main.py`).
- Inference runs in `api/nlp.py` via `transformers` pipeline with `truncation=True`, `max_length=512`.
- `texto_original` in the response is the user input (stripped); `truncado` is `true` when the tokenizer needs more than 512 tokens.
- Concurrent calls are serialized with a thread lock around inference; CSV writes are locked in the API.

## Reproduce benchmarks

From the project root, with dev dependencies installed:

```bash
python -m benchmarks.bench_inference
```

Raw output: `benchmarks/results.json` (also summarized in the root `README.md`).