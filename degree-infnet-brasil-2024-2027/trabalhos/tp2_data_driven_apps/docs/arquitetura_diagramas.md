# Diagramas de arquitetura — Parte 2

## Diagrama 1 — Questão 1: Chatbot com FakeListLLM

```mermaid
flowchart LR
    Cliente([Cliente HTTP])
    FastAPI[FastAPI<br/>POST /questao1/chat]
    Router[Router questao1]
    Service[fake_llm_service]
    LC[LangChain<br/>FakeListLLM]
    Resp[JSON ChatResponse]

    Cliente -->|mensagem JSON| FastAPI
    FastAPI --> Router
    Router --> Service
    Service -->|invoke prompt| LC
    LC -->|resposta simulada| Service
    Service --> Router
    Router --> Resp
    Resp --> Cliente
```

**Notas**

- Não há chamada externa: respostas vêm de uma lista fixa no `FakeListLLM`.
- Útil para testar contrato JSON, rotas e tratamento de erros sem consumir API paga.
- O comportamento de “rodízio” das respostas é inerente ao `FakeListLLM`, não a um modelo treinado.

---

## Diagrama 2 — Questão 2: Tradução EN→FR com OpenAI

```mermaid
flowchart LR
    Cliente([Cliente HTTP])
    FastAPI[FastAPI<br/>POST /questao2/traduzir]
    Router[Router questao2]
    Service[openai_service]
    Prompt[PromptTemplate<br/>EN → FR]
    Chat[ChatOpenAI<br/>LangChain]
    API[(API OpenAI<br/>nuvem)]
    Resp[JSON TranslationResponse]

    Cliente -->|texto_ingles| FastAPI
    FastAPI --> Router
    Router --> Service
    Service --> Prompt
    Prompt --> Chat
    Chat -->|HTTPS + API Key| API
    API -->|texto em francês| Chat
    Chat --> Service
    Service --> Router
    Router --> Resp
    Resp --> Cliente
```

**Notas**

- A chave `OPENAI_API_KEY` é lida de variável de ambiente no serviço (não versionada).
- Latência total ≈ rede + tempo do modelo remoto; `temperature=0` favorece traduções estáveis.
- Falhas de quota ou rede mapeiam para HTTP 502/503 nos routers.

---

## Diagrama 3 — Questão 3: Tradução EN→DE com HuggingFacePipeline

```mermaid
flowchart LR
    Cliente([Cliente HTTP])
    FastAPI[FastAPI<br/>POST /questao3/traduzir]
    Router[Router questao3]
    Service[huggingface_service]
    HFP[HuggingFacePipeline<br/>LangChain]
    Model[(Helsinki-NLP<br/>opus-mt-en-de)]
    Resp[JSON TranslationResponse]

    Cliente -->|texto_ingles| FastAPI
    FastAPI --> Router
    Router --> Service
    Service -->|invoke| HFP
    HFP -->|transformers pipeline| Model
    Model -->|tradução DE| HFP
    HFP --> Service
    Service --> Router
    Router --> Resp
    Resp --> Cliente
```

**Notas**

- O modelo é carregado no **lifespan** do FastAPI (uma vez por worker), amortizando cold start.
- Inferência local: sem custo por token, mas exige RAM e competição por CPU com outras requisições.
- Comparado à Parte 1 (MarianMT direto), o fluxo lógico é o mesmo; LangChain adiciona a facade `HuggingFacePipeline` para unificar `invoke()` com outros LLMs.
