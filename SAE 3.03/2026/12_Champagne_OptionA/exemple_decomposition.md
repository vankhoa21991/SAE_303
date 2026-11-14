# Champagne sales (Option A) — decomposition and forecasting explained

> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; here we apply the same method to **this** series.

## 0. The method in 6 lines

1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.
2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.
3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).
4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).
5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.
6. Always compare with a naïve forecast.

## 1. The data and its context

Monthly champagne sales (Perrin Frères), January 1964 → September 1972 (105 observations; the dataset sheet says ~108, document the difference). Sales peak every year-end (holidays).

## 2. Run: monthly 1964–1972

**Series**: Ventes de champagne — n = 105, frequency = 12 per cycle, from 1964/1 to 1972.67.

Summary: `Min. 1413 | 1st Qu. 3113 | Median 4217 | Mean 4761.15 | 3rd Qu. 5221 | Max. 13916 | sd=2553.5 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.0100 | stationary — H0 'unit root' rejected |
| Mann-Kendall (trend) | 9.785e-05 | significant monotone trend |
| Pettitt (level break) | 0.000765 | level break around 1966.75 |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### Additive or multiplicative? (step 6a — Buys-Ballot)

For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. If `a` is significantly positive the swings grow with the level ⇒ multiplicative.

| Cycle | Mean | Std |
|---|---|---|
| 1 | 3478.17 | 1555.29 |
| 2 | 3864.17 | 1900.88 |
| 3 | 4337.67 | 2119.89 |
| … | … | … |
| 7 | 5006.58 | 3324.22 |
| 8 | 5640.58 | 2995.57 |

Slope **a = 0.7257**, p = 0.002605, 8 cycles ⇒ Buys-Ballot suggests **MULTIPLICATIVE**. The spread grows with the level: seasonal effects are percentages of the trend. (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)

### Decomposition step by step (step 6b)

**Step A — centred moving average.** The period is p = 12 (even), so a window of 12 values has no centre. Use 13 values with half weight on the two ends:

```
T_t = (0.5·y_(t-6) + y_(t-5) + … + y_(t+5) + 0.5·y_(t+6)) / 12
```

By hand at t = 7: `T_7 = (0.5·2815 + 2672 + 2755 + 2721 + 2946 + 3036 + 2282 + 2212 + 2922 + 4301 + 5764 + 7312 + 0.5·2541) / 12 = 3466.750` — R gives **3466.750** ✓

The first 6 and last 6 trend values do not exist (the window would run outside the data).

**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:

| t | time | y_t | T_t | y/T | position |
|---|---|---|---|---|---|
| 7 | 1964.5 | 2282.00 | 3466.75 | 0.658 | Jul |
| 8 | 1964.58 | 2212.00 | 3447.12 | 0.642 | Aug |
| 9 | 1964.67 | 2922.00 | 3450.42 | 0.847 | Sep |
| 10 | 1964.75 | 4301.00 | 3484.62 | 1.234 | Oct |
| 11 | 1964.83 | 5764.00 | 3541.92 | 1.627 | Nov |
| 12 | 1964.92 | 7312.00 | 3584.58 | 2.040 | Dec |
| 13 | 1965 | 2541.00 | 3623.75 | 0.701 | Jan |
| 14 | 1965.08 | 2475.00 | 3635.96 | 0.681 | Feb |
| 15 | 1965.17 | 3031.00 | 3645.12 | 0.832 | Mar |
| 16 | 1965.25 | 3266.00 | 3680.38 | 0.887 | Apr |
| 17 | 1965.33 | 3776.00 | 3732.33 | 1.012 | May |
| 18 | 1965.42 | 3230.00 | 3820.62 | 0.845 | Jun |

**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them (averaging cancels the noise), then force the coefficients to average exactly 1:

| Position | n ratios | raw | normalised (decompose) | meaning |
|---|---|---|---|---|
| Jan | 8 | 0.7547 | 0.7546 | -25% vs trend |
| Feb | 8 | 0.6743 | 0.6742 | -33% vs trend |
| Mar | 8 | 0.8078 | 0.8077 | -19% vs trend |
| Apr | 7 | 0.8300 | 0.8300 | -17% vs trend |
| May | 7 | 0.8744 | 0.8743 | -13% vs trend |
| Jun | 7 | 0.8663 | 0.8662 | -13% vs trend |
| Jul | 8 | 0.7406 | 0.7405 | -26% vs trend |
| Aug | 8 | 0.3810 | 0.3810 | -62% vs trend |
| Sep | 8 | 0.9273 | 0.9272 | -7% vs trend |
| Oct | 8 | 1.1957 | 1.1956 | +20% vs trend |
| Nov | 8 | 1.7547 | 1.7546 | +75% vs trend |
| Dec | 8 | 2.1944 | 2.1942 | +119% vs trend |

The raw coefficients average 1.0001; they are rescaled to 1 so the season does not also move the overall level. Largest: **Dec**, smallest: **Aug**.

**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = y_t / S`; the residual is what trend × season (or trend + season) does not explain. Example at t = 7: y = 2282.00, T = 3466.75, S = 0.7405 ⇒ CVS = 3081.62, residual = 0.8889 (1 = perfect fit).

### Validation (step 7)

`mean=0.0001019 sd=0.1375 | Ljung-Box p=0.4158 (plausibly white noise) | Shapiro p=1.054e-07 (not normal)`

Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.

### Forecast (step 8)

Split: `train = 84 obs. | test = 21 obs. (de 1971.00 à 1972.67)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| Décomposition (tendance + saison) | 464.76 | 361.32 | 11.6 |
| Holt-Winters | 527.05 | 409.14 | 10.0 |
| Naïf | 996.53 | 823.14 | 18.3 |
| ARIMA(0,1,1)(1,1,0)[12] | 1082.08 | 940.80 | 20.0 |
| LED (Holt) | 6921.52 | 6556.96 | 184.0 |
| LES | 8156.78 | 7796.77 | 217.8 |

Best on the test set: **Décomposition (tendance + saison)** (RMSE 464.76). The decomposition method ranks 1 of 6. LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. Holt-Winters adds it and updates it each period. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=0.939 | LED : alpha=0.956 beta=0.001; Holt-Winters : alpha=0.295 beta=0.000 gamma=0.712` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

Model chosen by `auto.arima`: `ARIMA(0,1,1)(1,1,0)[12]`.

### ⭐ Subject-specific question — results from the log

```
Additif vs multiplicatif — critère chiffré
  additive        RMSE=758.469  MAPE=12.57%  autocorr(1) résidus=0.26
  multiplicative  RMSE=563.699  MAPE=8.94%  autocorr(1) résidus=0.14

Holt-Winters multiplicatif brut vs additif sur log(y)
  HW multiplicatif (brut)    RMSE=527.054 MAE=409.137 MAPE=10.05%
  HW additif sur log         RMSE=728.579 MAE=559.593 MAPE=12.70%
-> La méthode de choix (Buys-Ballot) avait retenu : multiplicative : confirmée ou non par le test ci-dessus ?
```

## 3. What to watch for in this subject

- Additive or multiplicative is a real debate here: the amplitude grows slowly. Check whether the three methods of the course agree.
- The ⭐ block compares both decompositions numerically and shows which Holt-Winters variant wins on the test set.
- Short series (8 full cycles): keep the test set to ~21 months.

**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.

## 4. Code and how to run

Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):

```r
res <- run_pipeline(y, 21, OUT, name = "Ventes de champagne")
compare_add_mult(y)
hw_compare(y, 21)
```

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/12_Champagne_OptionA"
Rscript solution.R      # sorties_R/
python3 solution.py     # sorties_python/
```
