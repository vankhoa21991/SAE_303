# UK lung-disease deaths (mdeaths, fdeaths, ldeaths) — decomposition and forecasting explained

> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; here we apply the same method to **this** series.

## 0. The method in 6 lines

1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.
2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.
3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).
4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).
5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.
6. Always compare with a naïve forecast.

## 1. The data and its context

Monthly UK deaths from bronchitis, emphysema and asthma, 1974–1979 (72 months): `mdeaths` = men, `fdeaths` = women, `ldeaths` = total. Deaths peak in winter (cold, respiratory infections).

## 2. Run: mdeaths — men

**Series**: mdeaths — n = 72, frequency = 12 per cycle, from 1974/1 to 1979.92.

Summary: `Min. 940 | 1st Qu. 1138.25 | Median 1344 | Mean 1495.94 | 3rd Qu. 1846 | Max. 2750 | sd=433.15 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.0100 | stationary — H0 'unit root' rejected |
| Mann-Kendall (trend) | 0.005184 | significant monotone trend |
| Pettitt (level break) | 0.0221 | level break around 1976.33 |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### Additive or multiplicative? (step 6a — Buys-Ballot)

For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. If `a` is significantly positive the swings grow with the level ⇒ multiplicative.

| Cycle | Mean | Std |
|---|---|---|
| 1 | 1589.25 | 328.79 |
| 2 | 1603.92 | 427.50 |
| 3 | 1558.08 | 579.87 |
| … | … | … |
| 5 | 1444.08 | 451.15 |
| 6 | 1369.75 | 414.86 |

Slope **a = 0.0732**, p = 0.8686, 6 cycles ⇒ Buys-Ballot suggests **ADDITIVE**. The spread does not grow significantly with the level: seasonal effects are constant amounts. (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)

### Decomposition step by step (step 6b)

**Step A — centred moving average.** The period is p = 12 (even), so a window of 12 values has no centre. Use 13 values with half weight on the two ends:

```
T_t = (0.5·y_(t-6) + y_(t-5) + … + y_(t+5) + 0.5·y_(t+6)) / 12
```

By hand at t = 7: `T_7 = (0.5·2134 + 1863 + 1877 + 1877 + 1492 + 1249 + 1280 + 1131 + 1209 + 1492 + 1621 + 1846 + 0.5·2103) / 12 = 1587.958` — R gives **1587.958** ✓

The first 6 and last 6 trend values do not exist (the window would run outside the data).

**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:

| t | time | y_t | T_t | y−T | position |
|---|---|---|---|---|---|
| 7 | 1974.5 | 1280.00 | 1587.96 | -307.958 | Jul |
| 8 | 1974.58 | 1131.00 | 1598.08 | -467.083 | Aug |
| 9 | 1974.67 | 1209.00 | 1621.00 | -412.000 | Sep |
| 10 | 1974.75 | 1492.00 | 1630.67 | -138.667 | Oct |
| 11 | 1974.83 | 1621.00 | 1625.12 | -4.125 | Nov |
| 12 | 1974.92 | 1846.00 | 1623.04 | 222.958 | Dec |
| 13 | 1975 | 2103.00 | 1620.75 | 482.250 | Jan |
| 14 | 1975.08 | 2137.00 | 1616.92 | 520.083 | Feb |
| 15 | 1975.17 | 2153.00 | 1610.50 | 542.500 | Mar |
| 16 | 1975.25 | 1833.00 | 1597.96 | 235.042 | Apr |
| 17 | 1975.33 | 1403.00 | 1588.75 | -185.750 | May |
| 18 | 1975.42 | 1288.00 | 1594.75 | -306.750 | Jun |

**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them (averaging cancels the noise), then force the coefficients to sum to 0:

| Position | n ratios | raw | normalised (decompose) | meaning |
|---|---|---|---|---|
| Jan | 5 | 622.0500 | 620.4472 | +620.4 vs trend |
| Feb | 5 | 621.2167 | 619.6139 | +619.6 vs trend |
| Mar | 5 | 488.9583 | 487.3556 | +487.4 vs trend |
| Apr | 5 | 118.8250 | 117.2222 | +117.2 vs trend |
| May | 5 | -209.8250 | -211.4278 | -211.4 vs trend |
| Jun | 5 | -307.0917 | -308.6944 | -308.7 vs trend |
| Jul | 5 | -369.4583 | -371.0611 | -371.1 vs trend |
| Aug | 5 | -472.7750 | -474.3778 | -474.4 vs trend |
| Sep | 5 | -484.3583 | -485.9611 | -486.0 vs trend |
| Oct | 5 | -246.0167 | -247.6194 | -247.6 vs trend |
| Nov | 5 | -119.6250 | -121.2278 | -121.2 vs trend |
| Dec | 5 | 377.3333 | 375.7306 | +375.7 vs trend |

The raw coefficients average 1.6028; they are rescaled to 0 so the season does not also move the overall level. Largest: **Jan**, smallest: **Sep**.

**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = y_t − S`; the residual is what trend × season (or trend + season) does not explain. Example at t = 7: y = 1280.00, T = 1587.96, S = -371.0611 ⇒ CVS = 1651.06, residual = 63.1028 (0 = perfect fit).

### Validation (step 7)

`mean=1.603 sd=146.6 | Ljung-Box p=0.005437 (autocorrelated) | Shapiro p=0.01288 (not normal)`

Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.

### Forecast (step 8)

Split: `train = 48 obs. | test = 24 obs. (de 1978.00 à 1979.92)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| ARIMA(0,0,1)(1,1,0)[12] | 128.48 | 86.72 | 6.3 |
| Décomposition (tendance + saison) | 156.24 | 117.77 | 8.8 |
| Naïf | 199.99 | 134.17 | 8.5 |
| Holt-Winters | 326.13 | 292.00 | 22.1 |
| LES | 484.85 | 448.15 | 36.7 |
| LED (Holt) | 933.46 | 827.64 | 70.7 |

Best on the test set: **ARIMA(0,0,1)(1,1,0)[12]** (RMSE 128.48). The decomposition method ranks 2 of 6. LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. Holt-Winters adds it and updates it each period. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=1.000 | LED : alpha=1.000 beta=0.121; Holt-Winters : alpha=0.016 beta=1.000 gamma=0.000` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

An α (and/or β) of exactly 1.000 means the optimiser hit its boundary: the smoother just repeats the last observation/slope, which is a symptom of a model that does not fit the series (no seasonal term here).

Model chosen by `auto.arima`: `ARIMA(0,0,1)(1,1,0)[12]`.

## 3. Run: fdeaths — women

**Series**: fdeaths — n = 72, frequency = 12 per cycle, from 1974/1 to 1979.92.

Summary: `Min. 330 | 1st Qu. 411 | Median 512 | Mean 560.68 | 3rd Qu. 681.5 | Max. 1141 | sd=179.72 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.0100 | stationary — H0 'unit root' rejected |
| Mann-Kendall (trend) | 0.09636 | no significant trend |
| Pettitt (level break) | 0.245 | no significant break |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### Additive or multiplicative? (step 6a — Buys-Ballot)

For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. If `a` is significantly positive the swings grow with the level ⇒ multiplicative.

| Cycle | Mean | Std |
|---|---|---|
| 1 | 589.08 | 169.74 |
| 2 | 571.17 | 176.15 |
| 3 | 585.08 | 252.61 |
| … | … | … |
| 5 | 551.83 | 170.89 |
| 6 | 541.75 | 160.01 |

Slope **a = 0.7814**, p = 0.2429, 6 cycles ⇒ Buys-Ballot suggests **ADDITIVE**. The spread does not grow significantly with the level: seasonal effects are constant amounts. (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)

### Decomposition step by step (step 6b)

**Step A — centred moving average.** The period is p = 12 (even), so a window of 12 values has no centre. Use 13 values with half weight on the two ends:

```
T_t = (0.5·y_(t-6) + y_(t-5) + … + y_(t+5) + 0.5·y_(t+6)) / 12
```

By hand at t = 7: `T_7 = (0.5·901 + 689 + 827 + 677 + 522 + 406 + 441 + 393 + 387 + 582 + 578 + 666 + 0.5·830) / 12 = 586.125` — R gives **586.125** ✓

The first 6 and last 6 trend values do not exist (the window would run outside the data).

**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:

| t | time | y_t | T_t | y−T | position |
|---|---|---|---|---|---|
| 7 | 1974.5 | 441.00 | 586.12 | -145.125 | Jul |
| 8 | 1974.58 | 393.00 | 585.79 | -192.792 | Aug |
| 9 | 1974.67 | 387.00 | 586.67 | -199.667 | Sep |
| 10 | 1974.75 | 582.00 | 584.38 | -2.375 | Oct |
| 11 | 1974.83 | 578.00 | 581.54 | -3.542 | Nov |
| 12 | 1974.92 | 666.00 | 580.58 | 85.417 | Dec |
| 13 | 1975 | 830.00 | 581.08 | 248.917 | Jan |
| 14 | 1975.08 | 752.00 | 581.04 | 170.958 | Feb |
| 15 | 1975.17 | 785.00 | 580.00 | 205.000 | Mar |
| 16 | 1975.25 | 664.00 | 572.25 | 91.750 | Apr |
| 17 | 1975.33 | 467.00 | 564.38 | -97.375 | May |
| 18 | 1975.42 | 438.00 | 566.79 | -128.792 | Jun |

**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them (averaging cancels the noise), then force the coefficients to sum to 0:

| Position | n ratios | raw | normalised (decompose) | meaning |
|---|---|---|---|---|
| Jan | 5 | 253.8667 | 253.3042 | +253.3 vs trend |
| Feb | 5 | 277.2833 | 276.7208 | +276.7 vs trend |
| Mar | 5 | 200.7500 | 200.1875 | +200.2 vs trend |
| Apr | 5 | 39.9250 | 39.3625 | +39.4 vs trend |
| May | 5 | -72.4917 | -73.0542 | -73.1 vs trend |
| Jun | 5 | -130.7667 | -131.3292 | -131.3 vs trend |
| Jul | 5 | -147.8000 | -148.3625 | -148.4 vs trend |
| Aug | 5 | -194.9333 | -195.4958 | -195.5 vs trend |
| Sep | 5 | -191.7000 | -192.2625 | -192.3 vs trend |
| Oct | 5 | -106.1250 | -106.6875 | -106.7 vs trend |
| Nov | 5 | -63.4167 | -63.9792 | -64.0 vs trend |
| Dec | 5 | 142.1583 | 141.5958 | +141.6 vs trend |

The raw coefficients average 0.5625; they are rescaled to 0 so the season does not also move the overall level. Largest: **Feb**, smallest: **Aug**.

**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = y_t − S`; the residual is what trend × season (or trend + season) does not explain. Example at t = 7: y = 441.00, T = 586.12, S = -148.3625 ⇒ CVS = 589.36, residual = 3.2375 (0 = perfect fit).

### Validation (step 7)

`mean=0.5625 sd=63.46 | Ljung-Box p=0.01034 (autocorrelated) | Shapiro p=0.0005 (not normal)`

Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.

### Forecast (step 8)

Split: `train = 48 obs. | test = 24 obs. (de 1978.00 à 1979.92)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| ARIMA(0,0,0)(1,1,0)[12] | 38.03 | 30.10 | 5.8 |
| Décomposition (tendance + saison) | 59.43 | 48.69 | 10.4 |
| Naïf | 64.74 | 49.04 | 8.2 |
| Holt-Winters | 69.73 | 62.06 | 12.4 |
| LES | 182.92 | 168.87 | 35.7 |
| LED (Holt) | 879.32 | 773.15 | 165.3 |

Best on the test set: **ARIMA(0,0,0)(1,1,0)[12]** (RMSE 38.03). The decomposition method ranks 2 of 6. LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. Holt-Winters adds it and updates it each period. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=1.000 | LED : alpha=1.000 beta=0.254; Holt-Winters : alpha=0.000 beta=0.000 gamma=0.078` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

An α (and/or β) of exactly 1.000 means the optimiser hit its boundary: the smoother just repeats the last observation/slope, which is a symptom of a model that does not fit the series (no seasonal term here).

Model chosen by `auto.arima`: `ARIMA(0,0,0)(1,1,0)[12]`.

## 4. Run: ldeaths — both sexes

**Series**: ldeaths — n = 72, frequency = 12 per cycle, from 1974/1 to 1979.92.

Summary: `Min. 1300 | 1st Qu. 1551.75 | Median 1870 | Mean 2056.62 | 3rd Qu. 2552.5 | Max. 3891 | sd=609.85 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.0100 | stationary — H0 'unit root' rejected |
| Mann-Kendall (trend) | 0.01027 | significant monotone trend |
| Pettitt (level break) | 0.0424 | level break around 1976.33 |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### Additive or multiplicative? (step 6a — Buys-Ballot)

For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. If `a` is significantly positive the swings grow with the level ⇒ multiplicative.

| Cycle | Mean | Std |
|---|---|---|
| 1 | 2178.33 | 494.60 |
| 2 | 2175.08 | 602.25 |
| 3 | 2143.17 | 831.87 |
| … | … | … |
| 5 | 1995.92 | 621.57 |
| 6 | 1911.50 | 572.25 |

Slope **a = 0.2116**, p = 0.6695, 6 cycles ⇒ Buys-Ballot suggests **ADDITIVE**. The spread does not grow significantly with the level: seasonal effects are constant amounts. (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)

### Decomposition step by step (step 6b)

**Step A — centred moving average.** The period is p = 12 (even), so a window of 12 values has no centre. Use 13 values with half weight on the two ends:

```
T_t = (0.5·y_(t-6) + y_(t-5) + … + y_(t+5) + 0.5·y_(t+6)) / 12
```

By hand at t = 7: `T_7 = (0.5·3035 + 2552 + 2704 + 2554 + 2014 + 1655 + 1721 + 1524 + 1596 + 2074 + 2199 + 2512 + 0.5·2933) / 12 = 2174.083` — R gives **2174.083** ✓

The first 6 and last 6 trend values do not exist (the window would run outside the data).

**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:

| t | time | y_t | T_t | y−T | position |
|---|---|---|---|---|---|
| 7 | 1974.5 | 1721.00 | 2174.08 | -453.083 | Jul |
| 8 | 1974.58 | 1524.00 | 2183.88 | -659.875 | Aug |
| 9 | 1974.67 | 1596.00 | 2207.67 | -611.667 | Sep |
| 10 | 1974.75 | 2074.00 | 2215.04 | -141.042 | Oct |
| 11 | 1974.83 | 2199.00 | 2206.67 | -7.667 | Nov |
| 12 | 1974.92 | 2512.00 | 2203.62 | 308.375 | Dec |
| 13 | 1975 | 2933.00 | 2201.83 | 731.167 | Jan |
| 14 | 1975.08 | 2889.00 | 2197.96 | 691.042 | Feb |
| 15 | 1975.17 | 2938.00 | 2190.50 | 747.500 | Mar |
| 16 | 1975.25 | 2497.00 | 2170.21 | 326.792 | Apr |
| 17 | 1975.33 | 1870.00 | 2153.12 | -283.125 | May |
| 18 | 1975.42 | 1726.00 | 2161.54 | -435.542 | Jun |

**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them (averaging cancels the noise), then force the coefficients to sum to 0:

| Position | n ratios | raw | normalised (decompose) | meaning |
|---|---|---|---|---|
| Jan | 5 | 875.9167 | 873.7514 | +873.8 vs trend |
| Feb | 5 | 898.5000 | 896.3347 | +896.3 vs trend |
| Mar | 5 | 689.7083 | 687.5431 | +687.5 vs trend |
| Apr | 5 | 158.7500 | 156.5847 | +156.6 vs trend |
| May | 5 | -282.3167 | -284.4819 | -284.5 vs trend |
| Jun | 5 | -437.8583 | -440.0236 | -440.0 vs trend |
| Jul | 5 | -517.2583 | -519.4236 | -519.4 vs trend |
| Aug | 5 | -667.7083 | -669.8736 | -669.9 vs trend |
| Sep | 5 | -676.0583 | -678.2236 | -678.2 vs trend |
| Oct | 5 | -352.1417 | -354.3069 | -354.3 vs trend |
| Nov | 5 | -183.0417 | -185.2069 | -185.2 vs trend |
| Dec | 5 | 519.4917 | 517.3264 | +517.3 vs trend |

The raw coefficients average 2.1653; they are rescaled to 0 so the season does not also move the overall level. Largest: **Feb**, smallest: **Sep**.

**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = y_t − S`; the residual is what trend × season (or trend + season) does not explain. Example at t = 7: y = 1721.00, T = 2174.08, S = -519.4236 ⇒ CVS = 2240.42, residual = 66.3403 (0 = perfect fit).

### Validation (step 7)

`mean=2.165 sd=205.6 | Ljung-Box p=0.005829 (autocorrelated) | Shapiro p=0.0027 (not normal)`

Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.

### Forecast (step 8)

Split: `train = 48 obs. | test = 24 obs. (de 1978.00 à 1979.92)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| ARIMA(0,0,2)(1,1,0)[12] with drift | 162.21 | 139.18 | 8.0 |
| Décomposition (tendance + saison) | 206.68 | 165.70 | 9.2 |
| Naïf | 256.23 | 167.79 | 7.5 |
| Holt-Winters | 388.32 | 347.49 | 19.0 |
| LES | 666.36 | 617.02 | 36.4 |
| LED (Holt) | 1929.22 | 1701.95 | 103.6 |

Best on the test set: **ARIMA(0,0,2)(1,1,0)[12] with drift** (RMSE 162.21). The decomposition method ranks 2 of 6. LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. Holt-Winters adds it and updates it each period. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=1.000 | LED : alpha=1.000 beta=0.177; Holt-Winters : alpha=0.013 beta=1.000 gamma=0.000` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

An α (and/or β) of exactly 1.000 means the optimiser hit its boundary: the smoother just repeats the last observation/slope, which is a symptom of a model that does not fit the series (no seasonal term here).

Model chosen by `auto.arima`: `ARIMA(0,0,2)(1,1,0)[12] with drift`.

### ⭐ Subject-specific question — results from the log

```
Additif vs multiplicatif — critère chiffré
  additive        RMSE=203.923  MAPE=6.57%  autocorr(1) résidus=0.10
  multiplicative  RMSE=202.433  MAPE=6.32%  autocorr(1) résidus=0.08
```

## 5. Extra results: `comparaison_m_f`

```
⭐ EMS-2 : coefficients saisonniers hommes vs femmes
corrélation des profils saisonniers : 0.998
mois de pic : 1 (hommes)  2 (femmes)
amplitude (max-min) : 1106.4 vs 472.2
```

## 6. What to watch for in this subject

- Only 6 cycles: every seasonal coefficient is the average of just 6 ratios, and the 24-month test set is a third of the data. State what so little data can and cannot prove.
- Early 1976 shows an unusually high winter peak: decide whether it is an outlier or a real event, and find a source for the explanation.
- Men and women have similar *shapes* but different *levels*: compare the coefficients (the ⭐ block), not the raw values.

**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.

## 7. Code and how to run

Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):

```r
Rm <- run_pipeline(mdeaths, 24, file.path(SRT, "mdeaths"), name = "mdeaths")
Rf <- run_pipeline(fdeaths, 24, file.path(SRT, "fdeaths"), name = "fdeaths")
res <- run_pipeline(ldeaths, 24, file.path(SRT, "ldeaths"), name = "ldeaths")
compare_add_mult(ldeaths)
```

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/02_Medecine_Deces_pulmonaires"
Rscript solution.R      # sorties_R/
python3 solution.py     # sorties_python/
```
