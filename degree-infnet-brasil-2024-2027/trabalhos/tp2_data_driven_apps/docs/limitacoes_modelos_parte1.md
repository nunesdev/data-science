# Limitações dos modelos — Parte 1 (FastAPI puro + Hugging Face)

## Helsinki-NLP / MarianMT (`opus-mt-en-fr`) — Questão 2

- **Precisão contextual**: modelos de tradução automática neurais (NMT) tendem a traduzir frase a frase; pronomes, polissemia e referências longas podem sair incorretas sem contexto global ou memória de documento.
- **Gírias e domínio específico**: treinados em corpora paralelos gerais; expressões informais, regionalismos, jargão médico/jurídico e neologismos frequentemente são traduzidos literalmente ou de forma inadequada.
- **Tempo de resposta em escala**: inferência local é **síncrona e CPU/GPU-bound**; sem fila, cache ou réplicas, muitas requisições concorrentes aumentam latência (p95/p99) e risco de timeout.
- **Custo computacional**: cada instância do serviço carrega pesos na memória; escalar horizontalmente multiplica RAM/VRAM; GPU melhora throughput mas eleva custo de infraestrutura.
- **Outras**: limite de comprimento de entrada (`max_length`); textos muito longos exigem chunking manual; qualidade cai em listas, tabelas e HTML/markup sem pré-processamento.

## GPT-2 (`gpt2`) — Questão 1

- **Coerência**: modelo autoregressivo pequeno (2019); continuações podem divergir do tema, repetir padrões ou perder consistência factual em textos longos.
- **Alucinações**: gera texto plausível sem verificação de fatos; não há base de conhecimento confiável — adequado a demonstração, não a conteúdo crítico.
- **Latência**: primeira carga do modelo é lenta; geração token a token em CPU é perceptível; `max_new_tokens` alto aumenta tempo linearmente.
- **Moderação de conteúdo**: **sem** filtros de segurança nativos; pode produzir linguagem inadequada se o prompt permitir — exige camadas externas (policies, classificadores) em produção.
- **Outras**: janela de contexto curta (~1024 tokens no GPT-2 clássico); viés dos dados de treino; sampling (`top_k`/`top_p`) introduz variabilidade entre execuções.
