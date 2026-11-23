# Project Charter — ConectaFood

| Campo | Valor |
|-------|--------|
| **Projeto** | ConectaFood — Plataforma inteligente de conexão com organizações sociais |
| **Fase TDSP** | 01 — Business Understanding |
| **Versão** | **Final — TP5** |
| **Data da revisão** | **23 de novembro de 2026** |
| **Líder** | Bruno Nunes Reis |
| **Início** | Agosto de 2026 |
| **Curso** | Projeto de Bloco — Inteligência Artificial Aplicada, Instituto Infnet |

Este documento substitui o charter do TP4. O PDF anterior registra a versão intermediária (API, coleta e sentimento local). A versão final descreve como o agente de linguagem fecha o ciclo: do dado coletado à decisão de conexão alinhada a ESG e aos ODS.

## 1. Informações gerais

| Campo | Valor |
|-------|--------|
| **Nome** | ConectaFood |
| **Problema** | Quem quer apoiar uma causa (investir, voluntariar, doar alimento ou cumprir uma agenda ESG) não consegue, a partir de uma lista bruta de organizações, decidir com quem se conectar nem explicar o impacto dessa escolha. |
| **Usuários da decisão** | Investidor social, voluntário, doador de alimentos, empresa com agenda ESG e gestor público |
| **ODS de origem** | ODS 2 (Fome Zero e Agricultura Sustentável) e ODS 12 (Consumo e Produção Responsáveis) |
| **ODS cobertos pelo catálogo** | Também 1, 3, 4, 5, 10, 13, 15 e 16, conforme a causa de cada organização |

O nome do projeto nasce da redistribuição de alimentos. A base coletada no Observatório do 3º Setor é mais ampla: infância, educação, mulheres, situação de rua, povos indígenas, saúde, refúgio, pessoas idosas, proteção animal e meio ambiente. A solução final respeita essa base real em vez de fingir que toda organização é um banco de alimentos.

## 2. Resumo executivo

Há alimento que se perde e gente que passa fome, e ao mesmo tempo há dezenas de organizações já em atividade cuja descrição está espalhada em páginas web. Listar essas organizações não resolve a decisão. Um investidor que escreve “quero apoiar educação de crianças” ainda precisa ler descrição por descrição, comparar causas e traduzir o resultado para a linguagem de ODS que um relatório ESG exige.

O ConectaFood trata esse percurso como um ciclo de ciência de dados:

1. **Coleta.** BeautifulSoup e Selenium extraem organizações do Observatório do 3º Setor para `projetos_sociais.csv`.
2. **Entendimento.** O Data Summary Report descreve colunas, falhas de qualidade e o que cada campo sustenta.
3. **Modelagem local (TP4).** Um modelo Hugging Face classifica o tom da descrição em 1 a 5 estrelas, sob demanda, sem gravar o resultado no CSV.
4. **Decisão (TP5).** Um agente da API Groq recebe o interesse de quem decide e o catálogo inteiro como contexto. Ele escolhe poucas organizações que existem no arquivo e justifica a parceria em ODS e em pilar ESG (ambiental, social ou governança).
5. **Apresentação.** O dashboard Streamlit mostra a tabela, dois gráficos exploratórios e a resposta do agente.

O modelo local continua útil para triar o tom de um texto. Ele não escolhe parceiros nem argumenta impacto. Essa decisão pede instrução explícita, comparação entre várias organizações e texto justificável — por isso a chamada vai para a API da Groq, no modelo `openai/gpt-oss-120b`, só quando alguém pede uma recomendação. Se esse identificador deixar de existir (HTTP 404), o serviço consulta `models.list()` e repete a chamada com o primeiro modelo de texto ativo da conta. Nesta entrega, o outro modelo de texto confirmado na conta é `qwen/qwen3.8-27b`.

## 3. Como o agente resolve o problema de negócio

O custo da decisão hoje é de leitura. O usuário não precisa de mais uma tabela; precisa de uma resposta do tipo: estas organizações atendem o que você descreveu, por estes motivos, e a conexão fortalece estes ODS.

O serviço `04_Deployment/services/agent_service.py` faz o seguinte:

- Lê `projetos_sociais.csv` em memória e descarta registro de teste e linha sem nome.
- Transforma cada organização em um bloco de texto (nome, cobertura, site, descrição). A ordenação lexical coloca primeiro os registros cujas palavras mais se aproximam do interesse. Enquanto o catálogo couber no limite de contexto, todos os registros válidos seguem no prompt. Isso é um RAG simples: recuperação do arquivo que o projeto já tem, sem base vetorial.
- Envia esse contexto, o perfil (investidor, voluntário, empresa, doador ou gestor) e o interesse para a API da Groq.
- O prompt de sistema fixa o papel de especialista ESG, proíbe inventar organizações e exige justificativa de ODS e pilar ESG.
- O serviço só devolve nomes que existem no CSV e preenche site e cobertura a partir da linha original. Recomendação que o modelo inventar é descartada.

Quem usa o dashboard descreve o objetivo em uma frase — por exemplo, “Quero investir em projetos de educação para crianças” — e recebe poucas opções acionáveis, com link, pilar ESG e próximos passos. A mesma rota `POST /agente_recomendacao` pode ser chamada fora do Streamlit, em `/docs`.

Isso conecta os dois lados do problema original. O doador ou investidor deixa de varrer o CSV. A organização deixa de depender de ser encontrada por acaso. A justificativa de ODS dá à empresa um texto utilizável em prestação de contas da agenda ESG, sempre amarrado a uma organização que está no arquivo.

## 4. Alinhamento com ESG e com os ODS

ESG aqui não é um rótulo genérico. O agente é instruído a nomear o pilar que a parceria de fato movimenta:

| Pilar | Quando a recomendação deve usá-lo | Exemplos no catálogo |
|-------|------------------------------------|----------------------|
| **Ambiental** | Clima, conservação, agroecologia, desperdício de recursos | WWF Brasil, Conservação Internacional, Instituto Socioambiental |
| **Social** | Cuidado, educação, inclusão, alimentação, equidade | Amigos do Bem, Ação da Cidadania, organizações de mulheres e de infância |
| **Governança** | Incidência em política pública, transparência, defesa de direitos | Fundação Abrinq, organizações de garantia de direitos |

Os ODS 2 e 12 continuam sendo a origem do ConectaFood: há organizações de refeição, arrecadação de alimentos e combate à pobreza, e o desperdício aparece como ponte entre fome e consumo responsável. O catálogo também sustenta outros objetivos da Agenda 2030, e o agente deve citar o número e o nome do ODS em cada recomendação, em vez de afirmar um alinhamento vazio.

A governança da própria solução acompanha o discurso ESG do produto: a chave da Groq fica no `.env` e fora do Git; o modelo não pode citar uma organização que não esteja no contexto; o dashboard separa o que é contagem exploratória (gráficos por palavras-chave) do que é decisão do agente.

## 5. Objetivos

**Principal (versão final).** Permitir que uma pessoa ou empresa descreva um interesse e receba, a partir dos dados coletados, uma recomendação curta de organizações reais, com justificativa de impacto em ESG e ODS.

**Alcançados nas etapas anteriores.**

- MVP de exploração do catálogo (tabela, filtro e visualização).
- Coleta estática e dinâmica para o mesmo CSV consumido pela API e pelo dashboard.
- Análise de sentimento local, em português, na escala de 1 a 5 estrelas, exposta em `POST /processar_texto`.

**Critério de pronto do TP5.**

- `POST /agente_recomendacao` operacional, com contratos Pydantic.
- Dashboard com a base visível, dois gráficos e a consulta ao agente.
- Project Charter e Data Summary Report descrevendo o ciclo inteiro, da coleta à decisão.

## 6. Escopo

**Dentro do escopo**

- Catálogo em CSV, API FastAPI e dashboard Streamlit.
- Coleta com BeautifulSoup e Selenium já integrada ao CSV.
- Sentimento local com Hugging Face.
- Agente de recomendação via API Groq (`openai/gpt-oss-120b`), com prompt de sistema ESG e contexto vindo do CSV. Se a Groq responder 404, a chamada é refeita com o primeiro modelo de texto ativo da conta (`qwen/qwen3.8-27b` já respondeu nesse papel).
- Documentação TDSP desta versão final.

**Fora do escopo**

- Mapa e geolocalização (previsto em versões anteriores, não entregue).
- Cadastro de usuários, pagamentos, autenticação e trilha de doação.
- Base vetorial, retreino de modelo e gravação do sentimento no CSV.
- Memória de conversa entre uma pergunta e outra. Cada consulta do agente é uma decisão nova.

## 7. Stakeholders

| Stakeholder | Interesse |
|-------------|-----------|
| **Professor avaliador** | Ver o ciclo de ciência de dados, o uso do dado real e a justificativa de negócio. |
| **Autor do projeto** | Entregar uma aplicação explicável, com chave de API fora do código. |
| **Investidor, empresa e gestor** | Escolher poucas organizações e levar a justificativa de ODS para uma decisão ou relatório. |
| **Voluntário e doador** | Encontrar uma organização coerente com o tempo ou o recurso que podem oferecer. |
| **Organizações do catálogo** | Serem encontradas a partir da própria descrição, sem cadastro manual nesta versão. |

## 8. Riscos e mitigação

| Risco | Mitigação nesta versão |
|-------|------------------------|
| O site fonte muda o HTML e a coleta quebra | Exceções no scraper e cópia local do CSV, que a API e o agente continuam lendo. |
| O modelo inventa uma organização ou um número | Prompt restringe a resposta ao catálogo; o serviço descarta nomes que não estão no CSV e reescreve site e cobertura a partir da linha original. |
| Cota ou modelo descontinuado na Groq | A chamada só ocorre quando alguém pede recomendação. O modelo padrão é `openai/gpt-oss-120b`. Um HTTP 404 dispara `models.list()` e a troca automática para outro modelo de texto ativo, como `qwen/qwen3.8-27b`. Sem chave, a rota responde 503. Se a cota acabar, a rota responde 502 e o restante da API segue no ar. O sentimento local não depende dessa chave. |
| A coluna `Atuação` ser lida como “causa” | No dado real ela é cobertura geográfica. O gráfico temático é separado e documentado como regra de palavras, não como rótulo da fonte. |
| Descrição desatualizada ou com lixo de scraping (`Voltar`, linha de teste) | Limpeza leve antes do prompt e exclusão da linha de teste. O relatório de dados registra o que não foi corrigido na origem. |

## 9. Engenharia de prompt e ciclo até a decisão

O prompt de sistema não pede um texto livre. Ele exige um JSON com resumo, lista de organizações, ODS, pilar ESG, impacto na Agenda 2030 e próximos passos. O perfil e o interesse vão na mensagem do usuário, separados do catálogo, para o modelo não confundir a pergunta com mais uma descrição de ONG.

O fluxo que o dashboard demonstra é o ciclo completo:

```text
Observatório do 3º Setor
        │  BeautifulSoup / Selenium
        ▼
projetos_sociais.csv
        │
        ├──► Dashboard: tabela e gráficos exploratórios
        │
        └──► POST /agente_recomendacao
                 │  contexto + perfil + interesse
                 ▼
             API Groq (gpt-oss-120b, com fallback)
                 │
                 ▼
             Recomendação reconciliada com o CSV
                 │
                 ▼
             Dashboard: decisão, ODS e próximos passos
```

A análise de sentimento permanece em paralelo, em `POST /processar_texto`, para quem quiser ler o tom de uma descrição. Ela não alimenta o agente. As duas inteligências têm papéis diferentes e as duas estão na aplicação.

## 10. Fontes e uso de IA

- Observatório do 3º Setor — origem das organizações em `projetos_sociais.csv`.
- Hugging Face, modelo `nlptown/bert-base-multilingual-uncased-sentiment` — sentimento local (TP4). Justificativa em `03_Modeling/Justificativa_Modelo_TP5.md`.
- Groq, API de inferência. Modelo padrão `openai/gpt-oss-120b` (variável opcional `GROQ_MODEL`). Reserva observada na conta: `qwen/qwen3.8-27b`, escolhida pelo fallback que lê `models.list()` quando o modelo principal responde 404. A chave fica em `GROQ_API_KEY`.
- Objetivos de Desenvolvimento Sustentável e a Agenda 2030, Organização das Nações Unidas — vocabulário de impacto exigido no prompt.
- Gemini Hydrogen 4, Composer 2.5

---

