import requests
from lxml import html
import pandas as pd
import re
from urllib.robotparser import RobotFileParser
import time


# biblioteca urllib para ler e verificar as permissões do robots.txt do fornecedor, 
# garantindo que sigo as diretrizes e regras de ética do site antes do web scraping.
print("Verificando permissões no robots.txt...")
rp = RobotFileParser()
rp.set_url("https://books.toscrape.com/robots.txt")
rp.read()

# Escolho a categoria "Science" para aplicar o escopo do projeto de coleta
url_base = "https://books.toscrape.com/catalogue/category/books/science_22/"
url_atual = url_base + "index.html"

if not rp.can_fetch("*", url_atual):
    print("Erro: O scraping não é permitido pelo robots.txt para esta URL.")
else:
    print("Permissão concedida. Iniciando a coleta...")

    # Estruturo um dicionário de 'headers' com um User-Agent para a minha requisição 
    # HTTP. Isso informa ao servidor quem está fazendo a requisição e previne bloqueios.
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    
    # Estruturo uma lista vazia que vai organizar os dados do catálogo após a extração.
    catalogo = []
    # Defino um dicionário para converter a representação textual de estrelas em número inteiro.
    star_mapping = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    
    # Implemento a rotina com um loop 'while' para percorrer automaticamente as páginas 
    # da categoria. O loop continua até que eu não encontre mais o botão "Next".
    while url_atual:
        # Executo a requisição HTTP GET usando a biblioteca requests.
        response = requests.get(url_atual, headers=headers)
        
        if response.status_code != 200:
            print(f"Falha de acesso ao site. Status HTTP: {response.status_code}")
            break
            
        # Analiso a estrutura em árvore (DOM) e transformo a resposta HTML em um objeto
        # de árvore com o 'lxml'. Optei pelo uso de expressões XPath para percorrer 
        # esse DOM e mapear perfeitamente os elementos exatos na hierarquia do HTML.
        tree = html.fromstring(response.content)
        
        # Mapeio todos os itens buscando pela tag 'article' que tem a classe 'product_pod'
        livros = tree.xpath('//article[@class="product_pod"]')

        for livro in livros:
            # Utilizo XPath para buscar dentro da tag 'h3' > 'a' o atributo 'title'.
            titulo = livro.xpath('.//h3/a/@title')[0]
            
            # Extraio a string suja do preço e aplico expressões regulares (Regex) 
            # combinadas com a extração para capturar e padronizar o dado para um valor float puro.
            preco_str = livro.xpath('.//p[@class="price_color"]/text()')[0]
            preco_match = re.search(r'\d+\.\d{2}', preco_str)
            preco = float(preco_match.group()) if preco_match else None
            
            disp_str = ''.join(livro.xpath('.//p[contains(@class, "instock availability")]//text()'))
            disp_limpa = re.sub(r'^\s+|\s+$', '', disp_str).replace('\n', '')
            
            # Comparo esse valor mapeando-o em inteiro de acordo com as chaves que defini acima.
            classe_estrela = livro.xpath('.//p[contains(@class, "star-rating")]/@class')[0]
            avaliacao = 0
            for texto_estrela, valor in star_mapping.items():
                if texto_estrela in classe_estrela:
                    avaliacao = valor
                    break
            
            # Armazeno os dados padronizados de forma estruturada em minha lista.
            catalogo.append({
                'Título': titulo,
                'Preço (£)': preco,
                'Disponibilidade': disp_limpa,
                'Avaliação (Estrelas)': avaliacao
            })
            
        # Analiso no final da página se há um botão "next" para avançar
        link_proximo = tree.xpath('//li[@class="next"]/a/@href')
        
        if link_proximo:
            url_atual = url_base + link_proximo[0]
            time.sleep(1) # Aguardo 1 segundo por boas práticas de raspagem
        else:
            url_atual = None # Não há mais páginas, saio do loop de crawling.

    # Organizo e armazeno o resultado da extração no Pandas, gerando um DataFrame estruturado.
    df_catalogo = pd.DataFrame(catalogo)
    nome_arquivo = 'catalogo_fornecedor.xlsx'
    
    # Exporto os dados coletados no arquivo Excel 
    with pd.ExcelWriter(nome_arquivo, engine='openpyxl') as writer:
        df_catalogo.to_excel(writer, index=False, sheet_name='Catalogo_Livraria')
        
    print(f"\nColeta concluída com sucesso! {len(catalogo)} livros exportados para o arquivo '{nome_arquivo}'.")