TP1: Dashboard Spotify 2024 com Streamlit
Objetivo do Trabalho

Este projeto é o resultado prático do primeiro Teste de Performance. O objetivo é desenvolver uma aplicação web interativa em Python, utilizando o framework Streamlit, 
para analisar e visualizar a base de dados "Most Streamed Spotify Songs 2024".
A aplicação consolida conceitos fundamentais para o desenvolvimento em Ciência de Dados, englobando a configuração de ambientes virtuais isolados, 
a manipulação de dados com a biblioteca Pandas e a renderização responsiva de componentes de interface, como tabelas dinâmicas, indicadores de métricas, textos formatados, elementos multimídia, comandos Magic e animações.

Estrutura do Projeto
app.py: Código fonte principal contendo a lógica e a interface da aplicação Streamlit.

Most Streamed Spotify Songs 2024.csv: Base de dados contendo os atributos, estatísticas e metadados das faixas no Spotify e em outras plataformas.

README.txt: Documentação explicativa do projeto e guia de execução.

Instruções de Uso e Configuração
1. Pré-requisitos
O sistema exige a instalação prévia do Python (versão 3.8 ou superior) e do gerenciador de pacotes pip. É necessário garantir que os arquivos app.py e Most Streamed Spotify Songs 2024.csv estejam no mesmo diretório.

2. Criação do Ambiente Virtual
Para garantir o isolamento das dependências, crie um ambiente virtual. Pelo terminal, na raiz do projeto, instale o pacote virtualenv e instancie o ambiente (nomeado aqui como venv):

Bash
pip install virtualenv
virtualenv venv
3. Ativação do Ambiente Virtual
Antes de instalar as bibliotecas ou executar a aplicação, ative o interpretador isolado.

No Windows:

Bash
.\venv\Scripts\activate
No Linux ou macOS:

Bash
source venv/bin/activate
4. Instalação das Dependências
Com o terminal apontando para o ambiente ativado (venv), instale os frameworks exigidos pelo código fonte:

Bash
pip install streamlit pandas
5. Execução do Código Fonte
O script não deve ser inicializado como um arquivo Python comum. Utilize a CLI do Streamlit para levantar o servidor web local:

Bash
streamlit run app.py
O terminal exibirá os endereços de rede locais (Network URL e Local URL) e o sistema operacional abrirá automaticamente o navegador padrão na porta 8501, exibindo o dashboard completo. Para encerrar a aplicação, pressione Ctrl+C no terminal.