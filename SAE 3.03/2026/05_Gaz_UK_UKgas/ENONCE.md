# SAE 3.03 — Exercice : Consommation de gaz UK

**Groupes concernés (2026)** :

| Classe | Groupe | Noms | Sujet saisi |
|---|---|---|---|
| EMS | 5 | Diallo / Kouyate | 2.8 Consommation de gaz UK |

> Complète l'énoncé général de la SAE : 8 étapes, rapport ≤ 12 pages, code en annexe, `Nom1_Nom2_rapport_SAE303.pdf`.

---

**Série** : Consommation de gaz au Royaume-Uni (UKgas) — pas de temps : trimestriel (période 4)
**Accès aux données** : R : `UKgas` (datasets, 1960 T1 – 1986 T4, 108 obs., millions de thermies).
**Découpage train/test imposé** : train = 1960–1984 ; test = 1985–1986 (8 trimestres).

### 1. Contexte à documenter (étapes 2-3)
Chauffage au gaz domestique ; mise en service du gaz de la mer du Nord (années 1960-70), choc pétrolier de 1973.
- Source exacte, unité, période, fréquence, nombre d'observations, valeurs manquantes.
- **Bibliographie** : au moins 2 références qui ont déjà analysé cette série (ou une proche) ; résumer leurs conclusions en 3 lignes et les comparer aux vôtres.

### 2. Exploration (étape 4)
1. Graphique de la série + une dataviz à un autre pas de temps (radial, month-plot, heatmap année × période).
2. Descripteurs par année (moyenne, écart-type, min, max).
3. ACF (et PACF) : décrire les pics, en déduire la période.
4. **Attendu sur la saisonnalité** : Saisonnalité trimestrielle forte (pic hiver) ET amplitude qui explose avec le niveau.

### 3. Tests (étape 5)
- ADF (niveau, puis différencié si besoin) ; test de tendance (Mann-Kendall ou régression) ; Pettitt.
- Pour chaque test : H₀/H₁, p-value, conclusion en langage clair, cohérence avec le graphique.
- **Point de vigilance** : Modèle **multiplicatif** clair (ou log). Attention : 4 coefficients seulement, de moyenne 1 (multiplicatif). Rupture de tendance vers 1970 : un seul modèle linéaire global est-il adapté ?

### 4. Décomposition (étape 6)
- Multiplicatif à justifier par les 3 méthodes ; comparer avec additif sur log(UKgas).
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
Détecter la rupture avec Pettitt, puis comparer droite de tendance globale vs tendance estimée après la rupture seulement pour la prévision.

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
