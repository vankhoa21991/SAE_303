# SAE 3.03 — Exercice : Données environnementales

**Groupes concernés (2026)** :

| Classe | Groupe | Noms | Sujet saisi |
|---|---|---|---|
| VCOD | 7 | Bach / Majde | 2.5 données environnementales |

> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.

---

**Série** : Température moyenne mensuelle à Nottingham (nottem) — pas de temps : mensuel (période 12)
**Accès aux données** : R : `nottem` (datasets, janv. 1920 – déc. 1939, 240 obs., °F).
**Découpage train/test imposé** : train = 1920–1936 ; test = 1937–1939 (36 mois).

### 1. Contexte à documenter (étapes 2-3)
Climat tempéré océanique ; Nottingham Castle Station ; température moyenne de l'air. (*Sujet « 2.5 environnement » : à confirmer avec l'enseignant.*)
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Saisonnalité annuelle très forte et stable, pas de tendance.

### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : Saisonnalité **additive** (température, pas multiplicatif : valeurs proches de zéro/négatives possibles en °C). Une prévision par coefficients saisonniers est quasi parfaite : la vraie question est la qualité des résidus.

### 4. Décomposition (étape 6)
- Additif ; les coefficients sont interprétables physiquement (°F au-dessus/dessous de la moyenne annuelle).
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
Après CVS, la série résiduelle est-elle un bruit blanc ? Tests de Ljung-Box, ACF résidus, normalité ; conclure sur ce qui reste à modéliser (AR faible ?).

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
