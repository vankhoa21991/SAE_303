# SAE 3.03 — Exercice : Taches solaires

**Groupes concernés (2026)** :

| Classe | Groupe | Noms | Sujet saisi | Variante |
|---|---|---|---|---|
| EMS | 4 | Casares Bello / Sabatier | nombre mensuel de taches solaire | Taches solaires — nombre mensuel (sunspots) |
| VCOD | 2 | Di Scala / Milazzo Guilhou | 2.3 tache solaire | Taches solaires — nombre annuel (sunspot.year) |

> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.

---

## Variante : Taches solaires — nombre mensuel (sunspots) (groupe EMS n°4 — Casares Bello / Sabatier)

**Série** : Taches solaires — nombre mensuel (sunspots) — pas de temps : mensuel, mais cycle d'environ 11 ans (≈ 132 mois)
**Accès aux données** : R : `sunspots` (datasets, janv. 1749 – déc. 1983, 2820 obs.).
**Découpage train/test imposé** : train = jusqu'à 1973 ; test = 1974–1983 (un cycle solaire entier).

#### 1. Contexte à documenter (étapes 2-3)
Qu'est-ce qu'une tache solaire ? Cycle de Schwabe (~11 ans), nombre de Wolf, minimum de Maunder.
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

#### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : **Pas** de saisonnalité annuelle : un pseudo-cycle de période variable (9–14 ans).

#### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : `decompose()` avec frequency = 12 est un **contresens** (le TP01 le fait : à critiquer). La période n'est ni 12 ni constante. Les coefficients 'saisonniers' mensuels n'ont pas de sens physique.

#### 4. Décomposition (étape 6)
- Série positive à variance croissante avec le niveau : tester log ou Box-Cox ; moyenne mobile d'ordre 132 (ou 133).
- Choix additif/multiplicatif justifié (au moins deux méthodes : bande, Buys-Ballot, profils).
- Tendance, coefficients saisonniers (si pertinents), série CVS.
- **À la main** (sur 1 cycle) : 3 valeurs de moyenne mobile, 1 coefficient saisonnier, 1 valeur CVS, puis vérification logicielle.

#### 5. Validation (étape 7)
Résidus : graphique, ACF, histogramme/QQ-plot, Ljung-Box. Lister les 3 observations les moins bien ajustées et les expliquer par un événement réel si possible.

#### 6. Prédiction (étape 8)
1. Décomposition (tendance + saisonnalité si pertinente).
2. Lissage (LES, Holt ou Holt-Winters : justifier, estimer α, β, γ).
3. Modèle AR/MA/ARIMA/SARIMA choisi via ACF/PACF (pas seulement `auto.arima`).
4. Tableau comparatif sur le **test** : RMSE, MAE, MAPE ; verdict argumenté.

#### 7. Question spécifique ⭐
Prouver par l'ACF que le vrai cycle est ≈ 130 mois, refaire la décomposition avec cette période (ou passer en annuel), et comparer avec celle du TP01.


---

## Variante : Taches solaires — nombre annuel (sunspot.year) (groupe VCOD n°2 — Di Scala / Milazzo Guilhou)

**Série** : Taches solaires — nombre annuel (sunspot.year) — pas de temps : annuel
**Accès aux données** : R : `sunspot.year` (datasets, 1700–1988, 289 obs.).
**Découpage train/test imposé** : train = 1700–1958 ; test = 1959–1988 (30 ans, ≈ 3 cycles).

#### 1. Contexte à documenter (étapes 2-3)
Cycle de Schwabe ~11 ans, minimum de Maunder (1645-1715), usage en météo spatiale.
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

#### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Annuel donc pas de saisonnalité infra-annuelle ; pseudo-cycle ≈ 11 ans à caractériser par l'ACF.

#### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : Lisser avec HoltWinters(gamma=FALSE) ne capturera pas le cycle : la prévision à 30 ans sera plate/inefficace. Le montrer, l'expliquer, puis proposer mieux (AR d'ordre ≥ 9 par ex.).

#### 4. Décomposition (étape 6)
- Pas de saisonnalité ; décomposition tendance seule + AR pour le cycle.
- Choix additif/multiplicatif justifié (au moins deux méthodes : bande, Buys-Ballot, profils).
- Tendance, coefficients saisonniers (si pertinents), série CVS.
- **À la main** (sur 1 cycle) : 3 valeurs de moyenne mobile, 1 coefficient saisonnier, 1 valeur CVS, puis vérification logicielle.

#### 5. Validation (étape 7)
Résidus : graphique, ACF, histogramme/QQ-plot, Ljung-Box. Lister les 3 observations les moins bien ajustées et les expliquer par un événement réel si possible.

#### 6. Prédiction (étape 8)
1. Décomposition (tendance + saisonnalité si pertinente).
2. Lissage (LES, Holt ou Holt-Winters : justifier, estimer α, β, γ).
3. Modèle AR/MA/ARIMA/SARIMA choisi via ACF/PACF (pas seulement `auto.arima`).
4. Tableau comparatif sur le **test** : RMSE, MAE, MAPE ; verdict argumenté.

#### 7. Question spécifique ⭐
Ce groupe travaille sur la série **annuelle** (le groupe EMS n°4 sur la mensuelle). Comparer le choix AR par ACF/PACF avec la prévision par lissage sur test de 30 ans.


---

## Barème indicatif (/20)
| Critère | Points |
|---|---|
| Contexte + biblio | 3 |
| Exploration + tests (interprétés) | 4 |
| Décomposition (choix justifié, calcul à la main) | 4 |
| Validation des résidus | 2 |
| Prédictions (3 méthodes, comparaison sur test) | 4 |
| Question spécifique ⭐ | 2 |
| Qualité du rapport, code en annexe | 1 |
