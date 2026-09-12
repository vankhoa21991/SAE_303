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

## Option C — Ventes retail avec effet marketing

**Dataset** : Retail Sales Data with Seasonal Trends & Marketing · Quotidien/mensuel selon agrégation, plusieurs années · [kaggle.com/datasets/abdullah0a/retail-sales-data-with-seasonal-trends-and-marketing](https://www.kaggle.com/datasets/abdullah0a/retail-sales-data-with-seasonal-trends-and-marketing)

**Pourquoi la choisir** : construit explicitement pour contenir tendance + saisonnalité + effet promotionnel superposé — pousse le binôme à *nettoyer et agréger* avant de pouvoir décomposer proprement, ce qui donne un vrai contenu à l'étape "Exploration des données" plutôt qu'une formalité.

**Ce que ça donne à chaque étape** :
- **Exploration (4)** : nécessite de choisir un pas de temps (journalier trop bruité pour la décomposition classique → argument pour agréger en mensuel), bon sujet de discussion sur les descripteurs statistiques.
- **Tests (5)** : le bruit "marketing" rend le test de stationnarité et l'ACF/PACF moins triviaux à lire — bonne occasion de vraiment interpréter plutôt que de lire un résultat évident.
- **Décomposition (6)** : le résidu $e_t$ restera plus grand qu'ailleurs (le marketing n'est pas capturé par trend+saison) — excellent point pour la partie "Validation du modèle" (étape 7) : discuter *pourquoi* le résidu ne suffit pas à tout capturer.
- **Modèle autorégressif** : bon cas pour tester si un ARIMA sur le résidu (après retrait de la saisonnalité) améliore la prévision par rapport à la décomposition seule.

**Point de vigilance** : demander au binôme de choisir *une seule* série (un magasin/produit/région) avant de commencer, sinon le dataset est multivarié et sort du cadre du cours.

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

## Option G — Une série au choix parmi 366 (Tourism Forecasting)

**Dataset** : Tourism Forecasting Part Two (compétition Kaggle) · Mensuel, 366 séries indépendantes · [kaggle.com/competitions/tourism2](https://www.kaggle.com/competitions/tourism2/data?select=tourism2_revision2.csv)

**Pourquoi la choisir** : si vous voulez que **chaque binôme de la classe travaille sur une série différente** (pas de risque de copier le voisin, correction plus intéressante à lire), c'est l'option la plus pratique — une seule source Kaggle, des centaines de séries indépendantes à distribuer.

**Ce que ça donne à chaque étape** :
- **Contextualisation (3)** : chaque binôme doit documenter *sa* série spécifique (secteur touristique, origine, durée) — variabilité garantie entre groupes.
- **Décomposition (6)** : certaines séries ont une saisonnalité nette, d'autres non — bon exercice réel de diagnostic (les binômes ne savent pas à l'avance ce qu'ils vont trouver, contrairement aux options A-C qui sont déjà connues comme saisonnières).
- **Modèle autorégressif** : certaines séries se prêteront à un ARIMA simple, d'autres à un SARIMA — bonne diversité pour la mise en commun en fin de séance.

**Point de vigilance** : donner une consigne claire sur comment choisir/assigner la série (numéro de série = numéro de groupe, par exemple) pour éviter que tout le monde prenne la même par facilité.

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

## Option I — Ventes retail multi-magasins (Store Sales, projet ambitieux)

**Dataset** : Store Sales – Time Series Forecasting (compétition Corporación Favorita) · Quotidien, plusieurs années, ~54 magasins × 33 familles de produits · [kaggle.com/competitions/store-sales-time-series-forecasting](https://www.kaggle.com/competitions/store-sales-time-series-forecasting)

**Pourquoi la choisir** : l'option la plus riche et la plus proche d'un cas réel d'entreprise — oblige le binôme à choisir/agréger lui-même une série pertinente (ex : une famille de produits sur tous les magasins, en mensuel) avant même de commencer l'étape 3. Bon choix pour un binôme motivé qui veut un projet qui "ressemble à un vrai cas".

**Ce que ça donne à chaque étape** :
- **Management de projet (1)** : le cadrage du sujet (quelle série choisir et pourquoi) doit apparaître comme une tâche à part entière dans le Gantt — ne pas le sous-estimer, ça peut prendre facilement une des 5 tranches de 2h.
- **Contextualisation (3)** : justifier le choix de la série extraite est en soi un exercice de cadrage de problème, proche de ce qu'on attend en entreprise.
- **Modèle autorégressif** : assez de données pour un SARIMA complet avec validation croisée digne de ce nom, et pour comparer sérieusement contre une méthode de machine learning si le binôme choisit l'option "optionnel" de l'énoncé.

**Point de vigilance** : volume très important — à réserver aux binômes solides techniquement, sous peine de passer les 10h uniquement sur le nettoyage/l'agrégation sans arriver à la prédiction.

---

## Option J — Demande de vélos en libre-service (Bike Sharing)

**Dataset** : Bike Sharing Demand · Horaire, ~2 ans, météo + calendrier · [kaggle.com/c/bike-sharing-demand](https://www.kaggle.com/c/bike-sharing-demand/data)

**Pourquoi la choisir** : c'est une série très parlante pour les étudiants : on peut relier la demande à l'heure de la journée, au jour travaillé, à la saison, à la météo et aux vacances. Elle est plus intéressante qu'une série univariée pure, car elle montre vite que la décomposition tendance+saison ne suffit pas toujours : température, pluie et calendrier expliquent une partie importante des résidus.

**Ce que ça donne à chaque étape** :
- **Contextualisation (3)** : service urbain de mobilité partagée ; facile de discuter des usages domicile-travail, week-end, météo et saison.
- **Exploration (4)** : excellent terrain pour visualiser plusieurs saisonnalités : horaire, hebdomadaire et annuelle. Pour rester dans le cadre du cours, agréger en **journalier** ou **mensuel** avant la décomposition classique.
- **Tests (5)** : stationnarité et ACF très dépendantes du niveau d'agrégation choisi — bon exercice pour montrer que le prétraitement change l'analyse.
- **Décomposition (6)** : décomposition mensuelle possible après agrégation ; les résidus restent interprétables via météo/calendrier.
- **Prédiction (8)** : comparer une méthode classique sur la série agrégée à une approche optionnelle utilisant les variables météo.

**Point de vigilance** : ne pas analyser directement la série horaire complète avec une moyenne mobile de période 12 : il faut d'abord choisir une granularité cohérente. Pour un rapport de 10h, recommander une agrégation **journalière** ou **mensuelle**.

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

## Option N — M5 Forecasting : ventes retail hiérarchiques Walmart

**Dataset** : M5 Forecasting - Accuracy · Quotidien, ventes Walmart, hiérarchie magasin/produit + prix + calendrier · [kaggle.com/competitions/m5-forecasting-accuracy](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data)

**Pourquoi la choisir** : probablement l'option la plus professionnelle de la liste : ventes quotidiennes, calendrier, événements, prix, magasins, familles de produits. Elle permet de parler de prévision à grande échelle, de hiérarchie de séries, et de variables explicatives — exactement ce qui dépasse les limites d'une décomposition simple.

**Ce que ça donne à chaque étape** :
- **Management de projet (1)** : le cadrage est central : choisir un seul magasin, une seule catégorie, voire un seul produit.
- **Recherche biblio (2)** : compétition très connue ; nombreuses solutions publiques et discussions méthodologiques.
- **Exploration (4)** : visualiser ventes quotidiennes, jours sans vente, effets calendrier et événements commerciaux.
- **Décomposition (6)** : agréger en hebdomadaire ou mensuel pour rester compatible avec les méthodes du cours.
- **Prédiction (8)** : comparer une baseline classique à une approche enrichie par calendrier/prix en option.

**Point de vigilance** : option ambitieuse, à réserver aux groupes techniquement solides. Sans cadrage strict, le groupe risque de passer tout le temps à comprendre les fichiers au lieu d'analyser une série.

---

## Option O — Consommation électrique française longue période

**Dataset** : Electricity consumption in France (2008–2017) · France, consommation électrique, période longue · [kaggle.com/datasets/malguibert/electricity-consumption-in-france-2008-2017](https://www.kaggle.com/datasets/malguibert/electricity-consumption-in-france-2008-2017)

**Pourquoi la choisir** : c'est une version plus directement française que les datasets énergie internationaux. Elle permet de travailler sur un sujet très contextualisable : chauffage électrique, saison hiver/été, jours ouvrés, vacances, politiques énergétiques et événements climatiques. La période 2008–2017 donne assez de recul pour observer plusieurs cycles annuels et discuter d'une tendance de fond.

**Ce que ça donne à chaque étape** :
- **Recherche biblio (2)** : nombreuses sources françaises possibles : RTE, INSEE, Ministère de la Transition écologique, bilans électriques annuels.
- **Exploration (4)** : bon terrain pour comparer granularité journalière, hebdomadaire ou mensuelle selon les fichiers disponibles.
- **Tests (5)** : stationnarité en niveau peu probable si la série garde une tendance ou une saisonnalité forte ; test de Pettitt intéressant si un changement de niveau apparaît.
- **Décomposition (6)** : décomposition mensuelle simple et très lisible, avec saisonnalité hivernale attendue.
- **Prédiction (8)** : Holt-Winters saisonnier donne une baseline solide ; SARIMA pertinent si l'ACF montre un cycle annuel clair.

**Point de vigilance** : vérifier la granularité exacte après téléchargement. Si la série est trop fine, agréger en mensuel pour rester proche des méthodes vues en cours.

---

## Option P — Gaz et électricité en France (2011–2021)

**Dataset** : French gas and electricity consumption (2011–2021) · France, énergie, deux séries possibles · [kaggle.com/datasets/mariofdz/french-gas-and-electricity-consumption-2011-2021](https://www.kaggle.com/datasets/mariofdz/french-gas-and-electricity-consumption-2011-2021)

**Pourquoi la choisir** : très bon dataset pour comparer deux usages énergétiques français : gaz et électricité. La série couvre potentiellement des événements importants, notamment les variations de consommation liées aux hivers, aux politiques énergétiques et à la période COVID.

**Ce que ça donne à chaque étape** :
- **Contextualisation (3)** : expliquer la différence d'usage entre gaz et électricité en France, et choisir clairement une variable principale.
- **Exploration (4)** : possibilité de comparer gaz vs électricité en annexe, mais l'analyse SAE doit rester centrée sur une seule série.
- **Tests (5)** : Pettitt peut être intéressant autour de 2020 ou lors d'un changement structurel de consommation.
- **Décomposition (6)** : saisonnalité hivernale attendue ; le modèle additif ou multiplicatif dépendra de l'évolution de l'amplitude.
- **Prédiction (8)** : utile pour comparer prévision classique et commentaire métier : météo, prix, comportements de consommation.

**Point de vigilance** : la licence Kaggle est indiquée comme spécifique/à vérifier. Avant de donner ce dataset à une classe, vérifier explicitement l'onglet licence et la source originale.

---

## Option Q — Vélib' Paris : disponibilité de vélos + météo

**Dataset** : velib_data · Paris, disponibilité Vélib' toutes les 5 minutes + météo · [kaggle.com/datasets/adrienmorel97/velib-data](https://www.kaggle.com/datasets/adrienmorel97/velib-data)

**Pourquoi la choisir** : option très concrète et française : mobilité urbaine parisienne, météo, pics domicile-travail, week-ends, vacances, stations plus ou moins fréquentées. C'est probablement l'un des datasets les plus intéressants pour des étudiants, car il relie directement série temporelle et usages quotidiens.

**Ce que ça donne à chaque étape** :
- **Management de projet (1)** : prévoir du temps pour choisir une station, une zone ou une agrégation globale.
- **Contextualisation (3)** : expliquer le service Vélib', la géographie parisienne et l'effet météo attendu.
- **Exploration (4)** : très riche : saisonnalité intra-journalière, hebdomadaire, météo, jours ouvrés.
- **Décomposition (6)** : agréger en journalier ou mensuel ; la série 5 minutes est trop fine pour une décomposition classique simple.
- **Prédiction (8)** : comparer une baseline lissage/décomposition à une approche optionnelle utilisant météo ou calendrier.

**Point de vigilance** : dataset volumineux et multivarié. Pour 10h, imposer **une seule station** ou une agrégation simple, sinon le projet devient un projet data engineering.

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

## Option S — MeteoNet Nord-Ouest France

**Dataset** : MeteoNet North-West France · Données météo ouvertes Météo-France · [kaggle.com/datasets/katerpillar/meteonet](https://www.kaggle.com/datasets/katerpillar/meteonet)

**Pourquoi la choisir** : option française scientifique, issue d'un contexte Météo-France. Elle permet de prévoir une variable naturelle — température, pluie, vent — et de discuter les saisonnalités physiques plutôt qu'économiques.

**Ce que ça donne à chaque étape** :
- **Contextualisation (3)** : choisir une station météo ou une zone du Nord-Ouest ; documenter le climat local.
- **Exploration (4)** : excellent pour visualiser l'effet de la granularité : horaire/journalier/mensuel.
- **Tests (5)** : tendance et rupture à interpréter prudemment : un changement peut venir d'un épisode météo ou d'un changement de station.
- **Décomposition (6)** : température moyenne mensuelle = cas simple ; précipitations = série plus intermittente et plus difficile.
- **Prédiction (8)** : Holt-Winters fonctionne bien comme baseline saisonnière pour température ; moins évident pour pluie.

**Point de vigilance** : dataset potentiellement volumineux et technique. Choisir **une station + une variable** dès le départ.

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
| Un vrai travail de nettoyage avant décomposition | **C** — Retail + Marketing |
| Une fréquence différente (hebdomadaire) | **D** — Avocado Prices |
| Discuter ce que le modèle ne capture pas (variables externes) | **E** — Walmart Sales |
| Un projet comparatif entre pays | **F** — Western Europe Power |
| Que chaque binôme ait une série différente | **G** — Tourism Forecasting (366 séries) |
| Travailler sur une rupture de tendance plutôt qu'une saisonnalité | **H** — US Census Retail |
| Le projet le plus ambitieux, proche d'un cas d'entreprise | **I** — Store Sales (Favorita) ou **N** — M5 Forecasting |
| Un sujet urbain concret avec météo et calendrier | **J** — Bike Sharing Demand ou **Q** — Vélib' Paris |
| Une vraie série métier avec plusieurs saisonnalités | **K** — PJM Hourly Energy Consumption |
| Un sujet météo/nature facile à contextualiser | **L** — Historical Hourly Weather ou **S** — MeteoNet France |
| Des séries irrégulières, bruitées, liées à l'actualité | **M** — Web Traffic Wikipédia |
| Un sujet français simple et très contextualisable | **O** — Électricité France 2008–2017 |
| Comparer deux énergies en France | **P** — Gaz et électricité France |
| Mobilité et fréquentation en France | **Q** — Vélib' ou **R** — Transports publics France |
| Énergie française avancée avec variables explicatives | **U** — France energy + weather |
| Un sujet français original lié au nucléaire | **T** — Réacteurs nucléaires français |

---

## Notes

- Les liens pointent vers des pages Kaggle publiques vérifiées/recherchées entre juillet et août 2026 ; vérifier la disponibilité et la licence exacte au moment du choix, Kaggle modifiant parfois l'URL ou le statut d'un dataset.
- Certaines pages Kaggle exposent peu de métadonnées sans connexion : avant de valider un groupe, télécharger le fichier ou lire l'onglet Data pour confirmer la période exacte, les colonnes, les valeurs manquantes et la licence.
- Pour les options françaises ajoutées en août 2026, les métadonnées Kaggle consultées indiquaient notamment : `velib_data` CC BY-SA 4.0, `Electricity consumption in France (2008-2017)` CC0, `Public transport traffic data in France` sous licence Open Database, `French nuclear reactors availability` CC BY-SA 4.0, et `France energy weather hourly/daily` CC BY 4.0 ; revérifier avant diffusion officielle.
- Pour toutes les options, prévoir une étape de téléchargement + import (`read.csv`/`pandas.read_csv`, ou import direct dans Excel) — ce n'est pas fourni ici, c'est au binôme de le faire (cf. script de traitement mentionné "pour plus tard").
- Rappel : l'énoncé demande de choisir un modèle autorégressif (AR, MA, ARMA, ARIMA, SARIMA) en s'appuyant sur ACF/PACF — toutes les options ci-dessus s'y prêtent, mais certaines (A, G, J, O) sont plus simples pour un premier contact avec SARIMA, tandis que d'autres (D, F, I, K, N, Q, T, U) demandent de réfléchir à l'ordre de différenciation saisonnière et au niveau d'agrégation.
- Si l'option choisie s'avère trop bruitée pour une décomposition propre, c'est en soi une observation pédagogique utile à mentionner dans le rapport à l'étape 7 (Validation du modèle) : un résidu qui reste grand = le modèle trend+saison(+AR) ne suffit pas à tout expliquer.
