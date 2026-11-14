# SAE 3.03 — Exercice : Données de pluie

**Groupes concernés (2026)** :

| Classe | Groupe | Noms | Sujet saisi |
|---|---|---|---|
| EMS | 7 | Accrombessi / Kare | Données de pluie |

> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.

---

**Série** : Précipitations journalières à Boulder, Colorado, USA (1948–2013) — pas de temps : journalier (période ≈ 365) — travail principal sur les totaux mensuels
**Accès aux données** : CSV : `data/boulder-precip.csv` (téléchargé depuis https://raw.githubusercontent.com/ef2020/TextFiles/master/805333-precip-daily-1948-2013.csv). Colonne `HPCP` en pouces, `999.99` = valeur manquante ; **plusieurs relevés par jour → sommer par date** ; jours absents du fichier = jours secs (0).
**Découpage train/test imposé** : Travail sur les totaux mensuels (pouces) : train = 1948-08 → 2003-12 ; test = 2004-01 → 2013-12 (120 mois).

### 1. Contexte à documenter (étapes 2-3)
Station COOP 050843 « BOULDER 2 CO US » (≈ 1650 m d'altitude), climat semi-aride : ~82 % de jours secs, pluviométrie médiane ≈ 17 po/an. Pourquoi la saisonnalité est-elle bimodale (pic au printemps + bosse du monsoon d'été) ?
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Saisonnalité annuelle forte sur les totaux mensuels (pic en mai, creux en hiver) ; série journalière à pics très irréguliers.

### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : Série journalière avec ~82 % de zéros : ne pas décomposer/prévoir directement le quotidien avec les outils classiques — passer aux totaux mensuels. Modèle multiplicatif impossible (mois nuls) : additif. Ne pas interpréter un ADF sur le quotidien comme « stationnaire » sans regarder l'échelle.

### 4. Décomposition (étape 6)
- Additif sur les totaux mensuels (période 12) ; comparer décomposition / ETS / SARIMA(0,1,1)×(0,1,1) au naïf saisonnier sur 120 mois.
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
Proportion de jours secs par mois (climatologie) et stabilité de la climatologie mensuelle par décennie ; ADF / Mann-Kendall / Pettitt sur les totaux mensuels ET annuels : les conclusions sont-elles les mêmes ?

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
