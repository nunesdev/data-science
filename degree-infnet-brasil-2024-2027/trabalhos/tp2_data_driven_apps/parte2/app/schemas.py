from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    mensagem: str = Field(
        ...,
        min_length=1,
        max_length=2048,
        description="Mensagem enviada ao chatbot.",
        examples=["What is LangChain?"],
    )


class ChatResponse(BaseModel):
    mensagem: str
    resposta: str
    provedor: str = "FakeListLLM (LangChain)"


class TranslationRequest(BaseModel):
    texto_ingles: str = Field(
        ...,
        min_length=1,
        max_length=4096,
        description="Texto em inglês a ser traduzido.",
        examples=["Good morning, team!"],
    )


class TranslationResponse(BaseModel):
    texto_ingles: str
    texto_traduzido: str
    idioma_destino: str
    provedor: str
