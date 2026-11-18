# SAE 3.03 — Exercice : Données d'économie — ventes de produits anti-diabète (Australie)

**Groupes concernés (2026)** :

| Classe | Groupe | Noms | Sujet saisi |
|---|---|---|---|
| EMS | 1 | Drackle / Hachemi | 10 donne economic |

> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.

---

**Série** : Dépenses mensuelles de produits anti-diabète en Australie (a10) — pas de temps : mensuel (période 12)
**Accès aux données** : R : `library(fpp2); a10` (juil. 1991 – juin 2008, 204 obs., millions de dollars australiens — dépenses du Pharmaceutical Benefit Scheme, code ATC A10, source Medicare Australia).
**Découpage train/test imposé** : train = juil. 1991 – juin 2006 ; test = juil. 2006 – juin 2008 (24 mois).

### 1. Contexte à documenter (étapes 2-3)
Pharmaceutical Benefit Scheme (PBS) : programme public australien qui subventionne les médicaments. Série = dépenses du gouvernement pour les antidiabétiques (ATC A10). Contexte : hausse du diabète de type 2, nouveaux traitements, règles de remboursement.
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Tendance fortement croissante ET saisonnalité annuelle très marquée dont l'amplitude grandit avec le niveau.

### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : Modèle multiplicatif attendu (ou log). Série courte (17 cycles) mais très structurée. La croissance accélère : une droite unique sur toute la période sous-estime la fin de série (rupture de tendance, Pettitt).

### 4. Décomposition (étape 6)
- Multiplicatif à justifier (Buys-Ballot + bande) ; coefficients saisonniers mensuels à interpréter mois par mois.
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
Trancher additif/multiplicatif par un critère chiffré (reconstruction), puis comparer Holt-Winters multiplicatif brut vs additif sur log(y) sur le test de 24 mois, et tendance globale vs tendance post-rupture.

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
