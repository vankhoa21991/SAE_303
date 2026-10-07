# SAE3.03 — Options de jeux de données pour le projet (Kaggle)

*Chaque binôme choisit **une option** ci-dessous — ou une série personnelle validée avec l'enseignant. Les options sont pensées pour couvrir les 8 étapes de l'énoncé (`PRESENTATION_SAE_Premiere_Seance.md` §1.2) : contextualisation, exploration, tests statistiques (stationnarité, tendance, Pettitt), décomposition, validation des résidus, et prédiction — décomposition **et** lissage, avec un modèle autorégressif (AR/MA/ARMA/ARIMA/SARIMA) choisi via ACF/PACF. Toutes proviennent de Kaggle et sont une alternative aux séries déjà données en exemple dans l'énoncé (wineind, FEDFUNDS, EuStockMarkets, gold, LakeHuron).*

**Avant de choisir une option, vérifier** :
- Au moins **3 cycles complets** de la période si vous cherchez une saisonnalité (ex : 3 ans de données mensuelles) — sinon impossible de calculer des coefficients saisonniers fiables.
- Peu ou pas de valeurs manquantes — sinon prévoir explicitement l'étape de nettoyage dans le rapport (et le mentionner à l'étape 4 "Explorer les données").
- Licence Kaggle compatible usage pédagogique (les options ci-dessous sont CC0 / usage libre à l'origine — revérifier sur la page Kaggle au moment de télécharger, les statuts changent parfois).
- Une série assez longue pour réserver un **jeu de test** (les dernières observations, non utilisées pour ajuster le modèle) — indispensable pour l'étape 8 "Prédire" et pour comparer objectivement vos deux méthodes de prévision.

---

## Option A — Ventes de champagne (Perrin Frères)

**Dataset** : Monthly Champagne Sales · Mensuel, ~9 ans (108 points) · [kaggle.com/datasets/piyushagni5/monthly-sales-of-french-champagne](https://www.kaggle.com/datasets/piyushagni5/monthly-sales-of-french-champagne)

**Pourquoi la choisir** : la série la plus "propre" de cette liste — une seule colonne, aucune valeur manquante, saisonnalité annuelle très marquée (pic fin d'année) et amplitude qui grandit légèrement avec le niveau. C'est l'option la plus sûre pour un binôme qui veut consacrer son temps à *soigner* chaque étape plutôt qu'à nettoyer des données difficiles.

**Ce que ça donne à chaque étape** :
- **Contextualisation (3)** : série économique française, facile à documenter (production/vente de vin effervescent).
- **Tests (5)** : tendance nette → attendre un test de Dickey-Fuller *rejetant* la stationnarité ; bon terrain pour illustrer la différence entre stationnarité en niveau et en tendance.
- **Décomposition (6)** : débat additif/multiplicatif légitime (amplitude qui croît un peu) — bon exercice pour appliquer les 3 méthodes de choix de modèle du cours et voir si elles sont d'accord entre elles.
- **Modèle autorégressif** : SARIMA quasi obligatoire vu la saisonnalité forte (composante saisonnière de période 12 nette sur l'ACF).

**Point de vigilance** : série courte et très "manuel", risque que le binôme survole les étapes faute de difficulté — bien insister sur la qualité de l'interprétation plutôt que la quantité de calculs.

---

## Option B — Consommation d'énergie mensuelle (France)

**Dataset** : Monthly Energy Consumption Dataset (France) · Mensuel, plusieurs années · [kaggle.com/datasets/auricdutt/monthly-energy-consumption-dataset-france](https://www.kaggle.com/datasets/auricdutt/monthly-energy-consumption-dataset-france/data)

**Pourquoi la choisir** : thème français, saisonnalité hiver/été très nette (effet chauffage) — proche des exemples déjà vus en cours (essence aviation, population française). Bon compromis entre série "réaliste" et série encore assez lisible.

**Ce que ça donne à chaque étape** :
- **Recherche biblio (2)** : sujet énergétique très documenté (RTE, INSEE) — facile de trouver des études comparables pour la partie bibliographie.
- **Exploration (4)** : bon candidat pour comparer plusieurs granularités (mensuel vs annuel) si le fichier le permet.
- **Tests (5)** : bon candidat pour un test de Pettitt si la période couvre un choc identifiable (crise énergétique, confinement…) — vérifier les dates couvertes par le fichier.
- **Décomposition (6)** : saisonnalité additive assez stable d'une année sur l'autre → bon cas pour un modèle additif "manuel" avant de comparer à SARIMA.

**Point de vigilance** : vérifier le nombre exact de valeurs manquantes et la période couverte avant de s'engager — certains jeux "France énergie" sur Kaggle sont partiels.

---

## Option D — Prix hebdomadaires de l'avocat (US)

**Dataset** : Avocado Prices · Hebdomadaire, ~4 ans, plusieurs régions US · [kaggle.com/datasets/neuromusic/avocado-prices](https://www.kaggle.com/neuromusic/avocado-prices)

**Pourquoi la choisir** : fréquence hebdomadaire (moins courante en cours, bon changement de rythme), saisonnalité bien documentée dans la littérature — nécessite de filtrer une seule région/type avant analyse, ce qui constitue un vrai travail préparatoire assumé dès l'étape 3.

**Ce que ça donne à chaque étape** :
- **Contextualisation (3)** : bien préciser dans le rapport quelle région/type a été retenu et pourquoi (évite un dataset multivarié déguisé en série simple).
- **Décomposition (6)** : période saisonnière à 52 (semaines) — bon test pour vérifier que les étudiants savent adapter l'ordre de la moyenne mobile à la fréquence réelle des données (pas juste recopier "p=12" du cours).
- **Modèle autorégressif** : SARIMA avec période 52 est plus lourd à ajuster — bon sujet pour discuter des limites pratiques d'ARIMA/SARIMA sur des séries à longue période saisonnière (lien avec le "Optionnel : machine learning" de l'énoncé si le binôme veut aller plus loin).

**Point de vigilance** : bien vérifier qu'il reste au moins 3 ans complets après filtrage d'une seule région — sinon pas assez de cycles saisonniers.

---

## Option E — Ventes hebdomadaires Walmart (avec variables externes)

**Dataset** : Walmart Sales Forecast (Walmart Recruiting) · Hebdomadaire, 45 magasins, ~3 ans · [kaggle.com/datasets/aslanahmedov/walmart-sales-forecast](https://www.kaggle.com/datasets/aslanahmedov/walmart-sales-forecast)

**Pourquoi la choisir** : au-delà de la décomposition pure, le dataset inclut des variables externes (CPI, chômage, prix carburant, indicateur jours fériés) — permet une vraie discussion sur "qu'est-ce que trend + saison + AR ne capturent pas" et ouvre naturellement vers la partie optionnelle de l'énoncé (autre méthode / ML).

**Ce que ça donne à chaque étape** :
- **Recherche biblio (2)** : dataset très utilisé en compétition Kaggle — facile de trouver des approches comparables (bon pour montrer que la série a "déjà été étudiée ailleurs").
- **Tests (5)** : jours fériés = ruptures ponctuelles identifiables → bon terrain pour le test de Pettitt et pour discuter la différence entre rupture ponctuelle et changement de tendance durable.
- **Prédiction (8)** : comparer une prévision décomposition/lissage classique à un modèle qui intègre (même informellement) les variables externes — bon sujet de discussion critique en conclusion de rapport.

**Point de vigilance** : dataset riche mais volumineux — imposer de choisir **un seul magasin et un seul département** dès le départ, sinon le binôme se noie avant même d'attaquer l'étape 4.

---

## Option F — Consommation électrique horaire (Europe de l'Ouest)

**Dataset** : Western Europe Power Consumption · Horaire, plusieurs pays, plusieurs années · [kaggle.com/datasets/francoisraucent/western-europe-power-consumption](https://www.kaggle.com/datasets/francoisraucent/western-europe-power-consumption)

**Pourquoi la choisir** : pour un binôme qui veut un projet plus ambitieux/comparatif — permet de comparer la saisonnalité (annuelle **et** hebdomadaire, voire journalière) entre deux pays différents ("la France a-t-elle le même profil saisonnier que l'Allemagne ?"), ce qui donne un vrai axe de recherche bibliographique et une conclusion plus riche.

**Ce que ça donne à chaque étape** :
- **Exploration (4)** : données horaires → obligation d'agréger à plusieurs granularités (journalier, mensuel) pour rendre la série exploitable, bon exercice de visualisation "à différents pas de temps" explicitement demandé par l'énoncé.
- **Tests (5)** : ACF/PACF particulièrement parlantes sur des données à forte périodicité — bon cas pour bien illustrer le rôle du PACF (optionnel dans l'énoncé, mais ici ça vaut le coup).
- **Décomposition (6) & Modèle autorégressif** : bon terrain pour un SARIMA multi-période ou pour justifier un choix pragmatique (ex. agréger en mensuel pour rester dans le cadre du cours plutôt que de gérer une double saisonnalité).

**Point de vigilance** : volume important — à réserver aux binômes à l'aise techniquement (R/Python), prévoir du temps de nettoyage/agrégation dans le Gantt de l'étape 1.

---

## Option H — Ventes retail longue durée (US Census)

**Dataset** : Retail and Retailers Sales Time Series Collection (US Census Bureau) · Mensuel, plusieurs secteurs, plusieurs décennies · [kaggle.com/datasets/census/retail-and-retailers-sales-time-series-collection](https://www.kaggle.com/datasets/census/retail-and-retailers-sales-time-series-collection)

**Pourquoi la choisir** : données officielles, séries très longues — pour un binôme qui veut travailler sur un **changement de régime de tendance** (ex : crise 2008, COVID 2020) plutôt que sur une saisonnalité classique. Bon contraste avec les autres options centrées "saisonnalité".

**Ce que ça donne à chaque étape** :
- **Tests (5)** : terrain idéal pour le test de Pettitt (rupture nette et documentée historiquement, donc vérifiable) et pour discuter la stationnarité avant/après la rupture séparément.
- **Décomposition (6)** : bon exemple des limites de la moyenne mobile face à une rupture brutale — la moyenne mobile "en retard" sur le changement de tendance doit être visible et commentée, pas juste calculée.
- **Modèle autorégressif** : bon cas pour justifier un ARIMA avec différenciation (d>0) plutôt qu'un simple AR, en expliquant pourquoi (série non stationnaire en niveau).

**Point de vigilance** : bien choisir un seul secteur, et si la rupture est trop violente (COVID), envisager de couper la série avant *ou* après la rupture pour l'ajustement du modèle, et le dire explicitement dans le rapport.

---

## Option K — Consommation électrique horaire PJM (US)

**Dataset** : Hourly Energy Consumption · Horaire, plusieurs zones électriques PJM · [kaggle.com/datasets/robikscube/hourly-energy-consumption](https://www.kaggle.com/datasets/robikscube/hourly-energy-consumption)

**Pourquoi la choisir** : dataset très réaliste pour la prévision opérationnelle : demande électrique, pics journaliers, effets week-end, saisonnalité été/hiver et possibles ruptures. Il ressemble davantage à un vrai cas métier qu'à une série pédagogique courte.

**Ce que ça donne à chaque étape** :
- **Recherche biblio (2)** : la prévision de charge électrique est un domaine très documenté ; facile de trouver des références sur la saisonnalité, la température et les pics de demande.
- **Exploration (4)** : visualisations à plusieurs pas de temps : horaire, journalier, hebdomadaire, mensuel. L'ACF révèle généralement des pics à 24h, 7 jours, et parfois une structure annuelle.
- **Tests (5)** : bon candidat pour discuter stationnarité après agrégation ou différenciation.
- **Décomposition (6)** : si le groupe reste dans le cours classique, agréger en **mensuel** pour une saisonnalité annuelle de période 12 ; si le groupe est plus avancé, travailler en journalier avec saisonnalité hebdomadaire.
- **Modèle autorégressif** : SARIMA utile, mais l'ordre saisonnier dépend fortement de la granularité retenue.

**Point de vigilance** : volume important et saisonnalités multiples. Imposer une seule zone PJM et une granularité avant de commencer, sinon le projet devient trop large pour 10h.

---

## Option L — Météo horaire multi-villes

**Dataset** : Historical Hourly Weather Data 2012–2017 · Horaire, plusieurs villes, variables météo · [kaggle.com/datasets/selfishgene/historical-hourly-weather-data](https://www.kaggle.com/datasets/selfishgene/historical-hourly-weather-data)

**Pourquoi la choisir** : c'est une option originale pour sortir des ventes/énergie. Les étudiants peuvent prévoir une variable physique simple (température, humidité, pression…) et relier les cycles observés à des phénomènes naturels : alternance jour/nuit, saisons, épisodes extrêmes.

**Ce que ça donne à chaque étape** :
- **Contextualisation (3)** : choisir une ville et une variable météo ; documenter brièvement le climat local.
- **Exploration (4)** : très bon support pour montrer les effets de granularité : l'horaire montre le cycle jour/nuit, le mensuel montre la saisonnalité annuelle.
- **Tests (5)** : le test de Pettitt peut détecter des changements artificiels liés à la collecte ou à des épisodes météo extrêmes ; à interpréter avec prudence.
- **Décomposition (6)** : agréger en mensuel pour une décomposition simple de température moyenne ; possibilité de comparer deux villes en option.
- **Prédiction (8)** : Holt-Winters peut donner une baseline saisonnière claire, surtout sur température mensuelle.

**Point de vigilance** : le dataset est multivarié et multi-villes. Il faut choisir **une ville + une variable + une granularité** dès le départ.

---

## Option M — Trafic web de pages Wikipédia

**Dataset** : Web Traffic Time Series Forecasting · Journalier, très grand nombre de pages web · [kaggle.com/c/web-traffic-time-series-forecasting](https://www.kaggle.com/c/web-traffic-time-series-forecasting/data)

**Pourquoi la choisir** : très intéressant si l'objectif est de montrer que toutes les séries ne sont pas propres : pics viraux, jours sans trafic, ruptures liées à l'actualité, séries intermittentes. C'est un bon contre-exemple aux séries trop régulières.

**Ce que ça donne à chaque étape** :
- **Contextualisation (3)** : chaque binôme choisit une page ou un petit groupe de pages ; le sujet de la page aide à interpréter les pics.
- **Exploration (4)** : beaucoup de séries sont bruitées ou intermittentes — très bon terrain pour discuter nettoyage, transformation logarithmique et valeurs extrêmes.
- **Tests (5)** : stationnarité et rupture peuvent être dominées par un événement d'actualité, ce qui force à commenter plutôt qu'à appliquer mécaniquement.
- **Décomposition (6)** : certaines pages ont une saisonnalité hebdomadaire, d'autres non ; le diagnostic devient une vraie partie du travail.
- **Modèle autorégressif** : ARIMA/SARIMA possible sur les pages régulières, mais pas adapté à toutes les séries — excellent point critique.

**Point de vigilance** : dataset très volumineux. Donner une règle stricte de sélection : une seule page, ou une page assignée par numéro de groupe. Éviter les séries trop courtes ou quasi nulles.

---

## Option R — Trafic des transports publics en France

**Dataset** : Public transport traffic data in France · validations de titres et régularité des trains · [kaggle.com/datasets/gatandubuc/public-transport-traffic-data-in-france](https://www.kaggle.com/datasets/gatandubuc/public-transport-traffic-data-in-france)

**Pourquoi la choisir** : dataset français très intéressant pour relier statistiques et vie quotidienne : fréquentation, grèves, vacances, régularité, effets COVID, différences entre réseaux. Il permet un rapport avec une vraie interprétation métier, pas seulement une prévision mécanique.

**Ce que ça donne à chaque étape** :
- **Recherche biblio (2)** : possibilité d'utiliser des sources SNCF, Île-de-France Mobilités, rapports publics de fréquentation.
- **Exploration (4)** : très bon candidat pour repérer ruptures, creux anormaux, cycles hebdomadaires ou annuels.
- **Tests (5)** : Pettitt particulièrement pertinent si la période inclut COVID, grèves ou changement de collecte.
- **Décomposition (6)** : choisir une métrique et une ligne/réseau ; agréger en mensuel pour faire ressortir la saisonnalité.
- **Validation (7)** : les résidus peuvent être interprétés comme événements sociaux, vacances, perturbations, grèves.

**Point de vigilance** : il faut choisir une seule sous-série exploitable. Les variables exactes et la granularité doivent être vérifiées dans les fichiers avant validation du sujet.

---

## Option T — Disponibilité des réacteurs nucléaires français

**Dataset** : French nuclear reactors availability (2015–2021) · pas de temps 30 minutes, 58 réacteurs · [kaggle.com/datasets/thrasy/french-nuclear-reactors-availability-20152021](https://www.kaggle.com/datasets/thrasy/french-nuclear-reactors-availability-20152021)

**Pourquoi la choisir** : option française originale et très liée à l'actualité énergétique. La disponibilité nucléaire peut montrer des arrêts programmés, des maintenances, des ruptures et une saisonnalité liée à la demande électrique et aux calendriers d'arrêt.

**Ce que ça donne à chaque étape** :
- **Contextualisation (3)** : expliquer ce que signifie la disponibilité d'un réacteur et pourquoi elle varie.
- **Exploration (4)** : choisir un réacteur ou agréger la disponibilité totale du parc ; visualiser arrêts et retours en service.
- **Tests (5)** : Pettitt utile pour détecter un changement de niveau moyen de disponibilité.
- **Décomposition (6)** : plus adapté après agrégation journalière ou mensuelle ; la série brute à 30 minutes est trop fine.
- **Validation (7)** : les gros résidus correspondent souvent à des arrêts non capturés par la saisonnalité.

**Point de vigilance** : série technique, pas forcément adaptée à tous les groupes. À réserver à un binôme capable de faire une bonne contextualisation métier.

---

## Option U — Énergie française + météo régionale

**Dataset** : France energy weather hourly/daily · consommation énergétique française + météo régionale · [kaggle.com/datasets/ravvvvvvvvvvvv/france-energy-weather-hourly](https://www.kaggle.com/datasets/ravvvvvvvvvvvv/france-energy-weather-hourly)

**Pourquoi la choisir** : probablement l'une des meilleures options françaises pour un projet avancé : elle relie directement consommation d'énergie et météo, ce qui permet d'expliquer pourquoi un modèle tendance+saisonnalité laisse encore des résidus importants.

**Ce que ça donne à chaque étape** :
- **Recherche biblio (2)** : lien direct avec prévision de charge, météo et énergie en France.
- **Exploration (4)** : comparer consommation et température ; regarder les pics en hiver ou lors de vagues de chaleur.
- **Tests (5)** : stationnarité à analyser après agrégation ; Pettitt possible sur périodes de rupture.
- **Décomposition (6)** : agrégation mensuelle conseillée pour appliquer proprement les coefficients saisonniers du cours.
- **Prédiction (8)** : très bon support pour comparer méthode classique et méthode optionnelle avec variable explicative météo.

**Point de vigilance** : dataset enrichi donc plus complexe. Pour rester dans les 10h, choisir une variable énergie principale et une granularité unique.

---

## Tableau récapitulatif — choix rapide

| Vous cherchez… | Option recommandée |
|---|---|
| La série la plus sûre, sans complications de nettoyage | **A** — Champagne Sales |
| Un thème français, saisonnalité nette (chauffage) | **B** — Énergie France |
| Une fréquence différente (hebdomadaire) | **D** — Avocado Prices |
| Discuter ce que le modèle ne capture pas (variables externes) | **E** — Walmart Sales |
| Un projet comparatif entre pays | **F** — Western Europe Power |
| Travailler sur une rupture de tendance plutôt qu'une saisonnalité | **H** — US Census Retail |
| Une vraie série métier avec plusieurs saisonnalités | **K** — PJM Hourly Energy Consumption |
| Un sujet météo/nature facile à contextualiser | **L** — Historical Hourly Weather |
| Des séries irrégulières, bruitées, liées à l'actualité | **M** — Web Traffic Wikipédia |
| Mobilité et fréquentation en France | **R** — Transports publics France |
| Énergie française avancée avec variables explicatives | **U** — France energy + weather |
| Un sujet français original lié au nucléaire | **T** — Réacteurs nucléaires français |

---

## Notes

- Les liens pointent vers des pages Kaggle publiques vérifiées/recherchées entre juillet et août 2026 ; vérifier la disponibilité et la licence exacte au moment du choix, Kaggle modifiant parfois l'URL ou le statut d'un dataset.
- Certaines pages Kaggle exposent peu de métadonnées sans connexion : avant de valider un groupe, télécharger le fichier ou lire l'onglet Data pour confirmer la période exacte, les colonnes, les valeurs manquantes et la licence.
- Pour les options françaises ajoutées en août 2026, les métadonnées Kaggle consultées indiquaient notamment : `Public transport traffic data in France` sous licence Open Database, `French nuclear reactors availability` CC BY-SA 4.0, et `France energy weather hourly/daily` CC BY 4.0 ; revérifier avant diffusion officielle.
- Pour toutes les options, prévoir une étape de téléchargement + import (`read.csv`/`pandas.read_csv`, ou import direct dans Excel) — ce n'est pas fourni ici, c'est au binôme de le faire (cf. script de traitement mentionné "pour plus tard").
- Rappel : l'énoncé demande de choisir un modèle autorégressif (AR, MA, ARMA, ARIMA, SARIMA) en s'appuyant sur ACF/PACF — toutes les options ci-dessus s'y prêtent, mais certaines (A) sont plus simples pour un premier contact avec SARIMA, tandis que d'autres (D, F, K, T, U) demandent de réfléchir à l'ordre de différenciation saisonnière et au niveau d'agrégation.
- Options retirées de cette liste (septembre-octobre 2026, après test réel de téléchargement et vérification quantitative tendance/saisonnalité — voir `scripts/check_trend_seasonality.py` et `scripts/plots/_trend_seasonality.md`) :
  - **G** (Tourism Forecasting), **J** (Bike Sharing Demand) et **N** (M5 Forecasting) sont des compétitions Kaggle dont les règles doivent être acceptées manuellement sur le site avant tout téléchargement via l'API — l'accès a échoué en l'état (403 Forbidden).
  - **S** (MeteoNet) s'est révélée trop volumineuse pour un téléchargement automatique raisonnable (archive de plusieurs Go).
  - **C** (Retail + Marketing) et **Q** (Vélib') : le fichier réellement téléchargé ne couvre que quelques semaines (4 mois pour C, 2 semaines pour Q) — bien trop court pour une saisonnalité ou une tendance exploitable, malgré une description Kaggle laissant penser à un historique long.
  - **O** (Électricité France 2008–2017) et **P** (Gaz et électricité France) : données **annuelles uniquement** (une valeur par an) — aucune saisonnalité infra-annuelle n'est mesurable par construction, quel que soit le nombre d'années couvertes.
  - **I** (Store Sales/Favorita) : après lecture du fichier réel, seulement quelques mois de données exploitables ont pu être extraits (probablement tronqué par la taille du fichier) — à re-vérifier manuellement si un binôme veut absolument cette option.
  - Ces options restent utilisables si un binôme accepte de gérer ces contraintes manuellement (règles de compétition, volume, agrégation annuelle→autre source), mais ne sont plus recommandées par défaut.
- Si l'option choisie s'avère trop bruitée pour une décomposition propre, c'est en soi une observation pédagogique utile à mentionner dans le rapport à l'étape 7 (Validation du modèle) : un résidu qui reste grand = le modèle trend+saison(+AR) ne suffit pas à tout expliquer.
