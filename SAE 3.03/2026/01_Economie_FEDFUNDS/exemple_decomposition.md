# FEDFUNDS — US federal funds rate — decomposition and forecasting explained

> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; here we apply the same method to **this** series.

## 0. The method in 6 lines

1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.
2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.
3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).
4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).
5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.
6. Always compare with a naïve forecast.

## 1. The data and its context

Effective federal funds rate (the overnight interest rate between US banks), monthly from July 1954, cut at December 2022 for the exercise. Monetary policy makes it move by **regimes** (rise to 1981, long fall, near zero after 2008 and 2020, sharp hikes in 2022), not by calendar season.

## 2. Run: FEDFUNDS monthly 1954–2022

**Series**: FEDFUNDS — n = 822, frequency = 12 per cycle, from 1954/7 to 2022.92.

Summary: `Min. 0.05 | 1st Qu. 1.75 | Median 4.11 | Mean 4.6 | 3rd Qu. 6.28 | Max. 19.1 | sd=3.62 | NA=0`

### Tests (step 5)

| Test | p-value | Reading (p < 0.05 ⇒ H0 rejected) |
|---|---|---|
| ADF (stationarity) | 0.0920 | **not** stationary — H0 'unit root' kept |
| Mann-Kendall (trend) | 2.247e-26 | significant monotone trend |
| Pettitt (level break) | 7.5e-75 | level break around 2001.42 |

ADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. A p-value below 0.05 rejects H0.

### No seasonal decomposition

This run has **no seasonal component** (annual data, or seasonality deliberately switched off). The pipeline therefore fits a straight line to the series: slope = **-0.0643** per time unit. Without seasonal coefficients there is nothing to 'adjust': the structure is trend (or level shifts) + residual.

Residuals of the line: `slope=-0.0643 ; residual sd=3.387 ; Ljung-Box p=0 ; Shapiro p=1.869e-19`

Mann-Kendall **and** Pettitt are both significant: on annual data this usually means a **level shift** (a step) rather than a steady slope — the straight line is only a rough summary. Look at the plot and the date given by Pettitt.

Interpretation: *Ljung-Box* tests whether residuals are autocorrelated (p < 0.05 ⇒ yes, structure left); *Shapiro* tests normality.

### Forecast (step 8)

Split: `train = 774 obs. | test = 48 obs. (de 2019.00 à 2022.92)`. Never evaluate a forecast on the data used to fit the model.

| Method | RMSE | MAE | MAPE % |
|---|---|---|---|
| ARIMA(2,1,1) | 1.65 | 1.41 | 1386.7 |
| LES | 1.67 | 1.42 | 1403.3 |
| Naïf | 1.67 | 1.42 | 1403.3 |
| Tendance seule (lm) | 2.17 | 1.95 | 1817.2 |
| LED (Holt) | 2.81 | 2.43 | 2279.8 |

Best on the test set: **ARIMA(2,1,1)** (RMSE 1.65). The trend-only method ranks 4 of 5. There is no seasonality here, so LES (level only), LED (level + slope) and the trend line are the natural candidates; Holt-Winters is not used. `auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.

Estimated smoothing constants: `LES : alpha=1.000 | LED : alpha=1.000 beta=0.041` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).

An α (and/or β) of exactly 1.000 means the optimiser hit its boundary: the smoother just repeats the last observation/slope, which is a symptom of a model that does not fit the series (no seasonal term here).

Model chosen by `auto.arima`: `ARIMA(2,1,1)`.

### ⭐ Subject-specific question — results from the log

```
⭐ Segmentation récursive par Pettitt (ruptures successives)
rupture vers 2001.42 (p=7.5e-75)
  rupture vers 1968.25 (p=3.46e-52)
    rupture vers 1991.08 (p=1.54e-27)
      rupture vers 1978.67 (p=6.83e-19)
        rupture vers 1984.92 (p=6.93e-22)
  rupture vers 2008.83 (p=1.41e-23)
    rupture vers 2015.92 (p=4.04e-08)
```

## 3. What to watch for in this subject

- No seasonality: the pipeline fits a trend line and looks at the residuals — and a single straight line is a poor description of several regimes.
- The test period (2019–2022) contains the Covid cut to ~0 and the 2022 hikes: every method is wrong there. That is the lesson, not a bug.
- MAPE is huge when the rate is close to 0 (division by a tiny observed value): read RMSE/MAE instead and say why.

**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.

## 4. Code and how to run

Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):

```r
res <- run_pipeline(yy, 48, OUT, name = "FEDFUNDS", seasonal = FALSE, trend = "linear")
segment_pettitt(as.numeric(yy), as.numeric(time(yy)))
```

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/01_Economie_FEDFUNDS"
Rscript solution.R      # sorties_R/
python3 solution.py     # sorties_python/
```
