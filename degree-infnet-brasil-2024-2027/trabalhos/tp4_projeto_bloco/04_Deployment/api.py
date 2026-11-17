from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import os

from schemas.nlp import ProcessarTextoRequest, ProcessarTextoResponse, TipoAnalise
from services import nlp_model

# Caminho do banco de dados em CSV
DATA_PATH = "../02_Data_Ingestion_Understanding/projetos_sociais.csv"


@asynccontextmanager
async def lifespan(app: FastAPI):
    nlp_model.carregar_modelos()
    yield


app = FastAPI(
    title="API ConectaFood",
    description=(
        "API para integração e gestão de dados de ONGs e Projetos Sociais, "
        "com análise de sentimento local via Hugging Face transformers."
    ),
    version="2.0",
    lifespan=lifespan,
)


class ONG(BaseModel):
    Nome: str
    Atuação: str
    Site: str
    Descrição: str


def _resolver_caminho_csv() -> str:
    if os.path.exists(DATA_PATH):
        return DATA_PATH
    alt = "02_Data_Ingestion_Understanding/projetos_sociais.csv"
    if os.path.exists(alt):
        return alt
    return DATA_PATH


@app.get("/")
def home():
    return {
        "mensagem": "Bem-vindo à API do ConectaFood! Acesse /docs para ver a documentação.",
        "nlp_disponivel": nlp_model.runtime.ready,
    }


@app.get("/ongs")
def listar_ongs():
    """Rota GET para listar todas as ONGs coletadas."""
    try:
        caminho = _resolver_caminho_csv()
        df = pd.read_csv(caminho)
        df = df.fillna("")
        return df.to_dict(orient="records")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo de dados não encontrado.")


@app.post("/ongs")
def adicionar_ong(ong: ONG):
    """Rota POST para adicionar uma nova ONG ao CSV."""
    caminho = _resolver_caminho_csv()

    if os.path.exists(caminho):
        df = pd.read_csv(caminho)
    else:
        df = pd.DataFrame(columns=["Nome", "Atuação", "Site", "Descrição"])

    novo_dado = pd.DataFrame([ong.model_dump()])
    df = pd.concat([df, novo_dado], ignore_index=True)
    df.to_csv(caminho, index=False)

    return {"mensagem": "ONG adicionada com sucesso!", "dados": ong}


@app.post(
    "/processar_texto",
    response_model=ProcessarTextoResponse,
    summary="Análise de sentimento (1–5 estrelas) em texto em português",
)
def processar_texto(payload: ProcessarTextoRequest):
    if not nlp_model.runtime.ready:
        raise HTTPException(
            status_code=503,
            detail={
                "mensagem": "Modelo de linguagem indisponível no momento.",
                "erro": nlp_model.runtime.error,
            },
        )

    if payload.tipo_analise != TipoAnalise.sentimento:
        raise HTTPException(
            status_code=400,
            detail="Apenas análise de sentimento está habilitada nesta versão da API.",
        )

    try:
        resultado, estrelas, confianca = nlp_model.analisar_sentimento(payload.texto)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar texto: {exc}",
        )

    return ProcessarTextoResponse(
        texto_original=payload.texto.strip(),
        tipo_analise=payload.tipo_analise,
        resultado=resultado,
        estrelas=estrelas,
        confianca=confianca,
        modelo=nlp_model.runtime.model_id,
    )