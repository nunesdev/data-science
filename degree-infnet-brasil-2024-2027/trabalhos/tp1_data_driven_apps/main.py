from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from routes import InvalidItemIdError, router

DESCRIPTION = (
    "API para o TP1 - Data Driven Apps. "
    "APIs permitem expor modelos, pipelines e métricas de forma padronizada, "
    "integrar fontes de dados em tempo real e automatizar fluxos analíticos "
    "entre equipes e sistemas, tornando os insights acionáveis e reproduzíveis."
)

app = FastAPI(
    title="TP1 Data Driven Apps",
    description=DESCRIPTION,
    version="1.0.0",
)

app.include_router(router)


@app.exception_handler(InvalidItemIdError)
async def invalid_item_id_handler(_request: Request, exc: InvalidItemIdError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )
