"""
Interface Streamlit — Monitor Climático e Alerta Integrado (Sul do Brasil).
"""

from __future__ import annotations

import streamlit as st

from agent import build_agent_executor

st.set_page_config(
  page_title="Monitor Climático — Sul do Brasil",
  page_icon="🌧️",
  layout="centered",
)

st.title("Monitor Climático e Alerta Integrado (Sul do Brasil)")
st.markdown(
  """
  Agente **ReAct** que combina **clima em tempo quase real** (Open-Meteo) com **alertas e notícias**
  (busca web) para apoiar decisões de viagem e atividades em regiões sujeitas a eventos extremos
  e ao contexto do **El Niño**.

  **Exemplos:** *“Posso ir para Porto Alegre neste fim de semana?”* ·
  *“Como está o tempo em Florianópolis e há notícias de alagamento?”*
  """
)


def _init_session() -> None:
  if "messages" not in st.session_state:
    st.session_state.messages: list[dict[str, str]] = []
  if "agent_executor" not in st.session_state:
    try:
      st.session_state.agent_executor = build_agent_executor()
    except ValueError as exc:
      st.session_state.agent_executor = None
      st.error(str(exc))


_init_session()

for message in st.session_state.messages:
  with st.chat_message(message["role"]):
    st.markdown(message["content"])

if st.session_state.agent_executor is None:
  st.stop()

if prompt := st.chat_input("Descreva sua dúvida sobre clima, alertas ou viagem no Sul do Brasil..."):
  st.session_state.messages.append({"role": "user", "content": prompt})
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    with st.spinner("Consultando clima e cruzando com alertas/notícias..."):
      try:
        result = st.session_state.agent_executor.invoke({"input": prompt})
        answer = result.get("output", "Não foi possível obter uma resposta do agente.")
      except Exception as exc:  # noqa: BLE001 — exibir erro amigável na UI acadêmica
        answer = (
          f"Ocorreu um erro ao processar sua solicitação: **{exc}**. "
          "Verifique a chave `GROQ_API_KEY` no `.env`, a conexão com a internet "
          "e tente reformular a pergunta."
        )
    st.markdown(answer)

  st.session_state.messages.append({"role": "assistant", "content": answer})