from contextlib import asynccontextmanager
from pathlib import Path
import threading

from fastapi import FastAPI, HTTPException
import pandas as pd

from api import nlp
from api.schemas import ONG, ProcessarTextoRequest, ProcessarTextoResponse, TipoAnalise

ROOT = Path(__file__).resolve().parents[1]
DATA_CSV = ROOT / "data" / "projetos_sociais.csv"
_csv_lock = threading.Lock()


@asynccontextmanager
async def lifespan(app: FastAPI):
    nlp.carregar_modelos()
    yield


app = FastAPI(
    title="API ConectaFood",
    description=(
        "API para integração e gestão de dados de ONGs e Projetos Sociais, "
        "com análise de sentimento local via Hugging Face transformers."
    ),
    version="2.1",
    lifespan=lifespan,
)


def _ler_ongs_df() -> pd.DataFrame:
    if not DATA_CSV.exists():
        raise FileNotFoundError(str(DATA_CSV))
    df = pd.read_csv(DATA_CSV)
    return df.fillna("")


@app.get("/")
def home():
    return {
        "mensagem": "Bem-vindo à API do ConectaFood! Acesse /docs para ver a documentação.",
        "nlp_disponivel": nlp.runtime.ready,
    }


@app.get("/ongs")
def listar_ongs():
    """Rota GET para listar todas as ONGs coletadas."""
    try:
        with _csv_lock:
            df = _ler_ongs_df()
        return df.to_dict(orient="records")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo de dados não encontrado.")


@app.post("/ongs")
def adicionar_ong(ong: ONG):
    """Rota POST para adicionar uma nova ONG ao CSV."""
    with _csv_lock:
        DATA_CSV.parent.mkdir(parents=True, exist_ok=True)
        if DATA_CSV.exists():
            df = pd.read_csv(DATA_CSV)
        else:
            df = pd.DataFrame(columns=["Nome", "Atuação", "Site", "Descrição"])

        novo_dado = pd.DataFrame([ong.model_dump()])
        df = pd.concat([df, novo_dado], ignore_index=True)
        df.to_csv(DATA_CSV, index=False)

    return {"mensagem": "ONG adicionada com sucesso!", "dados": ong}


@app.post(
    "/processar_texto",
    response_model=ProcessarTextoResponse,
    summary="Análise de sentimento (1–5 estrelas) em texto em português",
)
def processar_texto(payload: ProcessarTextoRequest):
    if not nlp.runtime.ready:
        raise HTTPException(
            status_code=503,
            detail={
                "mensagem": "Modelo de linguagem indisponível no momento.",
                "erro": nlp.runtime.error,
            },
        )

    if payload.tipo_analise != TipoAnalise.sentimento:
        raise HTTPException(
            status_code=400,
            detail="Apenas análise de sentimento está habilitada nesta versão da API.",
        )

    texto_original = payload.texto.strip()

    try:
        resultado, estrelas, confianca, truncado = nlp.analisar_sentimento(payload.texto)
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
        texto_original=texto_original,
        tipo_analise=payload.tipo_analise,
        resultado=resultado,
        estrelas=estrelas,
        confianca=confianca,
        modelo=nlp.runtime.model_id,
        truncado=truncado,
    )