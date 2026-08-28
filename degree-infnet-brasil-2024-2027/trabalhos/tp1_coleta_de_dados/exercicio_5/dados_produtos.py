import pandas as pd

# Lê o arquivo JSON gerado anteriormente
df = pd.read_json('../exercicio_4/dados_produtos.json')

# Converte e salva os dados no arquivo CSV com o cabeçalho correspondente
df.to_csv('produtos.csv', index=False, encoding='utf-8')