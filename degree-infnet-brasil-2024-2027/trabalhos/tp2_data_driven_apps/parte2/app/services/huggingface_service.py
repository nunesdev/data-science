from __future__ import annotations

import logging

from langchain_huggingface import HuggingFacePipeline

logger = logging.getLogger(__name__)

EN_DE_MODEL_ID = "Helsinki-NLP/opus-mt-en-de"

_llm: HuggingFacePipeline | None = None


class ModelNotLoadedError(RuntimeError):
    """Pipeline local ainda não foi inicializado."""


def load_en_de_translator() -> None:
    """Monta pipeline Transformers e encapsula no HuggingFacePipeline (LangChain)."""
    global _llm
    from transformers import pipeline

    logger.info("Carregando %s para HuggingFacePipeline...", EN_DE_MODEL_ID)
    hf_pipe = pipeline(
        task="translation",
        model=EN_DE_MODEL_ID,
        tokenizer=EN_DE_MODEL_ID,
    )
    _llm = HuggingFacePipeline(pipeline=hf_pipe)
    logger.info("HuggingFacePipeline EN→DE pronto.")


def is_translator_loaded() -> bool:
    return _llm is not None


def translate_en_to_de(texto_ingles: str) -> str:
    if _llm is None:
        raise ModelNotLoadedError(
            "Modelo Helsinki-NLP/opus-mt-en-de não carregado. Aguarde o lifespan da API."
        )
    try:
        saida = _llm.invoke(texto_ingles)
    except Exception as exc:
        logger.exception("Falha na tradução EN→DE (HuggingFacePipeline)")
        raise RuntimeError("Erro na inferência local de tradução.") from exc
    return str(saida).strip()
