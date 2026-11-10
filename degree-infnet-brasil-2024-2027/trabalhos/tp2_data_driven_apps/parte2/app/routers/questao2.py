import logging

from fastapi import APIRouter, HTTPException, status

from app.schemas import TranslationRequest, TranslationResponse
from app.services import openai_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/questao2", tags=["Questão 2 — OpenAI EN→FR"])


@router.post(
    "/traduzir",
    response_model=TranslationResponse,
    summary="Tradução inglês → francês (LangChain + ChatOpenAI)",
)
def traduzir_openai(payload: TranslationRequest) -> TranslationResponse:
    try:
        traducao = openai_service.translate_en_to_fr(payload.texto_ingles)
    except openai_service.OpenAIConfigurationError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("Erro inesperado na tradução OpenAI")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno na tradução via OpenAI.",
        ) from exc

    return TranslationResponse(
        texto_ingles=payload.texto_ingles,
        texto_traduzido=traducao,
        idioma_destino="fr",
        provedor=f"ChatOpenAI ({openai_service.DEFAULT_OPENAI_MODEL})",
    )
