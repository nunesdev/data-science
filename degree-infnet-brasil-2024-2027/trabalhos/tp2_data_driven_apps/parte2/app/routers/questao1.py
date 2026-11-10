import logging

from fastapi import APIRouter, HTTPException, status

from app.schemas import ChatRequest, ChatResponse
from app.services import fake_llm_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/questao1", tags=["Questão 1 — Chatbot Fake LLM"])


@router.post("/chat", response_model=ChatResponse, summary="Chat com FakeListLLM")
def chatbot(payload: ChatRequest) -> ChatResponse:
    try:
        resposta = fake_llm_service.chat(payload.mensagem)
    except Exception as exc:
        logger.exception("Erro no FakeListLLM")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao processar mensagem no chatbot simulado.",
        ) from exc

    return ChatResponse(mensagem=payload.mensagem, resposta=resposta)
