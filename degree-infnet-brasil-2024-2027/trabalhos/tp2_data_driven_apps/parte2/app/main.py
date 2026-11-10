"""
TP2 Parte 2 — FastAPI + LangChain.

Camadas: routers → services (chains/LLMs) → Fake LLM | OpenAI API | HF local.
Apenas o modelo local EN→DE é pré-carregado no lifespan (custo de memória/tempo).
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.routers import questao1, questao2, questao3
from app.services import huggingface_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    try:
        huggingface_service.load_en_de_translator()
    except Exception:
        logger.exception("Falha ao carregar HuggingFacePipeline EN→DE.")

    yield
    logger.info("Encerrando Parte 2.")


app = FastAPI(
    title="TP2 — Parte 2 (FastAPI + LangChain)",
    description=(
        "Chatbot Fake LLM, tradução EN→FR com OpenAI e EN→DE com "
        "HuggingFacePipeline integrado ao LangChain."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(questao1.router)
app.include_router(questao2.router)
app.include_router(questao3.router)


@app.get("/health", tags=["Sistema"])
def health() -> dict[str, object]:
    import os

    from app.services import openai_service

    return {
        "status": "ok",
        "hf_en_de_carregado": huggingface_service.is_translator_loaded(),
        "openai_api_key_configurada": bool(os.getenv(openai_service.OPENAI_API_KEY_ENV)),
    }
