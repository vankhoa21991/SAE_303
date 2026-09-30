#----------------------------------------------------------------------
#                      TP04_SeriesChronologiques_Tests
#----------------------------------------------------------------------
# Objectif : test de detection de la saisonnalite, analyse de la variance et test de
# Fisher, test de Buys-Ballot, test de detection de la tendance (Mann-Kendall), tests
# de stationnarite/non-stationnarite (ADF, KPSS, Phillips-Perron), tests de bruit
# blanc/autocorrelation (Box-Ljung) et test de normalite (Shapiro-Wilk).
#----------------------------------------------------------------------

if (!requireNamespace("trend", quietly=TRUE)) install.packages("trend")
if (!requireNamespace("tseries", quietly=TRUE)) install.packages("tseries")
library(trend)
library(tseries)

#----------------------------------------------------------------------
#                      0. Serie d'exemple : CO2 Mauna Loa
#----------------------------------------------------------------------
data(co2)
plot(co2, main="CO2 Mauna Loa (1959-1997)")

#----------------------------------------------------------------------
#                      1. Test de detection de la saisonnalite
#----------------------------------------------------------------------
## 1.1 Analyse de la variance et test de Fisher
# On teste si le mois (facteur) explique une part significative de la variance de la serie.
mois=cycle(co2)
annee=floor(time(co2))
anova_co2=aov(as.numeric(co2)~as.factor(mois))
summary(anova_co2)
# H0 : pas d'effet du mois sur la serie (pas de saisonnalite)
# H1 : effet du mois significatif (saisonnalite presente)
# Une p-value < 0.05 sur le facteur "mois" (statistique de Fisher) rejette H0 -> saisonnalite confirmee.

## 1.2 Methode/test de Buys-Ballot
# Regression de l'ecart-type annuel sur la moyenne annuelle :
# a proche de 0 -> modele additif plausible ; a significativement != 0 -> modele multiplicatif.
moy_an=tapply(as.numeric(co2),annee,mean)
sd_an=tapply(as.numeric(co2),annee,sd)
buys_ballot=lm(sd_an~moy_an)
summary(buys_ballot)
plot(moy_an,sd_an,main="Buys-Ballot : ecart-type annuel vs moyenne annuelle",
     xlab="moyenne annuelle",ylab="ecart-type annuel")
abline(buys_ballot,col="red")
# coefficient a (pente) : proche de 0 -> modele additif plausible pour cette serie.

#----------------------------------------------------------------------
#                      2. Test de detection de la tendance : Mann-Kendall
#----------------------------------------------------------------------
mk.test(as.numeric(co2))
# H0 : pas de tendance monotone
# H1 : tendance monotone (croissante ou decroissante)
# p-value < 0.05 -> on rejette H0, la tendance est jugee significative.
# Le signe de la statistique S (ou de tau) indique le sens de la tendance (ici, croissante).

#----------------------------------------------------------------------
#                      3. Tests de stationnarite / non-stationnarite
#----------------------------------------------------------------------
## 3.1 Dickey-Fuller augmente (H0 : serie non stationnaire)
adf.test(co2)
# p-value < 0.05 -> on rejette H0 -> serie stationnaire.
# Sur co2 brut (tendance + saisonnalite fortes), on s'attend a NE PAS rejeter H0.

## 3.2 KPSS (H0 : serie stationnaire - hypotheses inversees par rapport a l'ADF)
kpss.test(co2, null="Trend")
# p-value < 0.05 -> on rejette H0 -> serie non stationnaire (cohérent avec l'ADF ci-dessus :
# les deux tests s'accordent pour dire que la serie brute n'est pas stationnaire).

## 3.3 Phillips-Perron (H0 : serie non stationnaire, comme l'ADF)
pp.test(co2)

#----------------------------------------------------------------------
#                      4. Test de bruit blanc / autocorrelation : Box-Ljung
#----------------------------------------------------------------------
acf(co2, main="ACF de la serie CO2 brute")
Box.test(co2, lag=12, type="Ljung-Box")
# Sur la serie brute on s'attend a un rejet massif de H0 (bruit blanc) : la serie est
# fortement autocorrelee (tendance + saisonnalite). Ce test est surtout utile applique
# aux RESIDUS d'un modele deja ajuste (voir TP03, exercice CO2, modele ets()).

#----------------------------------------------------------------------
#                      5. Test de normalite
#----------------------------------------------------------------------
model_lin=lm(co2~time(co2))
shapiro.test(model_lin$residuals)
qqnorm(model_lin$residuals); qqline(model_lin$residuals,col="red")
hist(model_lin$residuals,freq=FALSE,main="Residus - regression lineaire CO2")
lines(density(model_lin$residuals),col="red",lwd=2)


#----------------------------------------------------------------------
#      TP2 > Exercice a preparer : validation d'un modele LES sur CO2
#----------------------------------------------------------------------
# 31. Decoupage en Data1 (apprentissage, 1959-1989) et DataVal (validation, 1990-1997)
Data1=window(co2,end=c(1989,12))
DataVal=window(co2,start=c(1990,1),end=c(1997,12))
length(Data1); length(DataVal)

# 32. Modele LES base sur Data1, prevision sur l'horizon de DataVal
model_LES=HoltWinters(Data1,beta=FALSE,gamma=FALSE)
model_LES$alpha
pred_LES=predict(model_LES,n.ahead=length(DataVal))
plot(Data1,xlim=c(1959,1998),ylim=range(co2),main="Validation LES sur CO2 (1990-1997)")
lines(DataVal,col="blue")
lines(pred_LES,col="red")
legend("topleft",c("apprentissage","realite 1990-1997","prevision LES"),
       col=c("black","blue","red"),lty=1)

# 33. RMSE entre predictions et DataVal
RMSE_LES=sqrt(mean((DataVal-pred_LES)^2))
cat("RMSE du modele LES :", RMSE_LES, "\n")
# Un LES pur (sans tendance ni saisonnalite) est structurellement mal adapte a CO2, qui a
# a la fois une forte tendance ET une forte saisonnalite -> RMSE attendu eleve
# (a comparer avec les modeles LED et LHW ci-dessous, point 5).

# 4. Si le modele semblait correct, on predirait 1997-2007 en reentrainant sur la serie
#    complete (ici a titre indicatif seulement : le LES n'etant pas adapte a cette serie,
#    ce n'est pas la methode a retenir en pratique - voir conclusion du point 5) :
model_LES_full=HoltWinters(co2,beta=FALSE,gamma=FALSE)
pred_1997_2007=predict(model_LES_full,n.ahead=12*10)
plot(co2,xlim=c(1959,2008),main="Prevision CO2 2007 via LES (modele non adapte, a titre indicatif)")
lines(pred_1997_2007,col="red")

# 5. Tester d'autres methodes : lissage double (LED) et Holt-Winters (LHW)
model_LED=HoltWinters(Data1,gamma=FALSE)
pred_LED=predict(model_LED,n.ahead=length(DataVal))
RMSE_LED=sqrt(mean((DataVal-pred_LED)^2))

model_LHW=HoltWinters(Data1,seasonal="additive")
pred_LHW=predict(model_LHW,n.ahead=length(DataVal))
RMSE_LHW=sqrt(mean((DataVal-pred_LHW)^2))

cat("RMSE LES :", RMSE_LES, "\n")
cat("RMSE LED :", RMSE_LED, "\n")
cat("RMSE LHW :", RMSE_LHW, "\n")
# Le modele Holt-Winters (LHW), qui integre a la fois tendance ET saisonnalite, doit
# donner la RMSE la plus faible sur cette serie : c'est le seul des trois modeles a
# capturer explicitement le cycle saisonnier tres marque du CO2.

plot(Data1,xlim=c(1985,1998),ylim=range(co2),main="Comparaison LES / LED / LHW sur CO2")
lines(DataVal,col="black",lwd=2)
lines(pred_LES,col="red")
lines(pred_LED,col="blue")
lines(pred_LHW,col="green")
legend("topleft",c("realite","LES","LED","LHW"),col=c("black","red","blue","green"),lty=1)
