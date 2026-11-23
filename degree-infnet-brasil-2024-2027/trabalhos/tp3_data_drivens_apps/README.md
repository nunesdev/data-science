# Monitor Climático e Alerta Integrado (Sul do Brasil)

Trabalho Prático 3 (TP3) — **Data-Driven Apps**  
Agente conversacional **ReAct** (LangChain + Groq) com interface **Streamlit**, voltado à análise integrada de **clima** e **alertas/notícias** para apoio a decisões em regiões do Sul do Brasil impactadas por eventos extremos e pelo contexto do **El Niño**.

---

## Descrição do problema e da solução

### Problema

O Sul do Brasil tem enfrentado ciclos de **chuvas extremas**, **enchentes**, **alagamentos urbanos** e **deslizamentos**, frequentemente agravados por fenômenos como o **El Niño**. Cidadãos, gestores e viajantes precisam decidir rapidamente se é seguro **deslocar-se**, **trabalhar em campo** ou **manter roteiros de viagem** — mas a informação está **fragmentada**: previsão meteorológica em um portal, alertas da Defesa Civil em outro, e notícias locais em veículos distintos. Cruzar manualmente essas fontes é lento, sujeito a viés e não escala em perguntas conversacionais (“e se eu for na sexta?”).

### Solução proposta

O sistema implementa um **agente ReAct** que:

1. **Raciocina** em passos explícitos (Thought → Action → Observation).
2. Invoca **`buscar_clima`**: geocodificação + previsão atual via **Open-Meteo** (temperatura e precipitação).
3. Invoca **`buscar_alertas_noticias`**: busca web via **DuckDuckGo** (LangChain Community) focada em defesa civil, enchentes e cobertura jornalística.
4. **Consolida** uma **Final Answer** em português, com nível de risco e recomendações práticas.

A interface Streamlit oferece chat com histórico na sessão e memória conversacional no agente, permitindo perguntas de acompanhamento.

### Arquitetura (visão geral)

```
Usuário (Streamlit)
       │
       ▼
 AgentExecutor (ReAct + memória)
       │
       ├──► buscar_clima ──► Open-Meteo (HTTP)
       └──► buscar_alertas_noticias ──► DuckDuckGo (LangChain)
       │
       ▼
 ChatGroq (openai/gpt-oss-120b)
```

---

## Estrutura do projeto

| Arquivo | Função |
|---------|--------|
| `requirements.txt` | Dependências Python |
| `.env` | Variável `GROQ_API_KEY` |
| `tools.py` | Ferramentas LangChain (`@tool`) |
| `agent.py` | LLM Groq (`openai/gpt-oss-120b`), prompt ReAct, memória, `AgentExecutor` |
| `app.py` | Interface Streamlit |
| `README.md` | Documentação acadêmica |

---

## Casos de uso testados e resultados observados

> **Nota:** Execute localmente com `GROQ_API_KEY` válida e internet estável. Os fluxos abaixo descrevem o comportamento esperado observado em testes de integração das ferramentas e do agente.

### Caso 1 — Previsão de chuva e decisão de viagem (Porto Alegre)

**Pergunta no chat:**  
*“Está chovendo agora em Porto Alegre? Vale a pena viajar amanhã?”*

**Fluxo do agente:**

1. **Thought:** necessidade de dados meteorológicos atuais.  
2. **Action:** `buscar_clima` · **Action Input:** `Porto Alegre, RS, Brasil`  
3. **Observation:** retorno com localização, temperatura e precipitação (mm) no fuso `America/Sao_Paulo`.  
4. **Thought:** complementar com alertas oficiais e notícias.  
5. **Action:** `buscar_alertas_noticias` · **Action Input:** `Porto Alegre defesa civil alerta enchente`  
6. **Observation:** snippets de busca com menções a alertas, níveis de rio ou ocorrências recentes (variável conforme a web).  
7. **Final Answer:** síntese em português — se há chuva ativa, tendência de risco e recomendação cautelosa (adiar deslocamento ou monitorar Defesa Civil).

**Resultado observado:** o agente **não se limita à temperatura**; cruza precipitação > 0 mm com contexto de notícias, explicitando incerteza quando a busca retorna pouco conteúdo.

### Caso 2 — Enchentes e segurança em cidade do Vale do Taquari (Lajeado)

**Pergunta no chat:**  
*“Há notícias de alagamento em Lajeado e o clima está estável hoje?”*

**Fluxo do agente:**

1. **Action:** `buscar_clima` → `Lajeado, RS`  
2. **Observation:** condições atuais (sem precipitação ou com chuva leve, conforme API).  
3. **Action:** `buscar_alertas_noticias` → `Lajeado RS enchente defesa civil alerta`  
4. **Observation:** resultados agregados sobre enchentes históricas ou alertas recentes.  
5. **Final Answer:** distinção entre **“tempo calmo no instante”** versus **risco hidrológico persistente** (solo encharcado, rios em cota), orientando evitar áreas de planície e confirmar rotas.

**Resultado observado:** respostas **acionáveis** (evitar deslocamento, checar rodovias, priorizar fontes oficiais), adequadas ao objetivo acadêmico de **data-driven decision support**.

---

## Instruções de execução

### Pré-requisitos

- Python 3.10+ (recomendado 3.11)
- Conta e chave de API no [Groq](https://console.groq.com/)

### Passo a passo

1. **Clone ou acesse** a pasta do projeto:

   ```bash
   cd tp3_data_drivens_apps
   ```

2. **Crie e ative** um ambiente virtual:

   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Linux/macOS
   # venv\Scripts\activate    # Windows
   ```

3. **Instale** as dependências:

   ```bash
   pip install -r requirements.txt
   ```

   > **DuckDuckGo:** versões recentes do `langchain-community` exigem o pacote `ddgs`
   > (incluído em `requirements.txt`). Se aparecer `ImportError: ddgs`, execute:
   > `pip install -U ddgs`.

4. **Configure** o arquivo `.env`:

   ```env
   GROQ_API_KEY=sua_chave_aqui
   ```

5. **Inicie** a aplicação Streamlit:

   ```bash
   streamlit run app.py
   ```

6. Abra o endereço exibido no terminal (geralmente `http://localhost:8501`) e converse com o agente.

### Teste rápido das ferramentas (opcional)

No Python interativo, com venv ativo:

```python
from tools import buscar_clima, buscar_alertas_noticias
print(buscar_clima.invoke("Curitiba, PR"))
print(buscar_alertas_noticias.invoke("Curitiba defesa civil alerta chuva"))
```

---

## Justificativa de valor

Pesquisar manualmente a segurança de uma viagem no Sul em cenário de El Niño costuma exigir **três ou mais contextos**: abrir um site de meteorologia, buscar no Google notícias de enchente, procurar perfil da Defesa Civil municipal/estadual e ainda **interpretar** se “sem chuva agora” significa baixo risco — quando o risco hidrológico pode permanecer elevado por dias.

O agente **automatiza o encadeamento cognitivo**:

| Atividade manual | Com o agente |
|------------------|--------------|
| Alternar abas e copiar números | Uma pergunta em linguagem natural |
| Memorizar o que foi dito antes | Memória `chat_history` no ReAct |
| Decidir qual fonte consultar primeiro | Política emergente via Thought/Action |
| Redigir conclusão | Final Answer estruturada em português |

Do ponto de vista de **engenharia de software**, o padrão **ReAct** torna o raciocínio **auditável** (útil em relatório acadêmico e em demos): cada **Observation** amarra a resposta final a dados externos reais (API + busca), reduzindo alucinação pura do LLM. As **docstrings detalhadas** das ferramentas são críticas para modelos open-weight/tool-calling: descrevem *quando* e *como* invocar cada capacidade.

**Limitações transparentes:** a busca DuckDuckGo não substitui boletins oficiais em tempo real; o Open-Meteo reflete modelo numérico, não sensores locais de cheia. O sistema **facilita triagem e conscientização**, não substitui autoridades em emergências.

---

## Autoria e contexto acadêmico

Projeto desenvolvido para entrega **TP3 — Data-Driven Apps**, demonstrando integração de:

- APIs de dados abertos (clima),
- ferramentas de busca,
- orquestração via **LangChain**,
- LLM **Groq** (`openai/gpt-oss-120b`),
- UI **Streamlit** para interação com usuário final.

---

## Licença e uso responsável

Uso educacional. Em situações de risco iminente, contate **Defesa Civil (199)**, **Bombeiros (193)** e fontes governamentais oficiais.