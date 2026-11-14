# Exercices SAE 3.03 — promo 2026 (par sujet)

| Sujet | Série | Groupe | Énoncé |
|---|---|---|---|
| Données économiques | Données économiques — FEDFUNDS (taux directeur de la Fed) | EMS 1 — Drackle / Hachemi | [01_Economie_FEDFUNDS/ENONCE.md](01_Economie_FEDFUNDS/ENONCE.md) |
| Médecine — décès pulmonaires (UK) | Décès mensuels par maladies pulmonaires — Royaume-Uni (mdeaths + fdeaths) | EMS 2 — Dione / Gouem | [02_Medecine_Deces_pulmonaires/ENONCE.md](02_Medecine_Deces_pulmonaires/ENONCE.md) |
| Médecine — décès pulmonaires (UK) | Décès mensuels par maladies pulmonaires — Royaume-Uni (ldeaths) | VCOD 6 — Lokossa / Chaabani | [02_Medecine_Deces_pulmonaires/ENONCE.md](02_Medecine_Deces_pulmonaires/ENONCE.md) |
| Transports publics en France | Transports publics en France — régularité des trains (Option R) | EMS 3 — Diop / Carien | [03_Transports_publics_France/ENONCE.md](03_Transports_publics_France/ENONCE.md) |
| Taches solaires | Taches solaires — nombre mensuel (sunspots) | EMS 4 — Casares Bello / Sabatier | [04_Taches_solaires/ENONCE.md](04_Taches_solaires/ENONCE.md) |
| Taches solaires | Taches solaires — nombre annuel (sunspot.year) | VCOD 2 — Di Scala / Milazzo Guilhou | [04_Taches_solaires/ENONCE.md](04_Taches_solaires/ENONCE.md) |
| Consommation de gaz UK | Consommation de gaz au Royaume-Uni (UKgas) | EMS 5 — Diallo / Kouyate | [05_Gaz_UK_UKgas/ENONCE.md](05_Gaz_UK_UKgas/ENONCE.md) |
| Production de gaz en Australie | Production mensuelle de gaz en Australie (gas) | EMS 6 — Obame Ndong Ntougou / Houngli | [06_Gaz_Australie/ENONCE.md](06_Gaz_Australie/ENONCE.md) |
| Données de pluie | Précipitations journalières à Boulder, Colorado, USA (1948–2013) | EMS 7 — Accrombessi / Kare | [07_Pluie_Boulder/ENONCE.md](07_Pluie_Boulder/ENONCE.md) |
| Données de CO2 | CO₂ atmosphérique à Mauna Loa (co2) | EMS 8 — Meye-Meye / Sawadogo | [08_CO2_Mauna_Loa/ENONCE.md](08_CO2_Mauna_Loa/ENONCE.md) |
| Accidents de la route UK | Conducteurs tués ou gravement blessés au Royaume-Uni (UKDriverDeaths) | VCOD 1 — Ayral / Furgal | [09_Accidents_route_UK/ENONCE.md](09_Accidents_route_UK/ENONCE.md) |
| Débit du Nil | Débit annuel du Nil à Assouan (Nile) | VCOD 3 — Pujal / Marquier | [10_Debit_du_Nil/ENONCE.md](10_Debit_du_Nil/ENONCE.md) |
| Météo et ville (option L) | Météo horaire multi-villes — température (Option L) | VCOD 4 — Nzau Ngoy / Livernet | [11_Meteo_ville_OptionL/ENONCE.md](11_Meteo_ville_OptionL/ENONCE.md) |
| Ventes de champagne | Ventes de champagne (Option A) | VCOD 5 — Rafaly / Rabat | [12_Champagne_OptionA/ENONCE.md](12_Champagne_OptionA/ENONCE.md) |
| Données environnementales | Température moyenne mensuelle à Nottingham (nottem) | VCOD 7 — Bach / Majde | [13_Environnement_Temperature_Nottingham/ENONCE.md](13_Environnement_Temperature_Nottingham/ENONCE.md) |

**À confirmer** : « 10 données économiques » (EMS-1 → FEDFUNDS) et « 2.5 environnement » (VCOD-7 → nottem).
Décès pulmonaires et taches solaires : un énoncé, deux variantes (mdeaths+fdeaths / ldeaths ; mensuel / annuel).

## Comment lancer les solutions (corrigés)

Chaque dossier contient `solution.py` et `solution.R` qui produisent `sorties_python/` et `sorties_R/`
(log `resultats.txt`, figures PNG, `comparaison_previsions.csv`).

**Python** (venv central) :
```bash
python3 -m venv /tmp/sae_venv && /tmp/sae_venv/bin/pip install numpy pandas scipy matplotlib statsmodels
cd "<dossier du sujet>" && /tmp/sae_venv/bin/python solution.py
```

**R** (packages : `forecast`, `tseries` ; + `fpp2` pour les décès pulmonaires) :
```bash
Rscript solution.R   # depuis n'importe quel dossier
```

Relancer tout :
```bash
cd "SAE 3.03/2026"
for d in [0-9]*_*/; do Rscript "$d/solution.R" && /tmp/sae_venv/bin/python "$d/solution.py"; done
```

## Sources des données

- **Séries R** (UKgas, gas, co2, Nile, nottem, sunspots, sunspot.year, UKDriverDeaths, mdeaths/fdeaths/ldeaths) :
  R de base + `fpp2` ; Python les lit via `statsmodels.datasets.get_rdataset`, avec repli sur le CSV local de `data/`.
- **FEDFUNDS** (01) : téléchargé depuis FRED → `data/FEDFUNDS.csv` (re-téléchargé automatiquement si absent).
- **Boulder** (07) : CSV du doc SAE (GitHub ef2020) → `data/boulder-precip.csv` ; HPCP en pouces, 999.99 = NA,
  plusieurs relevés par jour à sommer, jours absents = jours secs.
- **Options locales** (03 transports, 11 météo, 12 champagne) : fichiers de `SAE 3.03/data/`
  (Kaggle + `monthly_champagne_sales.csv`), lus en relatif depuis la racine du projet.

## À savoir avant de distribuer les corrigés

- Sujet 04 : le doc dit « sunspot.month, 1790–1970 » ; R n'a pas cet objet → `sunspots` (1749–1983), à signaler.
- Sujet 01 : FEDFUNDS est dans la section « sans saisonnalité — PAS AU PROGRAMME DES BUT2 » du doc — à confirmer si BUT2.
- Choix SARIMA par grille AIC restreinte (p,q ≤ 2, P,Q ≤ 1) ; p-values ADF de `tseries` bornées à 0.01 ;
  MAPE énorme sur FEDFUNDS (taux ≈ 0 : artefact du MAPE).
