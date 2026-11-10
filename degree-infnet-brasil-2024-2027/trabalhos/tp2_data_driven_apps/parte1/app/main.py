"""
Ponto de entrada FastAPI — Parte 1 (sem LangChain).

Arquitetura: camada HTTP (routers) → serviços de inferência → Transformers.
Modelos são carregados no lifespan para amortizar latência nas requisições.
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from app.routers import questao1, questao2
from app.services import gpt2_service, translation_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Carrega pesos dos modelos uma vez ao subir o servidor."""
    try:
        gpt2_service.load_gpt2()
    except Exception:
        logger.exception("Não foi possível carregar o GPT-2 na inicialização.")

    try:
        translation_service.load_en_fr_translator()
    except Exception:
        logger.exception("Não foi possível carregar o modelo de tradução na inicialização.")

    yield
    logger.info("Encerrando aplicação Parte 1.")


app = FastAPI(
    title="TP2 — Parte 1 (FastAPI + Hugging Face)",
    description=(
        "APIs RESTful para continuação de texto (GPT-2) e tradução EN→FR "
        "(Helsinki-NLP), implementadas com FastAPI puro."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(questao1.router)
app.include_router(questao2.router)


@app.get("/health", tags=["Sistema"])
def health() -> dict[str, bool | str]:
    return {
        "status": "ok",
        "gpt2_carregado": gpt2_service.is_gpt2_loaded(),
        "tradutor_en_fr_carregado": translation_service.is_translator_loaded(),
    }
