#!/usr/bin/env python3
"""SAE 3.03 — génère un énoncé d'exercice personnalisé par groupe (promo 2026).

Sortie : SAE 3.03/2026/<CLASSE>_G<n>_<noms>.md  +  2026/README.md (index)
Utilisation : python3 scripts/make_group_exercises.py
"""
from pathlib import Path
import re

OUT = Path(__file__).resolve().parent.parent / "2026"

# ---------------------------------------------------------------- jeux de données
# access : comment charger la série ; cut : découpage train/test ; ctx/pitfall/ang : spécifiques.
D = {
 "EURO": dict(
  titre="Indice boursier FTSE (EuStockMarkets)", freq="quotidien (jours ouvrés, 260/an)",
  acces="R : `ftse <- EuStockMarkets[, \"FTSE\"]` (package datasets, 1991–1998, 1860 obs.)",
  cut="train = jusqu'à fin 1997 ; test = 1998 (comme le CAC40 du TP03).",
  ctx="Série financière : que représente le FTSE 100 ? Quels événements marquent 1991–1998 (crise du SME 1992, crise asiatique 1997) ?",
  saison="Pas de saisonnalité calendaire attendue ; vérifier tout de même sur l'ACF.",
  piege="Série non stationnaire (marche aléatoire probable) : un ADF sur le niveau ne rejettera pas la racine unitaire ; travailler aussi sur les rendements $r_t=\\ln(x_t/x_{t-1})$.",
  angle="Comparer la prévision LES/Holt sur le niveau avec la prévision naïve « dernière valeur ». Le lissage fait-il mieux qu'une marche aléatoire ? Commenter.",
  modele="Pas de saisonnalité : décomposition = tendance + résidus seulement ; justifier pourquoi on ne calcule pas de coefficients saisonniers (ou les montrer proches de 0).",
 ),
 "MED": dict(
  titre="Décès mensuels par maladies pulmonaires — Royaume-Uni (mdeaths + fdeaths)", freq="mensuel (période 12)",
  acces="R : `mdeaths`, `fdeaths` (datasets, janv. 1974 – déc. 1979, 72 obs. chacune) ; `ldeaths = mdeaths + fdeaths`.",
  cut="train = 1974–1977 ; test = 1978–1979 (24 mois). Série courte : seulement 6 cycles.",
  ctx="Bronchite, emphysème, asthme : pourquoi les décès culminent-ils en hiver ? Quel événement sanitaire explique le pic de début 1976 ?",
  saison="Saisonnalité annuelle forte, tendance faible.",
  piege="Seulement 72 points : les coefficients saisonniers reposent sur 6 valeurs par mois — discuter leur fiabilité. Le pic de 1976 est-il une valeur aberrante ou un phénomène réel ?",
  angle="Ce groupe traite **mdeaths** (hommes) et **fdeaths** (femmes) séparément puis compare leurs coefficients saisonniers (le profil est-il le même ?). Le groupe VCOD n°6 traite `ldeaths` (total).",
  modele="Test des 3 méthodes de choix (bande, Buys-Ballot, profils) ; additif attendu mais à démontrer.",
 ),
 "LDEATHS": dict(
  titre="Décès mensuels par maladies pulmonaires — Royaume-Uni (ldeaths)", freq="mensuel (période 12)",
  acces="R : `ldeaths` (datasets, janv. 1974 – déc. 1979, 72 obs.).",
  cut="train = 1974–1977 ; test = 1978–1979 (24 mois).",
  ctx="Bronchite, emphysème, asthme : mécanismes de la surmortalité hivernale ; épidémie de grippe 1975-76.",
  saison="Saisonnalité annuelle forte, pas de tendance nette.",
  piege="Série très courte (6 cycles) : l'ARIMA saisonnier est fragile, la décomposition aussi. Dire explicitement ce que 6 cycles permettent ou non de conclure.",
  angle="Comparer décomposition additive vs multiplicative sur la **même** série avec un critère chiffré (écart-type des résidus, ACF des résidus), pas seulement visuel.",
  modele="Additif vs multiplicatif à trancher numériquement.",
 ),
 "SUNM": dict(
  titre="Taches solaires — nombre mensuel (sunspots)", freq="mensuel, mais cycle d'environ 11 ans (≈ 132 mois)",
  acces="R : `sunspots` (datasets, janv. 1749 – déc. 1983, 2820 obs.).",
  cut="train = jusqu'à 1973 ; test = 1974–1983 (un cycle solaire entier).",
  ctx="Qu'est-ce qu'une tache solaire ? Cycle de Schwabe (~11 ans), nombre de Wolf, minimum de Maunder.",
  saison="**Pas** de saisonnalité annuelle : un pseudo-cycle de période variable (9–14 ans).",
  piege="`decompose()` avec frequency = 12 est un **contresens** (le TP01 le fait : à critiquer). La période n'est ni 12 ni constante. Les coefficients 'saisonniers' mensuels n'ont pas de sens physique.",
  angle="Prouver par l'ACF que le vrai cycle est ≈ 130 mois, refaire la décomposition avec cette période (ou passer en annuel), et comparer avec celle du TP01.",
  modele="Série positive à variance croissante avec le niveau : tester log ou Box-Cox ; moyenne mobile d'ordre 132 (ou 133).",
 ),
 "SUNA": dict(
  titre="Taches solaires — nombre annuel (sunspot.year)", freq="annuel",
  acces="R : `sunspot.year` (datasets, 1700–1988, 289 obs.).",
  cut="train = 1700–1958 ; test = 1959–1988 (30 ans, ≈ 3 cycles).",
  ctx="Cycle de Schwabe ~11 ans, minimum de Maunder (1645-1715), usage en météo spatiale.",
  saison="Annuel donc pas de saisonnalité infra-annuelle ; pseudo-cycle ≈ 11 ans à caractériser par l'ACF.",
  piege="Lisser avec HoltWinters(gamma=FALSE) ne capturera pas le cycle : la prévision à 30 ans sera plate/inefficace. Le montrer, l'expliquer, puis proposer mieux (AR d'ordre ≥ 9 par ex.).",
  angle="Ce groupe travaille sur la série **annuelle** (le groupe EMS n°4 sur la mensuelle). Comparer le choix AR par ACF/PACF avec la prévision par lissage sur test de 30 ans.",
  modele="Pas de saisonnalité ; décomposition tendance seule + AR pour le cycle.",
 ),
 "UKGAS": dict(
  titre="Consommation de gaz au Royaume-Uni (UKgas)", freq="trimestriel (période 4)",
  acces="R : `UKgas` (datasets, 1960 T1 – 1986 T4, 108 obs., millions de thermies).",
  cut="train = 1960–1984 ; test = 1985–1986 (8 trimestres).",
  ctx="Chauffage au gaz domestique ; mise en service du gaz de la mer du Nord (années 1960-70), choc pétrolier de 1973.",
  saison="Saisonnalité trimestrielle forte (pic hiver) ET amplitude qui explose avec le niveau.",
  piege="Modèle **multiplicatif** clair (ou log). Attention : 4 coefficients seulement, de moyenne 1 (multiplicatif). Rupture de tendance vers 1970 : un seul modèle linéaire global est-il adapté ?",
  angle="Détecter la rupture avec Pettitt, puis comparer droite de tendance globale vs tendance estimée après la rupture seulement pour la prévision.",
  modele="Multiplicatif à justifier par les 3 méthodes ; comparer avec additif sur log(UKgas).",
 ),
 "GAS": dict(
  titre="Production mensuelle de gaz en Australie (gas)", freq="mensuel (période 12)",
  acces="R : `forecast::gas` (janv. 1956 – août 1995, 476 obs.).",
  cut="train = jusqu'à 1993 ; test = 1994 – août 1995 (20 mois).",
  ctx="Production industrielle de gaz naturel en Australie : essor après la découverte de gisements (années 1960-70), contexte énergétique.",
  saison="Très forte saisonnalité qui **change d'amplitude** (quasi nulle avant 1970, énorme après).",
  piege="Pas de tendance linéaire : croissance accélérée. Variance non constante → log ou modèle multiplicatif obligatoire. Rupture vers 1970 → Pettitt.",
  angle="Comparer la prévision Holt-Winters multiplicatif brut vs additif sur log(gas) (retransformer avec précaution).",
  modele="Multiplicatif ; discuter si les coefficients saisonniers sont constants sur 40 ans (non !).",
 ),
 "RAIN": dict(
  titre="Précipitations journalières à Boulder, Colorado, USA (1948–2013)", freq="journalier (période ≈ 365) — travail principal sur les totaux mensuels",
  acces="CSV : `data/boulder-precip.csv` (téléchargé depuis https://raw.githubusercontent.com/ef2020/TextFiles/master/805333-precip-daily-1948-2013.csv). Colonne `HPCP` en pouces, `999.99` = valeur manquante ; **plusieurs relevés par jour → sommer par date** ; jours absents du fichier = jours secs (0).",
  cut="Travail sur les totaux mensuels (pouces) : train = 1948-08 → 2003-12 ; test = 2004-01 → 2013-12 (120 mois).",
  ctx="Station COOP 050843 « BOULDER 2 CO US » (≈ 1650 m d'altitude), climat semi-aride : ~82 % de jours secs, pluviométrie médiane ≈ 17 po/an. Pourquoi la saisonnalité est-elle bimodale (pic au printemps + bosse du monsoon d'été) ?",
  saison="Saisonnalité annuelle forte sur les totaux mensuels (pic en mai, creux en hiver) ; série journalière à pics très irréguliers.",
  piege="Série journalière avec ~82 % de zéros : ne pas décomposer/prévoir directement le quotidien avec les outils classiques — passer aux totaux mensuels. Modèle multiplicatif impossible (mois nuls) : additif. Ne pas interpréter un ADF sur le quotidien comme « stationnaire » sans regarder l'échelle.",
  angle="Proportion de jours secs par mois (climatologie) et stabilité de la climatologie mensuelle par décennie ; ADF / Mann-Kendall / Pettitt sur les totaux mensuels ET annuels : les conclusions sont-elles les mêmes ?",
  modele="Additif sur les totaux mensuels (période 12) ; comparer décomposition / ETS / SARIMA(0,1,1)×(0,1,1) au naïf saisonnier sur 120 mois.",
 ),
 "CO2": dict(
  titre="CO₂ atmosphérique à Mauna Loa (co2)", freq="mensuel (période 12)",
  acces="R : `co2` (datasets, janv. 1959 – déc. 1997, 468 obs., ppm).",
  cut="train = 1959–1990 ; test = 1991–1997 (7 ans). Pour aller plus loin : comparer avec les données Scripps jusqu'à aujourd'hui.",
  ctx="Courbe de Keeling : cycle de la photosynthèse hémisphère nord, émissions fossiles, accord de Paris.",
  saison="Tendance croissante (légèrement convexe) + saisonnalité annuelle d'amplitude constante → additif.",
  piege="C'est l'exemple vu en TP : ne pas se limiter à `decompose`. Tendance convexe : droite insuffisante, tester un polynôme de degré 2 ; Holt-Winters additif attendu performant — vérifier sur le test.",
  angle="Extrapoler jusqu'en 2025 avec votre meilleur modèle, puis confronter à la valeur réelle connue (~420 ppm) : quel est l'écart et pourquoi ?",
  modele="Additif ; comparer tendance linéaire vs quadratique par les résidus.",
 ),
 "DRV": dict(
  titre="Conducteurs tués ou gravement blessés au Royaume-Uni (UKDriverDeaths)", freq="mensuel (période 12)",
  acces="R : `UKDriverDeaths` (datasets, janv. 1969 – déc. 1984, 192 obs.).",
  cut="train = 1969–1982 ; test = 1983–1984 (24 mois).",
  ctx="Accidents de la route au Royaume-Uni ; **loi sur le port obligatoire de la ceinture, 31 janvier 1983**, crise pétrolière 1973-74.",
  saison="Saisonnalité annuelle (pic en hiver/fin d'année) + tendance à la baisse + chute en 1983.",
  piege="Le test (1983-84) est **après la rupture** de la loi : le modèle appris sur le train va sur-prévoir. À exploiter, pas à cacher.",
  angle="Pettitt doit retrouver ≈ janv. 1983. Quantifier l'effet de la loi : (prévision sans loi) − (observé). Que vaut cette estimation ?",
  modele="Additif probable ; 2 tendances (avant/après) à discuter.",
 ),
 "NILE": dict(
  titre="Débit annuel du Nil à Assouan (Nile)", freq="annuel",
  acces="R : `Nile` (datasets, 1871–1970, 100 obs., 10⁸ m³).",
  cut="train = 1871–1950 ; test = 1951–1970 (20 ans).",
  ctx="Fleuve du Nil, mesures à Assouan ; barrages (ancien barrage d'Assouan 1902, haut barrage 1970) ; crues.",
  saison="Annuel : pas de saisonnalité. Rupture de niveau documentée vers **1898**.",
  piege="Série classique de test de **Pettitt** (rupture de moyenne ≈ 1898). Ajuster un seul modèle global est une erreur : séparer avant/après.",
  angle="Pettitt + ADF avant/après rupture. Prévoir avec LES appris uniquement sur la période post-rupture, comparer avec un LES sur toute la série.",
  modele="Pas de saisonnalité, tendance = changement de niveau (escalier), pas une droite.",
 ),
 "NOTT": dict(
  titre="Température moyenne mensuelle à Nottingham (nottem)", freq="mensuel (période 12)",
  acces="R : `nottem` (datasets, janv. 1920 – déc. 1939, 240 obs., °F).",
  cut="train = 1920–1936 ; test = 1937–1939 (36 mois).",
  ctx="Climat tempéré océanique ; Nottingham Castle Station ; température moyenne de l'air. (*Sujet « 2.5 environnement » : à confirmer avec l'enseignant.*)",
  saison="Saisonnalité annuelle très forte et stable, pas de tendance.",
  piege="Saisonnalité **additive** (température, pas multiplicatif : valeurs proches de zéro/négatives possibles en °C). Une prévision par coefficients saisonniers est quasi parfaite : la vraie question est la qualité des résidus.",
  angle="Après CVS, la série résiduelle est-elle un bruit blanc ? Tests de Ljung-Box, ACF résidus, normalité ; conclure sur ce qui reste à modéliser (AR faible ?).",
  modele="Additif ; les coefficients sont interprétables physiquement (°F au-dessus/dessous de la moyenne annuelle).",
 ),
 "ECO": dict(
  titre="Données économiques — FEDFUNDS (taux directeur de la Fed)", freq="mensuel",
  acces="Téléchargement FRED : https://fred.stlouisfed.org/series/FEDFUNDS (CSV) ; à lire en R avec `read.csv` puis `ts(x, start=c(1954,7), frequency=12)`. (*Sujet « 10 données économiques » ambigu : FEDFUNDS choisi car dans l'énoncé — à confirmer avec le groupe.*)",
  cut="train = jusqu'à fin 2018 ; test = 2019 – 2022 (observer la rupture COVID et la remontée des taux 2022).",
  ctx="Politique monétaire de la Réserve fédérale : taux, inflation, crises 1980, 2008, 2020.",
  saison="Pas de saisonnalité attendue ; tendances par régimes (hausse jusqu'en 1981, baisse, zéro, remontée).",
  piege="Plusieurs ruptures : un seul modèle de tendance est faux. Taux plancher à ≈ 0 : les prévisions peuvent devenir négatives (absurde économiquement).",
  angle="Segmenter par Pettitt (récursif) et mesurer l'échec des méthodes sur le test 2019-2022 : que valent les prévisions en période de rupture ?",
  modele="Pas de modèle saisonnier ; Holt ou LES sur régime récent.",
 ),
 "R": dict(
  titre="Transports publics en France — régularité des trains (Option R)", freq="mensuel (période 12)",
  acces="Fichier `data/kaggle_raw/R_gatandubuc-public-transport-traffic-data-in-france/Regularities_by_liaisons_Trains_France.csv` (colonne Period ; 66 mois, janv. 2015 – juin 2020).",
  cut="train = 2015–2018 ; test = 2019 – mi-2020. Attention : COVID dans le test → à traiter explicitement.",
  ctx="SNCF : TGV/Intercités, retards, grèves (2018, déc. 2019), COVID mars 2020.",
  saison="Tendance significative, saisonnalité faible (η²≈0,13 sur la métrique par défaut) : à vérifier sur **votre** métrique et **votre** liaison.",
  piege="Choisir **une seule** liaison + **une** métrique (retard moyen, % retards > 15 min, causes externes…). Valeurs manquantes par liaison ; le 'trend' peut être un artefact de couverture des données.",
  angle="Chercher les ruptures (Pettitt) et les relier à des événements datés (grèves, COVID) ; analyser les résidus comme événements sociaux.",
  modele="Si la saisonnalité est faible, justifier de ne garder que tendance + lissage (Holt) ; sinon HW additif.",
 ),
 "L": dict(
  titre="Météo horaire multi-villes — température (Option L)", freq="horaire → agrégé mensuel (période 12)",
  acces="Fichier `data/kaggle_raw/L_selfishgene-historical-hourly-weather-data/temperature.csv` (colonnes = villes, 2012-10 → 2017-11, en kelvins).",
  cut="train = 2012-10 → 2016-11 ; test = 2016-12 → 2017-11 (un cycle annuel complet).",
  ctx="Choisir **une ville** et la documenter (climat, latitude). Convertir K → °C.",
  saison="Saisonnalité annuelle très forte (η²≈0,96), pas de tendance significative (≈ 5 ans).",
  piege="Valeurs manquantes horaires à traiter avant l'agrégation ; seulement 5 ans → 5 cycles ; ne pas conclure à un 'réchauffement' sur 5 ans.",
  angle="Montrer l'effet de la granularité : cycle jour/nuit (horaire), semaine (rien), année (mensuel). Comparer deux villes sur leurs coefficients saisonniers (amplitude continentale vs océanique).",
  modele="Additif (°C) ; HW additif sans tendance (β=FALSE) à comparer au HW complet.",
 ),
 "A": dict(
  titre="Ventes de champagne (Option A)", freq="mensuel (période 12)",
  acces="Fichier `data/monthly_champagne_sales.csv` (janv. 1964 – sept. 1972, 105 obs.). Déjà traité dans `scripts/analyse_champagne.py` : **ne pas se contenter de ce script**.",
  cut="train = 1964–1970 ; test = 1971 – sept. 1972 (21 mois).",
  ctx="Perrin Frères ; vente de champagne : pic de fin d'année (fêtes) ; contexte économique français 1964-72.",
  saison="Saisonnalité forte (η²≈0,84) + tendance croissante significative.",
  piege="Amplitude qui croît légèrement : additif ou multiplicatif ? Les 3 méthodes du cours donnent-elles le même verdict ? Le dataset dit 105 obs., pas 108 : documenter l'écart.",
  angle="Trancher additif/multiplicatif avec les 3 méthodes ; puis HW additif vs multiplicatif sur le test : la méthode de choix a-t-elle bien prédit le meilleur modèle ?",
  modele="Débat additif/multiplicatif central.",
 ),
}

# ---------------------------------------------------------------- groupes
G = [
 ("EMS", 1, "Drackle / Hachemi", "ECO"), ("EMS", 2, "Dione / Gouem", "MED"),
 ("EMS", 3, "Diop / Carien", "R"), ("EMS", 4, "Casares Bello / Sabatier", "SUNM"),
 ("EMS", 5, "Diallo / Kouyate", "UKGAS"), ("EMS", 6, "Obame Ndong Ntougou / Houngli", "GAS"),
 ("EMS", 7, "Accrombessi / Kare", "RAIN"), ("EMS", 8, "Meye-Meye / Sawadogo", "CO2"),
 ("VCOD", 1, "Ayral / Furgal", "DRV"), ("VCOD", 2, "Di Scala / Milazzo Guilhou", "SUNA"),
 ("VCOD", 3, "Pujal / Marquier", "NILE"), ("VCOD", 4, "Nzau Ngoy / Livernet", "L"),
 ("VCOD", 5, "Rafaly / Rabat", "A"), ("VCOD", 6, "Lokossa / Chaabani", "LDEATHS"),
 ("VCOD", 7, "Bach / Majde", "NOTT"),
]
SUJET = {  # texte du tableau tel que saisi par les étudiants
 ("EMS",1):"10 donne economic", ("EMS",2):"9 donnee de medecine", ("EMS",3):"transports public en France",
 ("EMS",4):"nombre mensuel de taches solaire", ("EMS",5):"2.8 Consommation de gaz UK",
 ("EMS",6):"Production mensuelle de gaz en Australie", ("EMS",7):"Données de pluie",
 ("EMS",8):"Données de CO2",
 ("VCOD",1):"2.6 accidents de la route UK", ("VCOD",2):"2.3 tache solaire", ("VCOD",3):"2.2 débit du Nil",
 ("VCOD",4):"Météo et ville option L", ("VCOD",5):"Vente de champagne",
 ("VCOD",6):"2.9 décès mensuels maladies pulmonaires", ("VCOD",7):"2.5 données environnementales",
}

def slug(s): return re.sub(r"[^A-Za-z0-9]+", "-", s.replace("é", "e")).strip("-")

SUBJ = [  # (fichier, titre du sujet, [variantes])
 ("01_Economie_FEDFUNDS", "Données économiques", ["ECO"]),
 ("02_Medecine_Deces_pulmonaires", "Médecine — décès pulmonaires (UK)", ["MED", "LDEATHS"]),
 ("03_Transports_publics_France", "Transports publics en France", ["R"]),
 ("04_Taches_solaires", "Taches solaires", ["SUNM", "SUNA"]),
 ("05_Gaz_UK_UKgas", "Consommation de gaz UK", ["UKGAS"]),
 ("06_Gaz_Australie", "Production de gaz en Australie", ["GAS"]),
 ("07_Pluie_Boulder", "Données de pluie", ["RAIN"]),
 ("08_CO2_Mauna_Loa", "Données de CO2", ["CO2"]),
 ("09_Accidents_route_UK", "Accidents de la route UK", ["DRV"]),
 ("10_Debit_du_Nil", "Débit du Nil", ["NILE"]),
 ("11_Meteo_ville_OptionL", "Météo et ville (option L)", ["L"]),
 ("12_Champagne_OptionA", "Ventes de champagne", ["A"]),
 ("13_Environnement_Temperature_Nottingham", "Données environnementales", ["NOTT"]),
]
KEY_OF = {g[3]: g for g in G}

def body(key):
    d = D[key]
    return f"""**Série** : {d['titre']} — pas de temps : {d['freq']}
**Accès aux données** : {d['acces']}
**Découpage train/test imposé** : {d['cut']}

### 1. Contexte à documenter (étapes 2-3)
{d['ctx']}
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : {d['saison']}

### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : {d['piege']}

### 4. Décomposition (étape 6)
- {d['modele']}
- Choix additif/multiplicatif justifié (au moins deux méthodes : bande, Buys-Ballot, profils).
- Tendance, coefficients saisonniers (si pertinents), série CVS.
- **À la main** (sur 1 cycle) : 3 valeurs de moyenne mobile, 1 coefficient saisonnier, 1 valeur CVS, puis vérification logicielle.

### 5. Validation (étape 7)
Résidus : graphique, ACF, histogramme/QQ-plot, Ljung-Box. Lister les 3 observations les moins bien ajustées et les expliquer par un événement réel si possible.

### 6. Prédiction (étape 8)
1. Décomposition (tendance + saisonnalité si pertinente).
2. Lissage (LES, Holt ou Holt-Winters : justifier, estimer α, β, γ).
3. Modèle AR/MA/ARIMA/SARIMA choisi via ACF/PACF (pas seulement `auto.arima`).
4. Tableau comparatif sur le **test** : RMSE, MAE, MAPE ; verdict argumenté.

### 7. Question spécifique ⭐
{d['angle']}
"""

def render(fn, titre, keys):
    gs = [KEY_OF[k] for k in keys]
    lines = [f"# SAE 3.03 — Exercice : {titre}\n",
             "**Groupes concernés (2026)** :\n", "| Classe | Groupe | Noms | Sujet saisi |" + (" Variante |" if len(keys) > 1 else ""),
             "|---|---|---|---|" + ("---|" if len(keys) > 1 else "")]
    for k in keys:
        cl, n, noms, _ = KEY_OF[k]
        lines.append(f"| {cl} | {n} | {noms} | {SUJET[(cl, n)]} |" + (f" {D[k]['titre']} |" if len(keys) > 1 else ""))
    lines.append("\n> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.\n\n---\n")
    if len(keys) == 1:
        lines.append(body(keys[0]))
    else:
        for k in keys:
            cl, n, noms, _ = KEY_OF[k]
            lines.append(f"## Variante : {D[k]['titre']} (groupe {cl} n°{n} — {noms})\n")
            lines.append(body(k).replace("\n### ", "\n#### ").replace("**Série**", "**Série**", 1))
            lines.append("\n---\n")
    lines.append("""## Barème indicatif (/20)
| Critère | Points |
|---|---|
| Contexte + biblio | 3 |
| Exploration + tests (interprétés) | 4 |
| Décomposition (choix justifié, calcul à la main) | 4 |
| Validation des résidus | 2 |
| Prédictions (3 méthodes, comparaison sur test) | 4 |
| Question spécifique ⭐ | 2 |
| Qualité du rapport, code en annexe | 1 |
""")
    return "\n".join(lines)

def main():
    OUT.mkdir(exist_ok=True)
    for f in OUT.glob("[0-9]*.md"):   # anciens énoncés au niveau racine (avant le passage en dossiers)
        f.unlink()
    rows = []
    for fn, titre, keys in SUBJ:
        d = OUT / fn
        d.mkdir(exist_ok=True)
        (d / "ENONCE.md").write_text(render(fn, titre, keys), encoding="utf-8")
        for k in keys:
            cl, n, noms, _ = KEY_OF[k]
            rows.append(f"| {titre} | {D[k]['titre']} | {cl} {n} — {noms} | [{fn}/ENONCE.md]({fn}/ENONCE.md) |")
    idx = ["# Exercices SAE 3.03 — promo 2026 (par sujet)\n",
           "| Sujet | Série | Groupe | Énoncé |", "|---|---|---|---|", *rows,
           "\n**À confirmer** : « 10 données économiques » (EMS-1 → FEDFUNDS) et « 2.5 environnement » (VCOD-7 → nottem).",
           "Décès pulmonaires et taches solaires : un énoncé, deux variantes (mdeaths+fdeaths / ldeaths ; mensuel / annuel).",
           "",
           "## Comment lancer les solutions (corrigés)",
           "",
           "Chaque dossier contient `solution.py` et `solution.R` qui produisent `sorties_python/` et `sorties_R/`",
           "(log `resultats.txt`, figures PNG, `comparaison_previsions.csv`).",
           "",
           "**Python** (venv central) :",
           "```bash",
           "python3 -m venv /tmp/sae_venv && /tmp/sae_venv/bin/pip install numpy pandas scipy matplotlib statsmodels",
           'cd "<dossier du sujet>" && /tmp/sae_venv/bin/python solution.py',
           "```",
           "",
           "**R** (packages : `forecast`, `tseries` ; + `fpp2` pour les décès pulmonaires) :",
           "```bash",
           "Rscript solution.R   # depuis n'importe quel dossier",
           "```",
           "",
           "Relancer tout :",
           "```bash",
           'cd "SAE 3.03/2026"',
           'for d in [0-9]*_*/; do Rscript "$d/solution.R" && /tmp/sae_venv/bin/python "$d/solution.py"; done',
           "```",
           "",
           "## Sources des données",
           "",
           "- **Séries R** (UKgas, gas, co2, Nile, nottem, sunspots, sunspot.year, UKDriverDeaths, mdeaths/fdeaths/ldeaths) :",
           "  R de base + `fpp2` ; Python les lit via `statsmodels.datasets.get_rdataset`, avec repli sur le CSV local de `data/`.",
           "- **FEDFUNDS** (01) : téléchargé depuis FRED → `data/FEDFUNDS.csv` (re-téléchargé automatiquement si absent).",
           "- **Boulder** (07) : CSV du doc SAE (GitHub ef2020) → `data/boulder-precip.csv` ; HPCP en pouces, 999.99 = NA,",
           "  plusieurs relevés par jour à sommer, jours absents = jours secs.",
           "- **Options locales** (03 transports, 11 météo, 12 champagne) : fichiers de `SAE 3.03/data/`",
           "  (Kaggle + `monthly_champagne_sales.csv`), lus en relatif depuis la racine du projet.",
           "",
           "## À savoir avant de distribuer les corrigés",
           "",
           "- Sujet 04 : le doc dit « sunspot.month, 1790–1970 » ; R n'a pas cet objet → `sunspots` (1749–1983), à signaler.",
           "- Sujet 01 : FEDFUNDS est dans la section « sans saisonnalité — PAS AU PROGRAMME DES BUT2 » du doc — à confirmer si BUT2.",
           "- Choix SARIMA par grille AIC restreinte (p,q ≤ 2, P,Q ≤ 1) ; p-values ADF de `tseries` bornées à 0.01 ;",
           "  MAPE énorme sur FEDFUNDS (taux ≈ 0 : artefact du MAPE)."]
    (OUT / "README.md").write_text("\n".join(idx) + "\n", encoding="utf-8")
    print(len(SUBJ), "fichiers écrits dans", OUT)

if __name__ == "__main__":
    main()
