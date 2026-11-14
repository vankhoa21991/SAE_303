# SAE 3.03 — Exercice : Débit du Nil

**Groupes concernés (2026)** :

| Classe | Groupe | Noms | Sujet saisi |
|---|---|---|---|
| VCOD | 3 | Pujal / Marquier | 2.2 débit du Nil |

> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.

---

**Série** : Débit annuel du Nil à Assouan (Nile) — pas de temps : annuel
**Accès aux données** : R : `Nile` (datasets, 1871–1970, 100 obs., 10⁸ m³).
**Découpage train/test imposé** : train = 1871–1950 ; test = 1951–1970 (20 ans).

### 1. Contexte à documenter (étapes 2-3)
Fleuve du Nil, mesures à Assouan ; barrages (ancien barrage d'Assouan 1902, haut barrage 1970) ; crues.
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Annuel : pas de saisonnalité. Rupture de niveau documentée vers **1898**.

### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : Série classique de test de **Pettitt** (rupture de moyenne ≈ 1898). Ajuster un seul modèle global est une erreur : séparer avant/après.

### 4. Décomposition (étape 6)
- Pas de saisonnalité, tendance = changement de niveau (escalier), pas une droite.
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
Pettitt + ADF avant/après rupture. Prévoir avec LES appris uniquement sur la période post-rupture, comparer avec un LES sur toute la série.

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
