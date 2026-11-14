# SAE 3.03 — Exercice : Transports publics en France

**Groupes concernés (2026)** :

| Classe | Groupe | Noms | Sujet saisi |
|---|---|---|---|
| EMS | 3 | Diop / Carien | transports public en France |

> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.

---

**Série** : Transports publics en France — régularité des trains (Option R) — pas de temps : mensuel (période 12)
**Accès aux données** : Fichier `data/kaggle_raw/R_gatandubuc-public-transport-traffic-data-in-france/Regularities_by_liaisons_Trains_France.csv` (colonne Period ; 66 mois, janv. 2015 – juin 2020).
**Découpage train/test imposé** : train = 2015–2018 ; test = 2019 – mi-2020. Attention : COVID dans le test → à traiter explicitement.

### 1. Contexte à documenter (étapes 2-3)
SNCF : TGV/Intercités, retards, grèves (2018, déc. 2019), COVID mars 2020.
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Tendance significative, saisonnalité faible (η²≈0,13 sur la métrique par défaut) : à vérifier sur **votre** métrique et **votre** liaison.

### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : Choisir **une seule** liaison + **une** métrique (retard moyen, % retards > 15 min, causes externes…). Valeurs manquantes par liaison ; le 'trend' peut être un artefact de couverture des données.

### 4. Décomposition (étape 6)
- Si la saisonnalité est faible, justifier de ne garder que tendance + lissage (Holt) ; sinon HW additif.
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
Chercher les ruptures (Pettitt) et les relier à des événements datés (grèves, COVID) ; analyser les résidus comme événements sociaux.

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
