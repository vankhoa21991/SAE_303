#----------------------------------------------------------------------
#                      TP02_SeriesChronologiques_Decomposition_Modelisation
#----------------------------------------------------------------------
# Objectif : moyennes mobiles, decompositions (manuelle et automatique),
# modelisation de tendance (affine/exponentielle/quadratique), selection de modele.
#----------------------------------------------------------------------

#----------------------------------------------------------------------
#                      Exercice 1 : Volume de fret pour les aeroports de Paris
#----------------------------------------------------------------------

#------------------------- A - Phase exploratoire ------------------------------------
#--------------------------------------Bloc 1--------------------------------------
data=read.table("../data/fret.txt",sep=";")
View(data)
data[1:10,]
#-----------------------------------------Bloc 2--------------------------------------
série=data[,4]
série=rev(série)
série[100]  # doit valoir 79.2
#---------------------------------------Bloc 3--------------------------------------
série.ts=ts(série,start=c(1982,1),frequency=12)
#----------------------------------------Bloc 4--------------------------------------
#série est simplement un vecteur
#série.ts est un objet specifique de R "time-series object" : serie chronologique indexee sur le temps
#-----------------------------------------Bloc 5--------------------------------------
sd(série.ts)
summary(série.ts)
#-----------------------------------------Bloc 6--------------------------------------
plot.ts(série.ts, main="Volume de fret - aeroports de Paris", xlab="Annee", ylab="Fret (millions de tonnes)")
#----------------------------------------Bloc 7--------------------------------------
boxplot(data[,4]~data[,3], main="Fret par annee", xlab="Annee", ylab="Fret (millions de tonnes)")
#-----------------------------------------Bloc 8--------------------------------------
for (i in 1982:2005){
  cat("annee :",i,"\n")
  print(summary(data[data[,3]==i,4]))
}
#----------------------------------------Bloc 9--------------------------------------
boxplot(data[,4]~data[,2], main="Fret par mois", xlab="Mois", ylab="Fret (millions de tonnes)")
#-----------------------------------------Bloc 10-------------------------------------
for (k in unique(data[,2])){
  cat("Mois :",k,"\n")
  print(summary(data[data[,2]==k,4]))
}

#------------------------- B - Phase de modelisation : modele affine ------------------------------------
# y_t = a*t + b
length(série)   # 288 mois d'etude
t=1:288
model1=lm(série~t)
summary(model1)
model1$coefficients
# a (pente, coefficient de t) : tendance moyenne du fret par mois -> positive = trafic croissant
# b (Intercept) : niveau theorique du fret au mois t=0

# 3. serie initiale + tendance ajustee
tendance1.ts=ts(model1$fitted.values,start=c(1982,1),frequency=12)
ts.plot(série.ts,tendance1.ts,
        lty=c(1,2), col=c("black","red"),
        main="Modele affine : serie et tendance ajustee",
        xlab="Annee", ylab="Fret (millions de tonnes)")
legend("topleft",c("serie","tendance affine"),col=c("black","red"),lty=c(1,2))

# 4. residus normalises
n=length(série)
s=sqrt((n-1)*var(model1$residuals)/n)
res1=model1$residuals/s
plot(res1, main="Residus normalises - modele affine", ylab="residus normalises", xlab="Index")
abline(h=c(-2,0,2),lty=c(2,1,2),col=c("red","black","red"))

#------------------------- C - Phase de modelisation : modele exponentiel ------------------------------------
# y_t = exp(a*t+b)  <=>  log(y_t) = a*t + b  -> modele affine sur log(serie)
log.série=log(série)
model2=lm(log.série~t)
model2$coefficients
# a, b : coefficients de la regression affine sur le log de la serie

# valeurs estimees : y_hat_t = exp(a*t+b), c-a-d exp(model2$fitted.values)
tendance2=exp(model2$fitted.values)
tendance2.ts=ts(tendance2,start=c(1982,1),frequency=12)
ts.plot(série.ts,tendance2.ts,lty=c(1,2), col=c("black","red"),
        main="Modele exponentiel : serie et tendance ajustee",
        xlab="Annee", ylab="Fret (millions de tonnes)")
legend("topleft",c("serie","tendance exponentielle"),col=c("black","red"),lty=c(1,2))

# 6. comparaison graphique affine / exponentiel
par(mfrow=c(1,2))
ts.plot(série.ts,tendance1.ts,lty=c(1,2),col=c("black","red"),main="Modele affine")
ts.plot(série.ts,tendance2.ts,lty=c(1,2),col=c("black","red"),main="Modele exponentiel")
par(mfrow=c(1,1))
# Les deux modeles se ressemblent visuellement ; le modele exponentiel epouse en general
# un peu mieux l'acceleration de la tendance en fin de periode si la serie s'emballe.

# 7. residus (sans transformation, residus2 = serie - tendance2), normalises
residus2=série-tendance2
n2=length(residus2)
s2=sqrt((n2-1)*var(residus2)/n2)
res2=residus2/s2
plot(res2, main="Residus normalises - modele exponentiel", ylab="residus normalises", xlab="Index")
abline(h=c(-2,0,2),lty=c(2,1,2),col=c("red","black","red"))

#------------------------- D - Modele quadratique ------------------------------------
# y_t = a*t^2 + b
t_carre=t^2
model3=lm(série~t_carre)
model3$coefficients
# a = coefficient de t_carre ; b = (Intercept)

tendance3=model3$fitted.values
tendance3.ts=ts(tendance3,start=c(1982,1),frequency=12)
ts.plot(série.ts,tendance3.ts,lty=c(1,2),col=c("black","red"),
        main="Modele quadratique : serie et tendance ajustee",
        xlab="Annee", ylab="Fret (millions de tonnes)")
legend("topleft",c("serie","tendance quadratique"),col=c("black","red"),lty=c(1,2))

residus3=série-tendance3
n3=length(residus3)
s3=sqrt((n3-1)*var(residus3)/n3)
res3=residus3/s3
plot(res3, main="Residus normalises - modele quadratique", ylab="residus normalises", xlab="Index")
abline(h=c(-2,0,2),lty=c(2,1,2),col=c("red","black","red"))

#------------------------- E - Selection du meilleur modele ------------------------------------
# 1. critere visuel : comparer les 3 ajustements cote a cote
par(mfrow=c(1,3))
ts.plot(série.ts,tendance1.ts,lty=c(1,2),col=c("black","red"),main="Affine")
ts.plot(série.ts,tendance2.ts,lty=c(1,2),col=c("black","red"),main="Exponentiel")
ts.plot(série.ts,tendance3.ts,lty=c(1,2),col=c("black","red"),main="Quadratique")
par(mfrow=c(1,1))

# 2. somme des residus carres (SCR) pour chaque modele
SCR1=sum(model1$residuals^2)
SCR2=sum(residus2^2)
SCR3=sum(residus3^2)
cat("SCR modele affine       :", SCR1, "\n")
cat("SCR modele exponentiel  :", SCR2, "\n")
cat("SCR modele quadratique  :", SCR3, "\n")

# 3. le modele avec la SCR la plus faible est juge le meilleur au sens de ce critere
noms_modeles=c("affine","exponentiel","quadratique")
cat("Meilleur modele (SCR minimale) :", noms_modeles[which.min(c(SCR1,SCR2,SCR3))], "\n")


#----------------------------------------------------------------------
#                      Exercice 2 : Decomposition manuelle - modele additif (ausbeer)
#----------------------------------------------------------------------
if (!requireNamespace("fpp2", quietly=TRUE)) install.packages("fpp2")  # fpp (v1) est archive sur CRAN
library(fpp2)

data(ausbeer)
timeserie_beer=tail(head(ausbeer,17*4+2),17*4-4)
plot(as.ts(timeserie_beer), main="Production trimestrielle de biere en Australie")

# 2. Detection de la tendance : moyenne mobile centree d'ordre 4 (frequence trimestrielle)
trend_beer=ma(timeserie_beer,order=4,centre=TRUE)
plot(as.ts(timeserie_beer), main="Serie et tendance (MA ordre 4)")
lines(trend_beer,col="red",lwd=2)

# 3. Serie sans tendance (modele additif : on soustrait la tendance)
detrend_beer=timeserie_beer-trend_beer
plot(as.ts(detrend_beer), main="Serie sans tendance (modele additif)")

# 4. Saisonnalite moyenne
m_beer=t(matrix(data=detrend_beer,nrow=4))
seasonal_beer=colMeans(m_beer,na.rm=TRUE)
plot(as.ts(rep(seasonal_beer,16)), main="Composante saisonniere (repetee)")

# 5. Bruit aleatoire = serie - tendance - saisonnalite
random_beer=timeserie_beer-trend_beer-seasonal_beer
plot(as.ts(random_beer), main="Residu (modele additif)")

# 6. Comparaison avec decompose()
ts_beer=ts(timeserie_beer,frequency=4)
decompose_beer=decompose(ts_beer,"additive")
plot(decompose_beer)

par(mfrow=c(2,1))
plot(as.ts(trend_beer),main="Tendance (calcul manuel)")
plot(decompose_beer$trend,main="Tendance (decompose)")
par(mfrow=c(1,1))
# les deux tendances sont identiques : decompose() applique en interne la meme moyenne
# mobile centree que le calcul manuel ci-dessus.


#----------------------------------------------------------------------
#                      Exercice 3 : Decomposition manuelle - modele multiplicatif (AirPassengers)
#----------------------------------------------------------------------
data(AirPassengers)
timeserie_air=AirPassengers
plot(as.ts(timeserie_air), main="Passagers aeriens mensuels (AirPassengers)")

# 2. Tendance : moyenne mobile centree d'ordre 12 (frequence mensuelle)
trend_air=ma(timeserie_air,order=12,centre=TRUE)
plot(as.ts(timeserie_air), main="Serie et tendance (MA ordre 12)")
lines(trend_air,col="red",lwd=2)

# 3. Serie sans tendance (modele multiplicatif : on divise par la tendance)
detrend_air=timeserie_air/trend_air
plot(as.ts(detrend_air), main="Serie sans tendance (modele multiplicatif)")

# 4. Saisonnalite moyenne
m_air=t(matrix(data=detrend_air,nrow=12))
seasonal_air=colMeans(m_air,na.rm=TRUE)
plot(as.ts(rep(seasonal_air,12)), main="Composante saisonniere (repetee)")

# 5. Bruit aleatoire = serie / (tendance * saisonnalite)
random_air=timeserie_air/(trend_air*seasonal_air)
plot(as.ts(random_air), main="Residu (modele multiplicatif)")

# 6. Comparaison avec decompose()
ts_air=ts(timeserie_air,frequency=12)
decompose_air=decompose(ts_air,"multiplicative")
plot(decompose_air)


#----------------------------------------------------------------------
#                      Exercice 4 : Moyenne mobile et decomposition (elecequip)
#----------------------------------------------------------------------
if (!requireNamespace("zoo", quietly=TRUE)) install.packages("zoo")
if (!requireNamespace("fpp2", quietly=TRUE)) install.packages("fpp2")
library(zoo)
library(fpp2)   # fournit le jeu de donnees elecequip

# 1. description
is.ts(elecequip)
start(elecequip); end(elecequip); frequency(elecequip); length(elecequip)
plot.ts(elecequip, main="Production europeenne d'equipements electriques (elecequip)")

# 2. lissage par moyenne mobile (package forecast)
ma3=ma(elecequip,order=3)
ma5=ma(elecequip,order=5)
ma7=ma(elecequip,order=7)
plot(elecequip, col="black", main="elecequip et moyennes mobiles")
lines(ma3,col="red")
lines(ma5,col="blue")
lines(ma7,col="cyan")
legend("topleft",c("original","ma3","ma5","ma7"),col=c("black","red","blue","cyan"),lty=1)

# 23. les extremites sont a NA car la fenetre de la moyenne mobile centree deborde des
# donnees disponibles aux deux bouts de la serie (pas assez de voisins pour centrer).

# 24. rollmean() du package zoo (equivalent, avec gestion explicite du remplissage)
ma3_zoo=rollmean(elecequip,k=3,fill=NA)
ma5_zoo=rollmean(elecequip,k=5,fill=NA)
ma7_zoo=rollmean(elecequip,k=7,fill=NA)

# 3. decomposition
decompose_elec_add=decompose(elecequip,"additive")
plot(decompose_elec_add)
decompose_elec_mult=decompose(elecequip,"multiplicative")
plot(decompose_elec_mult)

# 33. la composante de tendance est identique quel que soit le modele (elle ne depend
# que de la moyenne mobile) ; la composante saisonniere et le residu different en revanche :
# en unites absolues pour l'additif, en facteurs relatifs autour de 1 pour le multiplicatif.

# 34. pour juger si tendance+saison expliquent bien le signal, comparer visuellement
# l'amplitude du residu a celle de la serie d'origine (residu petit et sans structure
# apparente = bonne decomposition) :
par(mfrow=c(1,2))
plot(decompose_elec_add$random,main="Residu (additif)")
plot(decompose_elec_mult$random,main="Residu (multiplicatif)")
par(mfrow=c(1,1))
