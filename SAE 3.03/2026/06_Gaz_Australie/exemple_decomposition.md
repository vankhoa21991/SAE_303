# Australian gas production (gas) — decomposition and forecasting explained

> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; here we apply the same method to **this** series.

## 0. The method in 6 lines

1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.
2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.
3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).
4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).
5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.
6. Always compare with a naïve forecast.

## 1. The data and its context

Monthly Australian gas production, 1956 → August 1995 (476 observations, `forecast::gas`). Production exploded after the 1960s–70s.

## 2. Run: monthly 1956–1995

**Series**: gas (Australie) — n = 476, frequency = 12 per cycle, from 1956/1 to 1995.58.

Summary: `Min. 1646 | 1st Qu. 2674.75 | Median 16787.5 | Mean 21415.27 | 3rd Qu. 38628.5 | Max. 66600 | sd=18678.34 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.2764 | **not** stationary — H0 'unit root' kept |
| Mann-Kendall (trend) | 6.951e-159 | significant monotone trend |
| Pettitt (level break) | 2.51e-77 | level break around 1976.33 |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### Additive or multiplicative? (step 6a — Buys-Ballot)

For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. If `a` is significantly positive the swings grow with the level ⇒ multiplicative.

| Cycle | Mean | Std |
|---|---|---|
| 1 | 2041.42 | 278.36 |
| 2 | 2103.08 | 293.38 |
| 3 | 2136.75 | 339.02 |
| … | … | … |
| 38 | 46332.33 | 8281.92 |
| 39 | 51035.83 | 8750.58 |

Slope **a = 0.1603**, p = 1.064e-31, 39 cycles ⇒ Buys-Ballot suggests **MULTIPLICATIVE**. The spread grows with the level: seasonal effects are percentages of the trend. (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)

### Decomposition step by step (step 6b)

**Step A — centred moving average.** The period is p = 12 (even), so a window of 12 values has no centre. Use 13 values with half weight on the two ends:

```
T_t = (0.5·y_(t-6) + y_(t-5) + … + y_(t+5) + 0.5·y_(t+6)) / 12
```

By hand at t = 7: `T_7 = (0.5·1709 + 1646 + 1794 + 1878 + 2173 + 2321 + 2468 + 2416 + 2184 + 2121 + 1962 + 1825 + 0.5·1751) / 12 = 2043.167` — R gives **2043.167** ✓

The first 6 and last 6 trend values do not exist (the window would run outside the data).

**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:

| t | time | y_t | T_t | y/T | position |
|---|---|---|---|---|---|
| 7 | 1956.5 | 2468.00 | 2043.17 | 1.208 | Jul |
| 8 | 1956.58 | 2416.00 | 2046.67 | 1.180 | Aug |
| 9 | 1956.67 | 2184.00 | 2053.67 | 1.063 | Sep |
| 10 | 1956.75 | 2121.00 | 2061.54 | 1.029 | Oct |
| 11 | 1956.83 | 1962.00 | 2069.92 | 0.948 | Nov |
| 12 | 1956.92 | 1825.00 | 2073.92 | 0.880 | Dec |
| 13 | 1957 | 1751.00 | 2079.25 | 0.842 | Jan |
| 14 | 1957.08 | 1688.00 | 2087.67 | 0.809 | Feb |
| 15 | 1957.17 | 1920.00 | 2092.96 | 0.917 | Mar |
| 16 | 1957.25 | 1941.00 | 2098.67 | 0.925 | Apr |
| 17 | 1957.33 | 2311.00 | 2099.54 | 1.101 | May |
| 18 | 1957.42 | 2279.00 | 2100.88 | 1.085 | Jun |

**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them (averaging cancels the noise), then force the coefficients to average exactly 1:

| Position | n ratios | raw | normalised (decompose) | meaning |
|---|---|---|---|---|
| Jan | 39 | 0.7978 | 0.7986 | -20% vs trend |
| Feb | 39 | 0.8073 | 0.8081 | -19% vs trend |
| Mar | 38 | 0.8901 | 0.8909 | -11% vs trend |
| Apr | 38 | 0.9136 | 0.9144 | -9% vs trend |
| May | 38 | 1.0860 | 1.0870 | +9% vs trend |
| Jun | 38 | 1.1726 | 1.1737 | +17% vs trend |
| Jul | 39 | 1.2608 | 1.2620 | +26% vs trend |
| Aug | 39 | 1.2081 | 1.2092 | +21% vs trend |
| Sep | 39 | 1.0734 | 1.0744 | +7% vs trend |
| Oct | 39 | 1.0069 | 1.0078 | +1% vs trend |
| Nov | 39 | 0.9222 | 0.9231 | -8% vs trend |
| Dec | 39 | 0.8499 | 0.8507 | -15% vs trend |

The raw coefficients average 0.9990; they are rescaled to 1 so the season does not also move the overall level. Largest: **Jul**, smallest: **Jan**.

**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = y_t / S`; the residual is what trend × season (or trend + season) does not explain. Example at t = 7: y = 2468.00, T = 2043.17, S = 1.2620 ⇒ CVS = 1955.67, residual = 0.9572 (1 = perfect fit).

### Validation (step 7)

`mean=-0.0009582 sd=0.04248 | Ljung-Box p=0 (autocorrelated) | Shapiro p=1.784e-06 (not normal)`

Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.

### Forecast (step 8)

Split: `train = 456 obs. | test = 20 obs. (de 1994.00 à 1995.58)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| Holt-Winters | 2038.78 | 1539.10 | 3.1 |
| Décomposition (tendance + saison) | 2295.42 | 1904.10 | 3.8 |
| ARIMA(0,1,1)(0,1,1)[12] | 2514.86 | 1962.18 | 4.1 |
| Naïf | 7226.26 | 6196.05 | 12.1 |
| LES | 11842.70 | 9729.42 | 17.3 |
| LED (Holt) | 11930.04 | 9793.11 | 17.4 |

Best on the test set: **Holt-Winters** (RMSE 2038.78). The decomposition method ranks 2 of 6. LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. Holt-Winters adds it and updates it each period. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=1.000 | LED : alpha=1.000 beta=0.001; Holt-Winters : alpha=0.416 beta=0.008 gamma=0.110` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

An α (and/or β) of exactly 1.000 means the optimiser hit its boundary: the smoother just repeats the last observation/slope, which is a symptom of a model that does not fit the series (no seasonal term here).

Model chosen by `auto.arima`: `ARIMA(0,1,1)(0,1,1)[12]`.

### ⭐ Subject-specific question — results from the log

```
⭐ Les coefficients saisonniers sont-ils stables ? (amplitude par décennie)
  1956-1970 : max/min des coef. = 1.69
  1970-1980 : max/min des coef. = 1.51
  1980-1990 : max/min des coef. = 1.55
  1990-1995 : max/min des coef. = 1.51

Holt-Winters multiplicatif brut vs additif sur log(y)
  HW multiplicatif (brut)    RMSE=2038.780 MAE=1539.099 MAPE=3.06%
  HW additif sur log         RMSE=3380.096 MAE=2780.376 MAPE=5.50%

Tendance globale vs ajustée après la rupture (obs. >= 245)
  tendance globale         RMSE=2295.419 MAPE=3.76%
  tendance post-rupture    RMSE=3260.135 MAPE=5.12%
```

## 3. What to watch for in this subject

- The growth is faster than linear and the seasonal swing grows with it: multiplicative model, or work on log(y).
- The seasonal coefficients are not stable over 40 years (nearly flat in the 1950s–60s, large later): a single set of coefficients is a compromise.
- A level/trend break around 1970 (Pettitt): the global linear trend extrapolates badly.

**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.

## 4. Code and how to run

Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):

```r
res <- run_pipeline(y, ntest, OUT, name = "gas (Australie)")
hw_compare(y, ntest)
trend_break_compare(y, ntest, 12, res$model, brk)
```

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/06_Gaz_Australie"
Rscript solution.R      # sorties_R/
python3 solution.py     # sorties_python/
```
