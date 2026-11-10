# Tabela comparativa — FastAPI puro vs LangChain (TP2)

Comparação entre a abordagem da **Parte 1** (FastAPI + `transformers` direto) e da **Parte 2** (FastAPI + LangChain orquestrando LLMs/pipelines).

| Critério | FastAPI puro (Parte 1) | LangChain (Parte 2) |
|----------|-------------------------|----------------------|
| **Facilidade de uso / configuração** | Menos dependências; código explícito (`generate`, `MarianMT`). Curva de aprendizado focada em FastAPI + HF. | Mais pacotes e conceitos (chains, prompts, integrações). Configuração rápida para múltiplos provedores, mas ambiente mais fragmentado. |
| **Latência e desempenho** | Menor overhead: chamada direta ao tensor/pipeline. Latência dominada pelo modelo (local). | Camada extra de abstração +, na Q2, latência de rede OpenAI. HF via LangChain: overhead leve sobre pipeline local. |
| **Flexibilidade para diferentes modelos** | Troca manual de classes/tokenizers em `services`; cada modelo pode exigir código específico. | Adaptadores (`ChatOpenAI`, `HuggingFacePipeline`, `FakeListLLM`) permitem trocar provedor com mudanças localizadas em `services`. |
| **Custo e escalabilidade** | Custo principal: infra (CPU/GPU/RAM) sob controle do time; escala com réplicas e filas. | OpenAI: custo variável por token + limites de API. HF local: mesmo perfil da Parte 1; Fake LLM: custo zero, sem valor de produção. |
| **Protótipos vs produção** | **Prototipagem**: excelente para APIs de inferência única e previsível. **Produção**: maduro com observabilidade, batching e serving dedicado (Triton, vLLM, etc.). | **Prototipagem**: ideal para integrar vários LLMs e experimentar prompts/chains rapidamente. **Produção**: viável com governança de custos, retries, versionamento de prompts e testes de regressão nas chains. |

## Custo e Escalabilidade (Aprofundamento)

* **Parte 1 (Modelos Locais):** O custo é fixo e dominado pela infraestrutura (tamanho e RAM da instância/VM). A escalabilidade exige replicação horizontal, o que multiplica o custo de hardware e a necessidade de memória, já que cada *worker* carrega os pesados modelos na memória.
* **Parte 2 - Questão 2 (OpenAI via LangChain):** O custo é variável e baseado na quantidade de tokens processados (modelo *Pay-as-you-go*), além de envolver latência de rede. A escalabilidade é muito mais simples (terceirizada para a OpenAI), sendo limitada apenas pelo seu *budget* e pelos *rate limits* da API.
* **Parte 2 - Questão 3 (Modelos Locais via LangChain):** Compartilha o mesmo perfil de infraestrutura da Parte 1, exigindo instâncias parrudas, com a adição de um pequeno *overhead* de processamento gerado pelas abstrações do próprio LangChain.