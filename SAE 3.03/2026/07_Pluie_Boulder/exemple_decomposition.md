# Boulder (Colorado) rainfall — decomposition and forecasting explained

> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; here we apply the same method to **this** series.

## 0. The method in 6 lines

1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.
2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.
3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).
4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).
5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.
6. Always compare with a naïve forecast.

## 1. The data and its context

Daily precipitation at Boulder, Colorado (1948–2013; value 999.99 = missing). The daily file is aggregated into **monthly totals** (in inches) to apply the course methods.

## 2. Run: monthly totals 1948–2013

**Series**: pluie Boulder — total mensuel — n = 785, frequency = 12 per cycle, from 1948/8 to 2013.92.

Summary: `Min. 0 | 1st Qu. 0.53 | Median 1.1 | Mean 1.48 | 3rd Qu. 2 | Max. 17.7 | sd=1.44 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.0100 | stationary — H0 'unit root' rejected |
| Mann-Kendall (trend) | 0.9292 | no significant trend |
| Pettitt (level break) | 0.921 | no significant break |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### Additive or multiplicative? (step 6a — Buys-Ballot)

For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. If `a` is significantly positive the swings grow with the level ⇒ multiplicative.

| Cycle | Mean | Std |
|---|---|---|
| 1 | 1.62 | 1.97 |
| 2 | 0.96 | 1.04 |
| 3 | 1.25 | 0.76 |
| … | … | … |
| 64 | 0.97 | 0.90 |
| 65 | 1.29 | 1.21 |

Slope **a = 1.0038**, p = 7.251e-11, 65 cycles ⇒ Buys-Ballot suggests **ADDITIVE**. The spread does not grow significantly with the level: seasonal effects are constant amounts. (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)

### Decomposition step by step (step 6b)

**Step A — centred moving average.** The period is p = 12 (even), so a window of 12 values has no centre. Use 13 values with half weight on the two ends:

```
T_t = (0.5·y_(t-6) + y_(t-5) + … + y_(t+5) + 0.5·y_(t+6)) / 12
```

By hand at t = 7: `T_7 = (0.5·0.36 + 0.83 + 0.55 + 0.99 + 0.2 + 0.52 + 0.1 + 2.47 + 2.12 + 3.28 + 7.03 + 1.05 + 0.5·0.31) / 12 = 1.623` — R gives **1.623** ✓

The first 6 and last 6 trend values do not exist (the window would run outside the data).

**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:

| t | time | y_t | T_t | y−T | position |
|---|---|---|---|---|---|
| 7 | 1949.08 | 0.10 | 1.62 | -1.523 | Feb |
| 8 | 1949.17 | 2.47 | 1.59 | 0.884 | Mar |
| 9 | 1949.25 | 2.12 | 1.59 | 0.529 | Apr |
| 10 | 1949.33 | 3.28 | 1.59 | 1.691 | May |
| 11 | 1949.42 | 7.03 | 1.55 | 5.480 | Jun |
| 12 | 1949.5 | 1.05 | 1.57 | -0.520 | Jul |
| 13 | 1949.58 | 0.31 | 1.59 | -1.282 | Aug |
| 14 | 1949.67 | 0.00 | 1.51 | -1.510 | Sep |
| 15 | 1949.75 | 1.49 | 1.45 | 0.043 | Oct |
| 16 | 1949.83 | 0.00 | 1.46 | -1.464 | Nov |
| 17 | 1949.92 | 0.27 | 1.19 | -0.922 | Dec |
| 18 | 1950 | 0.92 | 0.95 | -0.027 | Jan |

**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them (averaging cancels the noise), then force the coefficients to sum to 0:

| Position | n ratios | raw | normalised (decompose) | meaning |
|---|---|---|---|---|
| Jan | 64 | -0.8034 | -0.7986 | -0.8 vs trend |
| Feb | 65 | -0.7027 | -0.6979 | -0.7 vs trend |
| Mar | 65 | 0.2899 | 0.2947 | +0.3 vs trend |
| Apr | 65 | 0.9085 | 0.9133 | +0.9 vs trend |
| May | 65 | 1.2759 | 1.2807 | +1.3 vs trend |
| Jun | 65 | 0.2703 | 0.2750 | +0.3 vs trend |
| Jul | 64 | 0.0560 | 0.0608 | +0.1 vs trend |
| Aug | 64 | 0.0045 | 0.0093 | +0.0 vs trend |
| Sep | 64 | -0.0763 | -0.0716 | -0.1 vs trend |
| Oct | 64 | -0.2323 | -0.2276 | -0.2 vs trend |
| Nov | 64 | -0.3899 | -0.3851 | -0.4 vs trend |
| Dec | 64 | -0.6578 | -0.6530 | -0.7 vs trend |

The raw coefficients average -0.0048; they are rescaled to 0 so the season does not also move the overall level. Largest: **May**, smallest: **Jan**.

**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = y_t − S`; the residual is what trend × season (or trend + season) does not explain. Example at t = 7: y = 0.10, T = 1.62, S = -0.6979 ⇒ CVS = 0.80, residual = -0.8250 (0 = perfect fit).

### Validation (step 7)

`mean=-0.004777 sd=1.119 | Ljung-Box p=5.333e-08 (autocorrelated) | Shapiro p=2.386e-19 (not normal)`

Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.

### Forecast (step 8)

Split: `train = 665 obs. | test = 120 obs. (de 2004.00 à 2013.92)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| Décomposition (tendance + saison) | 1.79 | 0.93 | 140.0 |
| ARIMA(0,0,1)(2,0,0)[12] with non-zero mean | 1.84 | 0.98 | 155.0 |
| LES | 1.84 | 0.94 | 136.2 |
| Holt-Winters | 1.94 | 1.05 | 106.0 |
| LED (Holt) | 2.18 | 1.21 | 87.8 |
| Naïf | 2.34 | 1.45 | 161.9 |

Best on the test set: **Décomposition (tendance + saison)** (RMSE 1.79). The decomposition method ranks 1 of 6. LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. Holt-Winters adds it and updates it each period. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=0.029 | LED : alpha=0.153 beta=0.074; Holt-Winters : alpha=0.039 beta=0.033 gamma=0.196` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

Model chosen by `auto.arima`: `ARIMA(0,0,1)(2,0,0)[12] with non-zero mean`.

### ⭐ Subject-specific question — results from the log

```
⭐ Climatologie mensuelle (série journalière)
Proportion de jours secs par mois :  1=89%   2=85%   3=79%   4=76%   5=74%   6=80%   7=79%   8=82%   9=84%  10=86%  11=86%  12=87%
Climatologie mensuelle par décennie : CV inter-décennies par mois — max 0.87 (mois 6) ; moyenne des CV = 0.39. La saisonnalité est-elle stable sur 65 ans ?

⭐ Tests sur les totaux ANNUELS (65 ans)
ADF annuel : stat=-4.024, p=0.01413 -> stationnaire
Mann-Kendall annuel : p=0.9031, tau=0.011 -> pas de tendance significative
Pettitt annuel : p=0.886, changement possible après l'observation 20 (≈ année 1967)
```

## 3. What to watch for in this subject

- Most days are dry and rain is very irregular: the seasonality is much weaker than for temperature, and the residuals are large and skewed.
- Missing-value code 999.99 must be turned into NA *before* summing, otherwise one bad value ruins a month.
- The daily ACF has peaks at 365 and 730 days (figure `00_acf_journalier.png`): seasonality exists, but it is buried in noise.

**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.

## 4. Code and how to run

Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):

```r
res <- run_pipeline(ts_mon, 120, OUT, name = "pluie Boulder — total mensuel", fresh_log = FALSE)
```

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/07_Pluie_Boulder"
Rscript solution.R      # sorties_R/
python3 solution.py     # sorties_python/
```
