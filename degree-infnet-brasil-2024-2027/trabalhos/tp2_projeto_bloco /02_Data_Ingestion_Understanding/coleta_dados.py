import requests
from bs4 import BeautifulSoup
import csv

def coletar_dados_online(url):
    """
    Acessa a URL fornecida e extrai os dados dos projetos sociais.
    """
    # Cabeçalho para simular um navegador e evitar bloqueios
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    
    try:
        print(f"Acessando a URL: {url} ...")
        response = requests.get(url, headers=headers)
        response.raise_for_status() # Verifica se a requisição foi bem sucedida
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        projetos = []
        projeto_atual = {}
        
        # O conteúdo principal está dentro das tags <p>
        paragrafos = soup.find_all('p')
        
        for p in paragrafos:
            texto = p.get_text(strip=True)
            if not texto:
                continue
                
            # Identifica a 'Atuação' e pega o Nome do projeto
            if texto.startswith('Atuação:'):
                projeto_atual['Atuação'] = texto.replace('Atuação:', '').strip()
                
                # O nome do projeto geralmente está em uma tag <strong> no mesmo parágrafo ou no anterior
                strong = p.find('strong')
                if strong:
                    projeto_atual['Nome'] = strong.get_text(strip=True)
                else:
                    prev_p = p.find_previous_sibling('p')
                    if prev_p and prev_p.find('strong'):
                        projeto_atual['Nome'] = prev_p.find('strong').get_text(strip=True)
                        
            # Identifica o 'Site' e tenta pegar a URL do href
            elif texto.startswith('Site:'):
                link = p.find('a')
                if link and link.has_attr('href'):
                    projeto_atual['Site'] = link['href']
                else:
                    projeto_atual['Site'] = texto.replace('Site:', '').strip()
                    
            # Identifica a descrição 'O que faz'
            elif texto.startswith('O que faz:'):
                projeto_atual['Descrição'] = texto.replace('O que faz:', '').strip()
                
                # 'O que faz' é o último item do bloco do projeto, então salvamos na lista e limpamos o dicionário
                if 'Nome' in projeto_atual:
                    projetos.append(projeto_atual)
                projeto_atual = {}
                
        return projetos

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return []

def salvar_csv(dados, nome_arquivo='projetos_sociais.csv'):
    if not dados:
        print("Nenhum dado para salvar.")
        return

    colunas = ['Nome', 'Atuação', 'Site', 'Descrição']
    
    with open(nome_arquivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=colunas)
        writer.writeheader()
        writer.writerows(dados)
    
    print(f"Dados salvos com sucesso no arquivo '{nome_arquivo}'!")

if __name__ == "__main__":
    url_alvo = "https://observatorio3setor.org.br/lista-conheca-projetos-sociais-de-15-causas-diferentes/"
    
    dados_extraidos = coletar_dados_online(url_alvo)
    
    if dados_extraidos:
        print(f"\n{len(dados_extraidos)} projetos encontrados e processados.")
        salvar_csv(dados_extraidos)