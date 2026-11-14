# Résumé du triage des datasets Kaggle — SAE 3.03

*Généré automatiquement par `scripts/download_and_plot_datasets.py`. Vérifier visuellement chaque graphique avant de valider une option pour un binôme.*

| Option | Statut | Fichier retenu | Colonne date | Colonne(s) valeur | N obs (mensuel) | Période | Détail |
|---|---|---|---|---|---:|---|---|
| A — Ventes de champagne (Perrin Frères) | ✅ OK | `A_piyushagni5-monthly-sales-of-french-champagne/monthly_champagne_sales.csv` | Month | Sales | 105 | 1964-01–1972-09 | fichier retenu parmi 1 candidat(s) |
| B — Consommation d'énergie mensuelle (France) | ✅ OK | `B_auricdutt-monthly-energy-consumption-dataset-france/monthly_energy_dataset_france.csv` | Unnamed: 0 | Sub_metering_3, Sub_metering_2, Sub_metering_1 | 228 | 2006-12–2025-11 | fichier retenu parmi 1 candidat(s) |
| D — Prix hebdomadaires de l'avocat (US) | ✅ OK | `D_neuromusic-avocado-prices/avocado.csv` | Date | Total Volume, 4046, 4225 | 39 | 2015-01–2018-03 | fichier retenu parmi 1 candidat(s) |
| E — Ventes hebdomadaires Walmart (avec variables externes) | ✅ OK | `E_aslanahmedov-walmart-sales-forecast/train.csv` | Date | Weekly_Sales | 33 | 2010-02–2012-10 | fichier retenu parmi 4 candidat(s) |
| F — Consommation électrique horaire (Europe de l'Ouest) | ✅ OK | `<15 fichiers concaténés (colonnes communes)>` | start | load | 28 | 2015-01–2017-04 | fichier retenu parmi 5 candidat(s) |
| H — Ventes retail longue durée (US Census) | ✅ OK | `<23 fichiers concaténés (colonnes communes)>` | date | value | 333 | 1992-01–2019-09 | fichier retenu parmi 5 candidat(s) |
| K — Consommation électrique horaire PJM (US) | ✅ OK | `K_robikscube-hourly-energy-consumption/pjm_hourly_est.csv` | Datetime | PJME, PJM_Load, AEP | 200 | 1998-04–2018-08 | fichier retenu parmi 4 candidat(s) |
| L — Météo horaire multi-villes | ✅ OK | `L_selfishgene-historical-hourly-weather-data/temperature.csv` | datetime | Minneapolis, Montreal, Kansas City | 62 | 2012-10–2017-11 | fichier retenu parmi 4 candidat(s) |
| M — Trafic web de pages Wikipédia | ✅ OK | `M_web-traffic-time-series-forecasting/train_2.csv` | _wide_date | _value | 27 | 2015-07–2017-09 | fichier retenu parmi 4 candidat(s) |
| R — Trafic des transports publics en France | ✅ OK | `R_gatandubuc-public-transport-traffic-data-in-france/Regularities_by_liaisons_Trains_France.csv` | Period | Average travel time (min), Average train delay > 15min, Delay due to external causes | 66 | 2015-01–2020-06 | fichier retenu parmi 2 candidat(s) |
| T — Disponibilité des réacteurs nucléaires français | ✅ OK | `T_thrasy-french-nuclear-reactors-availability-20152021/French_nuclear_reactors_availability.csv` | Unnamed: 0 | Chooz 2, Civaux 2, Flamanville 1 | 84 | 2015-01–2021-12 | fichier retenu parmi 3 candidat(s) |
| U — Énergie française + météo régionale | ✅ OK | `U_ravvvvvvvvvvvv-france-energy-weather-hourly/merged_hourly_regional.csv` | date | conso_elec_mw, conso_gaz_mw, sunshine_duration | 35 | 2013-01–2015-11 | fichier retenu parmi 2 candidat(s) |

## Légende des statuts
- **OK** : un graphique a été généré (`plots/<option>.png`) — à valider visuellement.
- **échec téléchargement** : identifiants Kaggle manquants, compétition dont les règles n'ont pas été acceptées sur le site, ou dataset introuvable/renommé.
- **pas de CSV / pas de colonne détectée** : la détection automatique n'a pas trouvé de structure exploitable — inspecter le fichier manuellement.