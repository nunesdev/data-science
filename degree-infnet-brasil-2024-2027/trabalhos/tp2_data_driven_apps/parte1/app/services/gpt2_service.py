from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.config import settings

if TYPE_CHECKING:
    from transformers import GPT2LMHeadModel, PreTrainedTokenizer

logger = logging.getLogger(__name__)

# Instâncias carregadas uma vez no lifespan da aplicação (evita reload por request).
_tokenizer: PreTrainedTokenizer | None = None
_model: GPT2LMHeadModel | None = None


class ModelNotLoadedError(RuntimeError):
    """Modelo ainda não foi carregado ou falhou na inicialização."""


def load_gpt2() -> None:
    """Carrega tokenizer e GPT-2 na memória."""
    global _tokenizer, _model
    # Import tardio: reduz tempo de import do módulo FastAPI.
    from transformers import GPT2LMHeadModel, GPT2Tokenizer

    model_id = settings.GPT2_MODEL_ID
    logger.info("Carregando modelo %s...", model_id)
    _tokenizer = GPT2Tokenizer.from_pretrained(model_id)
    _model = GPT2LMHeadModel.from_pretrained(model_id)
    _model.eval()
    logger.info("Modelo %s carregado.", model_id)


def is_gpt2_loaded() -> bool:
    return _tokenizer is not None and _model is not None


def generate_continuation(frase: str, max_new_tokens: int) -> tuple[str, str]:
    """
    Gera continuação a partir da frase de entrada.

    Returns:
        Tupla (continuacao_apenas_novos_tokens, texto_completo).
    """
    if _tokenizer is None or _model is None:
        raise ModelNotLoadedError("GPT-2 não está disponível.")

    import torch

    inputs = _tokenizer.encode(frase, return_tensors="pt")
    with torch.no_grad():
        output_ids = _model.generate(
            inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            pad_token_id=_tokenizer.eos_token_id,
        )

    texto_completo = _tokenizer.decode(output_ids[0], skip_special_tokens=True)
    # Continuação = sufixo após o prompt original (comparação por texto decodificado).
    continuacao = texto_completo[len(frase) :].strip()
    if not continuacao and len(texto_completo) > len(frase):
        continuacao = texto_completo

    return continuacao, texto_completo
