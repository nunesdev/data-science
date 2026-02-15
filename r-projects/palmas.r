# Trabalho Final: Modelo de Regressão Linear (Versão com R Base)
# Análise da Relação entre Crescimento Populacional e Temperatura em Palmas-TO

# --------------------------------------------------------------------------
# 1. CARREGAMENTO E PREPARAÇÃO DOS DADOS
# --------------------------------------------------------------------------

# Carregando o conjunto de dados usando a função base do R.
# O arquivo 'dados_regressao_palmas.csv' deve estar no mesmo diretório.
dados <- read.csv("dados_regressao_palmas.csv")

# Exibindo as primeiras linhas do conjunto de dados para verificação
print("Visualização inicial dos dados:")
head(dados)

# Verificando a estrutura dos dados (tipos de colunas, etc.)
print("Estrutura do conjunto de dados:")
str(dados)


# --------------------------------------------------------------------------
# 2. ANÁLISE EXPLORATÓRIA DOS DADOS (EDA)
# --------------------------------------------------------------------------

# Calculando estatísticas descritivas para as variáveis de interesse
print("Resumo estatístico das variáveis:")
summary(dados[, c("Populacao_Estimada", "Temperatura_Media_Anual")])

# Para a visualização, primeiro vamos ajustar o modelo para depois plotar a linha
# de regressão sobre o gráfico de dispersão.

# --------------------------------------------------------------------------
# 3. CONSTRUÇÃO DO MODELO DE REGRESSÃO LINEAR
# --------------------------------------------------------------------------

# Ajustando o modelo de regressão linear simples
# Queremos prever a 'Temperatura_Media_Anual' com base na 'Populacao_Estimada'
modelo_regressao <- lm(Temperatura_Media_Anual ~ Populacao_Estimada, data = dados)

# Exibindo o resumo completo do modelo
print("Resumo do Modelo de Regressão Linear:")
summary(modelo_regressao)


# --------------------------------------------------------------------------
# 4. VISUALIZAÇÃO DO MODELO (GRÁFICO COM R BASE)
# --------------------------------------------------------------------------

# Criando um gráfico de dispersão com a função plot() do R base
png("plots/plt_palmas_plot.png", width = 800, height = 600)
plot(dados$Populacao_Estimada, dados$Temperatura_Media_Anual,
     main = "Relação entre População e Temperatura Média Anual em Palmas (2000-2024)",
     xlab = "População Estimada",
     ylab = "Temperatura Média Anual (°C)",
     pch = 19, # pch define o estilo do ponto (19 é um círculo sólido)
     col = "blue" # Define a cor dos pontos
)
dev.off()

# Adicionando a linha de regressão ao gráfico existente
abline(modelo_regressao, col = "red", lwd = 2) # lwd define a espessura da linha

# Adicionando uma legenda ao gráfico
legend("topleft", legend = "Linha de Regressão", col = "red", lty = 1, lwd = 2)


# --------------------------------------------------------------------------
# 5. ANÁLISE E DIAGNÓSTICO DO MODELO
# --------------------------------------------------------------------------

# Configurando a área de plotagem para exibir 4 gráficos (2x2)
par(mfrow = c(2, 2))

# Gerando os gráficos de diagnóstico padrão do R
plot(modelo_regressao)

# Restaurando a configuração de plotagem para o padrão (1x1)
par(mfrow = c(1, 1))

# Teste de Shapiro-Wilk para a normalidade dos resíduos
residuos <- residuals(modelo_regressao)
teste_shapiro <- shapiro.test(residuos)
print("Teste de Shapiro-Wilk para Normalidade dos Resíduos:")
print(teste_shapiro)


# --------------------------------------------------------------------------
# 6. INTERPRETAÇÃO DOS RESULTADOS
# --------------------------------------------------------------------------

# Extraindo os coeficientes do modelo
coeficientes <- coef(modelo_regressao)
intercepto <- coeficientes[1]
inclinacao <- coeficientes[2]

# Extraindo o R-quadrado ajustado
r_quadrado_ajustado <- summary(modelo_regressao)$adj.r.squared

# Usando cat() e sprintf() para formatar e imprimir a interpretação final
cat("\n--- Interpretação Final ---\n")
cat(sprintf("Intercepto (α): %.4f\n", intercepto))
cat(sprintf("   -> Valor esperado da temperatura quando a população é zero.\n"))
cat(sprintf("Coeficiente de Inclinação (β): %.8f\n", inclinacao))
cat(sprintf(
  "   -> Para cada aumento de 1 habitante na população, a temperatura média anual aumenta, em média, em %.8f °C.\n",
  inclinacao
))
cat(sprintf("R-quadrado Ajustado: %.4f\n", r_quadrado_ajustado))
cat(sprintf(
  "   -> Aproximadamente %.2f%% da variação na temperatura média anual pode ser explicada pela variação na população.\n",
  r_quadrado_ajustado * 100
))

# Fim do script