# Rapport d'analyse — ventes mensuelles de champagne Perrin Frères

## 1. Management de projet

Proposition de découpage des 10 heures demandées dans l'énoncé :

| Tranche | Travail prévu | Livrable intermédiaire |
|---|---|---|
| 0h–2h | Récupération du dataset, lecture de l'énoncé, Gantt, rôles | Données importées + plan de travail |
| 2h–4h | Recherche bibliographique et contextualisation | Source Kaggle + contexte économique |
| 4h–6h | Exploration, visualisations, ACF/PACF | Graphiques et statistiques descriptives |
| 6h–8h | Tests, choix additif/multiplicatif, décomposition | Coefficients saisonniers + CVS |
| 8h–10h | Prévisions, comparaison des erreurs, rédaction | Rapport final + code en annexe |

## 2. Recherche bibliographique

La série correspond au jeu **Monthly Champagne Sales** diffusé sur Kaggle : ventes mensuelles de champagne Perrin Frères. Elle est fréquemment utilisée comme série pédagogique pour illustrer une tendance croissante combinée à une saisonnalité annuelle forte, notamment un pic de fin d'année. Pour un rapport étudiant, on peut compléter cette source par une courte recherche sur la saisonnalité commerciale des vins effervescents : achats plus élevés lors des fêtes de fin d'année, effet des stocks et événements commerciaux.

## 3. Présentation et contextualisation des données

- Période observée : **1964-01 à 1972-09**.
- Nombre d'observations : **105 mois**.
- Fréquence : mensuelle.
- Variable : ventes mensuelles, unité exacte non documentée dans le fichier Kaggle.
- Valeurs manquantes : **0**.

Le dataset est adapté à la SAE car il contient plus de trois cycles saisonniers annuels et une saisonnalité visible : les ventes augmentent fortement en novembre-décembre.

## 4. Exploration des données

Statistiques descriptives principales :

| Indicateur | Valeur |
|---|---:|
| Moyenne | 4761.15 |
| Écart-type | 2553.50 |
| Minimum | 1413.00 |
| Médiane | 4217.00 |
| Maximum | 13916.00 |

Graphiques générés :

- `01_serie_temporelle.png` : série brute ;
- `02_profils_saisonniers.png` : profils annuels superposés ;
- `05_acf_pacf.png` : ACF/PACF si `statsmodels` est disponible.

La série présente une hausse globale du niveau moyen et une saisonnalité annuelle très marquée. Les profils saisonniers montrent un pic récurrent en fin d'année, surtout en novembre et décembre.

## 5. Tests statistiques

```json
{
  "mann_kendall": {
    "S": 1408.0,
    "tau": 0.2578754578754579,
    "z": 3.8958581039507294,
    "p_value": 9.785166693232483e-05,
    "decision": "tendance croissante significative"
  },
  "pettitt": {
    "K": 1238.0,
    "change_point_index": 33,
    "change_point_date": "1966-09-01",
    "p_value": 0.0007649921270995845,
    "decision": "rupture probable"
  },
  "stationarity": {
    "ADF": {
      "statistic_simplified": -6.130515910840617,
      "p_value": "non disponible sans statsmodels",
      "decision": "à interpréter avec statsmodels conseillé"
    },
    "KPSS": {
      "status": "non disponible sans statsmodels"
    }
  },
  "buys_ballot": {
    "slope_std_vs_mean": 0.8066498848556763,
    "intercept": -1425.2464723983705,
    "correlation": 0.8410364183147749,
    "decision_indicative": "multiplicatif",
    "years_used": 9
  },
  "linear_trend": {
    "slope_per_month": 24.078792535784256,
    "intercept": 3608.388063703792
  },
  "statsmodels_available": false
}
```

Interprétation attendue :

- **Mann-Kendall** vérifie la présence d'une tendance monotone. Une p-value inférieure à 5 % avec un tau positif indique une tendance croissante.
- **Pettitt** cherche une rupture de niveau central. Si une rupture apparaît, elle doit être commentée comme un changement de régime possible, pas comme une simple saisonnalité.
- **ADF/KPSS** nécessitent `statsmodels` pour obtenir les p-values de référence. Sans cette bibliothèque, le script produit une indication mais recommande de relancer avec `pip install statsmodels`.

## 6. Choix du modèle et décomposition

Les trois arguments pédagogiques vont plutôt vers un modèle **multiplicatif** :

1. la méthode de la bande suggère une amplitude saisonnière plus grande quand le niveau de ventes augmente ;
2. les profils saisonniers accentuent le pic de fin d'année ;
3. Buys-Ballot estime une relation entre moyenne annuelle et écart-type annuel.

Les coefficients saisonniers multiplicatifs normalisés sont :

| month_name | normalized_coefficient |
| ---------- | ---------------------- |
| Janvier    | 0.7627                 |
| Février    | 0.6827                 |
| Mars       | 0.7996                 |
| Avril      | 0.8202                 |
| Mai        | 0.8616                 |
| Juin       | 0.8744                 |
| Juillet    | 0.7413                 |
| Août       | 0.3629                 |
| Septembre  | 0.9350                 |
| Octobre    | 1.2001                 |
| Novembre   | 1.7615                 |
| Décembre   | 2.1980                 |

La propriété de normalisation est respectée lorsque la moyenne des coefficients vaut environ 1. La CVS est calculée par :

$X_t^* = X_t / s_t^*$

et le résidu multiplicatif par :

$e_t = X_t /(\hat m_t \times s_t^*)$.

## 7. Validation du modèle

Les fichiers `03_decomposition_multiplicative.png` et `04_residus.png` permettent de vérifier si les résidus sont centrés autour de 1. Les plus grands écarts apparaissent typiquement sur les mois exceptionnels, car un modèle tendance + saisonnalité ne capture pas les promotions, les ruptures commerciales ou les chocs économiques.

## 8. Prévision

Les 12 dernières observations sont réservées comme jeu de test. Les modèles comparés sont :

- décomposition paramétrique additive ;
- décomposition paramétrique multiplicative ;
- Holt-Winters additif ;
- Holt-Winters multiplicatif ;
- SARIMA exploratoire si `statsmodels` est installé.

### Erreurs sur le jeu de test

| model                                                      | EM        | EAM_MAE  | EQM_MSE     | RMSE     | MAPE_percent |
| ---------------------------------------------------------- | --------- | -------- | ----------- | -------- | ------------ |
| Holt-Winters multiplicative alpha=0.4, beta=0.2, gamma=0.6 | -6.4477   | 234.2347 | 94042.7792  | 306.6640 | 6.6329       |
| Décomposition paramétrique multiplicative                  | -419.9843 | 431.7087 | 264784.8519 | 514.5725 | 12.1160      |
| Holt-Winters additive alpha=0.2, beta=0.2, gamma=0.8       | -417.6649 | 471.7256 | 383466.9334 | 619.2471 | 10.3219      |
| Décomposition paramétrique additive                        | -446.6941 | 621.3448 | 607772.4660 | 779.5976 | 20.1968      |

### Prévisions et observations réelles

| date                | observed   | Décomposition paramétrique additive | Décomposition paramétrique multiplicative | Holt-Winters additive alpha=0.2, beta=0.2, gamma=0.8 | Holt-Winters multiplicative alpha=0.4, beta=0.2, gamma=0.6 |
| ------------------- | ---------- | ----------------------------------- | ----------------------------------------- | ---------------------------------------------------- | ---------------------------------------------------------- |
| 1971-10-01 00:00:00 | 6981.0000  | 6929.1749                           | 7157.7955                                 | 7523.3867                                            | 6833.2549                                                  |
| 1971-11-01 00:00:00 | 9851.0000  | 9700.7463                           | 10607.8236                                | 11008.7283                                           | 10163.8478                                                 |
| 1971-12-01 00:00:00 | 12670.0000 | 11824.1749                          | 13238.7596                                | 13956.3336                                           | 12583.3776                                                 |
| 1972-01-01 00:00:00 | 4348.0000  | 4932.7481                           | 4639.3931                                 | 4327.2870                                            | 3602.6136                                                  |
| 1972-02-01 00:00:00 | 3564.0000  | 4618.3731                           | 4212.7502                                 | 3716.7755                                            | 3451.4861                                                  |
| 1972-03-01 00:00:00 | 4577.0000  | 5158.3731                           | 4902.7497                                 | 4609.7875                                            | 4448.9600                                                  |
| 1972-04-01 00:00:00 | 4788.0000  | 5279.1231                           | 5037.1168                                 | 4876.4803                                            | 4799.5931                                                  |
| 1972-05-01 00:00:00 | 4618.0000  | 5515.8731                           | 5368.6576                                 | 4920.5245                                            | 4847.8197                                                  |
| 1972-06-01 00:00:00 | 5312.0000  | 5559.6231                           | 5389.4390                                 | 5008.3485                                            | 5165.5862                                                  |
| 1972-07-01 00:00:00 | 4298.0000  | 4995.8731                           | 4612.6872                                 | 4846.5691                                            | 4636.0665                                                  |
| 1972-08-01 00:00:00 | 1413.0000  | 3190.4981                           | 2362.9858                                 | 2175.5270                                            | 1883.5012                                                  |
| 1972-09-01 00:00:00 | 5877.0000  | 5952.7481                           | 5806.6532                                 | 6339.2303                                            | 5958.2658                                                  |

## Conclusion

La série Champagne est un bon choix pour la SAE 3.03 : elle est courte, propre, mensuelle, et met clairement en évidence les étapes centrales du cours. Le modèle multiplicatif est généralement plus cohérent que le modèle additif, car l'amplitude saisonnière augmente avec le niveau de la série. Pour la prévision, le meilleur modèle doit être choisi sur les erreurs du jeu de test, pas seulement sur l'apparence graphique. Les limites principales sont la taille modérée de la série et l'absence de variables explicatives externes.

## Annexes — fichiers produits

- `tables/descriptive_statistics.csv`
- `tables/tests_statistiques.json`
- `tables/coefficients_saisonniers_additifs.csv`
- `tables/coefficients_saisonniers_multiplicatifs.csv`
- `tables/decomposition_multiplicative.csv`
- `tables/previsions_test.csv`
- `tables/metriques_prevision.csv`
- `figures/*.png`
