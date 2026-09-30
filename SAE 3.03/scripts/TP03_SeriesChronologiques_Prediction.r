#----------------------------------------------------------------------
#                      TP03_SeriesChronologiques_Prediction
#----------------------------------------------------------------------
# Objectif : lissage exponentiel simple, double, Holt-Winters ; etude des residus.
#----------------------------------------------------------------------

if (!requireNamespace("forecast", quietly=TRUE)) install.packages("forecast")
if (!requireNamespace("tseries", quietly=TRUE)) install.packages("tseries")
library(datasets)
library(forecast)
library(tseries)  # fournit seqplot.ts()

#----------------------------------------------------------------------
#                      Exercice 1 : Prediction par lissage - valeurs boursieres (CAC40)
#----------------------------------------------------------------------
data(EuStockMarkets)
View(EuStockMarkets)
CAC=EuStockMarkets[,3]
plot(CAC, main="CAC40 - cours de cloture quotidiens")

# De quoi s'agit-il : cours de cloture quotidien du CAC40 (bourse de Paris), 1991-1998
# Type d'objet manipule :
is.ts(CAC)
start(CAC); end(CAC); frequency(CAC)
# 260 = nombre approximatif de jours de bourse ouverts par an (5 jours/semaine, hors feries)

# 2. decoupage en deux sous-series
x_train <- window(CAC,end=c(1997,260))
l_train <- length(x_train)
x_test <- window(CAC,start=c(1998,1))
length(x_train); length(x_test)

seqplot.ts(x_train,x_test,colx="blue",coly="red",
           ylab="CAC40",xlab="Dates",
           main="Separation de la serie temporelle en deux")
legend("topleft",c("train","test"),col=c("blue","red"),lty=1)

# 3. Lissage exponentiel simple
x_train_modeled_LS=HoltWinters(x_train,alpha=NULL,beta=FALSE,gamma=FALSE)
# Un seul parametre necessaire pour un lissage simple : alpha (beta et gamma desactives)
x_train_modeled_LS$alpha
x_train_modeled_LS$beta   # FALSE
x_train_modeled_LS$gamma  # FALSE
x_train_modeled_LS$SSE    # somme des carres des erreurs, sur l'echantillon d'apprentissage

x_test_mod=predict(x_train_modeled_LS,n.ahead=length(x_test))
plot(x_train_modeled_LS,x_test_mod,main="prediction de l'annee 1998 via LES")
lines(x_test,col="blue")
legend("topleft",c("train/fitted","prediction","test reel"),col=c("black","red","blue"),lty=1)

Error1 <- x_test[1:10]-x_test_mod[1:10]
plot(1:10,Error1,main="Erreurs de prevision LES (10 premiers jours)",xlab="h",ylab="erreur")
abline(h=0,col="red",lty=2)

# 4. Lissage exponentiel double
x_train_modeled_LD=HoltWinters(x_train,alpha=NULL,beta=NULL,gamma=FALSE)
x_train_modeled_LD$alpha
x_train_modeled_LD$beta
x_train_modeled_LD$SSE
plot(x_train_modeled_LD,main="Holt-Winters filtering (LED)")

x_test_mod_LD=predict(x_train_modeled_LD,n.ahead=length(x_test))
plot(x_train_modeled_LD,x_test_mod_LD,main="prediction de l'annee 1998 via LED")
lines(x_test,col="blue")
legend("topleft",c("train/fitted","prediction","test reel"),col=c("black","red","blue"),lty=1)

# 5. Lissage de Holt-Winters complet (avec composante saisonniere)
x_train_modeled_HW=HoltWinters(x_train,alpha=NULL,beta=NULL,gamma=NULL)
x_train_modeled_HW$alpha
x_train_modeled_HW$beta
x_train_modeled_HW$gamma
x_train_modeled_HW$SSE
x_test_mod_HW=predict(x_train_modeled_HW,n.ahead=length(x_test))
plot(x_train_modeled_HW,x_test_mod_HW,main="prediction de l'annee 1998 via LE de HW")
lines(x_test,col="blue")
legend("topleft",c("train/fitted","prediction","test reel"),col=c("black","red","blue"),lty=1)

# 6. comparaison des 3 predictions
par(mfrow=c(1,3))
plot(1:10,x_test[1:10]-x_test_mod[1:10],main="Erreurs LES",xlab="h",ylab="erreur"); abline(h=0,col="red")
plot(1:10,x_test[1:10]-x_test_mod_LD[1:10],main="Erreurs LED",xlab="h",ylab="erreur"); abline(h=0,col="red")
plot(1:10,x_test[1:10]-x_test_mod_HW[1:10],main="Erreurs HW",xlab="h",ylab="erreur"); abline(h=0,col="red")
par(mfrow=c(1,1))
# Le LES capture un niveau global mais reste plat (une serie financiere se comporte souvent
# comme une marche aleatoire, sans tendance ni saisonnalite claire a cet horizon). Le LED
# ajoute une pente qui peut sur/sous-estimer sur un horizon long si la pente locale n'est
# pas maintenue. Le HW ajoute une saisonnalite qui n'a pas vraiment de sens sur un cours
# boursier (pas de cycle calendaire marque) -> souvent le LES reste le plus raisonnable ici.


#----------------------------------------------------------------------
#                      Exercice 2 : Pluie a Londres
#----------------------------------------------------------------------
rain <- scan("http://robjhyndman.com/tsdldata/hurst/precip1.dat",skip=1)
rain.ts=ts(rain,start=1813,frequency=1)
plot(rain.ts, main="Cumuls annuels de pluie a Londres (1813-1912)")

# 3. LES, horizon 15
rain_LS=HoltWinters(rain.ts,beta=FALSE,gamma=FALSE)
rain_LS$alpha
rain_LS$SSE
plot(rain_LS,main="Lissage exponentiel simple - pluie a Londres")

rain_LS_pred=predict(rain_LS,n.ahead=15)
plot(rain_LS,rain_LS_pred,main="prediction a h=15 (LES)")

res_LS=rain.ts[-1]-fitted(rain_LS)[,1]  # serie d'origine moins serie modelisee (a partir de t=2)
plot(res_LS,main="Residus - LES pluie a Londres",type="l")
abline(h=0,col="red",lty=2)

# 4. LED, horizon 15
rain_LD=HoltWinters(rain.ts,gamma=FALSE)
rain_LD$alpha
rain_LD$beta
rain_LD$SSE
plot(rain_LD,main="Lissage exponentiel double - pluie a Londres")

rain_LD_pred=predict(rain_LD,n.ahead=15)
plot(rain_LD,rain_LD_pred,main="prediction a h=15 (LED)")

res_LD=rain.ts[-(1:2)]-fitted(rain_LD)[,1]
plot(res_LD,main="Residus - LED pluie a Londres",type="l")
abline(h=0,col="red",lty=2)

# 5. Holt-Winters complet (avec gamma)
rain_HW=tryCatch(
  HoltWinters(rain.ts,beta=NULL,gamma=NULL),
  error=function(e) e
)
print(rain_HW)
# Le modele echoue : HoltWinters() avec gamma actif exige une serie avec frequency > 1
# (composante saisonniere), or rain.ts a frequency=1 (donnees annuelles : par definition,
# aucune saisonnalite infra-annuelle n'est observable) -> erreur de type "time series has
# no or less than 2 periods". C'est la meme limite deja rencontree avec BJsales en TP01.

# 6. package forecast, previsions a horizon 15 et 30
rsH=HoltWinters(rain.ts,beta=FALSE,gamma=FALSE)  # seul modele valide ici (pas de saisonnalite)
rs15=forecast(rsH,h=15)
plot(rs15,main="Forecasts from HoltWinters (h=15)")
rs30=forecast(rsH,h=30)
plot(rs30,main="Forecasts from HoltWinters (h=30)")


#----------------------------------------------------------------------
#                      Exercice 3 : Concentration en CO2 a Hawai
#----------------------------------------------------------------------
data(co2)
plot(co2, main="Concentration mensuelle de CO2 - Mauna Loa (1959-1997)")

# 1. regression lineaire (donnees ~ temps) et etude des residus
model_co2=lm(co2~time(co2))
summary(model_co2)
plot(model_co2$residuals,main="Residus - regression lineaire CO2",type="l")
abline(h=0,col="red",lty=2)
# Les residus montrent un motif cyclique tres net -> la seule tendance lineaire ne suffit
# pas a expliquer la serie : il reste une saisonnalite non capturee par ce modele.
shapiro.test(model_co2$residuals)
qqnorm(model_co2$residuals); qqline(model_co2$residuals,col="red")
# Test de Shapiro-Wilk + QQ-plot : si p-value < 0.05, on rejette la normalite des residus
# (attendu ici, a cause du motif saisonnier residuel).

# 2. decomposition additive
decompose_co2=decompose(co2,"additive")
plot(decompose_co2)
co2_ajuste=co2-decompose_co2$seasonal   # serie corrigee des variations saisonnieres (CVS)
plot(co2_ajuste,main="Serie CO2 ajustee (CVS)")

# 3. prediction via ets() (lissage exponentiel automatique, package forecast)
CO2forecasts=ets(co2)
CO2forecasts
plot(forecast(CO2forecasts),main="Prevision CO2 (ets)")
CO2forecasts_44=forecast(CO2forecasts,h=44)
plot(CO2forecasts_44,main="Prevision CO2 a 44 mois")

# 4. autocorrelation et test de blancheur des residus
acf(residuals(CO2forecasts),main="ACF des residus (modele ets)")
Box.test(residuals(CO2forecasts),type="Ljung-Box")
# H0 : les residus forment un bruit blanc (pas d'autocorrelation residuelle)
# H1 : les residus sont autocorreles
# si p-value > 0.05, on ne rejette pas H0 -> le modele a bien capture la dependance
# temporelle de la serie (bon signe pour la qualite de l'ajustement).

par(mfrow=c(1,3))
plot(residuals(CO2forecasts),main="Residus",ylab="residu",xlab="Annee")
qqnorm(residuals(CO2forecasts)); qqline(residuals(CO2forecasts),col="red")
hist(residuals(CO2forecasts),freq=FALSE,main="Histogramme des residus",xlab="residu")
lines(density(residuals(CO2forecasts)),col="red",lwd=2)
par(mfrow=c(1,1))
shapiro.test(residuals(CO2forecasts))
