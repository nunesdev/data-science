# Lê o conteúdo do primeiro arquivo
with open('parte1.txt', 'r', encoding='utf-8') as f1:
    conteudo_parte1 = f1.read()

# Lê o conteúdo do segundo arquivo
with open('parte2.txt', 'r', encoding='utf-8') as f2:
    conteudo_parte2 = f2.read()

# Abre o arquivo de destino para escrita e combina os textos
with open('historia_completa.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(conteudo_parte1)
    
    # Adiciona uma quebra de linha caso a parte 1 não termine com uma
    if not conteudo_parte1.endswith('\n'):
        f_out.write('\n')
        
    f_out.write(conteudo_parte2)