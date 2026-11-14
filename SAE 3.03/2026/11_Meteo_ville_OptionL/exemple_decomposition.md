# Monthly temperature of a US city (Option L) — decomposition and forecasting explained

> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; here we apply the same method to **this** series.

## 0. The method in 6 lines

1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.
2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.
3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).
4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).
5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.
6. Always compare with a naïve forecast.

## 1. The data and its context

Hourly temperature from the Kaggle 'Historical Hourly Weather Data' (kelvin, converted to °C), averaged by month: 62 months, October 2012 → November 2017, for one city (Minneapolis; compare with San Francisco in the ⭐ block).

## 2. Run: Minneapolis, monthly

**Series**: Température mensuelle Minneapolis — n = 62, frequency = 12 per cycle, from 2012/10 to 2017.83.

Summary: `Min. -13.38 | 1st Qu. -2.83 | Median 8.52 | Mean 7.47 | 3rd Qu. 18.92 | Max. 22.58 | sd=11.36 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.0100 | stationary — H0 'unit root' rejected |
| Mann-Kendall (trend) | 0.1289 | no significant trend |
| Pettitt (level break) | 0.242 | no significant break |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### Additive or multiplicative? (step 6a — Buys-Ballot)

For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. If `a` is significantly positive the swings grow with the level ⇒ multiplicative.

| Cycle | Mean | Std |
|---|---|---|
| 1 | 7.03 | 11.83 |
| 2 | 5.68 | 13.32 |
| 3 | 6.82 | 12.86 |
| 4 | 9.31 | 10.41 |
| 5 | 8.86 | 10.46 |

Slope **a = -0.8606**, p = 0.006164, 5 cycles ⇒ Buys-Ballot suggests **ADDITIVE**. The spread does not grow significantly with the level: seasonal effects are constant amounts. (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)

### Decomposition step by step (step 6b)

**Step A — centred moving average.** The period is p = 12 (even), so a window of 12 values has no centre. Use 13 values with half weight on the two ends:

```
T_t = (0.5·y_(t-6) + y_(t-5) + … + y_(t+5) + 0.5·y_(t+6)) / 12
```

By hand at t = 7: `T_7 = (0.5·8.40926 + 2.48181 + -4.87622 + -8.63815 + -8.39676 + -3.34083 + 3.44056 + 13.5648 + 19.4462 + 22.4527 + 21.6995 + 18.0696 + 0.5·8.62077) / 12 = 7.035` — R gives **7.035** ✓

The first 6 and last 6 trend values do not exist (the window would run outside the data).

**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:

| t | time | y_t | T_t | y−T | position |
|---|---|---|---|---|---|
| 7 | 2013.25 | 3.44 | 7.03 | -3.594 | Apr |
| 8 | 2013.33 | 13.56 | 6.93 | 6.634 | May |
| 9 | 2013.42 | 19.45 | 6.55 | 12.896 | Jun |
| 10 | 2013.5 | 22.45 | 6.16 | 16.292 | Jul |
| 11 | 2013.58 | 21.70 | 5.85 | 15.850 | Aug |
| 12 | 2013.67 | 18.07 | 5.64 | 12.426 | Sep |
| 13 | 2013.75 | 8.62 | 5.73 | 2.891 | Oct |
| 14 | 2013.83 | -0.23 | 5.87 | -6.101 | Nov |
| 15 | 2013.92 | -11.30 | 5.94 | -17.248 | Dec |
| 16 | 2014 | -11.55 | 5.93 | -17.481 | Jan |
| 17 | 2014.08 | -12.96 | 5.87 | -18.828 | Feb |
| 18 | 2014.17 | -3.70 | 5.77 | -9.476 | Mar |

**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them (averaging cancels the noise), then force the coefficients to sum to 0:

| Position | n ratios | raw | normalised (decompose) | meaning |
|---|---|---|---|---|
| Jan | 4 | -16.7573 | 1.7820 | +1.8 vs trend |
| Feb | 4 | -15.6148 | -6.1887 | -6.2 vs trend |
| Mar | 4 | -7.1699 | -13.8335 | -13.8 vs trend |
| Apr | 5 | -0.3138 | -16.7879 | -16.8 vs trend |
| May | 5 | 6.8482 | -15.6454 | -15.6 vs trend |
| Jun | 4 | 12.7656 | -7.2005 | -7.2 vs trend |
| Jul | 4 | 14.7672 | -0.3445 | -0.3 vs trend |
| Aug | 4 | 13.8692 | 6.8176 | +6.8 vs trend |
| Sep | 4 | 10.1216 | 12.7350 | +12.7 vs trend |
| Oct | 4 | 1.8126 | 14.7365 | +14.7 vs trend |
| Nov | 4 | -6.1580 | 13.8385 | +13.8 vs trend |
| Dec | 4 | -13.8029 | 10.0910 | +10.1 vs trend |

The raw coefficients average 0.0306; they are rescaled to 0 so the season does not also move the overall level. Largest: **Oct**, smallest: **Apr**.

**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = y_t − S`; the residual is what trend × season (or trend + season) does not explain. Example at t = 7: y = 3.44, T = 7.03, S = -16.7879 ⇒ CVS = 3.79, residual = -3.2498 (0 = perfect fit).

### Validation (step 7)

`mean=0.03063 sd=2.058 | Ljung-Box p=0.008563 (autocorrelated) | Shapiro p=0.9332 (normal)`

Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.

### Forecast (step 8)

Split: `train = 50 obs. | test = 12 obs. (de 2016.92 à 2017.83)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| Naïf | 2.79 | 2.12 | 198.5 |
| Holt-Winters | 2.85 | 2.24 | 132.4 |
| Décomposition (tendance + saison) | 3.04 | 2.56 | 133.6 |
| ARIMA(0,1,1)(0,1,1)[12] | 3.15 | 2.75 | 180.6 |
| LES | 10.55 | 9.62 | 309.5 |
| LED (Holt) | 42.60 | 36.39 | 1412.7 |

Best on the test set: **Naïf** (RMSE 2.79). The decomposition method ranks 3 of 6. LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. Holt-Winters adds it and updates it each period. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=1.000 | LED : alpha=0.935 beta=1.000; Holt-Winters : alpha=0.325 beta=0.002 gamma=1.000` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

An α (and/or β) of exactly 1.000 means the optimiser hit its boundary: the smoother just repeats the last observation/slope, which is a symptom of a model that does not fit the series (no seasonal term here).

Model chosen by `auto.arima`: `ARIMA(0,1,1)(0,1,1)[12]`.

### ⭐ Subject-specific question — results from the log

```
⭐ Effet de la granularité (cycle jour/nuit vs année)
Cycle journalier : amplitude (max-min des moyennes horaires) = 6.9 °C
Cycle annuel     : amplitude (max-min des moyennes mensuelles) = 36.0 °C
  Minneapolis     amplitude saisonnière = 31.5 °C
  San Francisco   amplitude saisonnière = 9.5 °C
```

## 3. What to watch for in this subject

- Only 5 cycles and no significant trend: you cannot conclude anything about climate change from 5 years.
- Hourly gaps must be handled before averaging (missing hours, interpolation).
- Granularity matters: hourly data show the day/night cycle, monthly data the annual cycle — both are in the ⭐ block.

**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.

## 4. Code and how to run

Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):

```r
res <- run_pipeline(tsm, 12, OUT, name = paste("Température mensuelle", CITY), model = "additive")
```

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/11_Meteo_ville_OptionL"
Rscript solution.R      # sorties_R/
python3 solution.py     # sorties_python/
```
