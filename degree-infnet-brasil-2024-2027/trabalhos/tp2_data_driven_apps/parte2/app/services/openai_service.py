from __future__ import annotations

import logging
import os
from functools import lru_cache

from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

logger = logging.getLogger(__name__)


OPENAI_API_KEY_ENV = ""
DEFAULT_OPENAI_MODEL = "gpt-4o-mini" 


class OpenAIConfigurationError(RuntimeError):
    """API key ausente ou configuração inválida."""


def _require_api_key() -> str:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key or not api_key.strip():
        raise OpenAIConfigurationError(
            f"Variável {OPENAI_API_KEY_ENV} não definida. "
            "Defina: export OPENAI_API_KEY='SUA_CHAVE_AQUI'"
        )
    return api_key.strip()


@lru_cache(maxsize=1)
def _translation_prompt() -> PromptTemplate:
    return PromptTemplate(
        input_variables=["texto"],
        template=(
            "Traduza o texto abaixo do inglês para o francês.\n"
            "Retorne apenas a tradução, sem explicações.\n\n"
            "Inglês: {texto}\n"
            "Francês:"
        ),
    )


@lru_cache(maxsize=1)
def _get_chat_model() -> ChatOpenAI:
    return ChatOpenAI(
        model=DEFAULT_OPENAI_MODEL,
        temperature=0,
        api_key=_require_api_key(),
        max_retries=2,
        timeout=30,
    )


def translate_en_to_fr(texto_ingles: str) -> str:
    """Traduz inglês → francês via PromptTemplate + ChatOpenAI (LangChain)."""
    prompt = _translation_prompt()
    llm = _get_chat_model()
    chain = prompt | llm
    try:
        result = chain.invoke({"texto": texto_ingles})
    except OpenAIConfigurationError:
        raise
    except Exception as exc:
        logger.exception("Falha na chamada OpenAI via LangChain")
        raise RuntimeError("Erro ao traduzir com a API OpenAI.") from exc

    content = result.content if hasattr(result, "content") else str(result)
    return content.strip()
