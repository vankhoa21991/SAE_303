#----------------------------------------------------------------------
#                      TP01_SeriesChronologiques_PhaseExploratoire
#----------------------------------------------------------------------
#----------------------------------------------------------------------
#                      Exercice Tache solaires
#----------------------------------------------------------------------
#----------------------------------------question 1--------------------------------------
sun<-sunspots
is.ts(sun)
time(sun)
length(sun)
frequency(sun)
start(sun)
tsp(sun)

# Décrire les données 
# Sujet :  Monthly Sunspot Numbers, 1749–1983
#   Type de données : TS object 
#   Nombre d’entrées (nombre de lignes) : 2820
#   Pas de temps : 12
#   Début : 1749, 1
#   Fin : 1983, 12
  
#---------------------------------------question 2--------------------------------------
plot(sun, main="Taches solaires")
plot.ts(sun, main="Taches solaires")
#---------------------------------------question 3--------------------------------------
#décrire le graphique
# On observe une tendance à la hausse et une saisonalité
#---------------------------------------question 4--------------------------------------
require(graphics) #appel d’une librairie
madd<-decompose(sun, type = "additive", filter = NULL);plot(madd)
plot(madd)
#-----------------------------------------question 5--------------------------------------
Tendance=madd$trend
y = Tendance
x = time(Tendance)
reglin <- lm(Tendance~time(Tendance)) 
plot.ts(Tendance)
abline(reglin,col="red")
reglin 
# y= 0.10 x + -139.66
# on obtient un coefficient de 0.10,
# donc il y a une tendance à la hausse de 0.10 tache solaire par mois en plus depuis le debut de l'etude
#----------------------------------------question 6--------------------------------------
#Sur la duree de l'etude' : (2820 mois)
2820*0.10
#----------------------------------------question 7--------------------------------------
mmult<-decompose(sun,type="multiplicative", filter = NULL)
plot(mmult)


#----------------------------------------------------------------------
#                      Exercice (Volume de fret pour les aéroports de Paris)
#----------------------------------------------------------------------
#-----------------------  Phase exploratoire------------------------------------
#--------------------------------------question 1--------------------------------------
#library(readr) # not actually used below (read.table is base R); commented out because the package isn't installed here
data=read.table("../data/fret.txt",sep=";")
View(data)
data[1:10,]
#-----------------------------------------question 2--------------------------------------
série=data[,4]
série=rev(série)
série[100]
#---------------------------------------question 3--------------------------------------
série.ts=ts(série,start=c(1982,1),frequency=12)
#----------------------------------------question 4--------------------------------------
#série est simplement un vecteur
#série.ts est un objet specifique de R « time-séries object » il s’agit d’une série #chronologique indéxée sur le temps
#-----------------------------------------question 5--------------------------------------
sd(série.ts)
summary(série.ts)
#-----------------------------------------question 6--------------------------------------
plot.ts(série.ts)
#----------------------------------------question 7--------------------------------------
boxplot(data[,4]~+data[,3])
#-----------------------------------------question 8--------------------------------------
for (i in 1982:2005){
  cat("année :",i,"\n")
  print(summary(data[data[,3]==i,4]))
  }
#----------------------------------------question 9--------------------------------------
boxplot(data[,4]~data[,2])
#On pourrait ameliorer le graphique en organisant les abscisse selon la progression usuelle des mois de l’année et non l’ordre alphabetique
#-----------------------------------------question 10-------------------------------------
for (k in unique(data[,2])){ 
  cat("Mois :",k,"\n")
  print(summary( data[data[,2]==k,4]))
  }


#----------------------------------------------------------------------
#                      Exercice Ventes
#----------------------------------------------------------------------
#----------------------------------------question 1--------------------------------------
?BJsales  
#Marketing: sales per month; sales data with leading indicator
bj<-BJsales
is.ts(bj)
time(bj)
frequency(bj)
#---------------------------------------question 2--------------------------------------
plot(bj)
#----------------------------------------question 3--------------------------------------
#décrire le graphique
#----------------------------------------question 4--------------------------------------
require(graphics) #appel d’une librairie
madd<-decompose(bj, type = "additive", filter = NULL);
plot(madd)
# R a des difficulté a voir la saisonalité de la serie car l'indice de temps n'est pas clair