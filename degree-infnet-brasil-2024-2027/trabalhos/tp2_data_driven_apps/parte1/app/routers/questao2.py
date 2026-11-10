import logging

from fastapi import APIRouter, HTTPException, status

from app.config import settings
from app.schemas import TranslationRequest, TranslationResponse
from app.services import translation_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/questao2", tags=["Questão 2 — Tradução EN→FR"])


@router.post(
    "/traduzir",
    response_model=TranslationResponse,
    summary="Traduz inglês para francês (Helsinki-NLP/opus-mt-en-fr)",
)
def traduzir_en_fr(payload: TranslationRequest) -> TranslationResponse:
    """
    Recebe texto em inglês via JSON e retorna tradução em francês.
    """
    if not translation_service.is_translator_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo de tradução ainda não foi carregado.",
        )

    try:
        traducao = translation_service.translate_en_to_fr(payload.texto)
    except translation_service.ModelNotLoadedError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("Falha na tradução EN→FR")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao traduzir o texto.",
        ) from exc

    return TranslationResponse(
        texto_original=payload.texto,
        texto_traduzido=traducao,
        modelo=settings.EN_FR_MODEL_ID,
    )
