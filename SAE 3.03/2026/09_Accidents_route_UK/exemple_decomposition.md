# UK driver deaths (UKDriverDeaths) — decomposition and forecasting explained

> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; here we apply the same method to **this** series.

## 0. The method in 6 lines

1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.
2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.
3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).
4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).
5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.
6. Always compare with a naïve forecast.

## 1. The data and its context

Monthly drivers killed or seriously injured in Great Britain, January 1969 → December 1984. The **seat-belt law came into force on 31 January 1983**.

## 2. Run: monthly 1969–1984

**Series**: UKDriverDeaths — n = 192, frequency = 12 per cycle, from 1969/1 to 1984.92.

Summary: `Min. 1057 | 1st Qu. 1461.75 | Median 1631 | Mean 1670.31 | 3rd Qu. 1850.75 | Max. 2654 | sd=289.61 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.0100 | stationary — H0 'unit root' rejected |
| Mann-Kendall (trend) | 3.629e-10 | significant monotone trend |
| Pettitt (level break) | 3.03e-10 | level break around 1975.00 |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### Additive or multiplicative? (step 6a — Buys-Ballot)

For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. If `a` is significantly positive the swings grow with the level ⇒ multiplicative.

| Cycle | Mean | Std |
|---|---|---|
| 1 | 1662.58 | 241.90 |
| 2 | 1828.25 | 284.98 |
| 3 | 1859.08 | 214.14 |
| … | … | … |
| 15 | 1289.33 | 177.22 |
| 16 | 1368.42 | 218.05 |

Slope **a = 0.0495**, p = 0.4395, 16 cycles ⇒ Buys-Ballot suggests **ADDITIVE**. The spread does not grow significantly with the level: seasonal effects are constant amounts. (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)

### Decomposition step by step (step 6b)

**Step A — centred moving average.** The period is p = 12 (even), so a window of 12 values has no centre. Use 13 values with half weight on the two ends:

```
T_t = (0.5·y_(t-6) + y_(t-5) + … + y_(t+5) + 0.5·y_(t+6)) / 12
```

By hand at t = 7: `T_7 = (0.5·1687 + 1508 + 1507 + 1385 + 1632 + 1511 + 1559 + 1630 + 1579 + 1653 + 2152 + 2148 + 0.5·1752) / 12 = 1665.292` — R gives **1665.292** ✓

The first 6 and last 6 trend values do not exist (the window would run outside the data).

**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:

| t | time | y_t | T_t | y−T | position |
|---|---|---|---|---|---|
| 7 | 1969.5 | 1559.00 | 1665.29 | -106.292 | Jul |
| 8 | 1969.58 | 1630.00 | 1678.71 | -48.708 | Aug |
| 9 | 1969.67 | 1579.00 | 1698.17 | -119.167 | Sep |
| 10 | 1969.75 | 1653.00 | 1714.12 | -61.125 | Oct |
| 11 | 1969.83 | 2152.00 | 1718.96 | 433.042 | Nov |
| 12 | 1969.92 | 2148.00 | 1716.96 | 431.042 | Dec |
| 13 | 1970 | 1752.00 | 1727.58 | 24.417 | Jan |
| 14 | 1970.08 | 1765.00 | 1744.92 | 20.083 | Feb |
| 15 | 1970.17 | 1717.00 | 1757.83 | -40.833 | Mar |
| 16 | 1970.25 | 1558.00 | 1778.46 | -220.458 | Apr |
| 17 | 1970.33 | 1575.00 | 1797.00 | -222.000 | May |
| 18 | 1970.42 | 1520.00 | 1814.50 | -294.500 | Jun |

**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them (averaging cancels the noise), then force the coefficients to sum to 0:

| Position | n ratios | raw | normalised (decompose) | meaning |
|---|---|---|---|---|
| Jan | 15 | 19.3583 | 19.6417 | +19.6 vs trend |
| Feb | 15 | -180.1444 | -179.8611 | -179.9 vs trend |
| Mar | 15 | -124.8083 | -124.5250 | -124.5 vs trend |
| Apr | 15 | -236.8167 | -236.5333 | -236.5 vs trend |
| May | 15 | -105.4472 | -105.1639 | -105.2 vs trend |
| Jun | 15 | -154.6250 | -154.3417 | -154.3 vs trend |
| Jul | 15 | -72.3167 | -72.0333 | -72.0 vs trend |
| Aug | 15 | -58.7139 | -58.4306 | -58.4 vs trend |
| Sep | 15 | -11.4694 | -11.1861 | -11.2 vs trend |
| Oct | 15 | 129.8528 | 130.1361 | +130.1 vs trend |
| Nov | 15 | 333.6139 | 333.8972 | +333.9 vs trend |
| Dec | 15 | 458.1167 | 458.4000 | +458.4 vs trend |

The raw coefficients average -0.2833; they are rescaled to 0 so the season does not also move the overall level. Largest: **Dec**, smallest: **Apr**.

**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = y_t − S`; the residual is what trend × season (or trend + season) does not explain. Example at t = 7: y = 1559.00, T = 1665.29, S = -72.0333 ⇒ CVS = 1631.03, residual = -34.2583 (0 = perfect fit).

### Validation (step 7)

`mean=-0.2833 sd=111.5 | Ljung-Box p=0.0004481 (autocorrelated) | Shapiro p=0.399 (normal)`

Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.

### Forecast (step 8)

Split: `train = 168 obs. | test = 24 obs. (de 1983.00 à 1984.92)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| Décomposition (tendance + saison) | 246.41 | 221.44 | 17.3 |
| Naïf | 325.27 | 295.96 | 23.0 |
| ARIMA(0,0,2)(0,1,2)[12] | 355.69 | 339.45 | 26.4 |
| Holt-Winters | 382.83 | 371.04 | 28.9 |
| LES | 762.20 | 737.02 | 58.6 |
| LED (Holt) | 1040.63 | 1025.08 | 80.0 |

Best on the test set: **Décomposition (tendance + saison)** (RMSE 246.41). The decomposition method ranks 1 of 6. LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. Holt-Winters adds it and updates it each period. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=0.874 | LED : alpha=0.940 beta=0.049; Holt-Winters : alpha=0.343 beta=0.015 gamma=0.269` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

Model chosen by `auto.arima`: `ARIMA(0,0,2)(0,1,2)[12]`.

### ⭐ Subject-specific question — results from the log

```
Date de rupture trouvée par Pettitt : 1975.00 (loi : 31/01/1983)

⭐ Effet estimé de la loi sur la ceinture = (prévu sans l'événement) - (observé), sur le test
  Décomposition (tendance + saison)       écart cumulé=   5314.5  soit  14.3% du prévu
  LES                                      écart cumulé=  17688.4  soit  35.7% du prévu
  LED (Holt)                               écart cumulé=  24602.0  soit  43.5% du prévu
  Holt-Winters                             écart cumulé=   8904.9  soit  21.8% du prévu
  ARIMA(0,0,2)(0,1,2)[12]                  écart cumulé=   8146.8  soit  20.3% du prévu
  Naïf                                    écart cumulé=   7027.0  soit  18.1% du prévu
```

## 3. What to watch for in this subject

- The 24-month test set (1983–84) is entirely *after* the law: a model trained before it will over-forecast — the gap measures the effect of the law (⭐ block).
- Pettitt should detect a break close to January 1983; the oil crisis of 1973–74 also shows up as a dip.
- Seasonality: more accidents in winter (dark, bad weather).

**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.

## 4. Code and how to run

Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):

```r
res <- run_pipeline(y, 24, OUT, name = "UKDriverDeaths")
effect_of_break(y, length(y) - 24, res$F, "⭐ Effet estimé de la loi sur la ceinture")
```

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/09_Accidents_route_UK"
Rscript solution.R      # sorties_R/
python3 solution.py     # sorties_python/
```
