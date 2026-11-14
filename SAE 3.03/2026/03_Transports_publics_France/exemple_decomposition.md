# French trains — average arrival delay (Option R) — decomposition and forecasting explained

> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; here we apply the same method to **this** series.

## 0. The method in 6 lines

1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.
2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.
3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).
4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).
5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.
6. Always compare with a naïve forecast.

## 1. The data and its context

Monthly average delay of all arriving trains (minutes), averaged over all connections of the Kaggle file `Regularities_by_liaisons_Trains_France.csv`, January 2015 → June 2020. Choose your own metric/connection in the report and document it.

## 2. Run: with seasonality (period 12)

**Series**: Retard moyen à l'arrivée (toutes liaisons) — n = 66, frequency = 12 per cycle, from 2015/1 to 2020.42.

Summary: `Min. 1.24 | 1st Qu. 3.96 | Median 5.08 | Mean 5.19 | 3rd Qu. 6.38 | Max. 11.09 | sd=1.84 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.4144 | **not** stationary — H0 'unit root' kept |
| Mann-Kendall (trend) | 0.0226 | significant monotone trend |
| Pettitt (level break) | 0.00246 | level break around 2017.42 |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### Additive or multiplicative? (step 6a — Buys-Ballot)

For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. If `a` is significantly positive the swings grow with the level ⇒ multiplicative.

| Cycle | Mean | Std |
|---|---|---|
| 1 | 4.33 | 1.26 |
| 2 | 4.18 | 1.62 |
| 3 | 5.35 | 1.22 |
| 4 | 7.07 | 1.62 |
| 5 | 5.04 | 1.79 |

Slope **a = 0.0437**, p = 0.7461, 5 cycles ⇒ Buys-Ballot suggests **ADDITIVE**. The spread does not grow significantly with the level: seasonal effects are constant amounts. (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)

### Decomposition step by step (step 6b)

**Step A — centred moving average.** The period is p = 12 (even), so a window of 12 values has no centre. Use 13 values with half weight on the two ends:

```
T_t = (0.5·y_(t-6) + y_(t-5) + … + y_(t+5) + 0.5·y_(t+6)) / 12
```

By hand at t = 7: `T_7 = (0.5·4.00252 + 4.08187 + 2.29705 + 3.98791 + 3.81267 + 5.53209 + 6.68045 + 5.5073 + 5.17115 + 3.95443 + 4.45759 + 2.47151 + 0.5·2.64497) / 12 = 4.273` — R gives **4.273** ✓

The first 6 and last 6 trend values do not exist (the window would run outside the data).

**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:

| t | time | y_t | T_t | y−T | position |
|---|---|---|---|---|---|
| 7 | 2015.5 | 6.68 | 4.27 | 2.407 | Jul |
| 8 | 2015.58 | 5.51 | 4.17 | 1.333 | Aug |
| 9 | 2015.67 | 5.17 | 4.18 | 0.989 | Sep |
| 10 | 2015.75 | 3.95 | 4.19 | -0.237 | Oct |
| 11 | 2015.83 | 4.46 | 4.18 | 0.273 | Nov |
| 12 | 2015.92 | 2.47 | 4.28 | -1.811 | Dec |
| 13 | 2016 | 2.64 | 4.27 | -1.623 | Jan |
| 14 | 2016.08 | 3.06 | 4.12 | -1.058 | Feb |
| 15 | 2016.17 | 3.50 | 4.04 | -0.531 | Mar |
| 16 | 2016.25 | 3.02 | 4.08 | -1.062 | Apr |
| 17 | 2016.33 | 4.61 | 4.21 | 0.399 | May |
| 18 | 2016.42 | 7.10 | 4.23 | 2.866 | Jun |

**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them (averaging cancels the noise), then force the coefficients to sum to 0:

| Position | n ratios | raw | normalised (decompose) | meaning |
|---|---|---|---|---|
| Jan | 4 | -0.5011 | -0.4761 | -0.5 vs trend |
| Feb | 4 | 0.0829 | 0.1079 | +0.1 vs trend |
| Mar | 4 | -0.9475 | -0.9225 | -0.9 vs trend |
| Apr | 4 | -1.0510 | -1.0260 | -1.0 vs trend |
| May | 4 | -0.4135 | -0.3885 | -0.4 vs trend |
| Jun | 4 | 2.2389 | 2.2639 | +2.3 vs trend |
| Jul | 5 | 2.0426 | 2.0676 | +2.1 vs trend |
| Aug | 5 | 0.4340 | 0.4590 | +0.5 vs trend |
| Sep | 5 | -0.0389 | -0.0139 | -0.0 vs trend |
| Oct | 5 | -0.0860 | -0.0610 | -0.1 vs trend |
| Nov | 5 | -0.3319 | -0.3069 | -0.3 vs trend |
| Dec | 5 | -1.7286 | -1.7036 | -1.7 vs trend |

The raw coefficients average -0.0250; they are rescaled to 0 so the season does not also move the overall level. Largest: **Jun**, smallest: **Dec**.

**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = y_t − S`; the residual is what trend × season (or trend + season) does not explain. Example at t = 7: y = 6.68, T = 4.27, S = 2.0676 ⇒ CVS = 4.61, residual = 0.3397 (0 = perfect fit).

### Validation (step 7)

`mean=-0.02499 sd=0.983 | Ljung-Box p=0.2622 (plausibly white noise) | Shapiro p=0.4187 (normal)`

Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.

### Forecast (step 8)

Split: `train = 48 obs. | test = 18 obs. (de 2019.00 à 2020.42)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| LES | 2.59 | 2.16 | 69.1 |
| ARIMA(0,1,1)(1,0,0)[12] | 2.93 | 2.55 | 78.7 |
| Naïf | 2.95 | 2.45 | 71.1 |
| Décomposition (tendance + saison) | 3.40 | 2.93 | 86.6 |
| LED (Holt) | 3.54 | 3.01 | 94.9 |
| Holt-Winters | 3.56 | 3.09 | 87.8 |

Best on the test set: **LES** (RMSE 2.59). The decomposition method ranks 4 of 6. LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. Holt-Winters adds it and updates it each period. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=0.261 | LED : alpha=0.088 beta=0.000; Holt-Winters : alpha=0.224 beta=0.038 gamma=0.000` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

Model chosen by `auto.arima`: `ARIMA(0,1,1)(1,0,0)[12]`.

### ⭐ Subject-specific question — results from the log

```
⭐ Résidus = événements ? (dates des 5 plus grands écarts de la décomposition)
  2017.92  résidu=2.41  (grève ? vacances ? COVID ?)
  2018.08  résidu=1.99  (grève ? vacances ? COVID ?)
  2018.50  résidu=1.92  (grève ? vacances ? COVID ?)
  2019.83  résidu=-1.96  (grève ? vacances ? COVID ?)
  2019.92  résidu=-1.92  (grève ? vacances ? COVID ?)
```

## 3. Run: without seasonality

**Series**: Retard moyen à l'arrivée (toutes liaisons) — n = 66, frequency = 12 per cycle, from 2015/1 to 2020.42.

Summary: `Min. 1.24 | 1st Qu. 3.96 | Median 5.08 | Mean 5.19 | 3rd Qu. 6.38 | Max. 11.09 | sd=1.84 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.4144 | **not** stationary — H0 'unit root' kept |
| Mann-Kendall (trend) | 0.0226 | significant monotone trend |
| Pettitt (level break) | 0.00246 | level break around 2017.42 |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### No seasonal decomposition

This run has **no seasonal component** (annual data, or seasonality deliberately switched off). The pipeline therefore fits a straight line to the series: slope = **0.3028** per time unit. Without seasonal coefficients there is nothing to 'adjust': the structure is trend (or level shifts) + residual.

Residuals of the line: `slope=0.3028 ; residual sd=1.778 ; Ljung-Box p=0.08163 ; Shapiro p=0.5819`

Mann-Kendall **and** Pettitt are both significant: on annual data this usually means a **level shift** (a step) rather than a steady slope — the straight line is only a rough summary. Look at the plot and the date given by Pettitt.

Interpretation: *Ljung-Box* tests whether residuals are autocorrelated (p < 0.05 ⇒ yes, structure left); *Shapiro* tests normality.

### Forecast (step 8)

Split: `train = 48 obs. | test = 18 obs. (de 2019.00 à 2020.42)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| Naïf | 2.12 | 1.72 | 54.4 |
| ARIMA(1,1,1) | 2.51 | 2.07 | 66.7 |
| LES | 2.59 | 2.16 | 69.1 |
| Tendance seule (lm) | 3.41 | 2.89 | 91.5 |
| LED (Holt) | 3.54 | 3.01 | 94.9 |

Best on the test set: **Naïf** (RMSE 2.12). The trend-only method ranks 4 of 5. There is no seasonality here, so LES (level only), LED (level + slope) and the trend line are the natural candidates; Holt-Winters is not used. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=0.261 | LED : alpha=0.088 beta=0.000` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

Model chosen by `auto.arima`: `ARIMA(1,1,1)`.

## 4. What to watch for in this subject

- The seasonality is weak on this metric (η² ≈ 0.13 in the dataset sheet): the two runs (with / without a seasonal term) let you check whether adding one actually helps on the test set.
- The test period contains the 2019–2020 strikes and the Covid lockdown: the biggest residuals are *events*, not noise. Date them and link them to real events.
- The averaging over connections hides missing data per line: document how gaps were filled.

**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.

## 5. Code and how to run

Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):

```r
a <- run_pipeline(y, ntest, file.path(SRT, "avec_saison"), name = "Retard moyen à l'arrivée (toutes liaisons)")
b <- run_pipeline(y, ntest, file.path(SRT, "sans_saison"), name = "Retard moyen à l'arrivée (toutes liaisons)", seasonal = FALSE)
```

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/03_Transports_publics_France"
Rscript solution.R      # sorties_R/
python3 solution.py     # sorties_python/
```
