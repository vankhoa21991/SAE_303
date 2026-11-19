# UKgas — multiplicative decomposition, explained step by step (steps 6–8)

> One fully worked example from subject 05 (Consommation de gaz UK): the theory, every number
> computed from the real data, and the code. Companion to `ENONCE.md`, `solution.R`, `solution.py`.
> Every figure below comes from R (`UKgas`, built into R). Run `Rscript solution.R` from this folder to reproduce them.

**Reading guide.** Part A explains *why* we decompose. Part B explains *what* the model is and how to choose
it. Part C walks through the algorithm with real numbers. Part D uses the result to forecast. Part E is the code.
Part F lists the mistakes students usually make.

---

## A. The idea in plain words

### A.1 What the series looks like

`UKgas` = UK gas consumption, **quarterly**, 1960 Q1 → 1986 Q4, **n = 108** observations, in millions of
thermies (a unit of heat). Q1 = Jan–Mar (winter), Q3 = Jul–Sep (summer).

The first 12 values:

| Year | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| 1960 | 160.1 | 129.7 | 84.8 | 120.1 |
| 1961 | 160.1 | 124.9 | 84.8 | 116.9 |
| 1962 | 169.7 | 140.9 | 89.7 | 123.3 |

Two things are visible by eye, and they are the whole point of this subject:

1. **A trend**: consumption goes from ~120 per quarter in 1960 to ~725 in 1986.
2. **A seasonal pattern** that repeats every year: high in winter (Q1), low in summer (Q3) —
   people heat their homes in winter. And the winter–summer gap **gets bigger as the level rises**:
   in 1960 the swing is about 75 (160 vs 85), in 1986 it is about 816 (1164 vs 347).

### A.2 Why decompose?

A raw plot mixes everything: "is consumption going up because of a real trend, or just because it's winter?"
Decomposition **separates the causes** so we can:

- **describe** each one (how fast is the trend rising? how much does winter add?);
- **remove** the season to get the *seasonally adjusted* series (CVS, "corrigée des variations saisonnières"):
  the series you would see "if every quarter were an average quarter" — this is what newspapers quote
  when they say "unemployment fell, seasonally adjusted";
- **forecast**: extrapolate the trend, then put the season back.

### A.3 The components

| Component | Symbol | Meaning | UKgas |
|---|---|---|---|
| Trend | T_t | slow, long-term level | rising: more households use gas |
| Seasonal | S_t | pattern that repeats every p observations (here p = 4) | winter peak, summer trough |
| Residual | R_t | what is left: noise, one-off events | e.g. cold winters, 1973 oil shock |

(Courses sometimes split the residual into a *cycle* C_t and an *irregular* I_t. On 27 years of data we
cannot separate them, so everything left over is called the residual.)

---

## B. The model, and how to choose it

### B.1 Additive vs multiplicative

```
Additive:        Y_t = T_t + S_t + R_t        seasonal swing = a fixed number of units
Multiplicative:  Y_t = T_t × S_t × R_t        seasonal swing = a fixed percentage of the trend
```

Concretely for UKgas, if we (wrongly) forced the additive model, R gives these coefficients:

```
additive       : +175.1   −36.1   −169.0   +30.0      "Q1 is always 175 above the trend"
multiplicative :  1.454    0.956    0.558    1.032     "Q1 is always 45% above the trend"
```

"Always +175" is fine when the trend is 700 (1986) but absurd in 1960, when the whole quarter is only ~125
and Q3 would be negative (125 − 169 < 0 — gas consumption can't be negative!). "Always +45%" works at every level.
That is the intuition: **if the seasonal swings grow with the level, use the multiplicative model.**

### B.2 Three ways to choose (the course asks for at least two)

**(1) Look at the band (visual).** Draw the yearly max and min on the plot. If the two lines run parallel →
additive; if they fan out → multiplicative. For UKgas: 1960 spans 84.8–160.1 (range ≈ 75); 1986 spans
347.4–1163.9 (range ≈ 816). A clear fan. (Figure `02_choix_modele.png`.)

**(2) Buys-Ballot (a statistical test).** For each year *i* compute the mean `m_i` and the standard deviation
`s_i` of its 4 quarters, then regress `s_i = a·m_i + b`.

| Year | mean m_i | std s_i |
|---|---|---|
| 1960 | 123.67 | 31.02 |
| 1961 | 121.67 | 30.93 |
| 1962 | 130.90 | 33.47 |
| … | … | … |
| 1972 | 258.95 | 84.78 |
| 1973 | 281.35 | 100.64 |
| … | … | … |
| 1985 | 672.78 | 344.82 |
| 1986 | 726.80 | 342.08 |

How to read the result:

- slope `a` ≈ 0 → spread does not depend on the level → **additive**;
- slope `a` > 0 and significant → spread grows with the level → **multiplicative**.

On UKgas: **a = 0.580, p ≈ 0** (27 yearly points). The p-value tests "H0: a = 0"; p < 0.05 rejects it.

*A caution for the report:* the ratio s/m goes from 0.25 (1960) to 0.47 (1986), so the spread grows
**even faster than the level**. The multiplicative model is the better of the two, but it is not perfect — we
will see the symptom in the residuals (C.7).

**(3) A numerical criterion.** Decompose both ways, and compare the reconstruction error
(`compare_add_mult()` in `common.R`). Useful when (1) and (2) disagree.

**Hard rule:** the multiplicative model needs **all values > 0** (you cannot take a percentage of zero or a negative).

---

## C. The algorithm, with the real numbers

### C.1 Step A — extract the trend with a centred moving average (CMA)

*Idea:* to remove a pattern that repeats every 4 quarters, average over **exactly one full cycle**. Each quarter
then appears once in the window, so the seasonal ups and downs cancel, and what remains is the trend.

*Problem:* 4 is even, so a window of 4 consecutive values has no middle observation. The fix: use 5 values and
give the two edge values half weight:

```
T_t = ( 0.5·y_{t-2} + y_{t-1} + y_t + y_{t+1} + 0.5·y_{t+2} ) / 4
```

(Weights 0.5 + 1 + 1 + 1 + 0.5 = 4, so it is a true average.) For an **odd** period p the window is simply
p values with weight 1/p each, centred on t.

**By hand at t = 3** (window y₁…y₅ = 160.1, 129.7, 84.8, 120.1, 160.1):

```
T_3 = (0.5·160.1 + 129.7 + 84.8 + 120.1 + 0.5·160.1) / 4
    = (80.05 + 129.7 + 84.8 + 120.1 + 80.05) / 4
    = 494.7 / 4
    = 123.675          ← decompose() and ma() also give 123.675 ✓
```

The first 2 and last 2 trend values do not exist (the window would run past the data): 4 missing values in
total, i.e. p/2 at each end. That is why the trend plot starts a little after the series.

### C.2 Step B — divide by the trend, then average per quarter

For each t where the trend exists, compute `y_t / T_t`. What remains is *season × noise*:

| t | year-quarter | y_t | T_t (CMA) | y_t / T_t |
|---|---|---|---|---|
| 3 | 1960 Q3 | 84.8 | 123.675 | 0.686 |
| 4 | 1960 Q4 | 120.1 | 123.075 | 0.976 |
| 5 | 1961 Q1 | 160.1 | 122.475 | 1.307 |
| 6 | 1961 Q2 | 124.9 | 122.075 | 1.023 |
| 7 | 1961 Q3 | 84.8 | 122.875 | 0.690 |
| 8 | 1961 Q4 | 116.9 | 126.075 | 0.927 |
| 9 | 1962 Q1 | 169.7 | 128.688 | 1.319 |
| 10 | 1962 Q2 | 140.9 | 130.100 | 1.083 |

Look at the pattern: the Q1 ratios are all near 1.3, the Q3 ratios near 0.69. The seasonal pattern is stable —
that is what we want to estimate. Gather **all** ratios of one quarter (there are 26 of each) and average them:

```
Q1 ratios: 1.307, 1.319, 1.372, 1.317, 1.329, 1.347, ...   (26 values, range 1.275–1.671)
S_1 (raw) = mean of the 26 Q1 ratios = 1.4538
```

*Why average?* Each single ratio contains noise (a cold winter, a warm one). Averaging 26 of them cancels most
of it. That's why we need **at least 3 full cycles** in a project, and why more is better.

Raw results: **1.4538, 0.9560, 0.5585, 1.0320**.

### C.3 Step C — normalise so the coefficients average exactly 1

Their mean is 1.0001, not exactly 1. The coefficients are *multipliers on the trend*; if they did not average 1
they would also change the overall level and mix up trend and season. So we divide each by their mean:

```
S = (1.4538, 0.9560, 0.5585, 1.0320) / 1.0001 = (1.4537, 0.9559, 0.5584, 1.0319)   → mean = 1.0000 ✓
```

(Additive model: the equivalent constraint is that the coefficients **sum to 0**, achieved by subtracting
their mean.) R's `decompose()` prints exactly these values in `$figure`.

### C.4 How to read the coefficients

| Quarter | Coefficient | Meaning |
|---|---|---|
| Q1 (winter) | **1.454** | consumption ≈ **45% above** the trend |
| Q2 | 0.956 | ≈ 4% below trend |
| Q3 (summer) | **0.558** | ≈ **44% below** the trend — the trough |
| Q4 | 1.032 | ≈ 3% above trend |

### C.5 Step D — the seasonally adjusted series (CVS)

Divide each value by its quarter's coefficient: `CVS_t = y_t / S_q`.

```
1960 Q1:  160.1 / 1.4537 = 110.13        1960 Q3:   84.8 / 0.5584 = 151.85
1960 Q2:  129.7 / 0.9559 = 135.68        1960 Q4:  120.1 / 1.0319 = 116.39
```

(Why isn't the CVS flat? Because the trend moves, and the CVS keeps the trend + the residual. It is *not*
supposed to be constant — only free of the regular seasonal pattern.)

### C.6 The residual

What the model cannot explain: `R_t = y_t / (T_t × S_q)`. At t = 3: 84.8 / (123.675 × 0.5584) = **1.228**,
i.e. 1960 Q3 was 23% above what the model expects.

### C.7 Why is that residual so large? (the honest limit)

Because in 1960 the summer dip was *shallower* than the 26-year average: the 1960 Q3 ratio was 0.686, but the
average coefficient is 0.558. In other words, **the seasonal pattern itself changes over time** (the
winter/summer contrast grew as more homes used gas for heating). The classical decomposition assumes ONE fixed
pattern for 27 years. This shows up in the validation step (step 7):

- the residual standard deviation is 0.168 (≈ 17% of the model value);
- Ljung-Box p ≈ 0 → the residuals are **autocorrelated** (some structure is left);
- Shapiro p ≈ 0.004 → not perfectly normal.

*What to write in the report:* the decomposition captures the main structure, but the residuals show
a **drifting seasonality**; a model with evolving coefficients (Holt-Winters, SARIMA) is better suited.

---

## D. From decomposition to a forecast

**Rule number one:** never test a forecast on the data used to fit it. We keep the last 8 quarters (1985–86) as a
**test set** and fit on the first 100 (1960–1984).

### D.1 The method (parametric)

1. Decompose the **training** series (the coefficients are re-estimated on it: Q1 ≈ 1.438, Q2 ≈ 0.967, Q3 ≈ 0.572, Q4 ≈ 1.023, recovered as forecast ÷ trend).
2. Fit a straight line to the CVS series: `T_t = 36.21 + 5.296·t` (t = 1…100).
   Consumption rises ≈ 5.3 million thermies per quarter.
3. Extrapolate the line: t = 101…104 → trend 571.1, 576.4, 581.7, 587.0.
4. Put the season back: multiply by the coefficients.

| 1985 | Q1 | Q2 | Q3 | Q4 |
|---|---|---|---|---|
| Forecast | 821.1 | 557.3 | 332.7 | 600.7 |
| Observed | 1087.0 | 534.7 | 281.8 | 787.6 |

The shape is right (high Q1, low Q3), but the winter quarters are **under-forecast** by about 25%, and
the **RMSE is 170.7**.

### D.2 Why it does badly, and what beats it

- The straight line fitted on 25 years under-estimates the recent, steeper growth. A change of trend appears around
  1972 (Pettitt test: p ≈ 2·10⁻¹⁴). Fitting the line only after the break reduces the RMSE to **134.5**.
- The seasonal amplitude kept growing (C.7), but the coefficients are frozen.

Comparison on the same test set (RMSE; lower is better):

| Method | RMSE |
|---|---|
| auto.arima (seasonal, with drift) | 45.9 |
| Holt-Winters multiplicative | 76.5 |
| Naive seasonal (same quarter last year) | 101.9 |
| **Decomposition + linear trend** | **170.7** |
| LED (Holt, no season) | 321.4 |
| LES (simple, no season) | 327.2 |

LES and LED have **no seasonal term**, so on a series with a ×2.6 winter/summer ratio they are hopeless:
a useful reminder that the method must match the structure. Holt-Winters is the **seasonal** exponential smoothing: its
coefficients are updated each quarter, so it follows the drifting season that decomposition freezes.

---

## E. The code

### E.1 The subject file `solution.R`

```r
y <- UKgas
res <- run_pipeline(y, 8, OUT, name = "UKgas")   # 8 obs. held out for test (1985–86)
brk <- res$info$pettitt$idx + 1                  # ⭐ first observation after the break
trend_break_compare(y, 8, 4, res$model, brk)     # global trend vs post-break trend
hw_compare(y, 8)                                 # HW multiplicative vs additive on log(y)
save_log()
```

### E.2 The functions behind it (`_common/common.R`) — same functions as the TPs

```r
# Step 6a — Buys-Ballot (as in TP04)
cyc <- (seq_along(y) - 1) %/% period                 # cycle number of each observation
moy <- tapply(y, cyc, mean);  et <- tapply(y, cyc, sd)
fit <- summary(lm(et ~ moy))                         # sd = a*mean + b
fit$coefficients[2, 1]                               # slope a
fit$coefficients[2, 4]                               # its p-value

# Step 6b — decomposition
dec <- decompose(y, type = "multiplicative")         # does steps A + B + C
dec$figure                                           # the 4 seasonal coefficients
dec$trend                                            # the centred moving average
dec$random                                           # the residuals
cvs <- y / dec$seasonal                              # step D
mm  <- ma(y, order = 4, centre = TRUE)               # trend "by hand" to compare with dec$trend

# Step 8 — the 3 forecasts (TP03/TP04)
train <- window(y, end = c(1984, 4)); test <- window(y, start = c(1985, 1))
les <- HoltWinters(train, beta = FALSE, gamma = FALSE)   # simple smoothing
led <- HoltWinters(train, gamma = FALSE)                 # Holt (trend)
hw  <- HoltWinters(train, seasonal = "multiplicative")   # Holt-Winters
pred <- predict(hw, n.ahead = length(test))
sqrt(mean((test - pred)^2))                              # RMSE
```

The pipeline prints the moving average computed by `ma()` next to `decompose()`'s trend — exactly the
"**by hand, on one cycle: 3 moving-average values, 1 seasonal coefficient, 1 CVS value, then check with the
software**" requested in the exercise.

---

## F. Common mistakes

| Mistake | Why it is wrong |
|---|---|
| Using `decompose(y, "additive")` because it is the default | the amplitude grows with the level: check Buys-Ballot first |
| Forgetting to normalise the coefficients | they must average 1 (multiplicative) or sum to 0 (additive) |
| Interpreting the CVS as "the trend" | CVS = trend + residual; the trend is the moving average |
| Using a window of 4 without half weights at the ends | the window is not centred: values shifted by half a quarter |
| Evaluating the forecast on the training data | always keep a test set |
| Reporting "RMSE = 170" without comparing | an RMSE only means something against another method or the naive forecast |
| Concluding "the model is good" with Ljung-Box p ≈ 0 | residuals are autocorrelated: say what structure is left |
| Applying LES/LED to a strongly seasonal series | they have no seasonal term |

## G. Run it

```bash
cd "/home/lupin/projects/SAE_303/SAE 3.03/2026/05_Gaz_UK_UKgas"
Rscript solution.R        # sorties_R/    : resultats.txt + PNG figures + comparaison_previsions.csv
python3 solution.py       # sorties_python/ : same pipeline in Python (selected models may differ slightly)
```

---

## H. The formulas behind the tests and the forecasting methods

### H.1 The three tests (step 5 of the brief)

| Test | Question (H0) | Statistic | Read the result |
|---|---|---|---|
| ADF (`adf.test`) | H0: unit root, non-stationary | regression `Δy_t = α + γ·y_{t-1} + Σ φ_i·Δy_{t-i}`, test on γ | p < 0.05 → stationary |
| Mann-Kendall (`mk.test`) | H0: no monotonic trend | `S = Σ_{i<j} sign(y_j − y_i)`, `Z = S / √Var(S)`, `Var(S) = n(n−1)(2n+5)/18` | p < 0.05 → trend |
| Pettitt (`pettitt.test`) | H0: no change point | `U_t = Σ_{i≤t} Σ_{j>t} sign(y_i − y_j)`, `K = max|U_t|`, `p ≈ 2·exp(−6K²/(n³+n²))` | p < 0.05 → break after the t that maximises `|U_t|` |

On UKgas: ADF p = 0.74 (non-stationary), Mann-Kendall p ≈ 3·10⁻²² (strong trend),
Pettitt break after observation 51 = **1972 Q3**, p ≈ 2·10⁻¹⁴.

*Caution:* Mann-Kendall and Pettitt assume independent observations. A seasonal series is not, so treat
these p-values as strong evidence, not exact probabilities.

### H.2 Exponential smoothing (step 8)

Notation: `L` = level, `b` = slope, `S` = seasonal coefficient, `p` = period, `h` = horizon.

```
LES  (simple)        L_t = α·y_t + (1−α)·L_{t−1}                         forecast: ŷ_{t+h} = L_t
LED  (Holt)          L_t = α·y_t + (1−α)(L_{t−1} + b_{t−1})
                     b_t = β(L_t − L_{t−1}) + (1−β)·b_{t−1}              forecast: ŷ_{t+h} = L_t + h·b_t
Holt-Winters (mult.) L_t = α·y_t / S_{t−p} + (1−α)(L_{t−1} + b_{t−1})
                     b_t = β(L_t − L_{t−1}) + (1−β)·b_{t−1}
                     S_t = γ·y_t / L_t + (1−γ)·S_{t−p}                   forecast: ŷ_{t+h} = (L_t + h·b_t)·S_{t+h−p}
```

α, β, γ ∈ [0, 1] are chosen by `HoltWinters()` to minimise the sum of squared one-step errors.
A large α means the level follows the latest observation closely.

### H.3 Error measures

```
RMSE = √( mean( (y_t − ŷ_t)² ) )        penalises large errors
MAE  = mean( |y_t − ŷ_t| )
MAPE = 100 · mean( |y_t − ŷ_t| / y_t )   in %, only if y > 0
```

---

## I. Complete runnable script (every step, with its output)

Self-contained: it needs only R and the packages `tseries`, `trend`, `forecast`. Copy it into a file and
run `Rscript walk.R`. The printed values are the ones used throughout this document.

```r
library(tseries); library(trend); library(forecast)
y <- UKgas; p <- 4

## 1. Exploration et tests
cat("ADF p =", adf.test(y)$p.value, "\n")
cat("Mann-Kendall p =", mk.test(as.numeric(y))$p.value, "\n")
pt <- pettitt.test(as.numeric(y))
cat("Pettitt: dernier index avant rupture =", pt$estimate[1],
    "-> date", time(y)[pt$estimate[1]], " p =", pt$p.value, "\n")

## 2. Choix du modèle (Buys-Ballot)
cyc <- (seq_along(y) - 1) %/% p
m <- tapply(y, cyc, mean); s <- tapply(y, cyc, sd)
bb <- summary(lm(s ~ m))$coefficients
cat("Buys-Ballot: pente =", bb[2,1], " p =", bb[2,4], "\n")

## 3. Tendance : moyenne mobile centrée, à la main puis ma()
w <- c(0.5, 1, 1, 1, 0.5) / p
T3 <- sum(w * y[1:5]); cat("T_3 à la main =", T3, "\n")
mm <- ma(y, order = p, centre = TRUE)
cat("T_3 avec ma() =", mm[3], "\n")

## 4. Coefficients saisonniers
dec <- decompose(y, type = "multiplicative")
ratio <- y / dec$trend
raw <- tapply(ratio, cycle(y), mean, na.rm = TRUE)
print(round(raw, 4)); print(round(raw / mean(raw), 4))
print(round(tapply(dec$seasonal, cycle(y), mean), 4))

## 5. CVS et résidus
S <- tapply(dec$seasonal, cycle(y), mean)
cvs <- y / dec$seasonal
print(round(head(cvs, 4), 2))
cat("R_3 =", as.numeric(y[3] / (dec$trend[3] * S[3])), "\n")

## 6. Validation
r <- na.omit(dec$random)
print(Box.test(r, lag = 8, type = "Ljung-Box")$p.value)
print(shapiro.test(r)$p.value)

## 7. Prévision
train <- window(y, end = c(1984, 4)); test <- window(y, start = c(1985, 1))
h <- length(test)
rmse <- function(a, f) sqrt(mean((as.numeric(a) - as.numeric(f))^2))
d <- decompose(train, "multiplicative")
Sq <- tapply(d$seasonal, cycle(train), mean)
cvs_tr <- train / d$seasonal
t <- seq_along(train)
fit <- lm(as.numeric(cvs_tr) ~ t); print(coef(fit))
tn <- length(train) + 1:h
trend_f <- coef(fit)[1] + coef(fit)[2] * tn
pos <- as.integer(cycle(test))
f_dec <- trend_f * Sq[pos]
les <- HoltWinters(train, beta = FALSE, gamma = FALSE)
led <- HoltWinters(train, gamma = FALSE)
hw  <- HoltWinters(train, seasonal = "multiplicative")
f_les <- predict(les, h); f_led <- predict(led, h); f_hw <- predict(hw, h)
f_ar <- forecast(auto.arima(train), h = h)$mean
f_nv <- as.numeric(window(train, start = c(1984, 1)))
cat("trend_f:", round(trend_f,1), "\nf_dec:", round(f_dec,1), "\n")
print(round(c(Decomp = rmse(test, f_dec), LES = rmse(test, f_les), LED = rmse(test, f_led),
  HW = rmse(test, f_hw), ARIMA = rmse(test, f_ar), Naif = rmse(test, f_nv)), 1))
```

### Output (R 4.3.3)

```
ADF p = 0.739            Mann-Kendall p = 2.75e-22
Pettitt: break after index 51 (= 1972.5), p = 2.08e-14
Buys-Ballot: slope = 0.5801, p = 1.09e-23           -> multiplicative
T_3 by hand = 123.675    T_3 with ma() = 123.675
raw seasonal   : 1.4538 0.9560 0.5585 1.0320
normalised     : 1.4537 0.9559 0.5584 1.0319        (= dec$figure)
CVS 1960       : 110.13 135.68 151.85 116.39
R_3 = 1.2278
Ljung-Box p = 0          Shapiro p = 0.0040
trend line     : 36.207 + 5.296·t
trend forecast : 571.1 576.4 581.7 587.0 592.3 597.6 602.9 608.2
decomposition  : 821.1 557.3 332.7 600.7 851.6 577.8 344.8 622.4

RMSE  Decomp 170.7 | LES 327.2 | LED 321.4 | Holt-Winters 76.5 | auto.arima 71.3 | Naive 101.9
```

Note: `auto.arima` here is the default call on the training data (RMSE 71.3). The `solution.R` pipeline
allows drift and a log transform and gets 45.9, which is why the table in D.2 differs. The two scripts
are consistent; they just use different ARIMA settings.
