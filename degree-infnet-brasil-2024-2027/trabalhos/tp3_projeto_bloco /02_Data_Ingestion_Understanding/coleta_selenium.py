from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def coletar_dados_dinamicos():
    print("Iniciando o Selenium Webdriver...")
    # Configura o navegador para rodar em modo oculto (headless)
    opcoes = webdriver.ChromeOptions()
    opcoes.add_argument('--headless')
    
    servico = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=servico, options=opcoes)
    
    url = "https://observatorio3setor.org.br/lista-conheca-projetos-sociais-de-15-causas-diferentes/"
    driver.get(url)
    
    # Aguarda o JavaScript carregar
    time.sleep(3)
    
    print("Extraindo dados da página dinamicamente...")
    # Pega todos os parágrafos usando XPath
    paragrafos = driver.find_elements(By.TAG_NAME, 'p')
    
    dados_extras = []
    
    for p in paragrafos[:20]: # Pegamos uma amostra apenas para complementar
        texto = p.text
        if "Atuação:" in texto or "Site:" in texto:
            dados_extras.append({"Conteudo_Dinamico": texto})
            
    driver.quit()
    
    # Salva um novo CSV
    df_selenium = pd.DataFrame(dados_extras)
    df_selenium.to_csv("dados_coletados_selenium.csv", index=False)
    print("Coleta via Selenium concluída com sucesso! Arquivo 'dados_coletados_selenium.csv' gerado.")

if __name__ == "__main__":
    coletar_dados_dinamicos()