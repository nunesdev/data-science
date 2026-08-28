import pandas as pd

# Lê o arquivo CSV
df = pd.read_csv('dados_alunos.csv')

# Imprime os dados de todos os alunos
print("--- Dados dos Alunos ---")
print(df)
print("\n")

# Verifica e imprime o tipo de dados de todas as colunas
print("--- Tipos de Dados das Colunas ---")
print(df.dtypes)