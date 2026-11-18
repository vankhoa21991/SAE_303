![](data:image/png;base64...)

DESCRIPTION ET PRÉVISION DE DONNÉES TEMPORELLES

SAE3.03

![](data:image/png;base64...)![](data:image/png;base64...)

![](data:image/png;base64...)

# Présentation de la SAE

## La tache

Un jeu de données temporelles est donné. Vous avez la charge de les présenter, les analyser, les décomposer et proposer une prédiction.

## Etapes clés

1. Management de projet
   1. Diagramme de Gantt de votre progression sur 10h (par tranche de 2 heures)
   2. Organisation du groupe :
      1. Répartition des rôles
      2. Espace de travail en commun

2. Faire une recherche bibliographique pour voir si la série ou une série similaire n’a pas été traitée précédemment par quelqu’un d’autre

3. Présenter et contextualiser les données

Source des données, période d’étude considérée, unité des variables, présence d’une saisonnalité, ...

Optionnel : essayer de faire une carte de votre zone/lieu étude par rapport à une région du monde

4. Explorer des données (graphiques ou tableaux avec commentaires)

* Descripteurs statistiques
* Visualisation à différents pas de temps (journalier, mensuel, annuel)
* Dataviz visualisation de la série sous des formes originales (radial line graph ou autre)
* Calculer les fonction ACF (autocorrélation) et d’autocorrélation partielle PACF (optionnel)

5.Tests sur les séries (graphiques ou tableaux avec commentaires) (optionnel)

* Test de stationnarité (test augmenté de Dickey-Fuller)
* Test de tendance
* Test de Pettit pour tester un changement de tendance centrale
* Autres.

6. Choisir un modèle de décomposition de la série (modèle additif ou modèle multiplicatif), faire apparaître la tendance et, le cas échéant, calculer les coefficients saisonniers puis déterminer la série corrigée des variations saisonnières ;

7. Valider le modèle de décomposition de la série et repérer les valeurs mal ajustées par le modèle en analysant les résidus (graphiques ou tableaux avec commentaires)

8. Prédire

Effectuer des prévisions à court terme par

* Une méthode adaptée (modélisation paramétrique de la tendance avec ajout des coefficients saisonniers) ;
* Une méthode de lissage
* Optionnel : Une modélisation via un modèle autorégressif (AR, MA, ARMA, ARIMA, SARIMA, les sorties des fonctions ACF and PACF vous aident à décider du modèle de prédiction
* Optionnel : une autre méthode ou une méthode de machine learning.

## Groupes & Outils

Groupes de 2 personnes

Outils au choix, mais conseillé R ou Python

## Livrables

Temps imparti : 10h

Vous devez rédiger un rapport sur le travail effectué. Le rapport doit être simple, et sa structure peut suivre les points principaux présentés dans les "étapes clés".

La longueur ne doit pas dépasser 12 pages.

Les codes doivent figurer en annexes et ne comptent pas dans les 12 pages

Livrables : rapport et badge Date limite 2026-01-XX 23h59 au plus tard. Le rapport et le badge associé à la SAE doivent être déposés sur Moodle au format PDF. Le serveur est ouvert dès le 2026-01-10

Nom1\_Nom2\_Nom3\_rapport\_ SAE303.pdf

Nom\_Badge\_SAE303.pdf

# Jeux de données avec saisonnalité

## Données environnementales : températures à Nottingham, UK

### Description

Un objet de série chronologique contenant les températures moyennes de l'air au château de Nottingham en degrés Fahrenheit pendant 20 ans.

nottem\_ts = nottem

### Source & References

Anderson, O. D. (1976) Time Series Analysis and Forecasting: The Box-Jenkins approach. Butterworths. Series R.

## Données environnementales : débits de la rivière Nil

### Description

Mesures du débit annuel du Nil à Assouan (anciennement Assuan), 1871-1970, en 108 m3 avec un point de changement apparent vers 1898 (Cobb (1978), Tableau 1, p.249).

nile\_ts = Nile

### Source & References

Durbin, J. and Koopman, S. J. (2001). Time Series Analysis by State Space Methods. Oxford University Press.

Balke, N. S. (1993). Detecting level shifts in time series. Journal of Business and Economic Statistics, 11, 81–92. doi:10.2307/1391308.

Cobb, G. W. (1978). The problem of the Nile: conditional solution to a change-point problem. Biometrika 65, 243–51. doi:10.2307/2335202.

## Données astronomie : nombre mensuel de taches solaires de 1790 à 1970

### Description

Nombre mensuel de taches solaires, selon le World Data Center, alias SIDC. Il s'agit de la version des données qui sera occasionnellement mise à jour lorsque de nouveaux comptages seront disponibles.

sunspot\_ts = sunspot.month

### References

WDC-SILSO, Solar Influences Data Analysis Center (SIDC), Royal Observatory of Belgium, Av. Circulaire, 3, B-1180 BRUSSELS Currently at [<u>http://www.sidc.be/silso/datafiles</u>](http://www.sidc.be/silso/datafiles)

## Données environnementales : données de pluies

### Description

Données de pluies journalières à Boulder, Colorado, USA, de 1948 à 2013

Télécharger le fichier à l’adresse suivante : [<u>https://raw.githubusercontent.com/ef2020/TextFiles/master/805333-precip-daily-1948-2013.csv</u>](https://raw.githubusercontent.com/ef2020/TextFiles/master/805333-precip-daily-1948-2013.csv)

boulder\_precip <- read.csv(file = "data/boulder-precip.csv" , na.strings = 999.99)

precip\_boulder$DATE <- as.POSIXct(precip\_boulder$DATE,format = "%Y%m%d %H:%M")

#convertir au format timeseries de R

install.packages("xts");library(xts)

precip\_boulder\_ts <- xts(x = precip\_boulder$HPCP,order.by = precip\_boulder$DATE)

### Source & References

Pas vraiment de source. Surement, l’équivalent de Météo-France au Etats unis qui a relevé les données

## Données environnementales : données de CO2

### Description

Le fichier de données co2 contenu dans R contient les concentrations mensuelles en CO2 (en parties par million) à proximité du volcan Mauna Loa, Hawaï, USA, de 1959 à 1997.

co2\_ts = co2

### Source & References

Keeling, C. D. and Whorf, T. P., Scripps Institution of Oceanography (SIO), University of California, La Jolla, California USA 92093-0220. [<u>https://scrippsco2.ucsd.edu/data/atmospheric\_co2/</u>](https://scrippsco2.ucsd.edu/data/atmospheric_co2/) .

Cleveland, W. S. (1993) Visualizing Data. New Jersey: Summit Press.

## Données sociétales : accidentés de la route, UK

### Description

UKDriverDeaths est une série chronologique donnant les totaux mensuels des conducteurs de voitures en Grande-Bretagne tués ou gravement blessés de janvier 1969 à décembre 1984. Le port obligatoire de la ceinture de sécurité a été introduit le 31 janvier 1983. On s'intéresse ici au changement éventuel de régime dans les données UKDriverDeaths suite au changement dans la législation en janvier 1983

UKDriverDeaths \_ts = UKDriverDeaths

### Source & References

Harvey, A.C. (1989). Forecasting, Structural Time Series Models and the Kalman Filter. Cambridge University Press, pp. 519–523.

Durbin, J. and Koopman, S. J. (2001). Time Series Analysis by State Space Methods. Oxford University Press. http://www.ssfpack.com/dkbook/

Harvey, A. C. and Durbin, J. (1986). The effects of seat belt legislation on British road casualties: A case

## Données sociétales : accidentés de la route, USA

### Description

Une série chronologique donnant les totaux mensuels des décès accidentels aux USA (1969-1984)

USAccDeaths\_ts = USAccDeaths

### Source & References

P. J. Brockwell and R. A. Davis (1991) Time Series: Theory and Methods. Springer, New York.

## Données sociétales : consommation de gaz, UK

### Description

Consommation trimestrielle de gaz au Royaume-Uni de 1960 (trimestre 1) à 1986 (trimestre 4)

UKgas\_ts = UKgas

### Source & References

Durbin, J. and Koopman, S. J. (2001). *Time Series Analysis by State Space Methods*. Oxford University Press.

## Données de médecine : décès mensuels dus à des maladies pulmonaires

### Description

Trois séries chronologiques donnant les décès mensuels dus à des maladies pulmonaires (bronchite, à l'emphysème et à l'asthme) au Royaume-Uni, 1974-1979, pour les deux sexes (*ldeaths*).

ldeaths\_ts = ldeaths

### Source & References

P. J. Diggle (1990) Time Series: A Biostatistical Introduction. Oxford, table A.3

## Données d’économie : ventes de produits anti-diabète en Australie (1991-2008)

### Description

Dépenses mensuelles du gouvernement (millions de dollars) dans le cadre du Pharmaceutical Benefit Scheme pour les produits relevant du code ATC A10 (produits anti-diabète), telles qu'enregistrées par l'Australian Health Insurance Commission. Juillet 1991 - juin 2008

library(fpp2)

data\_ts = a10

### Source & References

Source: Medicare Australia

## Données industrielles : production mensuelle de gaz en Australie : 1956-1995

### Description

Production mensuelle de gaz australien (1956–1995).

library("forecast")

gas\_ts = gas

### Source & References

Source : bureau des statistiques australien

Australian Bureau of Statistics.

BIBLIOGRAPHIE

Aragon, Y., Séries temporelles avec R, Collection Pratique R, EDP sciences, ISBN : 978-2-7598-1779-5, 2011

Box, G.E. P., Jenkins G. M., Reinsel G.C.. *Time series analysis*. Wiley Series in Probability and Statistics. John Wiley & Sons, Inc., Hoboken, NJ, fourth édition, 2008

Chatfield, C.. *The Analysis of Time Series, an Introduction*. Fourth edition. Chapman & Hall, 1989

Goldfarb, B.,Pardoux, C.. Introduction à la méthode statistique,Dunod, 2011

Hamilton, J.D. *Time series analysis*. Princeton University Press, Princeton, NJ, 1994

Lagnoux, A.. *Statistique pour les Sciences Humaines II*. Disponible à l’adresse https://perso.math.univ-toulouse.fr/lagnoux/enseignements/.

# Jeux de données sans saisonnalité PAS AU PROGRAMME DES BUT2

## Données d’économie : données des taux d’intérêts mensuels américains

### Description

Ventes totales de vin par les viticulteurs australiens en bouteilles de moins de 1 litre de janvier 1980 à Août 1994

library("forecast")

wineind\_ts = wineind

### Source & References

[<u>Board of Governors of the Federal Reserve System</u>](http://www.federalreserve.gov/)

## Données d’économie : données des taux d’intérêts mensuels américains

### Description

Le taux des fonds fédéraux est le taux d'intérêt auquel les institutions de dépôt échangent des fonds fédéraux (soldes détenus dans les banques de la Réserve fédérale) entre elles pendant la nuit. Lorsqu'un établissement de dépôt dispose de soldes excédentaires sur son compte de réserve, il prête à d'autres banques qui ont besoin de soldes plus importants. En termes plus simples, une banque disposant d'un excédent de liquidités, que l'on appelle souvent "liquidité", prêtera à une autre banque qui a besoin d'augmenter rapidement ses liquidités. Le taux que l'établissement emprunteur paie à l'établissement prêteur est déterminé entre les deux banques ; le taux moyen pondéré de tous ces types de négociations s'appelle le taux effectif des fonds fédéraux. Le taux effectif des fonds fédéraux est essentiellement déterminé par le marché mais est influencé par la Réserve fédérale par le biais des opérations d'open market pour atteindre l'objectif du taux des fonds fédéraux.

Télécharger le fichier à l’adresse suivante : [<u>https://fred.stlouisfed.org/series/FEDFUNDS</u>](https://fred.stlouisfed.org/series/FEDFUNDS)

fedfunds<-read.csv("../input/FEDFUNDS.csv") *#Read the file from the data environment*

head(fedfunds)

ffr<-ts(fedfunds[,-1],start=c(1954,7),frequency=12)

head(ffr) *#Look at first few entries again*

### Source & References

[<u>Board of Governors of the Federal Reserve System</u>](http://www.federalreserve.gov/)

## Série du BTC et/ou du Nasdac

## Données de valeur boursières : le DAX (Allemagne), le SMI (Suisse) et FTSE (Royaume-Uni)

L'ensemble de données EuStockMarkets contient les cours de clôture quotidiens (à l'exception des week-ends/jours fériés) de quatre bourses européennes : le DAX (Allemagne), le SMI (Suisse), le CAC (France) et le FTSE (Royaume-Uni). Ici on s’interesse au FTSE.

library(readr)

FTSE\_ts\_data <- EuStockMarkets[,4]

## Uspop

Population aux USA

## Données de valeur boursières : cours quotidiens de l'or

library(fpp2)

gold\_ts = gold

Cours quotidiens de l'or le matin en dollars US. 1er janvier 1985 - 31 mars 1989

Wickham, H. (2016). ggplot2: Elegant graphics for data analysis (2nd ed). Springer.

Attention ce n’est pas au format time-series

## Série maladie : covid ?

## Données biologie : dendrologie

## Données environnementales : données du lac Huron

### Description

Mesures annuelles du niveau, en pieds, du lac Huron 1875-1972.

co2\_ts = co2

### Source & References

Brockwell, P. J. and Davis, R. A. (1991). Time Series and Forecasting Methods. Second edition. Springer, New York. Series A, page 555.

Brockwell, P. J. and Davis, R. A. (1996). Introduction to Time Series and Forecasting. Springer, New York. Sections 5.1 and 7.6.