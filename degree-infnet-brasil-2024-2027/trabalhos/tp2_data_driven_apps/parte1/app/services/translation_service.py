from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.config import settings

if TYPE_CHECKING:
    from transformers import MarianMTModel, MarianTokenizer

logger = logging.getLogger(__name__)

_tokenizer: MarianTokenizer | None = None
_model: MarianMTModel | None = None


class ModelNotLoadedError(RuntimeError):
    """Modelo de tradução indisponível."""


def load_en_fr_translator() -> None:
    """Carrega Helsinki-NLP/opus-mt-en-fr."""
    global _tokenizer, _model
    from transformers import MarianMTModel, MarianTokenizer

    model_id = settings.EN_FR_MODEL_ID
    logger.info("Carregando modelo de tradução %s...", model_id)
    _tokenizer = MarianTokenizer.from_pretrained(model_id)
    _model = MarianMTModel.from_pretrained(model_id)
    _model.eval()
    logger.info("Modelo %s carregado.", model_id)


def is_translator_loaded() -> bool:
    return _tokenizer is not None and _model is not None


def translate_en_to_fr(texto: str) -> str:
    if _tokenizer is None or _model is None:
        raise ModelNotLoadedError("Modelo de tradução EN→FR não está disponível.")

    import torch

    batch = _tokenizer([texto], return_tensors="pt", padding=True, truncation=True)
    with torch.no_grad():
        generated = _model.generate(**batch, max_length=512)

    traducao = _tokenizer.decode(generated[0], skip_special_tokens=True)
    return traducao.strip()
