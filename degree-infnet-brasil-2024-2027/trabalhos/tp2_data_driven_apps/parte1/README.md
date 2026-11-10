# TP2 — Parte 1: FastAPI puro + Hugging Face Transformers

Implementação das **Questões 1 e 2** com APIs REST em FastAPI, sem LangChain. Os modelos são encapsulados em serviços dedicados e carregados no **lifespan** da aplicação, evitando recarregar pesos a cada requisição (boa prática para latência e uso de memória).

## Estrutura do projeto

```text
parte1/
├── app/
│   ├── main.py                 # FastAPI app + lifespan (carga dos modelos)
│   ├── config.py               # IDs dos modelos Hugging Face
│   ├── schemas.py              # Contratos JSON (Pydantic)
│   ├── routers/
│   │   ├── questao1.py         # POST /questao1/continuar
│   │   └── questao2.py         # POST /questao2/traduzir
│   └── services/
│       ├── gpt2_service.py     # Inferência GPT-2
│       └── translation_service.py  # MarianMT EN→FR
├── requirements.txt
└── README.md
```

## Requisitos

- Python **3.10+**
- ~2–4 GB de RAM livre (primeira execução baixa os pesos do Hugging Face)
- Conexão com a internet na **primeira** execução (cache em `~/.cache/huggingface`)

Opcional: GPU CUDA acelera a inferência; o código funciona em CPU.

## Instalação

```bash
cd parte1
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Executar a API

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Aguarde o log de carregamento dos modelos antes de testar os endpoints (pode levar alguns minutos na primeira vez).

- Documentação interativa: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Health check: `GET /health`

## Endpoints

### Questão 1 — Continuação de texto (GPT-2)

**`POST /questao1/continuar`**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `frase` | string | Texto inicial (obrigatório) |
| `max_new_tokens` | int | Tokens gerados (padrão: 50, máx.: 256) |

**Exemplo (curl):**

```bash
curl -s -X POST http://127.0.0.1:8000/questao1/continuar \
  -H "Content-Type: application/json" \
  -d '{"frase": "The future of artificial intelligence is", "max_new_tokens": 40}'
```

**Resposta (exemplo):**

```json
{
  "frase_original": "The future of artificial intelligence is",
  "continuacao": "...",
  "texto_completo": "The future of artificial intelligence is ...",
  "modelo": "gpt2"
}
```

**Modelo:** [`gpt2`](https://huggingface.co/gpt2) via `transformers` (`GPT2LMHeadModel` + `GPT2Tokenizer`). Geração com amostragem (`top_k` / `top_p`) para texto mais variado em demonstrações.

### Questão 2 — Tradução inglês → francês

**`POST /questao2/traduzir`**

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `texto` | string | Texto em inglês (obrigatório) |

**Exemplo (curl):**

```bash
curl -s -X POST http://127.0.0.1:8000/questao2/traduzir \
  -H "Content-Type: application/json" \
  -d '{"texto": "Hello, how are you today?"}'
```

**Resposta (exemplo):**

```json
{
  "texto_original": "Hello, how are you today?",
  "texto_traduzido": "Bonjour, comment allez-vous aujourd'hui ?",
  "idioma_origem": "en",
  "idioma_destino": "fr",
  "modelo": "Helsinki-NLP/opus-mt-en-fr"
}
```

**Modelo:** [`Helsinki-NLP/opus-mt-en-fr`](https://huggingface.co/Helsinki-NLP/opus-mt-en-fr) (MarianMT).

## Tratamento de erros

- **422** — JSON inválido ou campos fora dos limites (validação Pydantic).
- **503** — Modelo ainda não carregado ou falha na inicialização (`/health` indica o estado).
- **500** — Erro inesperado na inferência (registrado no log do servidor).

## Decisões arquiteturais (rubrica)

1. **Separação routers / services** — Endpoints HTTP não importam `transformers` diretamente; facilita testes e manutenção.
2. **Lifespan** — Uma carga por processo do worker; padrão recomendado para modelos pesados em FastAPI.
3. **Config centralizada** — Troca de checkpoint (ex.: `gpt2-medium`) em um único arquivo (`config.py`).
4. **Respostas JSON explícitas** — Campos `modelo`, textos original e resultado para rastreabilidade acadêmica.

## Próximos passos

A **Parte 2** (LangChain + OpenAI + HF via chains) será implementada em `../parte2`. A documentação teórica ficará em `../docs`.
