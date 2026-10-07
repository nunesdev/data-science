import pandas as pd

# Carregar o ficheiro CSV inteiro do Tocantins (o separador costuma ser ponto e vírgula)
df_tocantins = pd.read_csv("dado_bruto/perfil_eleitor_secao_2026_TO.csv", sep=";", encoding="latin1")

# Filtrar apenas os Boletins de Urna de Palmas
df_palmas = df_tocantins[df_tocantins['CD_MUNICIPIO'] == 73440]

# Opcional: Filtrar apenas a Zona Eleitoral 29 (que abrange Taquaruçu e região sul)
df_taquarucu = df_palmas[df_palmas['NR_ZONA'] == 29]

# Guardar o ficheiro filtrado para usar no Streamlit
df_taquarucu.to_csv("dado_filtrado/dados_perfil_eleitorado_palmas.csv", index=False)