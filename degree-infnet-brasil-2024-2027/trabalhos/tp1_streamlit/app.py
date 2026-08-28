# Importo a biblioteca necessária para a interface
import streamlit as st
import pandas as pd

# Carrego o arquivo CSV referenciado para a memória e instancio o DataFrame na variável 'df'
df = pd.read_csv("Most Streamed Spotify Songs 2024.csv", encoding="latin-1")

# Ajuste os nomes das colunas 'Track Name', 'Artist' e 'Spotify Streams' caso sejam diferentes no CSV
top_3 = df.head(3)

# Defino o título principal da página web
st.title("Dashboard de Músicas Mais Tocadas")

# Crio o cabeçalho da seção principal
st.header("Estatísticas de 2024")

# Insiro um subcabeçalho para organizar o conteúdo específico
st.subheader("Base de dados: Most Streamed Spotify Songs")

# Exibo um parágrafo em texto puro para informações gerais
st.text("Os dados abaixo representam a compilação abrangente das métricas musicais.")

# Renderizo um parágrafo utilizando markdown para incluir negrito e um link, 
# já que st.text() não interpreta a linguagem de marcação
st.markdown("Para analisar os atributos das faixas com recursos avançados, consulte a **documentação oficial** no site do [Streamlit](https://streamlit.io/).")

# Crio um separador visual na página
st.divider()


# Crio um cabeçalho para separar a primeira visualização
st.header("Visualização usando st.dataframe()")
st.text("Esta função exibe uma tabela interativa:")
# Renderizo o DataFrame completo de forma interativa
st.dataframe(df)

# Crio um separador visual na página
st.divider()

# Crio um cabeçalho para separar a segunda visualização
st.header("Visualização usando st.table()")
st.text("Esta função exibe uma tabela estática (limitada a 5 linhas para não sobrecarregar a tela):")
# Renderizo uma versão estática da tabela. 
# Utilizo o .head() para limitar, caso contrário a página ficaria extremamente longa
st.table(df.head())


# Crio um separador visual na página
st.divider()

# Defino os textos de cabeçalho da aplicação
st.title("Indicadores do Spotify 2024")
st.header("Top 3 Músicas")

# Crio três colunas para organizar as métricas lado a lado na tela
col1, col2, col3 = st.columns(3)

# Extraio os dados da primeira linha e renderizo a métrica na primeira coluna
with col1:
    nome_1 = top_3.iloc[0]['Track']
    artista_1 = top_3.iloc[0]['Artist']
    streams_1 = top_3.iloc[0]['Spotify Streams']
    st.metric(label=f"{nome_1} ({artista_1})", value=streams_1)

# Extraio os dados da segunda linha e renderizo a métrica na segunda coluna
with col2:
    nome_2 = top_3.iloc[1]['Track']
    artista_2 = top_3.iloc[1]['Artist']
    streams_2 = top_3.iloc[1]['Spotify Streams']
    st.metric(label=f"{nome_2} ({artista_2})", value=streams_2)

# Extraio os dados da terceira linha e renderizo a métrica na terceira coluna
with col3:
    nome_3 = top_3.iloc[2]['Track']
    artista_3 = top_3.iloc[2]['Artist']
    streams_3 = top_3.iloc[2]['Spotify Streams']
    st.metric(label=f"{nome_3} ({artista_3})", value=streams_3)



# Uso st.write() para renderizar um texto com formatação markdown
st.write("### Demonstração da função `st.write()`")
st.write("A função `st.write()` interpreta *markdown* nativamente, permitindo formatações como **negrito**, itálico e listas.")

# Uso st.write() para renderizar o DataFrame (limitado a 3 linhas)
st.write("**Visualizando o DataFrame:**")
st.write(df.head(3))

# Uso st.write() para renderizar uma lista em Python
st.write("**Visualizando uma Lista Python:**")
plataformas = ["Spotify", "YouTube", "TikTok", "Apple Music"]
st.write(plataformas)

# Crio um separador visual na página
st.divider()

# Insiro um título no aplicativo apenas declarando uma string solta formatada em Markdown
"# Exploração usando Comandos Magic"

# Insiro um texto explicativo
"Os comandos *Magic* renderizam variáveis diretamente na tela de forma limpa e ágil."

# Defino uma lista nativa do Python e a coloco isolada na linha para ser exibida
"**Plataformas analisadas:**"
["Spotify", "Apple Music", "TikTok", "YouTube"]


# Coloco a variável correspondente à amostragem do DataFrame isolada na linha para renderizar a tabela
"**Amostra dos Dados:**"
df.head(3)

# Crio um separador visual na página
st.divider()

# Defino o título principal da seção
st.title("Integração de Multimídia")

# Crio um cabeçalho e renderizo uma imagem via URL (também aceita arquivos locais)
st.header("Exibição de Imagem")
st.image("https://images.unsplash.com/photo-1611162617474-5b21e879e113?w=800", caption="Imagem de demonstração (via URL)")

# Crio um cabeçalho e renderizo um reprodutor de áudio
# Substituo 'audio_exemplo.mp3' pelo caminho de um arquivo real no meu computador
st.header("Exibição de Áudio")
st.audio("audio_exemplo.mp3", format="audio/mpeg")

# Crio um cabeçalho e renderizo um reprodutor de vídeo
# Substituo 'video_exemplo.mp4' pelo caminho de um arquivo real no meu computador
st.header("Exibição de Vídeo")
st.video("video_exemplo.mov", format="video/mov")

st.divider()

# Adiciono emojis diretamente nas strings de texto renderizadas pelas funções de título
st.title("Emojis e Animações 🚀🎶")

# Utilizo st.write() combinando texto com emojis em formato de shortcode
st.write("A biblioteca interpreta códigos como :sunglasses:, :fire: e :star: nativamente.")

# Utilizo a função st.image() para renderizar um arquivo GIF animado via URL
st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExbzFzNjd5YWtidWY3enplZmpyYWEwbHVxZDA3dDEwam9iMWJxZjRtOCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/k1Psl92gw7YPSPYFKm/giphy.gif", caption="GIF animado renderizado com st.image()")
