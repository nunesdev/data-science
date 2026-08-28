import requests
import csv
import datetime

# --- Configurações Iniciais ---
CIDADE_NOME = "Nova York, EUA"
LATITUDE = "40.71"
LONGITUDE = "-74.00"

URL_AWESOME = "https://economia.awesomeapi.com.br/json/last/USD-BRL"
URL_METEO = f"https://api.open-meteo.com/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true"

URL_FORMS = "https://docs.google.com/forms/u/0/d/e/1FAIpQLSccv4QZyHk1uMR60kpqhtcAQ3ge9f5BFr5SObII-HXc8KMcMg/formResponse"

def obter_cotacao_dolar():
    """Busca a cotação do dólar na AwesomeAPI."""
    try:
        resposta = requests.get(URL_AWESOME)
        resposta.raise_for_status()
        dados = resposta.json()
        cotacao = float(dados["USDBRL"]["bid"])
        return round(cotacao, 2)
    except Exception as e:
        print(f"Erro ao obter cotação: {e}")
        return None

def obter_clima_cidade():
    """Busca a temperatura atual da cidade na Open-Meteo."""
    try:
        resposta = requests.get(URL_METEO)
        resposta.raise_for_status()
        dados = resposta.json()
        temperatura = dados["current_weather"]["temperature"]
        return f"{temperatura}°C"
    except Exception as e:
        print(f"Erro ao obter clima: {e}")
        return None

def salvar_dados_csv(cotacao, cidade, clima):
    """Salva os dados coletados em um arquivo CSV."""
    arquivo_csv = "dados_importacao.csv"
    data_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Adicionamos os dados no modo 'a' (append) para não sobrescrever execuções anteriores
    try:
        with open(arquivo_csv, mode="a", newline="", encoding="utf-8") as arquivo:
            escritor = csv.writer(arquivo)
            # Se o arquivo estiver vazio, pode ser interessante adicionar um cabeçalho primeiro
            # escritor.writerow(["Data_Hora", "Cotacao_USD", "Cidade", "Clima"])
            escritor.writerow([data_hora, cotacao, cidade, clima])
        print(f"Dados salvos com sucesso em {arquivo_csv}")
    except Exception as e:
        print(f"Erro ao salvar CSV: {e}")

def enviar_google_forms(cotacao, cidade, clima):
    """Envia os dados consolidados via POST para o Google Forms."""
    payload = {
        "entry.349468953": str(cotacao),
        "entry.1438383412": cidade,
        "entry.1801579020": clima
    }
    
    try:
        resposta = requests.post(URL_FORMS, data=payload)
        if resposta.status_code == 200:
            print("Formulário enviado com sucesso para a equipe de compras!")
        else:
            print(f"Falha ao enviar formulário. Status: {resposta.status_code}")
    except Exception as e:
        print(f"Erro de conexão com o Forms: {e}")

def executar_pipeline():
    print("Iniciando coleta de dados...")
    
    cotacao = obter_cotacao_dolar()
    clima = obter_clima_cidade()
    
    if cotacao and clima:
        print(f"Dados coletados -> Dólar: R${cotacao} | Cidade: {CIDADE_NOME} | Clima: {clima}")
        salvar_dados_csv(cotacao, CIDADE_NOME, clima)
        enviar_google_forms(cotacao, CIDADE_NOME, clima)
    else:
        print("Pipeline interrompido: falha na coleta de dados essenciais.")

# --- Execução ---
if __name__ == "__main__":
    executar_pipeline()