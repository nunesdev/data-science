from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Any, Optional, Tuple

import torch
from transformers import pipeline

logger = logging.getLogger(__name__)

MODEL_ID = "nlptown/bert-base-multilingual-uncased-sentiment"
MAX_CHARS = 512

LABEL_PT = {
    1: "1 estrela (muito negativo)",
    2: "2 estrelas (negativo)",
    3: "3 estrelas (neutro)",
    4: "4 estrelas (positivo)",
    5: "5 estrelas (muito positivo)",
}


@dataclass
class NLPRuntime:
    classifier: Any = None
    model_id: str = MODEL_ID
    ready: bool = False
    error: Optional[str] = None


runtime = NLPRuntime()


def _extrair_estrelas(label: str) -> int:
    match = re.search(r"(\d)", label)
    if match:
        stars = int(match.group(1))
        return max(1, min(5, stars))
    raise ValueError(f"Rótulo de sentimento não reconhecido: {label}")


def carregar_modelos() -> None:
    global runtime
    try:
        device = 0 if torch.cuda.is_available() else -1
        runtime.classifier = pipeline(
            "sentiment-analysis",
            model=MODEL_ID,
            device=device,
        )
        runtime.ready = True
        runtime.error = None
        logger.info("Modelo %s carregado.", MODEL_ID)
    except Exception as exc:
        runtime.ready = False
        runtime.error = str(exc)
        runtime.classifier = None
        logger.exception("Falha ao carregar modelo: %s", exc)


def analisar_sentimento(texto: str) -> Tuple[str, int, float]:
    if runtime.classifier is None:
        raise RuntimeError("Pipeline de sentimento não inicializada.")

    texto_truncado = texto.strip()[:MAX_CHARS]
    saida = runtime.classifier(texto_truncado)
    melhor = saida[0] if isinstance(saida, list) and saida else saida

    label = str(melhor.get("label", ""))
    score = float(melhor.get("score", 0.0))
    estrelas = _extrair_estrelas(label)
    resultado = LABEL_PT.get(estrelas, label)

    return resultado, estrelas, score