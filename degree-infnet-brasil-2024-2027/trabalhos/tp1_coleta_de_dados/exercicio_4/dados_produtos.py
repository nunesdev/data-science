import json

# Lê o arquivo JSON
with open('dados_produtos.json', 'r', encoding='utf-8') as f:
    produtos = json.load(f)

# Imprime o cabeçalho da tabela
print(f"{'ID':<5} | {'Nome':<15} | {'Preço':<10} | {'Quantidade':<10}")
print("-" * 50)

# Itera sobre a lista de produtos e imprime cada linha
for p in produtos:
    print(f"{p['id']:<5} | {p['nome']:<15} | {p['preco']:<10.2f} | {p['quantidade']:<10}")