# SAE 3.03 — Théorie et exigences du projet, étape par étape

*Ce document explique, pour chacune des 8 étapes attendues du projet (`PRESENTATION_SAE_Premiere_Seance.md` §1.2), ce qui est demandé (**exigence**), ce qu'il faut savoir (**théorie**), et un exemple chiffré réel (**exemple travaillé**) tiré de l'analyse déjà réalisée sur les ventes de champagne Perrin Frères (`scripts/analyse_champagne.py`, résultats dans `outputs/champagne/`). L'objectif est de pouvoir relire une étape et comprendre immédiatement quoi produire, pourquoi, et à quoi ça ressemble une fois fait.*

*Pour la lecture des symboles utilisés ci-dessous, voir `GLOSSAIRE_Symboles_Mathematiques_FR.md`.*

---

## 0. Cadre général du projet

**Exigence** : un binôme reçoit une série temporelle et doit la présenter, l'analyser, la décomposer, et proposer une prédiction, en 10 heures, avec un rapport de 12 pages maximum (code en annexe), en s'appuyant sur R ou Python.

**Contraintes à retenir** :
- Groupe de **2 personnes**.
- **10h** de travail, réparties en tranches de 2h (d'où le Gantt demandé en étape 1).
- Rapport **12 pages maximum**, hors code (annexe) et hors bibliographie.
- Dépôt Moodle en PDF, avec nom de fichier imposé (`Nom1_Nom2_rapport_SAE303.pdf`).
- Un modèle autorégressif (AR, MA, ARMA, ARIMA, SARIMA) doit être choisi via ACF/PACF — c'est une exigence explicite de l'énoncé (§1.3), au-delà de la décomposition classique.

**Exemple d'ancrage utilisé dans tout ce document** : la série *Monthly Champagne Sales* (ventes mensuelles de champagne Perrin Frères), 105 observations de janvier 1964 à septembre 1972, aucune valeur manquante. C'est l'option A du fichier `DATASETS_Kaggle_Projet.md`.

---

## Étape 1 — Management de projet

**Exigence** : produire un diagramme de Gantt couvrant les 10h (par tranches de 2h) et répartir les rôles dans le binôme ; mettre en place un espace de travail commun.

**Théorie** : ce n'est pas une théorie mathématique mais une compétence de gestion de projet — anticiper que la partie "prédiction" (étape 8) est souvent bâclée faute de temps si elle n'est pas budgétée dès le départ.

**Exemple travaillé** — proposition de découpage utilisée pour le projet Champagne :

| Tranche | Travail prévu | Livrable intermédiaire |
|---|---|---|
| 0h–2h | Récupération des données, lecture de l'énoncé, Gantt, rôles | Données importées + plan de travail |
| 2h–4h | Recherche bibliographique et contextualisation | Source Kaggle + contexte économique |
| 4h–6h | Exploration, visualisations, ACF/PACF | Graphiques et statistiques descriptives |
| 6h–8h | Tests, choix additif/multiplicatif, décomposition | Coefficients saisonniers + CVS |
| 8h–10h | Prévisions, comparaison des erreurs, rédaction | Rapport final + code en annexe |

---

## Étape 2 — Recherche bibliographique

**Exigence** : vérifier si la série (ou une série similaire) a déjà été étudiée ailleurs, et le documenter en bibliographie.

**Théorie** : en analyse de séries temporelles, savoir qu'une série a déjà été étudiée permet de comparer sa propre méthodologie à une référence, et de justifier certains choix (ex : pourquoi tel modèle est classiquement utilisé pour ce type de données).

**Exemple travaillé** : la série Champagne est un jeu de données pédagogique très utilisé (variante du classique *Perrin Freres monthly champagne sales*), fréquemment citée dans les cours de séries temporelles pour illustrer une saisonnalité annuelle forte combinée à une tendance. Une recherche bibliographique correcte citerait la source Kaggle, et éventuellement des articles ou tutoriels utilisant la même série pour comparer les méthodes de décomposition.

---

## Étape 3 — Présenter et contextualiser les données

**Exigence** : indiquer la source des données, la période d'étude, l'unité des variables, et si une saisonnalité est attendue a priori.

**Théorie** :
- **Série temporelle (série chronologique)** : suite d'observations $X_t$ indexées dans le temps, où l'ordre et la dépendance temporelle sont l'information principale (contrairement à des données i.i.d.).
- Avant toute analyse, il faut savoir répondre à : quelle est la fréquence (mensuelle, hebdomadaire...) ? Combien de cycles saisonniers complets sont couverts (minimum 3 recommandé) ? Y a-t-il des valeurs manquantes ?

**Exemple travaillé** :
- Source : Kaggle, *Monthly Champagne Sales*.
- Période : janvier 1964 à septembre 1972.
- Fréquence : mensuelle, 105 observations.
- Valeurs manquantes : 0.
- Saisonnalité attendue : oui, a priori annuelle ($p=12$), car les ventes de champagne sont culturellement liées aux fêtes de fin d'année.
- Cycles complets disponibles : environ 8 ans complets → largement suffisant (> 3 cycles requis).

---

## Étape 4 — Explorer les données

**Exigence** : calculer des descripteurs statistiques, visualiser la série à différents pas de temps, et produire les fonctions ACF (et PACF en option).

### 4.1 Descripteurs statistiques

**Théorie** : moyenne, écart-type, minimum, maximum, médiane — permettent de résumer le niveau et la dispersion de la série avant toute modélisation.

**Exemple travaillé** (calculé sur les 105 observations) :

| Indicateur | Valeur |
|---|---:|
| Moyenne | 4761,15 |
| Écart-type | 2553,50 |
| Minimum | 1413,00 |
| Médiane (Q2) | 4217,00 |
| 1er quartile (Q1) | 3113,00 |
| 3e quartile (Q3) | 5221,00 |
| Maximum | 13916,00 |

L'écart-type élevé par rapport à la moyenne (plus de 50 %) confirme une forte variabilité — cohérent avec une saisonnalité marquée.

### 4.2 Visualisation à différents pas de temps

**Théorie** : visualiser la même série à plusieurs granularités (ex : mensuelle vs annuelle) aide à séparer visuellement tendance et saisonnalité avant tout calcul.

**Exemple travaillé** : le graphique `01_serie_temporelle.png` montre une tendance globalement croissante avec des pics récurrents de fin d'année ; `02_profils_saisonniers.png` superpose chaque année (profils saisonniers) et montre que le pic de décembre s'accentue avec les années — un premier indice visuel en faveur d'un modèle **multiplicatif**.

### 4.3 ACF et PACF

**Définition — ACF (fonction d'autocorrélation)** : $\rho(k) = \gamma(k)/\gamma(0)$ mesure la corrélation entre la série $X_t$ et elle-même décalée de $k$ pas de temps ($X_{t+k}$). En clair : *"est-ce que la valeur d'aujourd'hui ressemble à la valeur d'il y a $k$ mois ?"*. $k$ s'appelle le **lag** (retard/décalage).

**Comment le lire sur un graphique (corrélogramme)** :
- Axe horizontal = le lag $k$ (0, 1, 2, 3...).
- Axe vertical = la valeur de $\rho(k)$, entre -1 et 1.
- Chaque barre = l'autocorrélation à ce lag précis.
- Une **zone grisée/pointillée horizontale** représente l'intervalle de confiance (souvent à 95 %) : toute barre qui dépasse cette bande est considérée comme statistiquement significative (pas due au hasard). Une barre qui reste dans la bande = autocorrélation non significative, proche de 0.

**Théorie — ce qu'on cherche à repérer** :
- **$\rho(0) = 1$ toujours** (une série est parfaitement corrélée avec elle-même) — c'est la première barre, normale, à ignorer dans l'interprétation.
- **Pic marqué à un lag précis** (ex : $k=12$ pour des données mensuelles) → saisonnalité à cette période. Si en plus on voit des pics secondaires à $k=24$, $k=36$... (multiples de 12) qui décroissent progressivement, c'est une confirmation supplémentaire de saisonnalité annuelle.
- **Décroissance lente sur de nombreux lags** (les barres restent hautes longtemps avant de redescendre) → signale une série **non stationnaire**, typiquement une tendance présente qu'il faudra différencier avant de modéliser un ARMA.
- **Décroissance rapide vers 0** (2-3 lags puis quasi nul) → série plus proche d'un bruit blanc ou déjà stationnaire.
- **Bruit blanc pur** : toutes les barres restent dans la bande de confiance, aucun motif reconnaissable.

**Définition — PACF (fonction d'autocorrélation partielle)** : mesure la corrélation entre $X_t$ et $X_{t+k}$ **après avoir retiré l'effet des lags intermédiaires** ($1, 2, ..., k-1$). C'est la "corrélation nette" à ce lag précis, sans la contamination des lags plus courts.

**Pourquoi avoir les deux (ACF + PACF) — règle de choix du modèle AR/MA** :

| Motif observé | ACF | PACF | Modèle suggéré |
|---|---|---|---|
| Coupe nette après le lag $q$, puis quasi nulle | décroît progressivement | — | **MA(q)** |
| Coupe nette après le lag $p$, puis quasi nulle | — | décroît progressivement | **AR(p)** |
| Les deux décroissent progressivement (pas de coupure nette) | décroît | décroît | **ARMA(p,q)** — combinaison des deux |
| Les deux restent dans la bande de confiance dès le lag 1 | ~0 | ~0 | Bruit blanc, pas de modèle AR/MA nécessaire |

En résumé : **l'ACF aide à repérer l'ordre MA ($q$)**, **la PACF aide à repérer l'ordre AR ($p$)** — c'est la méthode de Box-Jenkins classique.

**Exemple travaillé** : sur la série Champagne, l'ACF (fichier `05_acf_pacf.png`) montre un pic très net au lag 12 (et des échos aux lags 24, 36), cohérent avec la saisonnalité annuelle détectée visuellement à l'étape 4.2. La décroissance n'est pas immédiate non plus sur les premiers lags, ce qui confirme la présence d'une tendance (série non stationnaire en niveau, cohérent avec le test ADF de l'étape 5.1). La combinaison "pic saisonnier fort + tendance visible" est un argument fort pour un modèle **SARIMA** (saisonnalité de période 12) plutôt qu'un simple ARIMA — voir §8.4.

---

## Étape 5 — Tests sur la série

**Exigence** : réaliser un test de stationnarité (Dickey-Fuller augmenté), un test de tendance, un test de Pettitt (rupture), et éventuellement d'autres tests.

### 5.1 Test de stationnarité (ADF)

**Définition** : une série est **stationnaire** si sa moyenne, sa variance et sa structure d'autocorrélation ne changent pas dans le temps.

**Théorie** :
- $H_0$ : la série est **non stationnaire** (présence d'une racine unitaire).
- $H_1$ : la série est stationnaire.
- Règle de décision : on rejette $H_0$ si la $p\text{-value} < 0{,}05$ → dans ce cas, la série est considérée comme stationnaire.

**Exemple travaillé** : sur la série Champagne brute, on s'attend à un test **ne rejetant pas $H_0$** (série non stationnaire), car il y a à la fois une tendance et une saisonnalité fortes. Une statistique ADF simplifiée calculée sans `statsmodels` donne une valeur de $t \approx -6{,}13$ — mais la $p$-value de référence nécessite `statsmodels` (`pip install statsmodels`) pour être interprétée rigoureusement dans le rapport.

### 5.2 Test de tendance (Mann-Kendall)

**Définition** : test non paramétrique qui vérifie la présence d'une tendance monotone (croissante ou décroissante), sans supposer de forme linéaire précise.

**Théorie** :
- $H_0$ : pas de tendance.
- $H_1$ : tendance monotone existe.
- On calcule une statistique $S$, un $\tau$ (tau de Kendall, signe de la tendance), un $z$ (statistique normalisée) et une $p$-value.
- Décision : si $p < 0{,}05$ et $\tau > 0$ → tendance croissante significative.

**Exemple travaillé** (résultat réel du calcul sur la série Champagne) :

| Statistique | Valeur |
|---|---:|
| $S$ | 1408 |
| $\tau$ | 0,258 |
| $z$ | 3,896 |
| $p$-value | 0,0000979 |
| Décision | tendance croissante significative |

Interprétation : $p < 0{,}05$ et $\tau > 0$ → on confirme statistiquement ce que le graphique suggérait déjà : les ventes augmentent significativement sur la période.

### 5.3 Test de Pettitt (rupture)

**Définition** : détecte un point de rupture dans le niveau central (la moyenne) d'une série, sans supposer de forme paramétrique.

**Théorie** :
- $H_0$ : pas de changement de tendance centrale.
- $H_1$ : présence d'une rupture à une date donnée.
- On calcule une statistique $K$ (maximum d'une somme de rangs cumulée) et sa $p$-value associée.

**Exemple travaillé** (résultat réel) :

| Statistique | Valeur |
|---|---:|
| $K$ | 1238 |
| Date de rupture détectée | Septembre 1966 |
| $p$-value | 0,000765 |
| Décision | rupture probable |

Interprétation : le test identifie un changement de niveau moyen autour de septembre 1966. Dans un rapport, il faut commenter cette rupture : est-ce un vrai changement structurel (ex : changement dans la production/distribution) ou un artefact lié à la longueur encore courte de la série à cette date ? C'est exactement le type de discussion attendu à l'étape 7 (validation).

---

## Étape 6 — Choisir un modèle de décomposition

**Exigence** : choisir entre modèle additif et multiplicatif, extraire la tendance, calculer les coefficients saisonniers si besoin, produire la série CVS.

### 6.1 Modèles de composition

**Théorie** :

| Modèle | Équation | Utilisation |
|---|---|---|
| Additif | $X_t = m_t + s_t + e_t$ | Amplitude saisonnière constante quel que soit le niveau de la tendance. |
| Multiplicatif | $X_t = m_t \times s_t \times e_t$ | Amplitude saisonnière proportionnelle au niveau de la tendance. |

### 6.2 Méthodes de choix du modèle

**Théorie** — trois méthodes possibles :
1. **Méthode de la bande** : tracer des droites par les maxima et les minima ; parallèles → additif, divergentes → multiplicatif.
2. **Méthode du profil** : superposer les cycles saisonniers ; courbes parallèles → additif, écart qui s'accentue → multiplicatif.
3. **Méthode de Buys-Ballot** : régression de l'écart-type annuel $s_r$ sur la moyenne annuelle $\bar{y}$ : $s_r = a\bar{y} + b$. Si $a \approx 0$ → additif ; si $a \neq 0$ → multiplicatif.

**Exemple travaillé** (Buys-Ballot, calculé sur 9 années complètes) :

| Statistique | Valeur |
|---|---:|
| Pente $a$ | 0,807 |
| Ordonnée à l'origine $b$ | -1425,25 |
| Corrélation | 0,841 |
| Décision | **multiplicatif** |

Une pente de 0,807 (nettement différente de 0) et une forte corrélation (0,841) entre moyenne annuelle et écart-type annuel confirment que l'amplitude saisonnière grandit avec le niveau des ventes : le modèle **multiplicatif** est le plus adapté. Ce résultat est cohérent avec l'observation visuelle de l'étape 4 (pic de décembre qui s'accentue avec les années).

### 6.3 Estimation de la tendance

**Théorie — moyenne mobile centrée**, pour une période $p$ paire ($p=2k$, ex : $p=12$ donc $k=6$) :
$$m_{p,t} = \frac{1}{p}\left(\frac{X_{t-k}}{2} + \sum_{i=-k+1}^{k-1} X_{t+i} + \frac{X_{t+k}}{2}\right)$$

**Ce que dit cette formule, en clair** — l'idée est simplement de faire **une moyenne glissante sur $p$ mois autour du point $t$**, pour lisser la saisonnalité et ne garder que la tendance de fond :

- $m_{p,t}$ : la valeur de la tendance qu'on calcule, à l'instant $t$ ("m indice p, t" — voir le glossaire des symboles).
- $\frac{1}{p}$ : on divise par $p$ parce qu'on fait une **moyenne** — comme n'importe quelle moyenne, on additionne des valeurs puis on divise par leur nombre.
- $\sum_{i=-k+1}^{k-1} X_{t+i}$ : on additionne les valeurs observées $X$ de $k-1$ mois avant $t$ jusqu'à $k-1$ mois après $t$ (tous les mois "du milieu", sans les deux extrêmes).
- $\frac{X_{t-k}}{2}$ et $\frac{X_{t+k}}{2}$ : les deux valeurs **aux extrémités** de la fenêtre (le tout premier et le tout dernier mois de la fenêtre) ne comptent que pour **moitié**. C'est une astuce technique nécessaire uniquement quand $p$ est **pair** : comme $p=12$ mois ne peut pas être centré parfaitement sur un seul mois (il y a 6 mois avant et 6 mois après, sans mois central unique), on prend une demi-part de chaque extrémité pour que la fenêtre reste bien centrée sur $t$ et que la somme des poids fasse exactement $p$.

**Exemple numérique concret** (pour $p=12$, $k=6$, donc une fenêtre de 13 valeurs au total : 11 valeurs complètes + 2 demi-valeurs) :
$$m_{12,t} = \frac{1}{12}\left(\frac{X_{t-6}}{2} + X_{t-5} + X_{t-4} + \dots + X_{t+4} + X_{t+5} + \frac{X_{t+6}}{2}\right)$$

Concrètement : pour estimer la tendance du mois de juin 1968 par exemple, on prend les ventes de décembre 1967 à décembre 1968 (13 mois), on compte les deux mois extrêmes (les deux décembre) pour moitié chacun, on additionne le tout, et on divise par 12. Le résultat "lisse" la saisonnalité car chaque mois de l'année (haute ou basse saison) apparaît exactement une fois dans la fenêtre.

**Puis une droite de tendance** est ajustée sur cette moyenne mobile, par régression linéaire classique :
$$\beta_1 = \frac{\text{cov}(m_{p,t}, t)}{\text{var}(t)}, \quad \beta_0 = \bar{m}_{p,t} - \beta_1 \bar{t}$$

**Ce que dit cette formule, en clair** — c'est exactement la formule d'une régression linéaire simple $y = \beta_1 x + \beta_0$, où $y = m_{p,t}$ (la moyenne mobile calculée juste avant) et $x = t$ (le temps, 1, 2, 3...) :

- $\beta_1$ (la **pente**) : "covariance de $m_{p,t}$ et $t$, sur variance de $t$" — c'est la formule standard de la pente d'une droite de régression. Elle répond à : *"en moyenne, de combien la tendance augmente-t-elle à chaque mois qui passe ?"*
- $\beta_0$ (l'**ordonnée à l'origine**) : "moyenne de $m_{p,t}$, moins pente fois moyenne de $t$" — c'est la valeur théorique de la droite à $t=0$, calculée pour que la droite passe par le point moyen $(\bar{t}, \bar{m}_{p,t})$.

**Exemple travaillé** : sur la série Champagne, la droite de tendance ajustée sur la moyenne mobile centrée d'ordre 12 donne :
- Pente ($\beta_1$) : **24,08 unités/mois**
- Ordonnée à l'origine ($\beta_0$) : **3608,39**

Autrement dit, les ventes augmentent en moyenne d'environ **24 unités chaque mois** sur la période étudiée ; la droite de tendance estimée s'écrit $\hat{m}_t = 24{,}08 \times t + 3608{,}39$, où $t$ est le numéro du mois depuis le début de la série.

### 6.4 Coefficients saisonniers et CVS (modèle multiplicatif retenu)

**Théorie** :
- Coefficient brut : $\hat{s}_j = \text{moyenne de } (X_t / \hat{m}_t)$ pour chaque mois $j$.
- Coefficient normalisé : $s_j^* = \hat{s}_j / \bar{s}$, avec $\bar{s} = \frac{1}{p}\sum_{i=1}^p \hat{s}_i$.
- Propriété de vérification : la moyenne des $s_j^*$ doit valoir environ **1**.
- CVS : $X_t^* = X_t / s_t^*$.
- Résidu multiplicatif : $e_t = X_t / (\hat{m}_t \times s_t^*)$.

**Exemple travaillé** — coefficients saisonniers normalisés calculés sur la série Champagne :

| Mois | Coefficient $s_j^*$ |
|---|---:|
| Janvier | 0,763 |
| Février | 0,683 |
| Mars | 0,800 |
| Avril | 0,820 |
| Mai | 0,862 |
| Juin | 0,874 |
| Juillet | 0,741 |
| Août | 0,363 |
| Septembre | 0,935 |
| Octobre | 1,200 |
| Novembre | 1,762 |
| Décembre | 2,198 |

Interprétation : décembre vend en moyenne **2,2 fois plus** que le niveau de tendance du moment, tandis qu'août vend seulement **36 %** du niveau de tendance (creux estival typique, cohérent avec des fermetures/vacances de production). La moyenne de ces 12 coefficients est bien proche de 1, ce qui valide le calcul.

---

## Étape 7 — Valider le modèle

**Exigence** : analyser les résidus (graphiques/tableaux commentés), repérer les valeurs mal ajustées.

**Théorie** : pour un modèle multiplicatif, le résidu $e_t = X_t / (\hat{m}_t \times s_t^*)$ doit être centré autour de **1** et sans structure résiduelle particulière (pas de tendance ni de saisonnalité restante) si le modèle est bien spécifié.

**Exemple travaillé** : sur la série Champagne (`03_decomposition_multiplicative.png`, `04_residus.png`), les résidus oscillent globalement autour de 1, mais quelques mois s'écartent nettement (notamment autour de valeurs extrêmes comme le creux d'août 1972 à 1413 unités). Un résidu qui s'écarte fortement doit être commenté : est-ce un événement ponctuel (grève, rupture de stock, effet promotionnel) que le modèle tendance+saisonnalité ne peut pas capturer par construction ? C'est précisément le type de limite à documenter à cette étape plutôt qu'à ignorer.

---

## Étape 8 — Prédire

**Exigence** : prévoir à court terme par (a) une méthode paramétrique (tendance + coefficients saisonniers) **et** (b) une méthode de lissage, puis comparer.

### 8.1 Méthode paramétrique

**Théorie** :
- Additif : $\hat{x}_{T+h} = \hat{m}_{T+h} + \hat{s}_{T+h}$
- Multiplicatif : $\hat{x}_{T+h} = \hat{m}_{T+h} \times \hat{s}_{T+h}$, avec $\hat{m}_{T+h} = a(T+h) + b$

On prolonge simplement la droite de tendance et on réapplique le coefficient saisonnier du mois correspondant.

### 8.2 Lissage exponentiel

**Théorie** — trois niveaux, du plus simple au plus complet, chacun construit sur le précédent :

| Méthode | Cas d'usage | Ce qu'elle ajoute |
|---|---|---|
| Lissage exponentiel simple (LES/SES) | Pas de tendance, pas de saisonnalité | Une moyenne qui s'auto-corrige à chaque nouvelle observation |
| Lissage de Holt (LED) | Tendance locale, pas de saisonnalité | Un deuxième lissage pour estimer la pente |
| Holt-Winters (HW) | Tendance et saisonnalité | Une troisième équation pour la composante saisonnière |

*Le contenu détaillé ci-dessous provient d'une relecture directe des pages scannées du cours (`raw_cours/IMG_0946.HEIC` à `IMG_0950.HEIC`, pages 20 à 24), pas seulement du résumé synthétique.*

#### 8.2.1 Lissage Exponentiel Simple (LES/SES) en détail

**Modèle** : $x_t = a + e_t$ — une série sans tendance ni saisonnalité, juste du bruit autour d'un niveau constant $a$.

**L'idée fondatrice** : la formule ne sort pas de nulle part — elle vient de la résolution d'un problème de minimisation par moindres carrés pondérés :
$$\min_a \sum_{j=0}^{T-1} \beta^j (x_{T-j} - a)^2$$

Lecture : *"on cherche la constante $a$ qui s'ajuste le mieux aux données, en donnant à chaque observation passée $x_{T-j}$ un poids $\beta^j$ — plus $j$ est grand (donnée ancienne), plus ce poids est petit."* C'est cette décroissance géométrique des poids qui donne le nom "**exponentiel**" à la méthode. En résolvant ce problème, on obtient :
$$\hat{x}_T(h) = (1-\beta)\sum_{j=0}^{T-1}\beta^j x_{T-j}$$

**Sens de $\beta$ (à retenir précisément)** : la formule de mise à jour encadrée dans le cours est :
$$\hat{x}_T(h) := \beta\,\hat{x}_{T-1}(h) + (1-\beta)\,x_T$$

Donc $\beta$ est le poids donné à **l'ancienne prévision** (la mémoire du passé), et $(1-\beta)$ le poids donné à **la nouvelle observation**. Conséquence :
- $\beta$ proche de **0** → prévision **souple** : presque tout le poids va sur la donnée la plus récente ; cas extrême $\beta=0$ → la prévision est exactement égale à la dernière valeur observée.
- $\beta$ proche de **1** → prévision **rigide** : forte mémoire du passé lointain ; cas extrême $\beta=1$ → la prévision ne bouge jamais, elle reste égale à sa valeur d'initialisation.

**Deuxième écriture, plus intuitive** — la même formule se réécrit :
$$\hat{x}_T(h) = \hat{x}_{T-1}(h) + (1-\beta)\big(x_T - \hat{x}_{T-1}(h)\big)$$

Autrement dit : *nouvelle prévision = ancienne prévision + une fraction de l'erreur qu'on vient de commettre.* Le terme $x_T - \hat{x}_{T-1}(h)$ est littéralement "de combien je me suis trompé la dernière fois", et $(1-\beta)$ décide de la part de cette erreur qu'on corrige. C'est l'intuition commune à **toutes** les formules de lissage exponentiel de ce cours (Holt, Holt-Winters) : on ajuste sa dernière estimation d'une fraction de la surprise observée.

**Initialisation** : $\hat{x}_1(h) = x_1$ (ou la moyenne globale $\bar{x}$). Remarque du cours : ce choix initial importe peu en pratique car il est vite "oublié" — d'autant plus vite que $\beta$ est proche de 0.

**Exemple travaillé (issu du cours)** — série trimestrielle des ventes d'essence aviation en France. Le tableur du cours calcule la colonne `LES = 0,4*B3 + 0,6*C3`, c'est-à-dire : nouvelle valeur lissée $= 0{,}4\times$(nouvelle observation)$+0{,}6\times$(valeur lissée précédente). En comparant à la formule officielle $\beta\hat{x}_{T-1}+(1-\beta)x_T$ : le "$\alpha=0{,}4$" du tableur joue en réalité le rôle de $(1-\beta)$, donc le $\beta$ formel de cet exemple vaut $0{,}6$. **Cette confusion entre le "$\alpha$" du tableur (poids sur la nouvelle donnée) et le "$\beta$" du cours (poids sur la mémoire) est une source d'erreur fréquente** — toujours vérifier lequel des deux un document ou un logiciel appelle sa "constante de lissage".

Le cours compare ensuite les erreurs (EM, EAM, EQM) pour $\alpha=0{,}4$ et $\alpha=0{,}5$, puis balaie $\alpha$ de 0,1 à 0,9 sur le dernier tiers de la série pour trouver la valeur qui minimise l'EQM — c'est la **méthode objective** de choix de la constante de lissage (par opposition à la méthode subjective, voir §8.2.5).

#### 8.2.2 Lissage Exponentiel Double de Holt (LED)

**Modèle** : $x_t = b + at + e_t$ — une **tendance linéaire locale** ($a$ = pente, $b$ = ordonnée à l'origine), toujours sans saisonnalité.

Même logique de minimisation, mais on ajuste maintenant une **droite** plutôt qu'une constante :
$$\min_a \sum_{j=0}^{T-1}\beta^j\big(x_{T-j} - (b+ah)\big)^2$$

**Pourquoi "double"** : on effectue **deux** lissages simples, l'un appliqué sur l'autre :
$$S_1(T) = (1-\beta)\sum_{j=1}^{T-1}\beta^j x_{T-j} \quad\text{(lissage simple de la série brute)}$$
$$S_2(T) = (1-\beta)\sum_{j=1}^{T-1}\beta^j S_1(T-j) \quad\text{(lissage simple de la série déjà lissée)}$$

La pente et le niveau estimés se déduisent ensuite de $S_1$ et $S_2$ :
$$\hat{a}_T = \frac{1-\beta}{\beta}\big(S_1(T)-S_2(T)\big), \qquad \hat{b}_T = 2S_1(T) - S_2(T)$$

**Prévision** : $\hat{x}_T(h) = \hat{b}_T + \hat{a}_T h$ (une droite prolongée de $h$ pas à partir du niveau et de la pente actuels).

**Initialisation** : $\hat{a}_2 = x_2 - x_1$, $\hat{b}_2 = x_2$.

**Formule de mise à jour** (dérivée de ce qui précède, pour éviter de recalculer les sommes entières à chaque étape) :
$$\hat{a}_T = \hat{a}_{T-1} + (1-\beta)^2\big(x_T - \hat{x}_{T-1}(1)\big)$$
$$\hat{b}_T = \hat{b}_{T-1} + \hat{a}_{T-1} + (1-\beta^2)\big(x_T - \hat{x}_{T-1}(1)\big)$$

On retrouve le même schéma que pour le LES : *ancienne estimation + un certain poids × la dernière erreur de prévision.*

**Exemple travaillé (issu du cours)** — tableur mensuel avec "ALPHA = 0,4" (là encore, ce $0{,}4$ correspond en fait à $(1-\beta)$ dans la notation formelle), colonnes *1er lissage* ($S_1$), *2nd lissage* ($S_2$), $a$, $b$, et *PREV*. Arithmétique annotée à la main sur le document :
- $63{,}449 = (0{,}4 \times 65) + (0{,}6 \times 62{,}415)$ → mise à jour de $S_1$ : $0{,}4\times$(nouvelle observation)$+0{,}6\times S_1$ précédent.
- $1{,}080 = (0{,}4/0{,}6)\times(63{,}449 - 61{,}829)$ → correspond à $\hat{a}_T = \frac{1-\beta}{\beta}(S_1-S_2)$ avec $(1-\beta)/\beta = 0{,}4/0{,}6$.
- $65{,}069 = (2\times 63{,}449) - 61{,}829$ → correspond à $\hat{b}_T = 2S_1(T)-S_2(T)$.

Ceci confirme que le "$\alpha=0{,}4$" du tableur est bien le $(1-\beta)$ formel, donc $\beta=0{,}6$ dans cet exemple.

#### 8.2.3 Holt-Winters (HW) — version non saisonnière

**Modèle** : $x_t = b + at + e_t$ (identique à Holt — c'est une autre manière d'implémenter la même idée, avec deux constantes de lissage $\alpha, \gamma$ au lieu d'une seule $\beta$).

**Initialisation** : $\hat{b}_1 = x_1$, $\hat{a}_1 = x_1 - x_0$ (nécessite un point $x_0$ *avant* la première observation).

**Mise à jour** :
$$\hat{b}_T = \alpha\, x_t + (1-\alpha)(\hat{b}_{T-1}+\hat{a}_{T-1}) \qquad \text{(niveau)}$$
$$\hat{a}_T = \gamma(\hat{b}_T - \hat{b}_{T-1}) + (1-\gamma)\hat{a}_{T-1} \qquad \text{(tendance)}$$

**Prévision** : $\hat{x}_T(h) = \hat{b}_T + \hat{a}_T h$.

Remarque du cours : plus de flexibilité (2 réglages au lieu d'un), mais plus difficile à régler — si $\alpha$ et $\gamma$ sont tous les deux proches de 1, la prévision est lisse (fort poids du passé).

#### 8.2.4 Holt-Winters — version saisonnière additive (la méthode complète)

**Modèle** : $x_t = b + at + s_t + e_t$, avec $p$ = la période de la saisonnalité (ex : $p=12$ pour des données mensuelles).

**Prévision — attention à la structure par morceaux** :
$$\hat{x}_T(h) = \begin{cases} \hat{a}_T h + \hat{b}_T + \hat{S}_{T+h-p} & \text{si } 1 \leq h \leq p \\ \hat{a}_T h + \hat{b}_T + \hat{S}_{T+h-2p} & \text{si } p < h \leq 2p \\ \dots & \end{cases}$$

**Pourquoi cette structure** : quand on prévoit au-delà d'un cycle saisonnier complet, on n'a pas encore d'estimation "plus fraîche" du facteur saisonnier pour ce mois futur — on réutilise donc le facteur saisonnier d'**une période complète en arrière**, et on répète l'opération à chaque nouveau multiple de $p$ dépassé.

**Mise à jour — trois paramètres cette fois** :
$$\hat{a}_T = \beta(\hat{b}_T - \hat{b}_{T-1}) + (1-\beta)\hat{a}_{T-1} \qquad \text{(tendance)}$$
$$\hat{b}_T = \alpha(x_t - \hat{S}_{T-p}) + (1-\alpha)(\hat{b}_{T-1}+\hat{a}_{T-1}) \qquad \text{(niveau, saisonnalité retirée)}$$
$$\hat{S}_T = \gamma(x_t - \hat{b}_T) + (1-\gamma)\hat{S}_{T-p} \qquad \text{(facteur saisonnier)}$$

Interprétation donnée par le cours pour ces trois équations :
1. **Tendance** = moyenne pondérée entre *combien le niveau a bougé* depuis la dernière fois, et la pente précédemment estimée.
2. **Niveau** = moyenne pondérée entre *l'observation à laquelle on a retranché sa composante saisonnière*, et le niveau+tendance précédents.
3. **Facteur saisonnier** = moyenne pondérée entre *l'observation à laquelle on a retranché le niveau actuel*, et le facteur saisonnier d'une période complète en arrière.

**Remarque sur les notations** : ici $\hat{a}$ = tendance (pente) et $\hat{b}$ = niveau (ordonnée à l'origine), cohérent avec le modèle $x_t = b+at+\dots$. Le cheat sheet (`SAÉ 3-03 Time Series Forecasting Cheat Sheet - v3.md`) utilise la convention inverse ($\hat{a}$=niveau, $\hat{b}$=tendance). C'est la même mathématique, seuls les noms sont échangés — à garder en tête en comparant les deux documents.

#### 8.2.5 Choix de la constante de lissage

- **Méthode subjective** : choisir selon la rigidité souhaitée — $\beta \in [0{,}7\,;\,0{,}99]$ pour une prévision rigide, $\beta \in [0{,}01\,;\,0{,}3]$ pour une prévision souple.
- **Méthode objective** : minimiser un critère d'erreur calculé sur les erreurs de prévision passées (les mêmes EM/EAM/EQM que la formule officielle du cours ci-dessous, identiques à celles de l'étape 8.3) :

$$EM = \frac{1}{N}\sum_{i=1}^N (x_{i+1}-\hat{x}_i(1)), \quad EAM = \frac{1}{N}\sum_{i=1}^N|x_{i+1}-\hat{x}_i(1)|, \quad EQM = \frac{1}{N}\sum_{i=1}^N(x_{i+1}-\hat{x}_i(1))^2$$

#### 8.2.6 Limites du lissage exponentiel (verbatim du cours, page 24)

**Avantage** : fournir une prévision "bon marché" (peu coûteuse en moyens de calcul).

**Deux inconvénients** :
1. Rien ne garantit l'optimalité de la méthode sur une série de données donnée — les méthodes de lissage exponentiel sont parfois loin d'être les mieux adaptées.
2. Elles sont incapables de fournir des **intervalles de prévision** (un intervalle contenant la vraie valeur avec une probabilité donnée) — aucun cadre probabiliste.

Remarque de clôture du cours : à l'exception de la version multiplicative de Holt-Winters, les méthodes de lissage exponentiel correspondent à des modèles probabilistes particuliers — les méthodes probabilistes plus générales (famille ARIMA) permettent de lever ces deux limites.

#### Remarque importante pour le rapport — modèle multiplicatif hors programme

Le cours précise explicitement (page 22) : *"tendance linéaire locale × saisonnalité (modèle multiplicatif), **non-présenté dans ce cours**"* — seule la version **additive** de Holt-Winters est enseignée.

Or, dans l'analyse Champagne (`scripts/analyse_champagne.py`), c'est le **Holt-Winters multiplicatif** qui obtient la meilleure performance (RMSE 306,7 contre 619,2 pour l'additif) — voir §8.3. Pour le rapport SAE, deux options honnêtes :
1. Présenter le **Holt-Winters additif** comme comparaison officielle "dans le programme" (moins précis mais conforme au cours), et mentionner le multiplicatif en complément auto-formé qui améliore la performance — bon point de discussion en conclusion.
2. Garder le multiplicatif mais citer explicitement qu'il a été étudié au-delà du contenu du cours — montre une initiative généralement bien perçue, à condition de le signaler plutôt que de le présenter comme faisant partie du cours.

### 8.3 Validation par les erreurs de prévision

**Théorie** — sur un jeu de test (dernières observations non utilisées pour ajuster le modèle) :

| Métrique | Formule | Nom |
|---|---|---|
| EM | $\frac{1}{N}\sum (x_{i+1} - \hat{x}_i(1))$ | Erreur Moyenne |
| EAM (MAE) | $\frac{1}{N}\sum \lvert x_{i+1} - \hat{x}_i(1)\rvert$ | Erreur Absolue Moyenne |
| EQM (MSE) | $\frac{1}{N}\sum (x_{i+1} - \hat{x}_i(1))^2$ | Erreur Quadratique Moyenne |

Un bon modèle a un EM proche de 0 (pas de biais systématique) et un EQM/RMSE le plus faible possible.

**Exemple travaillé** — comparaison réelle sur les 12 derniers mois de la série Champagne (jeu de test), en comparant décomposition paramétrique et Holt-Winters, en additif et en multiplicatif :

| Modèle | RMSE | MAPE (%) |
|---|---:|---:|
| **Holt-Winters multiplicatif** | **306,66** | **6,63** |
| Décomposition paramétrique multiplicative | 514,57 | 12,12 |
| Holt-Winters additif | 619,25 | 10,32 |
| Décomposition paramétrique additive | 779,60 | 20,20 |

**Conclusion de l'exemple** : le modèle **Holt-Winters multiplicatif** obtient la meilleure performance (RMSE et MAPE les plus faibles), ce qui est cohérent avec le diagnostic de l'étape 6 (Buys-Ballot indiquait un modèle multiplicatif). Les modèles additifs sont clairement moins bons ici car l'amplitude saisonnière n'est pas constante — exactement le type de justification quantitative attendu dans la conclusion du rapport.

### 8.4 Modèle autorégressif (exigence complémentaire, §1.3 de l'énoncé)

**Théorie** : au-delà de la décomposition/lissage, l'énoncé demande de choisir un modèle parmi **AR, MA, ARMA, ARIMA, SARIMA**, en s'appuyant sur l'ACF et la PACF.

- **AR(p)** : la valeur actuelle dépend linéairement de $p$ valeurs passées.
- **MA(q)** : la valeur actuelle dépend linéairement de $q$ erreurs passées.
- **ARMA(p,q)** : combinaison des deux, pour une série déjà stationnaire.
- **ARIMA(p,d,q)** : ARMA appliqué après $d$ différenciations, pour rendre une série non stationnaire stationnaire.
- **SARIMA(p,d,q)(P,D,Q)[p]** : ARIMA avec une composante saisonnière explicite de période $p$.

**Exemple travaillé** : pour la série Champagne, la présence d'une tendance (donc $d \geq 1$) et d'une saisonnalité forte à $p=12$ (vue sur l'ACF) oriente naturellement vers un **SARIMA**, par exemple $SARIMA(1,1,1)(1,1,1)_{12}$ — c'est le modèle exploratoire utilisé en repère dans le script (nécessite `statsmodels`).

---

## Résumé — table de correspondance étape ↔ théorie ↔ résultat Champagne

| Étape | Concept théorique clé | Résultat sur l'exemple Champagne |
|---|---|---|
| 3. Contextualisation | Fréquence, cycles, valeurs manquantes | Mensuel, 105 points, 0 manquant, ≥ 8 cycles |
| 4. Exploration | Statistiques descriptives, ACF | Moyenne 4761, écart-type 2554, pic ACF à lag 12 |
| 5. Tests | Mann-Kendall, Pettitt, ADF | Tendance croissante ($p<0{,}0001$), rupture en 1966-09 |
| 6. Décomposition | Buys-Ballot, coefficients saisonniers | Modèle multiplicatif, pic décembre ×2,2, creux août ×0,36 |
| 7. Validation | Analyse des résidus | Résidus centrés sur 1, écarts sur mois extrêmes |
| 8. Prédiction | Comparaison EM/EAM/EQM | Holt-Winters multiplicatif meilleur (RMSE 306,7, MAPE 6,6 %) |

---

## Fichiers sources de cet exemple

- Script : `scripts/analyse_champagne.py`
- Données : `data/monthly_champagne_sales.csv`
- Résultats numériques : `outputs/champagne/tables/*.csv`, `outputs/champagne/tables/tests_statistiques.json`
- Graphiques : `outputs/champagne/figures/*.png`
- Rapport généré automatiquement : `outputs/champagne/rapport_champagne.md`
