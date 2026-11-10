# Teste de Performance — TP2

## Descrição

Este repositório reúne a entrega do **Teste de Performance (TP2)** da disciplina **Desenvolvimento de Data-Driven Apps com Python** (Infnet). O trabalho implementa APIs REST com **FastAPI**, integração a modelos **Hugging Face (Transformers)** e orquestração com **LangChain**, além da documentação teórica exigida pela rubrica (limitações de modelos, LangChain, tabela comparativa e diagramas de arquitetura).

O objetivo é demonstrar, de forma modular e reproduzível, dois estilos de integração de IA em serviços HTTP: **inferência direta com Transformers** (Parte 1) e **abstração via LangChain** com provedores locais, simulados e em nuvem (Parte 2).

---

## Estrutura do repositório

```text
tp2_data_driven_apps/
├── README.md              # Este guia mestre
├── parte1/                # Parte 1 — FastAPI puro + Hugging Face
│   ├── app/
│   ├── requirements.txt
│   └── README.md
├── parte2/                # Parte 2 — FastAPI + LangChain
│   ├── app/
│   ├── requirements.txt
│   └── README.md
└── docs/                    # Respostas teóricas e diagramas (Markdown)
    ├── limitacoes_modelos_parte1.md
    ├── limitacoes_langchain_parte2.md
    ├── tabela_comparativa.md
    └── arquitetura_diagramas.md
```

| Pasta | Propósito |
|-------|-----------|
| **`/parte1`** | Questões 1 e 2 com **FastAPI puro**: continuação de texto com **GPT-2** e tradução **inglês → francês** (`Helsinki-NLP/opus-mt-en-fr`) via `transformers`, sem LangChain. |
| **`/parte2`** | Questões 1, 2 e 3 com **FastAPI + LangChain**: chatbot **FakeListLLM**, tradução **EN→FR** com **OpenAI** (`ChatOpenAI`), tradução **EN→DE** com **HuggingFacePipeline** (`Helsinki-NLP/opus-mt-en-de`). |
| **`/docs`** | Conteúdo **teórico** para correção: limitações dos modelos (Parte 1), limitações do LangChain (Parte 2), **tabela comparativa** FastAPI puro vs LangChain e **diagramas Mermaid** das três arquiteturas da Parte 2. |

---

## Instruções de navegação (avaliador)

Os módulos **`parte1`** e **`parte2`** são **independentes**: cada um possui seu próprio `requirements.txt`, estrutura `app/` e **README dedicado** com instalação, execução, configuração (incluindo `OPENAI_API_KEY` na Parte 2) e **exemplos `curl`** para todos os endpoints.

**Recomendação de execução**

1. **Parte 1** — siga [`parte1/README.md`](parte1/README.md). Crie um ambiente virtual **dentro de `parte1/`**, instale as dependências e suba a API (porta sugerida: **8000**).
2. **Parte 2** — siga [`parte2/README.md`](parte2/README.md). Use um ambiente virtual **separado em `parte2/`**, defina `OPENAI_API_KEY` para a Questão 2 e suba a API (porta sugerida: **8001** para evitar conflito com a Parte 1).
3. **Documentação** — leia os arquivos em [`docs/`](docs/). Os diagramas em `arquitetura_diagramas.md` usam blocos **Mermaid** (renderizam no GitHub e em visualizadores compatíveis).

Não é necessário unificar dependências na raiz: isso evita conflitos de versão entre o stack “puro” da Parte 1 e o ecossistema LangChain da Parte 2.

**Documentação interativa das APIs**

- Parte 1: `http://127.0.0.1:8000/docs` (após `uvicorn app.main:app` em `parte1/`)
- Parte 2: `http://127.0.0.1:8001/docs` (após `uvicorn app.main:app` em `parte2/`)

---

## Nota de entrega

Conforme a **rubrica de avaliação**, o conteúdo teórico da pasta **`/docs`** (limitações, tabela comparativa e diagramas) foi **exportado para PDF** para compor o arquivo **`.ZIP` final** da entrega, junto com o código-fonte de `/parte1` e `/parte2`. Os arquivos `.md` neste repositório permanecem como fonte versionável e referência no GitHub; o PDF reflete o mesmo conteúdo entregue na avaliação.

---

## Autor e contexto acadêmico

Trabalho obrigatório — **Teste de Performance TP2** — curso de Ciência de Dados / Data-Driven Apps (Infnet Brasil, 2024–2027).
