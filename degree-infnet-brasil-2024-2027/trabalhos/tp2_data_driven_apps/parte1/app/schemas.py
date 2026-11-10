from pydantic import BaseModel, Field


class TextContinuationRequest(BaseModel):
    """Entrada para continuação de texto com GPT-2."""

    frase: str = Field(
        ...,
        min_length=1,
        max_length=1024,
        description="Frase ou trecho inicial para o modelo completar.",
        examples=["The future of artificial intelligence is"],
    )
    max_new_tokens: int = Field(
        default=50,
        ge=1,
        le=256,
        description="Quantidade máxima de tokens gerados após o prompt.",
    )


class TextContinuationResponse(BaseModel):
    frase_original: str
    continuacao: str
    texto_completo: str
    modelo: str


class TranslationRequest(BaseModel):
    """Entrada para tradução inglês → francês."""

    texto: str = Field(
        ...,
        min_length=1,
        max_length=512,
        description="Texto em inglês a ser traduzido.",
        examples=["Hello, how are you today?"],
    )


class TranslationResponse(BaseModel):
    texto_original: str
    texto_traduzido: str
    idioma_origem: str = "en"
    idioma_destino: str = "fr"
    modelo: str


class ErrorResponse(BaseModel):
    detail: str
    codigo: str | None = None
