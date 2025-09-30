# =====================================================
# Trabalho Final - Modelo de Regressão Linear
# Dataset: Netflix Subscribers
# =====================================================

setwd("/Volumes/Extreme SSD/www/data-science/r-projects")

# 1. Importa dados
netflix <- read.csv("dataset_netflix.csv", stringsAsFactors = FALSE)

str(netflix)
summary(netflix)

# 2. Limpa e prepara
# Converte datas para formato Date
netflix$Join.Date        <- as.Date(netflix$Join.Date, format = "%d-%m-%y")
netflix$Last.Payment.Date <- as.Date(netflix$Last.Payment.Date, format = "%d-%m-%y")

# Converte variáveis categóricas em fator
netflix$Subscription.Type <- as.factor(netflix$Subscription.Type)
netflix$Country           <- as.factor(netflix$Country)
netflix$Gender            <- as.factor(netflix$Gender)
netflix$Device            <- as.factor(netflix$Device)
netflix$Plan.Duration     <- as.factor(netflix$Plan.Duration)

# 3. Estatísticas descritivas
summary(netflix$Monthly.Revenue)
sd(netflix$Monthly.Revenue)
median(netflix$Monthly.Revenue)

png("plots/plt_histograma.png", width = 800, height = 600)
hist(netflix$Monthly.Revenue,
     main = "Distribuição da Receita Mensal",
     xlab = "Receita Mensal ($)",
     col = "lightgreen", border = "white")
dev.off()

png("plots/plt_boxplot.png", width = 800, height = 600)
boxplot(netflix$Age ~ netflix$Subscription.Type,
        main = "Idade por Tipo de Assinatura",
        xlab = "Tipo de Assinatura", ylab = "Idade")
dev.off()

# 4. Construção do modelo
modelo <- lm(Monthly.Revenue ~ Age + Subscription.Type + Gender, data = netflix)

summary(modelo)

# 5. Diagnóstico do modelo
par(mfrow = c(2, 2))

png("plots/plt_modelo.png", width = 800, height = 600)
plot(modelo)
dev.off()

# 6. Validação simples
pred <- predict(modelo, newdata = netflix)
rmse <- sqrt(mean((pred - netflix$Monthly.Revenue)^2))
rmse
