# Limitações do LangChain — Parte 2

## OpenAI via LangChain (`ChatOpenAI` + `PromptTemplate`) — Questão 2

- **Latência de rede**: cada tradução depende de ida/volta HTTP à API OpenAI; soma-se ao tempo de serialização LangChain e ao processamento do modelo remoto (RTT + fila do provedor).
- **Rate limits**: cotas por minuto/dia e por organização; picos de tráfego geram HTTP 429 — exige retry com backoff, filas ou múltiplas chaves (governança complexa).
- **Custo e escalabilidade**: cobrança por token; prompts longos e alto volume elevam custo rapidamente; escalar usuários ≠ escalar só instâncias FastAPI — o gargalo é o billing/limites da API.
- **Dependência externa**: indisponibilidade, mudanças de modelo, depreciação de endpoints ou políticas de uso afetam o sistema sem controle total no código local.
- **Qualidade variável**: tradução via LLM genérico pode ser excelente em frases curtas, mas menos previsível que um NMT dedicado; `temperature=0` ajuda, não elimina variância entre versões de modelo.

## Hugging Face via LangChain (`HuggingFacePipeline`) — Questão 3

- **Consumo CPU/GPU**: o pipeline roda no mesmo processo do worker Uvicorn; CPU saturada degrada todas as rotas; GPU exige drivers e alocação de memória.
- **Tempo de carregamento**: download de pesos + inicialização do `transformers.pipeline` no **lifespan** pode levar minutos; cold start em serverless é especialmente penalizado.
- **Overhead de abstração**: `HuggingFacePipeline` encapsula chamadas genéricas; depuração, tuning de batch size, `torch.compile` ou ONNX exigem contornar ou estender a integração LangChain.
- **Fine-tuning**: treino e avaliação costumam ser feitos com API nativa `transformers`/`Trainer`; reencaixar pesos customizados na chain LangChain é possível, porém com atrito (paths, tokenizer, task head).
- **Recursos vs Parte 1**: mesma carga de modelo, mas camada extra de conversão de tipos e `invoke()` — overhead pequeno, porém não nulo em alta taxa de requisições.
