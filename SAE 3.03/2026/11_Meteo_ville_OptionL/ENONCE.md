# SAE 3.03 — Exercice : Météo et ville (option L)

**Groupes concernés (2026)** :

| Classe | Groupe | Noms | Sujet saisi |
|---|---|---|---|
| VCOD | 4 | Nzau Ngoy / Livernet | Météo et ville option L |

> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.

---

**Série** : Météo horaire multi-villes — température (Option L) — pas de temps : horaire → agrégé mensuel (période 12)
**Accès aux données** : Fichier `data/kaggle_raw/L_selfishgene-historical-hourly-weather-data/temperature.csv` (colonnes = villes, 2012-10 → 2017-11, en kelvins).
**Découpage train/test imposé** : train = 2012-10 → 2016-11 ; test = 2016-12 → 2017-11 (un cycle annuel complet).

### 1. Contexte à documenter (étapes 2-3)
Choisir **une ville** et la documenter (climat, latitude). Convertir K → °C.
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Saisonnalité annuelle très forte (η²≈0,96), pas de tendance significative (≈ 5 ans).

### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : Valeurs manquantes horaires à traiter avant l'agrégation ; seulement 5 ans → 5 cycles ; ne pas conclure à un 'réchauffement' sur 5 ans.

### 4. Décomposition (étape 6)
- Additif (°C) ; HW additif sans tendance (β=FALSE) à comparer au HW complet.
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
Montrer l'effet de la granularité : cycle jour/nuit (horaire), semaine (rien), année (mensuel). Comparer deux villes sur leurs coefficients saisonniers (amplitude continentale vs océanique).

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
