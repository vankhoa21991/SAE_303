# SAE 3.03 — Exercice : Données de CO2

**Groupes concernés (2026)** :

| Classe | Groupe | Noms | Sujet saisi |
|---|---|---|---|
| EMS | 8 | Meye-Meye / Sawadogo | Données de CO2 |

> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.

---

**Série** : CO₂ atmosphérique à Mauna Loa (co2) — pas de temps : mensuel (période 12)
**Accès aux données** : R : `co2` (datasets, janv. 1959 – déc. 1997, 468 obs., ppm).
**Découpage train/test imposé** : train = 1959–1990 ; test = 1991–1997 (7 ans). Pour aller plus loin : comparer avec les données Scripps jusqu'à aujourd'hui.

### 1. Contexte à documenter (étapes 2-3)
Courbe de Keeling : cycle de la photosynthèse hémisphère nord, émissions fossiles, accord de Paris.
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Tendance croissante (légèrement convexe) + saisonnalité annuelle d'amplitude constante → additif.

### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : C'est l'exemple vu en TP : ne pas se limiter à `decompose`. Tendance convexe : droite insuffisante, tester un polynôme de degré 2 ; Holt-Winters additif attendu performant — vérifier sur le test.

### 4. Décomposition (étape 6)
- Additif ; comparer tendance linéaire vs quadratique par les résidus.
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
Extrapoler jusqu'en 2025 avec votre meilleur modèle, puis confronter à la valeur réelle connue (~420 ppm) : quel est l'écart et pourquoi ?

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
