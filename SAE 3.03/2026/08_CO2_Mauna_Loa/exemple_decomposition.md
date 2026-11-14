# Atmospheric CO₂ at Mauna Loa (co2) — decomposition and forecasting explained

> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; here we apply the same method to **this** series.

## 0. The method in 6 lines

1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.
2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.
3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).
4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).
5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.
6. Always compare with a naïve forecast.

## 1. The data and its context

Monthly CO₂ concentration near Mauna Loa (Hawaii), ppm, 1959–1997 — the Keeling curve. Photosynthesis in the northern hemisphere makes it dip every summer; fossil-fuel emissions make it rise.

## 2. Run: monthly 1959–1997

**Series**: CO2 Mauna Loa — n = 468, frequency = 12 per cycle, from 1959/1 to 1997.92.

Summary: `Min. 313.18 | 1st Qu. 323.53 | Median 335.17 | Mean 337.05 | 3rd Qu. 350.26 | Max. 366.84 | sd=14.97 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.2269 | **not** stationary — H0 'unit root' kept |
| Mann-Kendall (trend) | 8.994e-188 | significant monotone trend |
| Pettitt (level break) | 7.39e-76 | level break around 1978.08 |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### Additive or multiplicative? (step 6a — Buys-Ballot)

For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. If `a` is significantly positive the swings grow with the level ⇒ multiplicative.

| Cycle | Mean | Std |
|---|---|---|
| 1 | 315.83 | 1.62 |
| 2 | 316.75 | 2.04 |
| 3 | 317.49 | 1.78 |
| … | … | … |
| 38 | 362.69 | 2.03 |
| 39 | 363.82 | 2.05 |

Slope **a = 0.0059**, p = 0.0002573, 39 cycles ⇒ Buys-Ballot suggests **MULTIPLICATIVE**. The spread grows with the level: seasonal effects are percentages of the trend. (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)

**But `solution.R` imposes the ADDITIVE model.** Do not hide the disagreement in your report: the slope may be statistically significant yet practically small (here the cycle standard deviation goes from 1.62 to 2.05 while the mean goes from 315.83 to 363.82), so judge the *size* of the effect, the band plot, and the residuals of both decompositions before choosing. The tables below use the additive model.

### Decomposition step by step (step 6b)

**Step A — centred moving average.** The period is p = 12 (even), so a window of 12 values has no centre. Use 13 values with half weight on the two ends:

```
T_t = (0.5·y_(t-6) + y_(t-5) + … + y_(t+5) + 0.5·y_(t+6)) / 12
```

By hand at t = 7: `T_7 = (0.5·315.42 + 316.31 + 316.5 + 317.56 + 318.13 + 318 + 316.39 + 314.65 + 313.68 + 313.18 + 314.66 + 315.43 + 0.5·316.27) / 12 = 315.861` — R gives **315.861** ✓

The first 6 and last 6 trend values do not exist (the window would run outside the data).

**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:

| t | time | y_t | T_t | y−T | position |
|---|---|---|---|---|---|
| 7 | 1959.5 | 316.39 | 315.86 | 0.529 | Jul |
| 8 | 1959.58 | 314.65 | 315.92 | -1.267 | Aug |
| 9 | 1959.67 | 313.68 | 315.98 | -2.297 | Sep |
| 10 | 1959.75 | 313.18 | 316.07 | -2.890 | Oct |
| 11 | 1959.83 | 314.66 | 316.20 | -1.537 | Nov |
| 12 | 1959.92 | 315.43 | 316.33 | -0.899 | Dec |
| 13 | 1960 | 316.27 | 316.46 | -0.186 | Jan |
| 14 | 1960.08 | 316.81 | 316.57 | 0.241 | Feb |
| 15 | 1960.17 | 317.42 | 316.63 | 0.793 | Mar |
| 16 | 1960.25 | 318.87 | 316.66 | 2.208 | Apr |
| 17 | 1960.33 | 319.87 | 316.69 | 3.180 | May |
| 18 | 1960.42 | 319.43 | 316.72 | 2.708 | Jun |

**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them (averaging cancels the noise), then force the coefficients to sum to 0:

| Position | n ratios | raw | normalised (decompose) | meaning |
|---|---|---|---|---|
| Jan | 38 | -0.0519 | -0.0536 | -0.1 vs trend |
| Feb | 38 | 0.6123 | 0.6106 | +0.6 vs trend |
| Mar | 38 | 1.3774 | 1.3756 | +1.4 vs trend |
| Apr | 38 | 2.5186 | 2.5168 | +2.5 vs trend |
| May | 38 | 3.0020 | 3.0003 | +3.0 vs trend |
| Jun | 38 | 2.3310 | 2.3292 | +2.3 vs trend |
| Jul | 38 | 0.8147 | 0.8129 | +0.8 vs trend |
| Aug | 38 | -1.2488 | -1.2505 | -1.3 vs trend |
| Sep | 38 | -3.0528 | -3.0546 | -3.1 vs trend |
| Oct | 38 | -3.2502 | -3.2519 | -3.3 vs trend |
| Nov | 38 | -2.0679 | -2.0697 | -2.1 vs trend |
| Dec | 38 | -0.9634 | -0.9651 | -1.0 vs trend |

The raw coefficients average 0.0017; they are rescaled to 0 so the season does not also move the overall level. Largest: **May**, smallest: **Oct**.

**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = y_t − S`; the residual is what trend × season (or trend + season) does not explain. Example at t = 7: y = 316.39, T = 315.86, S = 0.8129 ⇒ CVS = 315.58, residual = -0.2842 (0 = perfect fit).

### Validation (step 7)

`mean=0.001743 sd=0.2651 | Ljung-Box p=0 (autocorrelated) | Shapiro p=0.1549 (normal)`

Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.

### Forecast (step 8)

Split: `train = 384 obs. | test = 84 obs. (de 1991.00 à 1997.92)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| Holt-Winters | 1.23 | 1.12 | 0.3 |
| ARIMA(1,1,2)(2,1,2)[12] | 1.28 | 1.17 | 0.3 |
| Décomposition (tendance + saison) | 3.08 | 2.85 | 0.8 |
| Naïf | 6.07 | 5.26 | 1.5 |
| LES | 6.37 | 5.39 | 1.5 |
| LED (Holt) | 61.64 | 53.42 | 14.8 |

Best on the test set: **Holt-Winters** (RMSE 1.23). The decomposition method ranks 3 of 6. LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. Holt-Winters adds it and updates it each period. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=1.000 | LED : alpha=1.000 beta=1.000; Holt-Winters : alpha=0.493 beta=0.012 gamma=0.489` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

An α (and/or β) of exactly 1.000 means the optimiser hit its boundary: the smoother just repeats the last observation/slope, which is a symptom of a model that does not fit the series (no seasonal term here).

Model chosen by `auto.arima`: `ARIMA(1,1,2)(2,1,2)[12]`.

### ⭐ Subject-specific question — results from the log

```
⭐ Tendance linéaire vs quadratique (décomposition, sur le test)
  linear  RMSE=2.933 MAE=2.831
  quad    RMSE=3.076 MAE=2.852
Extrapolation HW (série complète) : déc. 2025 ≈ 407.6 ppm -> à comparer à la valeur NOAA/Scripps réelle (cherchez-la et commentez l'écart)
```

## 3. What to watch for in this subject

- The seasonal amplitude is constant while the level rises: **additive** model.
- The trend is slightly convex: a straight line leaves a curved pattern in the residuals; a quadratic trend does better (see ⭐).
- This is the TP example: do not stop at `decompose()` — compare methods on the 1991–97 test set and extrapolate.

**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.

## 4. Code and how to run

Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):

```r
res <- run_pipeline(co2i, 84, OUT, name = "CO2 Mauna Loa", model = "additive", trend = "quad")
```

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/08_CO2_Mauna_Loa"
Rscript solution.R      # sorties_R/
python3 solution.py     # sorties_python/
```
