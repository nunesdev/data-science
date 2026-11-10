import logging

from fastapi import APIRouter, HTTPException, status

from app.schemas import TranslationRequest, TranslationResponse
from app.services import huggingface_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/questao3", tags=["Questão 3 — HF EN→DE"])


@router.post(
    "/traduzir",
    response_model=TranslationResponse,
    summary="Tradução inglês → alemão (LangChain HuggingFacePipeline)",
)
def traduzir_hf(payload: TranslationRequest) -> TranslationResponse:
    if not huggingface_service.is_translator_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo Helsinki-NLP/opus-mt-en-de ainda não foi carregado.",
        )

    try:
        traducao = huggingface_service.translate_en_to_de(payload.texto_ingles)
    except huggingface_service.ModelNotLoadedError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("Erro inesperado na tradução HF")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno na tradução via Hugging Face.",
        ) from exc

    return TranslationResponse(
        texto_ingles=payload.texto_ingles,
        texto_traduzido=traducao,
        idioma_destino="de",
        provedor="HuggingFacePipeline (Helsinki-NLP/opus-mt-en-de)",
    )
