# TP2 — Parte 2: FastAPI + LangChain

APIs das **questões 1, 2 e 3** com LangChain: `FakeListLLM`, `ChatOpenAI` (tradução EN→FR) e `HuggingFacePipeline` com `Helsinki-NLP/opus-mt-en-de`.

## Estrutura

```text
parte2/
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── questao1.py    # POST /questao1/chat
│   │   ├── questao2.py    # POST /questao2/traduzir  (OpenAI)
│   │   └── questao3.py    # POST /questao3/traduzir  (HF local)
│   └── services/
│       ├── fake_llm_service.py
│       ├── openai_service.py
│       └── huggingface_service.py
├── requirements.txt
└── README.md
```

## Instalação

```bash
cd parte2
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Chave da OpenAI (Questão 2)

**Não** coloque a chave no código. Use variável de ambiente:

```bash
export OPENAI_API_KEY="SUA_CHAVE_AQUI"
```

Substitua `SUA_CHAVE_AQUI` pela chave real da plataforma OpenAI. O arquivo `app/services/openai_service.py` documenta o mesmo placeholder.

Verifique com `GET /health` → `openai_api_key_configurada: true`.

## Executar

Use a porta **8001** para não conflitar com a Parte 1 (8000):

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

- Swagger: http://127.0.0.1:8001/docs  
- Health: http://127.0.0.1:8001/health  

Aguarde o carregamento do modelo EN→DE no log antes de testar a questão 3.

## Exemplos curl

### Questão 1 — Chat (FakeListLLM)

```bash
curl -s -X POST http://127.0.0.1:8001/questao1/chat \
  -H "Content-Type: application/json" \
  -d '{"mensagem": "Hello, can you explain APIs?"}'
```

### Questão 2 — Tradução EN→FR (OpenAI)

```bash
curl -s -X POST http://127.0.0.1:8001/questao2/traduzir \
  -H "Content-Type: application/json" \
  -d '{"texto_ingles": "The deployment was successful."}'
```

### Questão 3 — Tradução EN→DE (Hugging Face local)

```bash
curl -s -X POST http://127.0.0.1:8001/questao3/traduzir \
  -H "Content-Type: application/json" \
  -d '{"texto_ingles": "Machine learning transforms data into insights."}'
```

## Códigos de erro comuns

| HTTP | Causa |
|------|--------|
| 422 | JSON inválido (Pydantic) |
| 503 | `OPENAI_API_KEY` ausente (Q2) ou modelo HF não carregado (Q3) |
| 502 | Falha na API OpenAI (rede, quota, etc.) |
| 500 | Erro interno na cadeia LangChain |

## Modularidade

Cada `service` encapsula um provedor LangChain; os `routers` só validam entrada e mapeiam exceções para HTTP. Diagramas e análise teórica estão em `../docs/`.
