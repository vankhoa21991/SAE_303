# Nottingham temperatures (nottem) — decomposition and forecasting explained

> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; here we apply the same method to **this** series.

## 0. The method in 6 lines

1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.
2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.
3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).
4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).
5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.
6. Always compare with a naïve forecast.

## 1. The data and its context

Average monthly air temperature at Nottingham Castle, °F, 20 years (1920–1939, 240 observations).

## 2. Run: monthly 1920–1939

**Series**: nottem — n = 240, frequency = 12 per cycle, from 1920/1 to 1939.92.

Summary: `Min. 31.3 | 1st Qu. 41.55 | Median 47.35 | Mean 49.04 | 3rd Qu. 57 | Max. 66.5 | sd=8.57 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.0100 | stationary — H0 'unit root' rejected |
| Mann-Kendall (trend) | 0.4329 | no significant trend |
| Pettitt (level break) | 0.912 | no significant break |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### Additive or multiplicative? (step 6a — Buys-Ballot)

For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. If `a` is significantly positive the swings grow with the level ⇒ multiplicative.

| Cycle | Mean | Std |
|---|---|---|
| 1 | 48.89 | 7.15 |
| 2 | 50.73 | 8.76 |
| 3 | 47.27 | 7.91 |
| … | … | … |
| 19 | 50.27 | 7.48 |
| 20 | 49.39 | 8.61 |

Slope **a = 0.1522**, p = 0.5116, 20 cycles ⇒ Buys-Ballot suggests **ADDITIVE**. The spread does not grow significantly with the level: seasonal effects are constant amounts. (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)

### Decomposition step by step (step 6b)

**Step A — centred moving average.** The period is p = 12 (even), so a window of 12 values has no centre. Use 13 values with half weight on the two ends:

```
T_t = (0.5·y_(t-6) + y_(t-5) + … + y_(t+5) + 0.5·y_(t+6)) / 12
```

By hand at t = 7: `T_7 = (0.5·40.6 + 40.8 + 44.4 + 46.7 + 54.1 + 58.5 + 57.7 + 56.4 + 54.3 + 50.5 + 42.9 + 39.8 + 0.5·44.2) / 12 = 49.042` — R gives **49.042** ✓

The first 6 and last 6 trend values do not exist (the window would run outside the data).

**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:

| t | time | y_t | T_t | y−T | position |
|---|---|---|---|---|---|
| 7 | 1920.5 | 57.70 | 49.04 | 8.658 | Jul |
| 8 | 1920.58 | 56.40 | 49.15 | 7.250 | Aug |
| 9 | 1920.67 | 54.30 | 49.14 | 5.162 | Sep |
| 10 | 1920.75 | 50.50 | 49.18 | 1.321 | Oct |
| 11 | 1920.83 | 42.90 | 49.19 | -6.292 | Nov |
| 12 | 1920.92 | 39.80 | 49.20 | -9.400 | Dec |
| 13 | 1921 | 44.20 | 49.57 | -5.367 | Jan |
| 14 | 1921.08 | 39.80 | 50.07 | -10.271 | Feb |
| 15 | 1921.17 | 45.10 | 50.33 | -5.229 | Mar |
| 16 | 1921.25 | 47.00 | 50.60 | -3.596 | Apr |
| 17 | 1921.33 | 54.10 | 50.62 | 3.483 | May |
| 18 | 1921.42 | 58.70 | 50.61 | 8.092 | Jun |

**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them (averaging cancels the noise), then force the coefficients to sum to 0:

| Position | n ratios | raw | normalised (decompose) | meaning |
|---|---|---|---|---|
| Jan | 19 | -9.3618 | -9.3394 | -9.3 vs trend |
| Feb | 19 | -9.9224 | -9.8999 | -9.9 vs trend |
| Mar | 19 | -6.9691 | -6.9466 | -6.9 vs trend |
| Apr | 19 | -2.7798 | -2.7573 | -2.8 vs trend |
| May | 19 | 3.4309 | 3.4534 | +3.5 vs trend |
| Jun | 19 | 8.9640 | 8.9865 | +9.0 vs trend |
| Jul | 19 | 12.9447 | 12.9672 | +13.0 vs trend |
| Aug | 19 | 11.4366 | 11.4591 | +11.5 vs trend |
| Sep | 19 | 7.3776 | 7.4001 | +7.4 vs trend |
| Oct | 19 | 0.6322 | 0.6547 | +0.7 vs trend |
| Nov | 19 | -6.6401 | -6.6177 | -6.6 vs trend |
| Dec | 19 | -9.3827 | -9.3602 | -9.4 vs trend |

The raw coefficients average -0.0225; they are rescaled to 0 so the season does not also move the overall level. Largest: **Jul**, smallest: **Feb**.

**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = y_t − S`; the residual is what trend × season (or trend + season) does not explain. Example at t = 7: y = 57.70, T = 49.04, S = 12.9672 ⇒ CVS = 44.73, residual = -4.3089 (0 = perfect fit).

### Validation (step 7)

`mean=-0.02248 sd=2.079 | Ljung-Box p=7.138e-07 (autocorrelated) | Shapiro p=0.373 (normal)`

Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.

### Forecast (step 8)

Split: `train = 204 obs. | test = 36 obs. (de 1937.00 à 1939.92)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| Décomposition (tendance + saison) | 2.06 | 1.56 | 3.4 |
| ARIMA(1,0,2)(1,1,2)[12] | 2.15 | 1.71 | 3.7 |
| Holt-Winters | 2.25 | 1.76 | 3.8 |
| Naïf | 3.11 | 2.39 | 5.4 |
| LED (Holt) | 9.42 | 7.69 | 14.6 |
| LES | 11.61 | 9.17 | 16.7 |

Best on the test set: **Décomposition (tendance + saison)** (RMSE 2.06). The decomposition method ranks 1 of 6. LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. Holt-Winters adds it and updates it each period. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=1.000 | LED : alpha=1.000 beta=0.000; Holt-Winters : alpha=0.163 beta=0.021 gamma=0.259` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

An α (and/or β) of exactly 1.000 means the optimiser hit its boundary: the smoother just repeats the last observation/slope, which is a symptom of a model that does not fit the series (no seasonal term here).

Model chosen by `auto.arima`: `ARIMA(1,0,2)(1,1,2)[12]`.

### ⭐ Subject-specific question — results from the log

```
⭐ Que reste-t-il dans les résidus ? (ordre AR par AIC)
ordre AR sélectionné : 6
coefficients AR : -0.037 -0.121 -0.224 -0.268 -0.193 -0.153
```

## 3. What to watch for in this subject

- Very strong and stable annual cycle, no trend: **additive** (temperatures can be near 0 or negative in °C, so a percentage model makes no sense).
- Because the seasonal model fits so well, the interesting question is what is left in the residuals (⭐ block: AR order of the residuals).
- A degree-Fahrenheit coefficient is directly interpretable: '+2 °F above the annual mean'.

**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.

## 4. Code and how to run

Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):

```r
res <- run_pipeline(y, 36, OUT, name = "nottem", model = "additive")
```

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/13_Environnement_Temperature_Nottingham"
Rscript solution.R      # sorties_R/
python3 solution.py     # sorties_python/
```
