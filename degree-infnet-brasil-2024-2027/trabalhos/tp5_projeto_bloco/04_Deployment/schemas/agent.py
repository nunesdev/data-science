from pydantic import BaseModel, Field, field_validator


class AgenteRecomendacaoRequest(BaseModel):
    interesse: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Interesse do usuário em linguagem natural.",
        examples=["Quero investir em projetos de educação para crianças"],
    )
    perfil: str = Field(
        default="Investidor social",
        max_length=120,
        description="Quem decide: investidor, voluntário, empresa ou doador.",
    )
    limite: int = Field(
        default=3,
        ge=1,
        le=5,
        description="Quantidade máxima de organizações recomendadas.",
    )

    @field_validator("interesse", "perfil")
    @classmethod
    def texto_util(cls, valor: str) -> str:
        texto = (valor or "").strip()
        if not texto:
            raise ValueError("O texto não pode ser vazio.")
        return texto


class RecomendacaoONG(BaseModel):
    nome: str
    atuacao: str = ""
    site: str = ""
    justificativa: str
    ods: list[str] = Field(default_factory=list)
    pilar_esg: str = ""


class AgenteRecomendacaoResponse(BaseModel):
    interesse: str
    perfil: str
    resumo: str
    recomendacoes: list[RecomendacaoONG]
    impacto_ods: str
    proximos_passos: list[str] = Field(default_factory=list)
    modelo: str
    ongs_no_contexto: int = Field(..., ge=0)
