from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import os

# Inicializa a API
app = FastAPI(
    title="API ConectaFood",
    description="API para integração e gestão de dados de ONGs e Projetos Sociais.",
    version="1.0"
)

# Caminho do banco de dados em CSV
DATA_PATH = '../02_Data_Ingestion_Understanding/projetos_sociais.csv'

# Define a estrutura de dados esperada no POST
class ONG(BaseModel):
    Nome: str
    Atuação: str
    Site: str
    Descrição: str

@app.get("/")
def home():
    return {"mensagem": "Bem-vindo à API do ConectaFood! Acesse /docs para ver a documentação."}

@app.get("/ongs")
def listar_ongs():
    """Rota GET para listar todas as ONGs coletadas."""
    try:
        # Se estiver rodando da raiz, ajusta o caminho
        caminho = DATA_PATH if os.path.exists(DATA_PATH) else '02_Data_Ingestion_Understanding/projetos_sociais.csv'
        df = pd.read_csv(caminho)
        df = df.fillna("")

        return df.to_dict(orient="records")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Arquivo de dados não encontrado.")

@app.post("/ongs")
def adicionar_ong(ong: ONG):
    """Rota POST para adicionar uma nova ONG ao CSV."""
    caminho = DATA_PATH if os.path.exists(DATA_PATH) else '02_Data_Ingestion_Understanding/projetos_sociais.csv'
    
    if os.path.exists(caminho):
        df = pd.read_csv(caminho)
    else:
        df = pd.DataFrame(columns=['Nome', 'Atuação', 'Site', 'Descrição'])
    
    # Adiciona o novo registro
    novo_dado = pd.DataFrame([ong.dict()])
    df = pd.concat([df, novo_dado], ignore_index=True)
    
    # Salva no CSV
    df.to_csv(caminho, index=False)
    
    return {"mensagem": "ONG adicionada com sucesso!", "dados": ong}