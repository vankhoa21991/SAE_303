# SAE 3.03 — Exercice : Données économiques

**Groupes concernés (2026)** :

| Classe | Groupe | Noms | Sujet saisi |
|---|---|---|---|
| EMS | 1 | Drackle / Hachemi | 10 donne economic |

> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.

---

**Série** : Données économiques — FEDFUNDS (taux directeur de la Fed) — pas de temps : mensuel
**Accès aux données** : Téléchargement FRED : https://fred.stlouisfed.org/series/FEDFUNDS (CSV) ; à lire en R avec `read.csv` puis `ts(x, start=c(1954,7), frequency=12)`. (*Sujet « 10 données économiques » ambigu : FEDFUNDS choisi car dans l'énoncé — à confirmer avec le groupe.*)
**Découpage train/test imposé** : train = jusqu'à fin 2018 ; test = 2019 – 2022 (observer la rupture COVID et la remontée des taux 2022).

### 1. Contexte à documenter (étapes 2-3)
Politique monétaire de la Réserve fédérale : taux, inflation, crises 1980, 2008, 2020.
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Pas de saisonnalité attendue ; tendances par régimes (hausse jusqu'en 1981, baisse, zéro, remontée).

### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : Plusieurs ruptures : un seul modèle de tendance est faux. Taux plancher à ≈ 0 : les prévisions peuvent devenir négatives (absurde économiquement).

### 4. Décomposition (étape 6)
- Pas de modèle saisonnier ; Holt ou LES sur régime récent.
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
Segmenter par Pettitt (récursif) et mesurer l'échec des méthodes sur le test 2019-2022 : que valent les prévisions en période de rupture ?

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
