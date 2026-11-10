# Tabela comparativa — FastAPI puro vs LangChain (TP2)

Comparação entre a abordagem da **Parte 1** (FastAPI + `transformers` direto) e da **Parte 2** (FastAPI + LangChain orquestrando LLMs/pipelines).

| Critério | FastAPI puro (Parte 1) | LangChain (Parte 2) |
|----------|-------------------------|----------------------|
| **Facilidade de uso / configuração** | Menos dependências; código explícito (`generate`, `MarianMT`). Curva de aprendizado focada em FastAPI + HF. | Mais pacotes e conceitos (chains, prompts, integrações). Configuração rápida para múltiplos provedores, mas ambiente mais fragmentado. |
| **Latência e desempenho** | Menor overhead: chamada direta ao tensor/pipeline. Latência dominada pelo modelo (local). | Camada extra de abstração +, na Q2, latência de rede OpenAI. HF via LangChain: overhead leve sobre pipeline local. |
| **Flexibilidade para diferentes modelos** | Troca manual de classes/tokenizers em `services`; cada modelo pode exigir código específico. | Adaptadores (`ChatOpenAI`, `HuggingFacePipeline`, `FakeListLLM`) permitem trocar provedor com mudanças localizadas em `services`. |
| **Custo e escalabilidade** | Custo principal: infra (CPU/GPU/RAM) sob controle do time; escala com réplicas e filas. | OpenAI: custo variável por token + limites de API. HF local: mesmo perfil da Parte 1; Fake LLM: custo zero, sem valor de produção. |
| **Protótipos vs produção** | **Prototipagem**: excelente para APIs de inferência única e previsível. **Produção**: maduro com observabilidade, batching e serving dedicado (Triton, vLLM, etc.). | **Prototipagem**: ideal para integrar vários LLMs e experimentar prompts/chains rapidamente. **Produção**: viável com governança de custos, retries, versionamento de prompts e testes de regressão nas chains. |
