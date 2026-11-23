# Data Summary Report

| Campo | Valor |
|-------|--------|
| **Projeto** | ConectaFood — Plataforma inteligente de conexão com organizações sociais |
| **Fase TDSP** | 02 — Data Ingestion & Understanding |
| **Versão** | **v4.0 — Ciclo fechado (TP5)** |
| **Data da revisão** | **23 de novembro de 2026** |

Este relatório fecha o ciclo de vida dos dados do ConectaFood. As versões anteriores registraram a coleta (BeautifulSoup e Selenium), a publicação do CSV na API e o uso das descrições no modelo local de sentimento. Esta versão registra o uso que faltava: o mesmo CSV vira o contexto de um agente de linguagem que recomenda organizações e justifica a decisão em ESG e ODS.

## 1. Fontes de dados

| Fonte de dados | Método de coleta | Tipo de dado | Uso no ciclo |
| :--- | :--- | :--- | :--- |
| **Observatório do 3º Setor** | Web scraping (BeautifulSoup / Requests) | Texto estruturado | Carga inicial de `projetos_sociais.csv` (nome, atuação, site, descrição). |
| **Observatório do 3º Setor (dinâmico)** | Web scraping (Selenium / WebDriver) | Texto estruturado, acrescentado ao CSV principal | Atualizar a mesma base lida pela API, pelo dashboard e pelo agente (`coleta_selenium.py`). |
| **API ConectaFood (FastAPI)** | HTTP (GET/POST) | JSON | `GET/POST /ongs`, `POST /processar_texto` (sentimento local) e `POST /agente_recomendacao` (decisão ESG). |
| **Painel Streamlit** | Leitura do CSV e chamadas HTTP | Tabela, gráficos e texto | Visão geral do catálogo e formulário do agente. O sentimento continua em página própria e não grava estrela no arquivo. |
| **Modelo de sentimento (Hugging Face)** | `transformers` em CPU | JSON | Classifica uma descrição enviada na hora, em 1 a 5 estrelas. Não altera o CSV. |
| **API Groq** | Chat Completions, sob demanda. Padrão: `openai/gpt-oss-120b`. Se a Groq responder 404, `models.list()` escolhe outro modelo de texto ativo (na conta desta entrega, `qwen/qwen3.8-27b`). | JSON | Recebe o catálogo como contexto e devolve a recomendação. Não é fonte de organizações: só lê o que o CSV já tem. |

A geolocalização citada em versões anteriores permanece fora do ciclo. Não há coordenada no CSV e o dashboard final não desenha mapa.

## 2. O que há no arquivo principal

Arquivo: `02_Data_Ingestion_Understanding/projetos_sociais.csv`.

| Coluna | O que contém de fato | Uso |
|--------|----------------------|-----|
| `Nome` | Nome da organização | Identidade da recomendação. Linha sem nome sai do contexto do agente e dos gráficos. |
| `Atuação` | Cobertura geográfica (cidade, estado, Brasil, vários países). Não é a causa social. | Contexto da recomendação e gráfico de cobertura. |
| `Site` | URL ou contato | Link devolvido ao usuário, copiado da linha original. |
| `Descrição` | Texto livre em português, vindo da página coletada | Matéria-prima do sentimento, do gráfico temático e do contexto do agente. |

Não existe coluna de sentimento, de ODS nem de pilar ESG. Estrelas, temas dos gráficos e ODS da recomendação são camadas calculadas na aplicação. O arquivo bruto continua sendo só o que a coleta gravou.

Artefatos vizinhos:

- `dados_coletados_selenium.csv` — snapshot dos últimos registros incluídos pelo Selenium, para auditoria da coleta. Não é a base que a API lê.
- `04_Deployment/projetos_filtrados.csv` — recorte antigo de exploração. A aplicação final lê o CSV da pasta de ingestão.

## 3. Qualidade observada

A coleta funcionou, e o arquivo ainda carrega marcas disso:

- Há uma linha de teste (`Nome` = Teste) e uma linha com nome vazio. As duas aparecem na tabela do dashboard, para a base não ser escondida, e saem dos gráficos e do prompt.
- Algumas descrições terminam com a palavra `Voltar`, resto de botão da página. O agente remove esse sufixo ao montar o contexto. O CSV original não é regravado por essa limpeza.
- `Atuação` mistura valores curtos (`São Paulo`, `Brasil`) com frases longas (“sede em São Paulo, mas realiza trabalho em todo o país”). Por isso o gráfico de cobertura agrupa rótulos, em vez de contar cada frase como uma categoria.
- Os textos são institucionais e majoritariamente positivos. Isso explica, no TP4, por que o sentimento local tende a 4 ou 5 estrelas com confiança moderada: o modelo foi treinado em avaliações, e aqui o texto é uma descrição de missão.
- Não há data de coleta por linha nem chave estável além do nome. Uma nova execução do Selenium pode repetir organizações se a deduplicação do script não reconhecer o mesmo nome.

Nada disso impede o uso analítico. Impede tratar o CSV como um cadastro oficial de ODS.

## 4. Como o CSV vira contexto do agente

O agente não consulta o Observatório na hora da pergunta. Ele relê o arquivo que a coleta já consolidou. O caminho está em `04_Deployment/services/agent_service.py` e é o que o enunciado pede como uso dos dados na decisão:

1. **Carga.** `pandas.read_csv` traz a tabela para memória a cada `POST /agente_recomendacao`.
2. **Seleção.** Saem a linha de teste e as linhas sem nome. A descrição perde o sufixo `Voltar` e espaços repetidos.
3. **Recuperação simples.** O interesse do usuário é reduzido a palavras (sem acento, sem termos vazios como “quero” e “para”). Cada organização recebe uma contagem dessas palavras no nome, na cobertura e na descrição. A lista é ordenada por essa contagem. Não há embedding nem índice vetorial: com dezenas de linhas, o catálogo válido cabe no prompt (teto de 28 mil caracteres; a descrição de cada uma é cortada em 600 caracteres se passar disso). Se a base crescer além do teto, as primeiras posições — as mais parecidas com o interesse — são as que permanecem.
4. **Geração.** O prompt de sistema define o especialista ESG. A mensagem do usuário leva perfil, interesse e os blocos do catálogo. O modelo padrão é `openai/gpt-oss-120b`, na API da Groq. Se esse id responder 404, o serviço lista os modelos da conta e refaz a chamada com o primeiro modelo de texto ativo (`qwen/qwen3.8-27b` já ocupou esse lugar). A resposta volta em JSON.
5. **Conferência.** Cada nome recomendado é comparado ao CSV. Site e cobertura exibidos são os da linha encontrada, não os que o modelo reescreveu. Nome ausente no arquivo é descartado.

Esse é o ciclo que faltava documentar. O CSV deixa de ser só a tabela do dashboard e passa a ser a base de conhecimento da decisão. A ordenação lexical ajuda o modelo a ver primeiro o que se parece com a pergunta; a permissão de usar somente o catálogo, e a conferência posterior, é o que impede a resposta de se soltar dos dados coletados.

O sentimento local não entra nesse contexto. São duas leituras do mesmo texto: uma classifica o tom de uma descrição avulsa; a outra compara o catálogo com um objetivo de quem decide.

## 5. O que o dashboard calcula em cima do mesmo arquivo

A aba **Visão geral e dados** lê o CSV direto, sem passar pela Groq.

| Visual | Regra | O que não é |
|--------|--------|-------------|
| Tabela | Arquivo inteiro, inclusive linha fraca | Lista já recomendada pelo agente |
| Organizações por área temática | Palavras na descrição e no nome (educação, fome, mulheres, clima, e outras). Uma linha pode contar em mais de um tema. | Classificador treinado ou rótulo oficial da fonte |
| Organizações por cobertura | Agrupamento da coluna `Atuação` (nacional, internacional, vários estados, ou o lugar citado) | Mapa |

Não há gráfico de sentimento porque a estrela não foi persistida. Incluir um gráfico desse tipo exigiria classificar o CSV inteiro e guardar o resultado — passo não feito, e declarado aqui para não parecer um dado que a base não tem.

## 6. Fluxo de dados da versão final

```text
Observatório do 3º Setor
        │
        ├─ BeautifulSoup  ─┐
        └─ Selenium       ─┴─► projetos_sociais.csv
                                    │
                                    ├─► GET/POST /ongs  ─► cadastro no dashboard
                                    ├─► descrição avulsa ─► POST /processar_texto
                                    │                         └─► estrelas (não grava no CSV)
                                    ├─► aba Visão geral (tabela e gráficos)
                                    └─► POST /agente_recomendacao
                                            │  limpeza + ordenação + prompt
                                            ▼
                                        API Groq (gpt-oss-120b ou fallback)
                                            │  JSON
                                            ▼
                                        nomes conferidos no CSV
                                            │
                                            ▼
                                        aba Agente inteligente ESG
```

## 7. Limitações que permanecem

- O contexto é o arquivo inteiro (até o teto de caracteres), não um índice semântico. Um interesse escrito com sinônimos que não aparecem na descrição depende do modelo para fazer a ponte, e a ordenação lexical pode não colocar essa organização na frente.
- A recomendação é tão atual quanto o CSV. Se a página fonte mudou e o scraper não rodou de novo, o agente decide com dado velho.
- ODS e pilar ESG são inferência do modelo sobre o texto, não um campo auditado pela organização.
- A chave `GROQ_API_KEY` fica no `.env` da raiz, fora do Git. Sem ela, a rota do agente responde 503. Cota esgotada responde 502. Coleta, listagem e sentimento local não usam essa chave.

## 8. Fechamento do ciclo

| Etapa | Estado nesta entrega |
|-------|----------------------|
| Obtenção | Feita. Duas coletas web gravam o mesmo CSV. |
| Descrição e qualidade | Feita. Colunas, falhas e o sentido real de `Atuação` estão acima. |
| Preparação para uso | Feita na leitura do agente (teste, nome vazio, sufixo `Voltar`, corte de descrição). O arquivo fonte não é sobrescrito por essa preparação. |
| Análise exploratória | Feita no dashboard, com tabela e dois gráficos. |
| Modelo local | Feito no TP4, sob demanda, sem nova coluna. |
| Decisão | Feita. O CSV é o contexto do agente ESG e a resposta volta amarrada às linhas reais. |
| Apresentação | Feita no dashboard final, ao lado dos dados que a sustentam. |

O dado coletado no início do bloco é o mesmo dado que, na última etapa, entra no prompt. Não houve uma base paralela criada só para a demonstração do modelo.

---

*Artefato final do TDSP (Data Ingestion & Understanding), entrega TP5. Metodologias de referência: CRISP-DM e TDSP.*
