import logging

from fastapi import APIRouter, HTTPException, status

from app.config import settings
from app.schemas import TextContinuationRequest, TextContinuationResponse
from app.services import gpt2_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/questao1", tags=["Questão 1 — GPT-2"])


@router.post(
    "/continuar",
    response_model=TextContinuationResponse,
    summary="Continua uma frase usando GPT-2 (Hugging Face)",
)
def continuar_frase(payload: TextContinuationRequest) -> TextContinuationResponse:
    """
    Recebe JSON com `frase`, executa geração com GPT-2 e devolve JSON estruturado.
    """
    if not gpt2_service.is_gpt2_loaded():
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Modelo GPT-2 ainda não foi carregado. Aguarde a inicialização.",
        )

    try:
        continuacao, texto_completo = gpt2_service.generate_continuation(
            payload.frase,
            payload.max_new_tokens,
        )
    except gpt2_service.ModelNotLoadedError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("Falha na geração GPT-2")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao gerar continuação do texto.",
        ) from exc

    return TextContinuationResponse(
        frase_original=payload.frase,
        continuacao=continuacao,
        texto_completo=texto_completo,
        modelo=settings.GPT2_MODEL_ID,
    )
