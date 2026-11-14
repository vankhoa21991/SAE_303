# SAE 3.03 — Exercice : Accidents de la route UK

**Groupes concernés (2026)** :

| Classe | Groupe | Noms | Sujet saisi |
|---|---|---|---|
| VCOD | 1 | Ayral / Furgal | 2.6 accidents de la route UK |

> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.

---

**Série** : Conducteurs tués ou gravement blessés au Royaume-Uni (UKDriverDeaths) — pas de temps : mensuel (période 12)
**Accès aux données** : R : `UKDriverDeaths` (datasets, janv. 1969 – déc. 1984, 192 obs.).
**Découpage train/test imposé** : train = 1969–1982 ; test = 1983–1984 (24 mois).

### 1. Contexte à documenter (étapes 2-3)
Accidents de la route au Royaume-Uni ; **loi sur le port obligatoire de la ceinture, 31 janvier 1983**, crise pétrolière 1973-74.
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Saisonnalité annuelle (pic en hiver/fin d'année) + tendance à la baisse + chute en 1983.

### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : Le test (1983-84) est **après la rupture** de la loi : le modèle appris sur le train va sur-prévoir. À exploiter, pas à cacher.

### 4. Décomposition (étape 6)
- Additif probable ; 2 tendances (avant/après) à discuter.
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
Pettitt doit retrouver ≈ janv. 1983. Quantifier l'effet de la loi : (prévision sans loi) − (observé). Que vaut cette estimation ?

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
