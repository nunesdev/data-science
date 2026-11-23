"""
Configuração do agente ReAct (LangChain + Groq) com memória conversacional.
"""

from __future__ import annotations

import os
from typing import List

from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import BaseMessage
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from tools import get_tools

load_dotenv()

REACT_PROMPT_TEMPLATE = """Você é um analista de risco climático focado no Sul do Brasil (RS, SC, PR),
especialmente em contextos de El Niño, chuvas intensas, enchentes e deslizamentos.

Seu objetivo é cruzar dados meteorológicos em tempo quase real com alertas e notícias,
orientando se é razoavelmente seguro viajar, deslocar-se ou realizar atividades ao ar livre
na região perguntada. Seja cauteloso: em caso de dúvida ou ausência de dados, recomende
confirmar com fontes oficiais (Defesa Civil, INMET).

Ferramentas disponíveis:

{tools}

Nomes das ferramentas: [{tool_names}]

Use EXATAMENTE o formato ReAct abaixo (Thought, Action, Action Input, Observation até concluir):

Question: a pergunta do usuário
Thought: raciocínio sobre qual ferramenta usar ou se já pode responder
Action: uma de [{tool_names}]
Action Input: entrada JSON ou texto para a ferramenta
Observation: resultado da ferramenta
... (repita Thought/Action/Action Input/Observation quantas vezes necessário)
Thought: consolide clima + notícias/alertas e formule a recomendação
Final Answer: resposta final em português, clara, com nível de risco e recomendações práticas

Histórico da conversa:
{chat_history}

Question: {input}
Thought:{agent_scratchpad}"""


class FormattedConversationBufferMemory(ConversationBufferMemory):
  """
  Memória com return_messages=True formatada como texto para o prompt ReAct.
  Mantém a especificação memory_key='chat_history' e return_messages=True.
  """

  def load_memory_variables(self, inputs: dict) -> dict:
    variables = super().load_memory_variables(inputs)
    raw = variables.get(self.memory_key, [])
    if isinstance(raw, list):
      variables[self.memory_key] = self._messages_to_text(raw)
    elif raw is None:
      variables[self.memory_key] = "Nenhuma interação anterior."
    return variables

  @staticmethod
  def _messages_to_text(messages: List[BaseMessage]) -> str:
    if not messages:
      return "Nenhuma interação anterior."
    parts: List[str] = []
    for msg in messages:
      role = getattr(msg, "type", "message")
      if role == "human":
        label = "Usuário"
      elif role == "ai":
        label = "Assistente"
      else:
        label = role
      parts.append(f"{label}: {msg.content}")
    return "\n".join(parts)


def build_agent_executor() -> AgentExecutor:
  """
  Instancia LLM Groq, memória, prompt ReAct e retorna AgentExecutor pronto para invoke.
  """
  api_key = os.getenv("GROQ_API_KEY")
  if not api_key or not api_key.strip():
    raise ValueError(
      "GROQ_API_KEY não configurada. Preencha o arquivo .env antes de executar o app."
    )

  llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.2,
    groq_api_key=api_key.strip(),
  )

  tools = get_tools()

  prompt = PromptTemplate(
    input_variables=["tools", "tool_names", "chat_history", "input", "agent_scratchpad"],
    template=REACT_PROMPT_TEMPLATE,
  )

  memory = FormattedConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
  )

  agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

  return AgentExecutor(
    agent=agent,
    tools=tools,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
    max_iterations=8,
  )