# PROGRESS — dossiers par sujet + code de résolution R et Python

**État : TERMINÉ (2026-11-14).** Les 13 sujets × 2 langages (R + Python) tournent, les sorties sont
générées, la doc est à jour. Les séries suivent la liste du doc SAE ; les options A/L/R utilisent les
fichiers locaux de `SAE 3.03/data/`. Voir « Fait » ci-dessous pour le détail et les bugs corrigés.

## Objectif
Un dossier par sujet dans `2026/`, contenant l'énoncé et une solution en **R** et en **Python**.
La plupart des séries viennent de R, donc R est la référence et Python reprend les mêmes données.

## Architecture
- `_common/common.py` et `_common/common.R` : pipeline commun (exploration, tests ADF/Mann-Kendall/Pettitt,
  choix additif/multiplicatif Buys-Ballot, décomposition + MM à la main, validation des résidus,
  prévisions décomposition + lissage ETS + ARIMA/SARIMA (grille AIC, d par ADF) + naïf,
  tableau RMSE/MAE/MAPE) et outils pour les questions ⭐.
- `NN_sujet/ENONCE.md`, `solution.py`, `solution.R`, `data/`, `sorties_python/`, `sorties_R/`.
- Python lit les séries R via `statsmodels.datasets.get_rdataset` (miroir Rdatasets) avec repli sur le
  CSV local du dossier `data/`. Pour ldeaths/mdeaths/fdeaths et co2, `solution.R` exporte le CSV que
  Python lit ensuite ; FEDFUNDS et boulder-precip sont téléchargés (R ou Python) et copiés dans `data/`.
- `run_pipeline` accepte un log existant (`log=` en Python, `fresh_log=FALSE` en R) pour les sujets en
  plusieurs parties (ex. 07 : analyse journalière + pipeline mensuel dans un seul resultats.txt).
- Les coefficients saisonniers sont étiquetés par mois réel quand période=12 (la série peut ne pas
  commencer en janvier, cf. Boulder qui commence en août) ; le choix additif/multiplicatif explique
  sa raison dans le log.

## Fait
- [x] 13 énoncés par sujet en `NN_sujet/ENONCE.md` (générés par `scripts/make_group_exercises.py`,
      mis à jour pour la nouvelle arborescence ; re-exécuté, contenu identique).
- [x] `common.py` + 13 × `solution.py` : **exécutés, tous verts** (venv `/tmp/sae_venv` :
      numpy pandas scipy matplotlib statsmodels).
- [x] R installé (4.3.3) ; packages `forecast` 9.0.2, `tseries`, `fpp2` dans la lib utilisateur
      `/home/lupin/R/lib` (`~/.Renviron` : `R_LIBS_USER`).
- [x] `common.R` + 13 × `solution.R` : **exécutés, tous verts** (`Rscript solution.R`, depuis n'importe
      quel dossier). Sorties R et Python en nombre identique (logs + PNG) pour chaque sujet.
- [x] Données manquantes résolues :
  - FEDFUNDS téléchargé via `url()` R (curl échoue dans cet environnement) →
    `01_Economie_FEDFUNDS/data/FEDFUNDS.csv` (mensuel, 1954-07 → 2026-10).
  - mdeaths/fdeaths/ldeaths exportés par R (fpp2) → `02_*/data/*.csv`.
  - co2 exporté par R (NA interpolés) → `08_*/data/co2.csv`.
- [x] **Sujet 07 aligné sur le doc SAE** : pluie journalière de **Boulder, Colorado** (1948–2013,
      `data/boulder-precip.csv`, URL du doc) au lieu de precip1 Londres. Dossier renommé
      `07_Pluie_Boulder`. Particularités du fichier : HPCP en pouces, `999.99` = NA, **plusieurs
      relevés par jour à sommer**, jours absents = jours secs (~82 %). Travail sur les totaux mensuels
      (train 1948-08→2003-12, test 2004–2013) + ⭐ climatologie/jours secs par décennie et tests annuels.
- [x] Doc : `2026/README.md` (index avec liens corrigés + section « Comment lancer »),
      `scripts/make_group_exercises.py` régénère l'arborescence actuelle.

## Bugs corrigés au passage (à connaître si on retouche le code)
- `common.R` : nommage ARIMA = `arma[c(1,6,2)]` (p,d,q) / saisonnier `arma[c(3,7,4)]` (P,D,Q) — `arma` vaut (p,q,P,Q,période,d,D) ; fenêtre de la MM à la main = `y[(t-h):(t+h)]` ; garde `is.finite(aicc)` dans
  `fc_smoothing` ; `run_pipeline` renvoie aussi `log`.
- `init_out()` modifie la **globale** OUT : avec plusieurs `run_pipeline` enchaînés, calculer les
  chemins depuis `getwd()` (variable `SRT`), jamais depuis OUT (bug de dossiers imbriqués, corrigé
  dans 02/03/04).
- R : tendance amortie = `ets(model="AAA", damped=TRUE)` (ni `"AAdA"` ni `"AAAd"`) ; corrigé 2026-11-14, vérifié sur UKgas. Les sorties R des autres sujets datent d'avant ce correctif : relancer `Rscript solution.R`.
- R : `read.csv(check.names=FALSE)` pour les CSV Kaggle (sinon `"San Francisco"` → `"San.Francisco"`).
- R : ce build ne parse pas `"%Y-%m"` seul dans `as.POSIXlt` → parser `paste0(Period, "-01")` avec
  `"%Y-%m-%d"`.

## Limites / écarts avec le doc SAE (à annoncer dans les rapports)
- Le choix SARIMA se fait par une grille AIC restreinte (p,q ≤ 2, P,Q ≤ 1) ; l'ACF/PACF n'est pas
  automatisée dans le choix.
- Les p-values ADF de `tseries` sont bornées à 0.01 (Python donne la valeur exacte).
- MAPE énorme sur FEDFUNDS (taux ≈ 0 sur certaines périodes) : artefact connu du MAPE, à commenter.
- Sujet 04 : le doc dit « sunspot.month, 1790–1970 » ; R n'a pas cet objet → on utilise `sunspots`
  (1749–1983), la seule série mensuelle de base. À signaler dans le rapport.
- Sujet 01 : FEDFUNDS est listé dans la section « sans saisonnalité — PAS AU PROGRAMME DES BUT2 »
  du doc ; à confirmer si le binôme est BUT2.
- Les corrigés restent des guides pour l'enseignant : à vérifier avant distribution.

## Reprendre / relancer
```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026"
for i in 01 02 03 04 05 06 07 08 09 10 11 12 13; do d=$(ls -d ${i}_*)
  Rscript "$d/solution.R" && /tmp/sae_venv/bin/python "$d/solution.py"; done
```
(Le venv `/tmp/sae_venv` est dans /tmp : à recréer si la machine a été redémarrée, voir README.md.)
