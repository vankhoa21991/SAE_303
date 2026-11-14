# SAE 3.03 — Exercice : Ventes de champagne

**Groupes concernés (2026)** :

| Classe | Groupe | Noms | Sujet saisi |
|---|---|---|---|
| VCOD | 5 | Rafaly / Rabat | Vente de champagne |

> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.

---

**Série** : Ventes de champagne (Option A) — pas de temps : mensuel (période 12)
**Accès aux données** : Fichier `data/monthly_champagne_sales.csv` (janv. 1964 – sept. 1972, 105 obs.). Déjà traité dans `scripts/analyse_champagne.py` : **ne pas se contenter de ce script**.
**Découpage train/test imposé** : train = 1964–1970 ; test = 1971 – sept. 1972 (21 mois).

### 1. Contexte à documenter (étapes 2-3)
Perrin Frères ; vente de champagne : pic de fin d'année (fêtes) ; contexte économique français 1964-72.
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Saisonnalité forte (η²≈0,84) + tendance croissante significative.

### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : Amplitude qui croît légèrement : additif ou multiplicatif ? Les 3 méthodes du cours donnent-elles le même verdict ? Le dataset dit 105 obs., pas 108 : documenter l'écart.

### 4. Décomposition (étape 6)
- Débat additif/multiplicatif central.
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
Trancher additif/multiplicatif avec les 3 méthodes ; puis HW additif vs multiplicatif sur le test : la méthode de choix a-t-elle bien prédit le meilleur modèle ?

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
