from __future__ import annotations

import logging

from langchain_community.llms import FakeListLLM

logger = logging.getLogger(__name__)

# Respostas fixas: adequado para demonstração acadêmica sem custo de API.
_FAKE_RESPONSES: list[str] = [
    "Olá! Sou um assistente simulado (FakeListLLM). Sua mensagem foi recebida.",
    "Este chatbot usa o LangChain FakeListLLM — útil para testes de integração.",
    "Resposta simulada: em produção, aqui entraria um LLM real (OpenAI, local, etc.).",
    "Entendi. Posso ajudar com exemplos conceituais sobre NLP e APIs REST.",
]

_llm: FakeListLLM | None = None


def _get_llm() -> FakeListLLM:
    global _llm
    if _llm is None:
        _llm = FakeListLLM(responses=_FAKE_RESPONSES)
        logger.info("FakeListLLM inicializado com %d respostas.", len(_FAKE_RESPONSES))
    return _llm


def chat(mensagem: str) -> str:
    """
    Invoca o FakeListLLM com a mensagem do usuário.

    O FakeListLLM consome respostas da lista em sequência (comportamento LangChain).
    """
    llm = _get_llm()
    # Concatena contexto mínimo para simular um turno de conversa.
    prompt = f"User: {mensagem}\nAssistant:"
    resposta = llm.invoke(prompt)
    return str(resposta).strip()
