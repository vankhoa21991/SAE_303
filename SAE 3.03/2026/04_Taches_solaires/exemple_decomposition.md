# Sunspot numbers (monthly and annual) — decomposition and forecasting explained

> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; here we apply the same method to **this** series.

## 0. The method in 6 lines

1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.
2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.
3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).
4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).
5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.
6. Always compare with a naïve forecast.

## 1. The data and its context

Sunspot counts. The monthly series (`sunspots`, 1749–1983) and the annual series (`sunspot.year`, 1700–1988). The Sun has a ≈ 11-year activity cycle (Schwabe cycle) — **not** a yearly season.

## 2. Run: monthly, period 132

**Series**: sunspots mensuel — n = 2820, frequency = 12 per cycle, from 1749/1 to 1983.92.

Summary: `Min. 0 | 1st Qu. 15.7 | Median 42 | Mean 51.27 | 3rd Qu. 74.93 | Max. 253.8 | sd=43.45 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.0100 | stationary — H0 'unit root' rejected |
| Mann-Kendall (trend) | 9.046e-10 | significant monotone trend |
| Pettitt (level break) | 2.66e-26 | level break around 1935.67 |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### Additive or multiplicative? (step 6a — Buys-Ballot)

For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. If `a` is significantly positive the swings grow with the level ⇒ multiplicative.

| Cycle | Mean | Std |
|---|---|---|
| 1 | 41.49 | 28.07 |
| 2 | 58.02 | 34.29 |
| 3 | 69.63 | 48.96 |
| … | … | … |
| 20 | 76.97 | 58.15 |
| 21 | 65.62 | 45.88 |

Slope **a = 0.6322**, p = 1.917e-10, 21 cycles ⇒ Buys-Ballot suggests **ADDITIVE**. The spread does not grow significantly with the level: seasonal effects are constant amounts. (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)

### Decomposition step by step (step 6b)

**Step A — centred moving average.** The period is p = 132 (even), so a window of 132 values has no centre. Use 133 values with half weight on the two ends:

```
T_t = (0.5·y_(t-66) + y_(t-65) + … + y_(t+65) + 0.5·y_(t+66)) / 132
```

(With p = 132 the window is too long to write out; `ma(y, order=132, centre=TRUE)` computes it and is compared with `decompose()` in the log.)

The first 66 and last 66 trend values do not exist (the window would run outside the data).

**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:

| t | time | y_t | T_t | y−T | position |
|---|---|---|---|---|---|
| 67 | 1754.5 | 18.80 | 41.53 | -22.729 | pos 67 |
| 68 | 1754.58 | 12.30 | 41.55 | -29.253 | pos 68 |
| 69 | 1754.67 | 8.20 | 41.56 | -33.359 | pos 69 |
| 70 | 1754.75 | 24.10 | 41.59 | -17.486 | pos 70 |
| 71 | 1754.83 | 13.20 | 41.55 | -28.347 | pos 71 |
| 72 | 1754.92 | 4.20 | 41.36 | -37.164 | pos 72 |
| 73 | 1755 | 10.20 | 41.12 | -30.922 | pos 73 |
| 74 | 1755.08 | 11.20 | 41.05 | -29.848 | pos 74 |
| 75 | 1755.17 | 6.80 | 41.03 | -34.228 | pos 75 |
| 76 | 1755.25 | 6.50 | 40.88 | -34.378 | pos 76 |
| 77 | 1755.33 | 0.00 | 40.41 | -40.409 | pos 77 |
| 78 | 1755.42 | 0.00 | 39.94 | -39.943 | pos 78 |

**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them (averaging cancels the noise), then force the coefficients to sum to 0:

| Position | n ratios | raw | normalised (decompose) | meaning |
|---|---|---|---|---|
| pos 1 | 20 | 20.7677 | 21.1597 | +21.2 vs trend |
| pos 2 | 20 | 21.7767 | 22.1687 | +22.2 vs trend |
| pos 3 | 20 | 24.5616 | 24.9536 | +25.0 vs trend |
| pos 4 | 20 | 27.0962 | 27.4882 | +27.5 vs trend |
| pos 5 | 20 | 31.3896 | 31.7816 | +31.8 vs trend |
| pos 6 | 20 | 30.7943 | 31.1863 | +31.2 vs trend |
| … | … | … | … |  |
| pos 131 | 20 | 18.2168 | 18.6088 | +18.6 vs trend |
| pos 132 | 20 | 22.3865 | 22.7785 | +22.8 vs trend |

The raw coefficients average -0.3920; they are rescaled to 0 so the season does not also move the overall level. Largest: **pos 12**, smallest: **pos 92**.

**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = y_t − S`; the residual is what trend × season (or trend + season) does not explain. Example at t = 67: y = 18.80, T = 41.53, S = -14.8443 ⇒ CVS = 33.64, residual = -7.8849 (0 = perfect fit).

### Validation (step 7)

`mean=-0.392 sd=33.6 | Ljung-Box p=0 (autocorrelated) | Shapiro p=2.87e-23 (not normal)`

Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.

### Forecast (step 8)

Split: `train = 2700 obs. | test = 120 obs. (de 1974.00 à 1983.92)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| Décomposition (tendance + saison) | 46.88 | 37.17 | 92.2 |
| LES | 79.76 | 61.48 | 91.2 |
| Naïf | 82.05 | 63.08 | 86.0 |
| LED (Holt) | 106.00 | 83.14 | 93.6 |

Best on the test set: **Décomposition (tendance + saison)** (RMSE 46.88). The decomposition method ranks 1 of 4. LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. Holt-Winters adds it and updates it each period. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=0.530 | LED : alpha=0.543 beta=0.009` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

## 3. Run: annual 1700–1988

**Series**: sunspot.year — n = 289, frequency = 1 per cycle, from 1700/1 to 1988.00.

Summary: `Min. 0 | 1st Qu. 15.6 | Median 39 | Mean 48.61 | 3rd Qu. 68.9 | Max. 190.2 | sd=39.47 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.0100 | stationary — H0 'unit root' rejected |
| Mann-Kendall (trend) | 0.003585 | significant monotone trend |
| Pettitt (level break) | 0.0104 | level break around 1936.00 |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### No seasonal decomposition

This run has **no seasonal component** (annual data, or seasonality deliberately switched off). The pipeline therefore fits a straight line to the series: slope = **0.0971** per time unit. Without seasonal coefficients there is nothing to 'adjust': the structure is trend (or level shifts) + residual.

Residuals of the line: `slope=0.0971 ; residual sd=38.631 ; Ljung-Box p=0 ; Shapiro p=2.432e-10`

Mann-Kendall **and** Pettitt are both significant: on annual data this usually means a **level shift** (a step) rather than a steady slope — the straight line is only a rough summary. Look at the plot and the date given by Pettitt.

Interpretation: *Ljung-Box* tests whether residuals are autocorrelated (p < 0.05 ⇒ yes, structure left); *Shapiro* tests normality.

### Forecast (step 8)

Split: `train = 259 obs. | test = 30 obs. (de 1959.00 à 1988.00)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| ARIMA(2,0,1) with non-zero mean | 43.23 | 34.02 | 70.1 |
| Tendance seule (lm) | 48.32 | 40.52 | 102.6 |
| Naïf | 124.95 | 115.85 | 415.6 |
| LES | 124.95 | 115.85 | 415.6 |
| LED (Holt) | 153.37 | 145.01 | 498.2 |

Best on the test set: **ARIMA(2,0,1) with non-zero mean** (RMSE 43.23). The trend-only method ranks 2 of 5. There is no seasonality here, so LES (level only), LED (level + slope) and the trend line are the natural candidates; Holt-Winters is not used. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=1.000 | LED : alpha=1.000 beta=0.012` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

An α (and/or β) of exactly 1.000 means the optimiser hit its boundary: the smoother just repeats the last observation/slope, which is a symptom of a model that does not fit the series (no seasonal term here).

Model chosen by `auto.arima`: `ARIMA(2,0,1) with non-zero mean`.

### ⭐ Subject-specific question — results from the log

```
⭐ PACF : ordre p de l'AR (retards significatifs)
retards significatifs : 1 2 5 6 7 8 16 -> p proposé =16
```

## 4. Extra results: `mensuel_cycle132`

```
⭐ Quelle est la vraie période ?
Pic de l'ACF dans [100,170] : retard 126 mois = 10.5 ans
Contresens du TP01 (période 12) : amplitude des coef. saisonniers = 3.30 pour une moyenne de 51.3 -> saisonnalité annuelle négligeable
```

## 5. What to watch for in this subject

- `decompose()` with period 12 (as in TP01) is a misreading: there is no 12-month pattern. The ACF peaks near lag ≈ 130 months ≈ 11 years: that is the period to use (see the ⭐ block).
- The cycle length varies (9–14 years), so a fixed-period seasonal model is only an approximation.
- Smoothing without a seasonal term cannot reproduce the cycle: forecasts a decade ahead are nearly flat. An AR model of order ≈ 9 (PACF) does better.

**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.

## 6. Code and how to run

Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):

```r
res <- run_pipeline(y, 120, file.path(SRT, "mensuel"), name = "sunspots mensuel", period = 132, model = "additive",
res2 <- run_pipeline(ya, 30, file.path(SRT, "annuel"), name = "sunspot.year", seasonal = FALSE, max_p = 9, max_q = 1)
```

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/04_Taches_solaires"
Rscript solution.R      # sorties_R/
python3 solution.py     # sorties_python/
```
