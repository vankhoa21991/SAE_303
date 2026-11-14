# Tendance et saisonnalité — verification quantitative des datasets Kaggle

*Genere par `scripts/check_trend_seasonality.py`. Tendance = test de Mann-Kendall (p<0.05 = tendance significative). Saisonnalite = eta2 (part de variance expliquee par le mois ; >=0.15 = saisonnalite exploitable, >=0.40 = forte). Necessite au moins ~2 ans d'historique pour evaluer la saisonnalite.*

| Option | N (mois) | Periode | Tendance | Saisonnalite | Verdict |
|---|---:|---|---|---|---|
| A — Ventes de champagne (Perrin Frères) | 105 | 8.7 ans | tendance croissante (p=0.0001) | saisonnalité forte (eta2=0.84) | ✅ bon (tendance + saisonnalité) |
| B — Consommation d'énergie mensuelle (France) | 228 | 18.9 ans | pas de tendance significative (p=0.7302) | saisonnalité forte (eta2=0.82) | ⚠️ partiel (un seul des deux) |
| D — Prix hebdomadaires de l'avocat (US) | 39 | 3.2 ans | pas de tendance significative (p=0.1605) | saisonnalité forte (eta2=0.66) | ⚠️ partiel (un seul des deux) |
| E — Ventes hebdomadaires Walmart (avec variables externes) | 33 | 2.7 ans | pas de tendance significative (p=1.0000) | saisonnalité forte (eta2=0.98) | ⚠️ partiel (un seul des deux) |
| F — Consommation électrique horaire (Europe de l'Ouest) | 28 | 2.2 ans | tendance croissante (p=0.0086) | saisonnalité forte (eta2=0.68) | ✅ bon (tendance + saisonnalité) |
| H — Ventes retail longue durée (US Census) | 333 | 27.7 ans | tendance croissante (p=0.0000) | saisonnalité faible/absente (eta2=0.00) | ⚠️ partiel (un seul des deux) |
| K — Consommation électrique horaire PJM (US) | 200 | 16.6 ans | pas de tendance significative (p=0.1552) | saisonnalité forte (eta2=0.82) | ⚠️ partiel (un seul des deux) |
| L — Météo horaire multi-villes | 62 | 5.1 ans | pas de tendance significative (p=0.1289) | saisonnalité forte (eta2=0.96) | ⚠️ partiel (un seul des deux) |
| M — Trafic web de pages Wikipédia | 27 | 2.2 ans | pas de tendance significative (p=0.5878) | saisonnalité modérée (eta2=0.23) | ⚠️ partiel (un seul des deux) |
| R — Trafic des transports publics en France | 66 | 5.4 ans | tendance croissante (p=0.0003) | saisonnalité faible/absente (eta2=0.13) | ⚠️ partiel (un seul des deux) |
| T — Disponibilité des réacteurs nucléaires français | 84 | 6.9 ans | tendance décroissante (p=0.0037) | saisonnalité faible/absente (eta2=0.13) | ⚠️ partiel (un seul des deux) |
| U — Énergie française + météo régionale | 35 | 2.8 ans | pas de tendance significative (p=0.2329) | saisonnalité forte (eta2=0.95) | ⚠️ partiel (un seul des deux) |