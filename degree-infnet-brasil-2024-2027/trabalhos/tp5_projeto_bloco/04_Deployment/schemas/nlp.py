from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class TipoAnalise(str, Enum):
    sentimento = "sentimento"


class ProcessarTextoRequest(BaseModel):
    texto: str = Field(..., min_length=10, max_length=4000, description="Texto a analisar")
    tipo_analise: TipoAnalise = Field(
        default=TipoAnalise.sentimento,
        description="Tipo de análise NLP (apenas sentimento nesta versão).",
    )

    @field_validator("texto")
    @classmethod
    def texto_nao_vazio(cls, v: str) -> str:
        stripped = v.strip()
        if not stripped:
            raise ValueError("O texto não pode ser apenas espaços em branco.")
        return stripped


class ProcessarTextoResponse(BaseModel):
    texto_original: str
    tipo_analise: TipoAnalise
    resultado: str
    estrelas: int = Field(..., ge=1, le=5, description="Classificação em escala de 1 a 5 estrelas")
    confianca: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Probabilidade da classe prevista"
    )
    modelo: str