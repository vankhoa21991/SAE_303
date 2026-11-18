# Anti-diabetic drug spending in Australia (a10) — decomposition and forecasting explained

> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; here we apply the same method to **this** series.

## 0. The method in 6 lines

1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.
2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.
3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).
4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).
5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.
6. Always compare with a naïve forecast.

## 1. The data and its context

Monthly government spending (millions of Australian dollars) on anti-diabetic drugs (ATC code A10) under the Pharmaceutical Benefit Scheme, July 1991 → June 2008 (204 observations, `fpp2::a10`, source Medicare Australia). Spending grows strongly (more diabetes, new treatments, reimbursement rules) and follows a very marked yearly cycle: in our run January is the peak (about +33% vs trend), February the sharpest drop (about −22%), December also high (+23%).

## 2. Run: monthly Jul 1991 – Jun 2008

**Series**: a10 anti-diabète (M$) — n = 204, frequency = 12 per cycle, from 1991/7 to 2008.42.

Summary: `Min. 2.81 | 1st Qu. 5.84 | Median 9.32 | Mean 10.69 | 3rd Qu. 14.29 | Max. 29.67 | sd=5.96 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.0100 | stationary — H0 'unit root' rejected |
| Mann-Kendall (trend) | 2.212e-72 | significant monotone trend |
| Pettitt (level break) | 2.36e-32 | level break around 1999.83 |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### Additive or multiplicative? (step 6a — Buys-Ballot)

For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. If `a` is significantly positive the swings grow with the level ⇒ multiplicative.

| Cycle | Mean | Std |
|---|---|---|
| 1 | 3.49 | 0.63 |
| 2 | 4.19 | 0.88 |
| 3 | 4.89 | 1.02 |
| … | … | … |
| 16 | 20.27 | 3.53 |
| 17 | 23.17 | 2.96 |

Slope **a = 0.1414**, p = 5.653e-10, 17 cycles ⇒ Buys-Ballot suggests **MULTIPLICATIVE**. The spread grows with the level: seasonal effects are percentages of the trend. (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)

### Decomposition step by step (step 6b)

**Step A — centred moving average.** The period is p = 12 (even), so a window of 12 values has no centre. Use 13 values with half weight on the two ends:

```
T_t = (0.5·y_(t-6) + y_(t-5) + … + y_(t+5) + 0.5·y_(t+6)) / 12
```

By hand at t = 7: `T_7 = (0.5·3.52659 + 3.18089 + 3.25222 + 3.611 + 3.56587 + 4.30637 + 5.08833 + 2.81452 + 2.98581 + 3.20478 + 3.12758 + 3.27052 + 0.5·3.73785) / 12 = 3.503` — R gives **3.503** ✓

The first 6 and last 6 trend values do not exist (the window would run outside the data).

**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:

| t | time | y_t | T_t | y/T | position |
|---|---|---|---|---|---|
| 7 | 1992 | 5.09 | 3.50 | 1.452 | Jan |
| 8 | 1992.08 | 2.81 | 3.53 | 0.798 | Feb |
| 9 | 1992.17 | 2.99 | 3.57 | 0.837 | Mar |
| 10 | 1992.25 | 3.20 | 3.60 | 0.890 | Apr |
| 11 | 1992.33 | 3.13 | 3.65 | 0.857 | May |
| 12 | 1992.42 | 3.27 | 3.74 | 0.873 | Jun |
| 13 | 1992.5 | 3.74 | 3.85 | 0.970 | Jul |
| 14 | 1992.58 | 3.56 | 3.93 | 0.907 | Aug |
| 15 | 1992.67 | 3.78 | 3.99 | 0.948 | Sep |
| 16 | 1992.75 | 3.92 | 4.04 | 0.971 | Oct |
| 17 | 1992.83 | 4.39 | 4.09 | 1.071 | Nov |
| 18 | 1992.92 | 5.81 | 4.16 | 1.397 | Dec |

**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them (averaging cancels the noise), then force the coefficients to average exactly 1:

| Position | n ratios | raw | normalised (decompose) | meaning |
|---|---|---|---|---|
| Jan | 16 | 1.3298 | 1.3305 | +33% vs trend |
| Feb | 16 | 0.7791 | 0.7796 | -22% vs trend |
| Mar | 16 | 0.8759 | 0.8764 | -12% vs trend |
| Apr | 16 | 0.8573 | 0.8578 | -14% vs trend |
| May | 16 | 0.9325 | 0.9330 | -7% vs trend |
| Jun | 16 | 0.9161 | 0.9166 | -8% vs trend |
| Jul | 16 | 0.9780 | 0.9785 | -2% vs trend |
| Aug | 16 | 0.9892 | 0.9897 | -1% vs trend |
| Sep | 16 | 0.9859 | 0.9864 | -1% vs trend |
| Oct | 16 | 1.0449 | 1.0455 | +5% vs trend |
| Nov | 16 | 1.0750 | 1.0756 | +8% vs trend |
| Dec | 16 | 1.2297 | 1.2304 | +23% vs trend |

The raw coefficients average 0.9994; they are rescaled to 1 so the season does not also move the overall level. Largest: **Jan**, smallest: **Feb**.

**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = y_t / S`; the residual is what trend × season (or trend + season) does not explain. Example at t = 7: y = 5.09, T = 3.50, S = 1.3305 ⇒ CVS = 3.82, residual = 1.0916 (1 = perfect fit).

### Validation (step 7)

`mean=-0.0005546 sd=0.04848 | Ljung-Box p=0.01125 (autocorrelated) | Shapiro p=0.05621 (normal)`

Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.

### Forecast (step 8)

Split: `train = 180 obs. | test = 24 obs. (de 2006.50 à 2008.42)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| ARIMA(0,1,1)(2,1,1)[12] | 2.54 | 2.17 | 9.8 |
| Holt-Winters | 3.04 | 2.63 | 11.8 |
| Décomposition (tendance + saison) | 4.70 | 4.27 | 19.1 |
| Naïf | 4.94 | 4.50 | 20.2 |
| LED (Holt) | 5.02 | 4.06 | 17.1 |
| LES | 6.14 | 5.11 | 21.6 |

Best on the test set: **ARIMA(0,1,1)(2,1,1)[12]** (RMSE 2.54). The decomposition method ranks 3 of 6. LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. Holt-Winters adds it and updates it each period. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=0.255 | LED : alpha=0.199 beta=0.076; Holt-Winters : alpha=0.154 beta=0.049 gamma=0.454` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

Model chosen by `auto.arima`: `ARIMA(0,1,1)(2,1,1)[12]`.

### ⭐ Subject-specific question — results from the log

```
Additif vs multiplicatif — critère chiffré
  additive        RMSE=0.905  MAPE=7.35%  autocorr(1) résidus=0.03
  multiplicative  RMSE=0.608  MAPE=3.83%  autocorr(1) résidus=-0.22

Holt-Winters multiplicatif brut vs additif sur log(y)
  HW multiplicatif (brut)    RMSE=3.040 MAE=2.630 MAPE=11.82%
  HW additif sur log         RMSE=2.729 MAE=2.319 MAPE=10.48%

⭐ Rupture de tendance ?
Pettitt (série brute) : voir ÉTAPE 5 — la croissance accélère-t-elle ? comparer tendance globale et tendance post-rupture :

Tendance globale vs ajustée après la rupture (obs. >= 101)
  tendance globale         RMSE=4.704 MAPE=19.07%
  tendance post-rupture    RMSE=3.367 MAPE=13.00%
-> La méthode de choix (Buys-Ballot) avait retenu : multiplicative
```

## 3. What to watch for in this subject

- Strong trend **and** strong seasonality whose amplitude grows with the level: the multiplicative model (or log(y)) is the natural choice — the ⭐ block backs this with a numerical criterion.
- The first observation is **July**, not January: position 1 of the cycle is January in the tables (calendar position), not the first value of the series. Mixing the two shifts every coefficient by 6 months.
- Growth accelerates (Pettitt finds a break around 1999–2000): a single straight line over the whole period under-forecasts the last two years; the ⭐ block compares it with a trend fitted after the break.

**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.

## 4. Code and how to run

Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):

```r
res <- run_pipeline(y, 24, OUT, name = "a10 anti-diabète (M$)")   # test = 24 derniers mois (juil. 2006 - juin 2008)
compare_add_mult(y)                                   # ⭐ additif vs multiplicatif tranché par un critère chiffré
hw_compare(y, 24)                                     # ⭐ Holt-Winters multiplicatif brut vs additif sur log(y)
trend_break_compare(y, 24, 12, res$model, max(2, as.integer(res$info$pettitt$idx) + 1))
```

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/01_Economie_a10_antidiabete"
Rscript solution.R      # sorties_R/
python3 solution.py     # sorties_python/
```
