# Nile annual flow at Aswan (Nile) — decomposition and forecasting explained

> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; here we apply the same method to **this** series.

## 0. The method in 6 lines

1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.
2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.
3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).
4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).
5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.
6. Always compare with a naïve forecast.

## 1. The data and its context

Annual flow of the Nile at Aswan, 1871–1970, in 10⁸ m³. A well-known level shift appears around 1898–1899 (change of regime linked to dams and climate).

## 2. Run: annual 1871–1970

**Series**: Nile — n = 100, frequency = 1 per cycle, from 1871/1 to 1970.00.

Summary: `Min. 456 | 1st Qu. 798.5 | Median 893.5 | Mean 919.35 | 3rd Qu. 1032.5 | Max. 1370 | sd=169.23 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.0642 | **not** stationary — H0 'unit root' kept |
| Mann-Kendall (trend) | 3.658e-05 | significant monotone trend |
| Pettitt (level break) | 3.59e-07 | level break around 1899.00 |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### No seasonal decomposition

This run has **no seasonal component** (annual data, or seasonality deliberately switched off). The pipeline therefore fits a straight line to the series: slope = **-2.7143** per time unit. Without seasonal coefficients there is nothing to 'adjust': the structure is trend (or level shifts) + residual.

Residuals of the line: `slope=-2.7143 ; residual sd=149.790 ; Ljung-Box p=0.0005 ; Shapiro p=0.4921`

Mann-Kendall **and** Pettitt are both significant: on annual data this usually means a **level shift** (a step) rather than a steady slope — the straight line is only a rough summary. Look at the plot and the date given by Pettitt.

Interpretation: *Ljung-Box* tests whether residuals are autocorrelated (p < 0.05 ⇒ yes, structure left); *Shapiro* tests normality.

### Forecast (step 8)

Split: `train = 80 obs. | test = 20 obs. (de 1951.00 à 1970.00)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| LES | 123.02 | 104.50 | 11.9 |
| Naïf | 123.06 | 101.95 | 12.0 |
| ARIMA(1,1,1) | 125.05 | 106.16 | 12.0 |
| LED (Holt) | 126.23 | 101.62 | 12.1 |
| Tendance seule (lm) | 133.31 | 108.01 | 13.2 |

Best on the test set: **LES** (RMSE 123.02). The trend-only method ranks 5 of 5. There is no seasonality here, so LES (level only), LED (level + slope) and the trend line are the natural candidates; Holt-Winters is not used. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=0.246 | LED : alpha=0.437 beta=0.060` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

Model chosen by `auto.arima`: `ARIMA(1,1,1)`.

### ⭐ Subject-specific question — results from the log

```
⭐ Pettitt (train) + ADF avant/après
rupture vers 1899 (p=1.5e-07)
  ADF avant : p=0.710   moyenne=1097.8
  ADF après : p=0.010   moyenne=839.6
  LES sur toute la série d'entraînement    alpha=0.246 RMSE=123.02 MAE=104.50
  LES sur la période post-rupture seule     alpha=0.056 RMSE=127.67 MAE=106.88
```

## 3. What to watch for in this subject

- Annual data: no seasonality, so no coefficients — the structure is a **level shift**, not a straight-line trend. Pettitt is the right test.
- Fitting one LES on the whole series mixes two regimes; compare with a LES on the post-break part only (⭐ block).
- Every method has a similar RMSE: on such a series, 'beating' the naïve forecast is hard — say so honestly.

**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.

## 4. Code and how to run

Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):

```r
res <- run_pipeline(y, 20, OUT, name = "Nile", seasonal = FALSE, trend = "mean")
```

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/10_Debit_du_Nil"
Rscript solution.R      # sorties_R/
python3 solution.py     # sorties_python/
```
