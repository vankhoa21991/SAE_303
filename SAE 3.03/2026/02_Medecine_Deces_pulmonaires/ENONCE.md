# SAE 3.03 — Exercice : Médecine — décès pulmonaires (UK)

**Groupes concernés (2026)** :

| Classe | Groupe | Noms | Sujet saisi | Variante |
|---|---|---|---|---|
| EMS | 2 | Dione / Gouem | 9 donnee de medecine | Décès mensuels par maladies pulmonaires — Royaume-Uni (mdeaths + fdeaths) |
| VCOD | 6 | Lokossa / Chaabani | 2.9 décès mensuels maladies pulmonaires | Décès mensuels par maladies pulmonaires — Royaume-Uni (ldeaths) |

> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.

---

## Variante : Décès mensuels par maladies pulmonaires — Royaume-Uni (mdeaths + fdeaths) (groupe EMS n°2 — Dione / Gouem)

**Série** : Décès mensuels par maladies pulmonaires — Royaume-Uni (mdeaths + fdeaths) — pas de temps : mensuel (période 12)
**Accès aux données** : R : `mdeaths`, `fdeaths` (datasets, janv. 1974 – déc. 1979, 72 obs. chacune) ; `ldeaths = mdeaths + fdeaths`.
**Découpage train/test imposé** : train = 1974–1977 ; test = 1978–1979 (24 mois). Série courte : seulement 6 cycles.

#### 1. Contexte à documenter (étapes 2-3)
Bronchite, emphysème, asthme : pourquoi les décès culminent-ils en hiver ? Quel événement sanitaire explique le pic de début 1976 ?
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

#### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Saisonnalité annuelle forte, tendance faible.

#### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : Seulement 72 points : les coefficients saisonniers reposent sur 6 valeurs par mois — discuter leur fiabilité. Le pic de 1976 est-il une valeur aberrante ou un phénomène réel ?

#### 4. Décomposition (étape 6)
- Test des 3 méthodes de choix (bande, Buys-Ballot, profils) ; additif attendu mais à démontrer.
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
Ce groupe traite **mdeaths** (hommes) et **fdeaths** (femmes) séparément puis compare leurs coefficients saisonniers (le profil est-il le même ?). Le groupe VCOD n°6 traite `ldeaths` (total).


---

## Variante : Décès mensuels par maladies pulmonaires — Royaume-Uni (ldeaths) (groupe VCOD n°6 — Lokossa / Chaabani)

**Série** : Décès mensuels par maladies pulmonaires — Royaume-Uni (ldeaths) — pas de temps : mensuel (période 12)
**Accès aux données** : R : `ldeaths` (datasets, janv. 1974 – déc. 1979, 72 obs.).
**Découpage train/test imposé** : train = 1974–1977 ; test = 1978–1979 (24 mois).

#### 1. Contexte à documenter (étapes 2-3)
Bronchite, emphysème, asthme : mécanismes de la surmortalité hivernale ; épidémie de grippe 1975-76.
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

#### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Saisonnalité annuelle forte, pas de tendance nette.

#### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : Série très courte (6 cycles) : l'ARIMA saisonnier est fragile, la décomposition aussi. Dire explicitement ce que 6 cycles permettent ou non de conclure.

#### 4. Décomposition (étape 6)
- Additif vs multiplicatif à trancher numériquement.
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
Comparer décomposition additive vs multiplicative sur la **même** série avec un critère chiffré (écart-type des résidus, ACF des résidus), pas seulement visuel.


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
