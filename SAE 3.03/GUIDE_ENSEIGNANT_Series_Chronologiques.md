# SAE3.03 — Séries Chronologiques : Guide pour l'enseignant(e)

*A refresher-and-teach guide reconstructed from the course booklet (BUT SD, 2025-2026). French technical terms are kept throughout since they are the exam vocabulary; explanations are in plain English so you can rebuild your intuition quickly.*

---

## 0. Course map (so you know where each idea fits)

| Volume | Hours | Content |
|---|---|---|
| Cours (CM) | 8h | Theory: sections 1–4 below |
| TD | 14h (7×2h) | Worked exercises on paper |
| TP | 6h (3×2h) | Same exercises in a tool (R / Excel / Python) |
| Projet | 10h | Applied decomposition + forecast on a real dataset |
| Évaluation | CM-TD exam | Tests theory + hand computation |

The whole course answers one question: **given a sequence of numbers indexed by time, how do I describe its behavior (trend + seasonality + noise) and how do I predict what comes next?**

Two big families of tools are taught:
1. **Decomposition**: split $x_t$ into trend + seasonal + noise, by hand, using moving averages.
2. **Forecasting**: either (a) extrapolate the decomposition, or (b) exponential smoothing (a completely different, recursive technique).

Everything else (ACF/PACF, ARMA/ARIMA, Census, LOESS — section 5 "hors programme") is **not examined**; it's there to show students what's next if they want to go further (that's what a real stats software like R does under the hood).

---

## 1. What is a time series?

**Definition.** A *série chronologique* (time series) is a sequence of observations $x_{t_1}, x_{t_2}, \dots, x_{t_n}$ of some quantity, indexed by time, where **the order matters**. That's the whole difference with a normal statistical sample: in a random sample, shuffling the rows changes nothing; in a time series, shuffling destroys the information, because the dependency *between consecutive observations* is the signal we're trying to model.

Convention: values are always plotted in chronological order and consecutive points are joined by line segments (never a bar chart, never a scatter without order).

**Why do we study time series?**
- Understand the past (explain observed values).
- Predict the future (build forecasts for values not yet observed).
- Study the relationship between two or more series (e.g., does rainfall predict crop yield next month?).

**Classic teaching examples used throughout the booklet** (keep these — they recur in every section):
- **"Airlines"**: monthly international air passenger traffic, Jan 1949 – Dec 1960 (the textbook `AirPassengers` dataset). Strong upward trend + yearly seasonality + growing amplitude → this is the go-to example for a **multiplicative** model.
- **French population** 1920–1992 (INSEE) — smooth trend, no seasonality (annual data).
- **Essence aviation** (aviation fuel sales in France, quarterly 2005–2008) — the worked spreadsheet example, moderate trend + clear quarterly seasonality, used for both additive and multiplicative decomposition.
- **Ventes d'huîtres** (quarterly oyster sales) — used to show the effect of moving-average order.
- Real-world "flavor" examples for context: Bitcoin price, CO₂/temperature anomaly curves, Venezuela hyperinflation, CAC40 stock index.

**Where time series show up** (good motivating slide): economics/finance (INSEE, stock markets), environmental science (rainfall, temperature, river flow), life sciences (cell/animal behavior over time), and any "random phenomenon in time" (phone traffic, road traffic, bank counter usage).

---

## 2. Cleaning the data before you start (§1.2)

Two kinds of correction, applied *before* decomposition:

### 2.1 Transformation of the whole series
Sometimes the **variance grows with the level** of the series (a very common symptom — e.g. traffic that fluctuates ±5 in January but ±50 in August, simply because the level is higher). The fix is a **log transform**:

$$y_t = \ln(x_t)$$

**Why it works (the intuition to give students):** for small variations, $y_{t+1} - y_t \approx \dfrac{x_{t+1}-x_t}{x_t}$, i.e. a fixed increment on the log scale corresponds to a fixed *percentage* change on the original scale. So if your series grows by a roughly constant percentage each period (very common for economic series), the log-transformed series grows by a roughly constant *absolute* amount — variance stabilizes.

This is part of the wider **Box-Cox family** of transforms; a *logistic transform* exists too, for series bounded within a fixed range.

*Example from the booklet*: raw air-traffic series has amplitude that visibly grows over the years (100→600 range); after taking logs, the seasonal swings look the same size every year (4.5→6.5 range, roughly constant band) — variance is stabilized. This is a great "before/after" plot to show in class.

### 2.2 Point-wise corrections
- Missing data → interpolation.
- Accidental / aberrant values (sensor glitches, typos) → filtering (e.g. clip or remove obvious spikes). Booklet example: 15-minute evaporation sensor data with clearly impossible spikes, cleaned with a simple outlier filter.

---

## 3. Decomposition: the heart of the course (§1.3–1.5)

### 3.1 The three components

Any time series is treated, classically, as the *result* of three additive-or-multiplicative ingredients:

| Component | Symbol | Meaning |
|---|---|---|
| **Tendance** (trend) | $m_t$ | Long-run, persistent direction (up/down/flat) maintained over a long time span. The "average behavior" of the series. |
| **Composante périodique / saisonnière** (seasonal) | $s_t$ | A pattern that repeats at *fixed, regular* intervals (e.g. every 12 months, every 4 quarters). Independent of the trend. |
| **Composante résiduelle / aléas** (residual / noise) | $e_t$ | What's left over — irregular, usually small, random, mean-zero. Captures one-off shocks (strikes, weather, a crash). |

A trend is called **déterministe** if the series' fluctuations around it are small, **aléatoire** if they're large.

### 3.2 The stability property of the seasonal component

If $p$ is the period (12 for monthly, 4 for quarterly...), the seasonal coefficients repeat exactly:

$$s_t = s_{t+p} = s_{t+2p} = \dots$$

So a seasonal pattern is entirely described by just $p$ numbers: $s_1, \dots, s_p$ (e.g. 12 monthly coefficients).

**Normalization constraint**: because a constant shift could always be absorbed into the trend instead, we force the seasonal coefficients to have **zero mean** (additive model) — this makes them unique:

$$s_t^* = s_t - \bar s, \quad \bar s = \frac{1}{p}\sum_{i=1}^p s_i \quad \Rightarrow \quad \sum_t s_t^* = 0$$

*(For the multiplicative model the equivalent constraint is that the seasonal coefficients average to 1, so their sum over one period equals $p$ — see §5.)*

### 3.3 The three composition models

| Model | Formula | When to use |
|---|---|---|
| **Additif** | $x_t = m_t + s_t + e_t$ | Seasonal swings have **constant amplitude** regardless of the trend level. |
| **Multiplicatif** | $x_t = m_t \times s_t \times e_t$ | Seasonal swings **grow proportionally** with the trend level (amplitude increases as the series grows). |
| **Mixte** | $x_t = m_t \times s_t + e_t$ | *Not covered in this course* — just mention it exists. |

**Useful trick**: if $x_t>0$, a multiplicative series can always be turned additive by taking logs:
$$\ln(x_t) = \ln(m_t) + \ln(s_t) + \ln(e_t)$$
This is *why* the log transform from §2.1 matters — it's often the practical way to "convert" a multiplicative problem into an additive one that's easier to fit with linear tools.

### 3.4 How to decide which model to use — three methods

This is a favorite exam question ("look at this graph, which model?") — teach all three, they reinforce each other.

**(a) Méthode de la bande** (band method) — purely visual.
Draw the line through the local *maxima* and the line through the local *minima* of the raw series.
- Lines roughly **parallel** → amplitude is constant → **additive**.
- Lines **diverge** (fan out) → amplitude grows with the level → **multiplicative**.

**(b) Méthode du profil** (superimposed-curves / profile method) — also visual.
Overlay one curve per period-cycle (e.g. one line per year, x-axis = month 1–12).
- Curves roughly **parallel** → additive.
- Curves show peaks/troughs that get **more pronounced** over time → multiplicative.

**(c) Méthode du tableau de Buys-Ballot** — the *quantitative* method, good for exam calculation questions.
For each full period (e.g. each year), compute the **mean** $\bar Y$ and the **standard deviation** $s_Y$ of that period's values. Then fit a simple linear regression (least squares) between them:
$$s_Y = a \times \bar Y + b$$
- If the slope $a \approx 0$ → std-dev doesn't depend on the mean → **additive**.
- If $a \neq 0$ → std-dev grows/shrinks with the mean → **multiplicative**.

> **Worked mini-example (from the booklet, reproduce this on the board):**
> Two toy datasets, 4 years × 4 quarters each.
> - Dataset 1: regression gives `écart-type = 0.0613 × moyenne + 17.18` → slope ≈ 0 → **additive**.
> - Dataset 2: regression gives `écart-type = 0.1148 × moyenne + 8.8078` → slope clearly non-zero → **multiplicative**.

---

## 4. Estimating the trend (Section 2)

Two philosophies:

### 4.1 Tendance paramétrique
Assume the trend follows a known analytic shape and fit its parameters by least squares:

| Shape | Formula |
|---|---|
| Linéaire | $m_t = a + bt$ |
| Quadratique | $m_t = a + bt + ct^2$ |
| Logarithmique | $m_t = a + b\ln(t)$ |
| Exponentielle | $m_t = \lambda e^{a+bt}$ |
| Puissance | $m_t = \lambda t^a$ |
| (also mentioned: logistique, Gompertz) | — |

**Limitation to flag for students**: this only works if you're confident the trend really follows that shape for the whole series — a strong, unverifiable assumption.

### 4.2 Tendance non-paramétrique — the moving average (§2.1)

No assumption about shape; instead we use a **filter**: a linear transformation of the series into a smoother one,
$$y_t = \sum_{k \in K} \alpha_k \, x_{t+k}, \qquad \sum_{k} \alpha_k = 1$$
The **moving average** is the simplest and most important such filter.

**Definition — centered moving average of order $p$.**
Split the series into periods of $p$ observations. Two cases:

- **$p$ odd** ($p = 2k+1$): equal weights, symmetric window.
$$m_{p,t} = \frac{1}{p}\sum_{i=-k}^{k} x_{t+i} = \frac{x_{t-k}+\dots+x_t+\dots+x_{t+k}}{p}$$

- **$p$ even** ($p = 2k$): the two edge terms get **half weight** so the window stays centered on $t$ (there's no single middle point when $p$ is even):
$$m_{p,t} = \frac{1}{p}\left(\frac{x_{t-k}}{2} + \sum_{i=-k+1}^{k-1} x_{t+i} + \frac{x_{t+k}}{2}\right) = \frac{\frac{x_{t-k}}{2}+\dots+x_t+\dots+\frac{x_{t+k}}{2}}{p}$$

> **Why the halved edges for even $p$?** With $p=4$ (quarterly data), a symmetric window around $t$ needs 5 points ($t-2,\dots,t+2$), which is $p+1$ terms — one too many for a clean average of $p$ values. Giving the two outer terms half-weight brings the effective count back down to exactly $p$ while keeping the average centered.

**Toy hand-computation (do this live in class, it's the "aha" moment):**
$$m_{4,3} = \frac{\tfrac{x_1}{2}+x_2+x_3+x_4+\tfrac{x_5}{2}}{4}$$
i.e., for $p=4$ centered at $t=3$, you need $x_1$ through $x_5$, with $x_1$ and $x_5$ each counting half.

**Properties (worth a boxed slide):** applying a moving average of order $p$:
1. **Preserves a linear trend** — if $x_t$ has a linear trend, $m_{p,t}$ has the exact same trend.
2. **Removes seasonality of period $p$** entirely — if $x_t$ has a period-$p$ seasonal component, $m_{p,t}$ has none.
3. **Attenuates noise optimally** — $m_{p,t}$ is less noisy than $x_t$.

**Practical rule**: pick $p$ = the periodicity of your data (12 for monthly, 4 for quarterly) so property 2 kicks in and seasonality disappears, leaving a clean trend to look at.

**Limitations (important, don't skip):**
- **Edge loss**: you lose $k$ points at each end of the series ($p$ odd) or $k$ points ($p$ even) — the smoothed series is shorter than the original, so moving averages are **not recommended for forecasting** directly (no value exists at the most recent dates).
- **Lag near turning points**: if the trend changes level or slope at some date, the moving average badly misrepresents that region for a while before *and* after the change (it "blurs" structural breaks).
- **Effet de Slutsky-Yule**: smoothing can *introduce* spurious autocorrelated wiggles that weren't in the true underlying trend — a caution against over-interpreting a smoothed curve as "the truth."

**Extensions** (mention, not exam-critical): weighted moving averages (e.g. Gaussian weights, or more weight on recent points), and **médiane mobile** (median instead of mean — much more robust to outliers, same window logic).

### 4.3 La droite de tendance (fitting a straight line to the smoothed series)

Once $m_{p,t}$ shows a visually linear trend, fit a regression line to it (not to the raw $x_t$ — the seasonality in $x_t$ would just add noise to the fit and weaken the correlation):

$$y = \beta_1 x + \beta_0, \qquad \beta_1 = \frac{\text{Cov}(m_{p,t}, t)}{\text{Var}(t)}, \qquad \beta_0 = \overline{m_{p,t}} - \beta_1 \bar t$$

This gives you a usable analytic formula $\hat m_t = \beta_1 t + \beta_0$ for the trend at *any* $t$, including future dates — which is exactly what you need to forecast (§6).

---

## 5. Estimating the seasonal component & building the CVS (Section 3)

Goal: once you have an estimated trend $\hat m_t$ (from a moving average or from the regression line), strip it out and look at what's left to isolate seasonality.

**The one-sentence intuition to hold onto through this whole section**: *"seasonal coefficient" is just "how far above/below the trend this particular season usually sits, averaged over all the years you've observed."* Everything else — centering, ratios vs. differences, CVS — is bookkeeping around that one idea.

### 5.1 Additive model — full procedure
1. Estimate $\hat m_t$ (moving average of order $p$, or parametric fit).
2. For each of the $p$ seasons, collect the **differences** $\{x_t - \hat m_t\}$ across all the years you have, and average them (per season) into $p$ raw seasonal coefficients $\hat s_t$.
3. Force the mean to zero over one period: $s_t^* = \hat s_t - \bar s$, with $\bar s = \frac{1}{p}\sum_{i=1}^p \hat s_i$.

**Deseasonalized series (série corrigée des variations saisonnières, CVS):**
$$x_t^* = x_t - s_t^*$$
This is the number you'd compare across seasons directly (e.g., a January value vs. a July value), because the seasonal effect has been removed.

**Residual/error check**: $e_t = x_t - \hat m_t - s_t^* = x_t^* - \hat m_t$. If the model fits well, these should be small and centered around 0, roughly $N(0,\sigma^2)$ with small $\sigma$.

#### 5.1.1 Worked toy example (additive) — small numbers, zero noise, fully computed

Before the messy real dataset, walk through a *constructed* series where nothing is left to chance — this is the version to put on the board first, because every number checks out exactly and it makes the mechanics undeniable.

Two years of quarterly data ($p=4$, $t=1,\dots,8$), built so it's *exactly* trend + season with no noise:

| $t$ | Année | Trim | $x_t$ |
|---|---|---|---|
| 1 | An 1 | T1 | 20 |
| 2 | An 1 | T2 | 35 |
| 3 | An 1 | T3 | 40 |
| 4 | An 1 | T4 | 25 |
| 5 | An 2 | T1 | 24 |
| 6 | An 2 | T2 | 39 |
| 7 | An 2 | T3 | 44 |
| 8 | An 2 | T4 | 29 |

**Step 1 — moving average of order 4** (even order, so use the half-weight-edges formula from §4.2). With only 8 points and $p=4$ ($k=2$), you can only compute it for $t=3,4,5,6$ — this is the "edge loss" from §4.2 showing up in practice; with a short series, it bites hard (you lose *half* the data here).

$$m_{4,3} = \frac{x_1/2+x_2+x_3+x_4+x_5/2}{4} = \frac{10+35+40+25+12}{4} = 30.5$$
$$m_{4,4} = \frac{x_2/2+x_3+x_4+x_5+x_6/2}{4} = \frac{17.5+40+25+24+19.5}{4} = 31.5$$
$$m_{4,5} = \frac{x_3/2+x_4+x_5+x_6+x_7/2}{4} = \frac{20+25+24+39+22}{4} = 32.5$$
$$m_{4,6} = \frac{x_4/2+x_5+x_6+x_7+x_8/2}{4} = \frac{12.5+24+39+44+14.5}{4} = 33.5$$

**Step 2 — detrend** ($x_t - m_{4,t}$), only where $m_{4,t}$ exists:

| $t$ | Trim | $x_t$ | $m_{4,t}$ | $x_t - m_{4,t}$ |
|---|---|---|---|---|
| 3 | T3 | 40 | 30.5 | **9.5** |
| 4 | T4 | 25 | 31.5 | **-6.5** |
| 5 | T1 | 24 | 32.5 | **-8.5** |
| 6 | T2 | 39 | 33.5 | **5.5** |

Because this toy series only has one usable observation per season (T1 only appears once in the computable range, at $t=5$; same for T2, T3, T4), there's nothing to *average* per season yet — the raw coefficient **is** that single difference: $\hat s_1=-8.5$, $\hat s_2=5.5$, $\hat s_3=9.5$, $\hat s_4=-6.5$. *(With more years, as in the real example below, you'd have 3 or 4 values per season here and would average them.)*

**Step 3 — center.** Sum of raw coefficients: $-8.5+5.5+9.5-6.5 = 0$ already, so $\bar s = 0$ and $s_t^* = \hat s_t$ — no adjustment needed this time (a nice coincidence of the constructed numbers, not something to expect in general).

**Step 4 — CVS**, applied to *all 8* points (the seasonal coefficient for "T1" applies to every T1 you have, even the ones outside the moving-average window):

| $t$ | Trim | $x_t$ | $s_t^*$ | $x_t^* = x_t - s_t^*$ |
|---|---|---|---|---|
| 1 | T1 | 20 | -8.5 | **28.5** |
| 2 | T2 | 35 | 5.5 | **29.5** |
| 3 | T3 | 40 | 9.5 | **30.5** |
| 4 | T4 | 25 | -6.5 | **31.5** |
| 5 | T1 | 24 | -8.5 | **32.5** |
| 6 | T2 | 39 | 5.5 | **33.5** |
| 7 | T3 | 44 | 9.5 | **34.5** |
| 8 | T4 | 29 | -6.5 | **35.5** |

**The payoff, worth pointing out explicitly**: the CVS column ($28.5, 29.5, 30.5, \dots, 35.5$) increases by exactly $1$ every quarter — a perfectly clean straight line. Because this toy series has zero noise, deseasonalizing it *exactly reconstructs the trend*. That's the whole point of a CVS in one picture: **once seasonality is correctly removed, what's left is (an estimate of) the trend** — the residual $e_t$ is $0$ everywhere here; in real data it won't be exactly $0$, but it should be *small*.

#### 5.1.2 Worked toy example (multiplicative) — same idea, ratios instead of differences

Same structure, but now built so the seasonal *swing grows with the level* (trend $10+2t$, season factors $0.8, 1.1, 1.3, 0.8$ for T1–T4, chosen to average to 1):

| $t$ | Trim | $x_t$ |
|---|---|---|
| 1 | T1 | 9.6 |
| 2 | T2 | 15.4 |
| 3 | T3 | 20.8 |
| 4 | T4 | 14.4 |
| 5 | T1 | 16.0 |
| 6 | T2 | 24.2 |
| 7 | T3 | 31.2 |
| 8 | T4 | 20.8 |

**Step 1 — moving average** (same formula, $t=3,\dots,6$):
$$m_{4,3}=\tfrac{4.8+15.4+20.8+14.4+8.0}{4}=15.85 \quad m_{4,4}=\tfrac{7.7+20.8+14.4+16.0+12.1}{4}=17.75$$
$$m_{4,5}=\tfrac{10.4+14.4+16.0+24.2+15.6}{4}=20.15 \quad m_{4,6}=\tfrac{7.2+16.0+24.2+31.2+10.4}{4}=22.25$$

*(Notice these don't land on perfectly round numbers the way the additive example did — a moving average removes additive seasonality exactly, but only approximates the trend when the true model is multiplicative. That's precisely why §3.3's "take logs to turn multiplicative into additive" trick is worth knowing: on the log scale, the moving average would recover the trend cleanly again.)*

**Step 2 — ratios** $x_t/m_{4,t}$, one per season here too:

| $t$ | Trim | $x_t/m_{4,t}$ |
|---|---|---|
| 3 | T3 | $20.8/15.85=1.312$ |
| 4 | T4 | $14.4/17.75=0.811$ |
| 5 | T1 | $16.0/20.15=0.794$ |
| 6 | T2 | $24.2/22.25=1.088$ |

**Step 3 — normalize to mean 1.** Raw coefficients $\hat s_1=0.794,\ \hat s_2=1.088,\ \hat s_3=1.312,\ \hat s_4=0.811$; mean $\bar s = 1.001$ (essentially 1 already). $s_t^*=\hat s_t/\bar s$: $s_1^*\approx0.793$, $s_2^*\approx1.086$, $s_3^*\approx1.311$, $s_4^*\approx0.810$.

**Step 4 — CVS** ($x_t^*=x_t/s_t^*$) for all 8 points: $12.1,\ 14.2,\ 15.9,\ 17.8,\ 20.2,\ 22.3,\ 23.8,\ 25.7$ — again a smoothly increasing series tracking the underlying trend ($12,14,16,\dots,26$), just not landing exactly on it because the moving-average step wasn't exact this time.

### 5.2 Multiplicative model — full procedure (recap)
Same three steps as 5.1, but with **ratios instead of differences**, and **proportional correction instead of subtraction** (see the worked example just above):
1. Estimate $\hat m_t$.
2. Raw seasonal coefficients from the ratios $\{x_t/\hat m_t\}$, summarized per season.
3. Force the coefficients to average to **1** (sum to $p$ over a period): $s_t^* = \hat s_t / \bar s$, $\bar s = \frac{1}{p}\sum \hat s_i$.

**CVS**: $x_t^* = x_t / s_t^*$.
**Residual**: $e_t = \dfrac{x_t}{\hat m_t \times s_t^*} = \dfrac{x_t^*}{\hat m_t}$.

### 5.3 Full worked example — Ventes d'essence aviation (reproduce this end-to-end in TD)

Now the real, noisier dataset from the booklet — same procedure, but this time each season has **3 usable observations** to average (instead of 1 like the toy example), which is the realistic case. Quarterly aviation fuel sales in France, 2005–2008 (thousands of tonnes):

| Année | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| 2005 | 3.6 | 7.0 | 7.6 | 3.7 |
| 2006 | 3.6 | 6.7 | 7.4 | 3.9 |
| 2007 | 3.7 | 6.4 | 7.1 | 4.1 |
| 2008 | 3.6 | 5.7 | 7.1 | 3.7 |

**Column layout** (build these exact columns with students, e.g. in Excel or R):

| Col | Meaning | Additive formula | Multiplicative formula |
|---|---|---|---|
| A, B | index $t$, raw value $x_t$ | — | — |
| C | trend estimate | $\hat m_t = m_{4,t}$ | $\hat m_t = m_{4,t}$ (same) |
| D | detrended | $x_t - \hat m_t$ | $x_t/\hat m_t$ |
| E | raw seasonal coeff. | average of col-D per season | average of col-D per season |
| F | seasonal coeff. (normalized) | $s_t^*=\hat s_t-\bar s$ | $s_t^*=\hat s_t/\bar s$ |
| G | CVS | $x_t^*=x_t-s_t^*$ | $x_t^*=x_t/s_t^*$ |
| H | residual $e_t$ | $x_t-\hat m_t-s_t^*$ | $x_t/(\hat m_t\times s_t^*)$ |

**Columns A–D, fully computed** ($m_{4,t}$ only exists for $t=3,\dots,14$ — 2 points lost at each end):

| $t$ | Année | Trim | $x_t$ | $m_{4,t}$ | $x_t-m_{4,t}$ |
|---|---|---|---|---|---|
| 1 | 2005 | T1 | 3.6 | — | — |
| 2 | 2005 | T2 | 7.0 | — | — |
| 3 | 2005 | T3 | 7.6 | 5.475 | 2.125 |
| 4 | 2005 | T4 | 3.7 | 5.4375 | -1.7375 |
| 5 | 2006 | T1 | 3.6 | 5.375 | -1.775 |
| 6 | 2006 | T2 | 6.7 | 5.375 | 1.325 |
| 7 | 2006 | T3 | 7.4 | 5.4125 | 1.9875 |
| 8 | 2006 | T4 | 3.9 | 5.3875 | -1.4875 |
| 9 | 2007 | T1 | 3.7 | 5.3125 | -1.6125 |
| 10 | 2007 | T2 | 6.4 | 5.3 | 1.1 |
| 11 | 2007 | T3 | 7.1 | 5.3125 | 1.7875 |
| 12 | 2007 | T4 | 4.1 | 5.2125 | -1.1125 |
| 13 | 2008 | T1 | 3.6 | 5.125 | -1.525 |
| 14 | 2008 | T2 | 5.7 | 5.075 | 0.625 |
| 15 | 2008 | T3 | 7.1 | — | — |
| 16 | 2008 | T4 | 3.7 | — | — |

**Column E — average column D per season** (3 values each, since T1 2005 and T3/T4 2008 fell outside the computable range):

| Trim | Values ($x_t-m_t$) | $\hat s_t$ (raw) | $s_t^*$ (centered) |
|---|---|---|---|
| T1 | -1.775, -1.6125, -1.525 | -1.638 | **-1.613** |
| T2 | 1.325, 1.1, 0.625 | 1.017 | **1.042** |
| T3 | 2.125, 1.9875, 1.7875 | 1.967 | **1.992** |
| T4 | -1.7375, -1.4875, -1.1125 | -1.446 | **-1.421** |

($\bar s = -0.025$, essentially zero — nearly no centering adjustment needed. Notice $s_1^*=-1.613$ matches the $-1.61$ used in the §6.1 forecast worked example — same number, computed from scratch here.)

**Columns G, H — CVS and residual**, applying each season's $s_t^*$ to *every* occurrence of that season (all 16 points, not just $t=3..14$):

| $t$ | Trim | $x_t$ | $s_t^*$ | CVS $x_t^*=x_t-s_t^*$ | $e_t=(x_t-m_t)-s_t^*$ |
|---|---|---|---|---|---|
| 1 | T1 | 3.6 | -1.613 | 5.213 | — |
| 2 | T2 | 7.0 | 1.042 | 5.958 | — |
| 3 | T3 | 7.6 | 1.992 | 5.608 | 0.133 |
| 4 | T4 | 3.7 | -1.421 | 5.121 | -0.317 |
| 5 | T1 | 3.6 | -1.613 | 5.213 | -0.163 |
| 6 | T2 | 6.7 | 1.042 | 5.658 | 0.283 |
| 7 | T3 | 7.4 | 1.992 | 5.408 | -0.004 |
| 8 | T4 | 3.9 | -1.421 | 5.321 | -0.067 |
| 9 | T1 | 3.7 | -1.613 | 5.313 | 0.000 |
| 10 | T2 | 6.4 | 1.042 | 5.358 | 0.058 |
| 11 | T3 | 7.1 | 1.992 | 5.108 | -0.204 |
| 12 | T4 | 4.1 | -1.421 | 5.521 | 0.308 |
| 13 | T1 | 3.6 | -1.613 | 5.213 | 0.088 |
| 14 | T2 | 5.7 | 1.042 | 4.658 | -0.417 |
| 15 | T3 | 7.1 | 1.992 | 5.108 | — |
| 16 | T4 | 3.7 | -1.421 | 5.121 | — |

**What to point out to students**: the CVS column stays in a tight $4.66$–$5.96$ band, all residuals are small ($|e_t|\le0.42$) and scattered around 0 with no obvious pattern — that's the visual/numeric signature of a **good fit**. If instead the residuals grew steadily over time or all had the same sign in a block, that would signal the wrong model was chosen back in §3.4.

**Multiplicative version — same $\hat m_t$, condensed** (full method is identical to the toy example in §5.1.2, just with 3 values averaged per season instead of 1):

| Trim | Raw ratio avg $\hat s_t$ | Normalized $s_t^*$ |
|---|---|---|
| T1 | 0.690 | **0.694** |
| T2 | 1.192 | **1.200** |
| T3 | 1.364 | **1.372** |
| T4 | 0.730 | **0.735** |

(Matches the $0.69$ used for T1 in the §6.1 forecast example.) CVS values ($x_t^*=x_t/s_t^*$) come out in a very similar $4.75$–$5.84$ band to the additive version above — confirming the guide's earlier point that **for this dataset the two models are nearly indistinguishable in fit quality**, which is itself a useful thing to show students: Buys-Ballot told us multiplicative was technically the better call (§3.4), but additive would have worked almost as well here because the trend barely moves.

---

## 6. Forecasting (Section 4)

Two families of method. **Golden rule to hammer home first**: never evaluate a forecast on the data used to fit the model — always split into a **training series** and a **test series** (train/test split), exactly like in machine learning.

Notation: $\hat x_T(h)$ = the forecast made at date $T$ for horizon $h$ steps ahead (so $\hat x_T(h) = \hat x_{T+h}$). Hats distinguish *estimated* quantities from theoretical ones.

### 6.1 Forecasting from the trend + seasonal decomposition
If the series is well described by trend + season only (small residuals), just evaluate the fitted model at a future date:

$$\hat x_t = \hat m_t + \hat s_t \quad \text{(additive)} \qquad \hat x_t = \hat m_t \times \hat s_t \quad \text{(multiplicative)}$$

where $\hat m_t = a + bt$ comes from the regression line of §4.3, and $\hat s_t$ is just the known periodic seasonal coefficient (all $p$ of them are already known from §5).

**Worked example (continuing the essence-aviation data):** forecast the 1st quarter of 2009, i.e. $t=17$.
- Trend regression found: $\hat m_t = -0.032t + 5.59 \Rightarrow \hat m_{17} = -0.032(17)+5.59 = 5.046$.
- Additive: $s_{17}^* = s_1^* = -1.61 \Rightarrow \hat x_{17} = 5.046 - 1.61 = 3.436$.
- Multiplicative: $s_{17}^* = s_1^* = 0.69 \Rightarrow \hat x_{17} = 5.046 \times 0.69 = 3.48$.

Both models land close together — reassuring given they gave nearly identical residuals in §5.3.

### 6.2 Exponential smoothing — a completely different idea

**Motivation**: forecast from the *most recent* observations without re-doing the full trend/seasonal estimation every time a new point arrives. It's a *recursive*, cheap, "online" method — you just update yesterday's forecast with today's new observation.

| Method | Model assumed | Smoothing constants | Fits series that are... |
|---|---|---|---|
| **LES / SES** (simple) | $x_t = a + e_t$ | $\beta$ | flat (no trend, no season) |
| **LED / Holt** (double) | $x_t = b+at+e_t$ | $\beta$ | linear trend, no season |
| **Holt-Winters non-saisonnier** | $x_t = b+at+e_t$ | $\alpha,\gamma$ | linear trend, no season (alt. parametrization) |
| **Holt-Winters saisonnier additif** | $x_t = b+at+s_t+e_t$ | $\alpha,\beta,\gamma$ | linear trend + additive season |
| Holt-Winters saisonnier multiplicatif | $x_t = (b+at)\times s_t + e_t$ | $\alpha,\beta,\gamma$ | linear trend × season — **not covered** |

#### 6.2.1 Lissage exponentiel simple (LES / SES)

**Idea**: the best constant forecast is the one minimizing a *weighted* least-squares problem where recent observations count more, with weights decaying geometrically:
$$\min_a \sum_{j=0}^{T-1} \beta^j (x_{T-j}-a)^2, \qquad \beta \in [0,1]$$

**Result** — the forecast is a weighted average of *all* past observations, weights shrinking exponentially with age:
$$\hat x_T(h) := (1-\beta)\sum_{j=0}^{T-1}\beta^j x_{T-j}$$

**Recursive update (the practical formula you'll actually compute with):**
$$\hat x_T(h) := \beta \, \hat x_{T-1}(h) + (1-\beta)\, x_T$$
Initialization: $\hat x_1(h) = x_1$ (or the sample mean $\bar x$ — choice barely matters, it's "forgotten" quickly).

**Interpreting $\beta$ (a key intuition — draw this on the board):**
- $\beta$ close to **0** → "**souple**" (flexible) forecast: heavily driven by the most recent point; at $\beta=0$, $\hat x_T(h)$ = last observed value.
- $\beta$ close to **1** → "**rigide**" (rigid) forecast: remembers far into the past, barely reacts to new shocks; at $\beta=1$, the forecast never changes from its initial value.

#### 6.2.2 Lissage exponentiel double de Holt (LED)

Same idea, but fitting a **line** instead of a constant (handles a linear trend):
$$\min_a \sum_{j=0}^{T-1}\beta^j\big(x_{T-j}-(b+ah)\big)^2$$

Requires **two nested smoothings**: smooth the raw series once ($S_1$), then smooth the smoothed series again ($S_2$) — hence "double":
$$S_1(T) = (1-\beta)\sum_{j=1}^{T-1}\beta^j x_{T-j}, \qquad S_2(T) = (1-\beta)\sum_{j=1}^{T-1}\beta^j S_1(T-j)$$
$$\hat a_T = \frac{1-\beta}{\beta}\big(S_1(T)-S_2(T)\big), \qquad \hat b_T = 2S_1(T)-S_2(T)$$
Forecast: $\hat x_T(h) = \hat b_T + \hat a_T \, h$.

**Recursive update form:**
- Init: $\hat a_2 = x_2-x_1$, $\hat b_2 = x_2$.
- Update: $\hat a_T = \hat a_{T-1} + (1-\beta)^2\big(x_T-\hat x_{T-1}(1)\big)$
  $\hat b_T = \hat b_{T-1}+\hat a_{T-1}+(1-\beta^2)\big(x_T-\hat x_{T-1}(1)\big)$

*(Booklet has a full worked monthly table with $\alpha=0.4$ — good template for a TD exercise: give students the raw data column and have them fill in "1er lissage," "2nd lissage," $a$, $b$, "PREV" columns by hand or in Excel.)*

#### 6.2.3 Lissage exponentiel de Holt-Winters (HW)

Generalizes Holt to allow **seasonality** too. Two variants are taught:

**(a) Méthode non saisonnière** (equivalent reparametrization of Holt, using $\alpha,\gamma$ instead of $\beta$):
- Init: $\hat b_1 = x_1$, $\hat a_1 = x_1-x_0$.
- Update: $\hat b_T = \alpha x_t + (1-\alpha)(\hat b_{T-1}+\hat a_{T-1})$
  $\hat a_T = \gamma(\hat b_T-\hat b_{T-1}) + (1-\gamma)\hat a_{T-1}$
- Forecast: $\hat x_T(h) = \hat b_T + \hat a_T h$.

**(b) Méthode saisonnière additive** (three parameters $\alpha,\beta,\gamma$, model $x_t = b+at+s_t+e_t$, period $p$):
$$\hat a_T=\beta(\hat b_T-\hat b_{T-1})+(1-\beta)\hat a_{T-1}$$
$$\hat b_T=\alpha(x_t-\hat S_{T-p})+(1-\alpha)(\hat b_{T-1}+\hat a_{T-1})$$
$$\hat S_T=\gamma(x_t-\hat b_T)+(1-\gamma)\hat S_{T-p}$$
Forecast (piecewise, reusing the seasonal coefficient one period back):
$$\hat x_T(h)=\hat a_T h + \hat b_T + \hat S_{T+h-p} \quad (1\le h\le p), \qquad \hat S_{T+h-2p}\ \text{for } p<h\le 2p,\ \text{etc.}$$

**Teaching tip**: point out the pattern across all three update equations — each is a weighted average of "new evidence" (something derived from $x_t$) and "old belief" (last period's estimate). That's the unifying idea of every exponential-smoothing method in this table.

### 6.3 Choosing the smoothing constant(s)

**Méthode subjective**: pick based on how rigid/flexible you want the forecast.
- Rigid forecast → $\beta \in [0.7, 0.99]$.
- Flexible forecast → $\beta \in [0.01, 0.3]$.

**Méthode objective**: choose the constant that **minimizes a forecast-error criterion**, computed on a held-out portion of the series:

$$EM = \frac1N\sum_{i=1}^{N}\big(x_{i+1}-\hat x_i(1)\big) \qquad \text{(mean error — can cancel out, checks for bias)}$$
$$EAM = \frac1N\sum_{i=1}^{N}\big|x_{i+1}-\hat x_i(1)\big| \qquad \text{(mean absolute error)}$$
$$EQM = \frac1N\sum_{i=1}^{N}\big(x_{i+1}-\hat x_i(1)\big)^2 \qquad \text{(mean squared error)}$$

*(Booklet example sweeps $\alpha$ from 0.1 to 0.9 on the essence-aviation series and tabulates EM/EQM/EAM for each — a perfect spreadsheet exercise: EQM is minimized around $\alpha \approx 0.4$–$0.5$ in that example.)*

### 6.4 Limits of exponential smoothing (a good closing slide for section 4)
- **Advantage**: cheap, fast, "bon marché" forecasts, no re-estimation of a full model needed.
- **Disadvantage 1**: nothing guarantees optimality on a given dataset — it can be far from the best possible method.
- **Disadvantage 2**: no natural **prediction interval** (no probabilistic framework), unlike model-based (ARIMA-type) forecasting.
- Bridge to "hors programme": except for multiplicative Holt-Winters, these smoothing methods actually correspond to specific probabilistic models — this is *why* ARMA/ARIMA (section 5) exist: to generalize and justify these simpler techniques with a proper statistical framework, and to provide prediction intervals.

---

## 7. Beyond the exam (Section 5 — mention only, don't test)

Use this as a "if you continue in stats/data science, here's what's next" wrap-up slide:
- **ACF / PACF** (autocorrelation / partial autocorrelation functions) — diagnose dependency structure, guide AR/MA order choice.
- **Stationarity** — a series is (weakly) stationary if mean/variance/autocorrelation don't change over time (white noise = the simplest stationary series).
- **Other decomposition methods**: Census method, LOESS (locally estimated scatterplot smoothing).
- **ARMA(p,q), SARMA, ARIMA(p,d,q), SARIMA, ARMAX** — proper probabilistic forecasting models; compared via **AIC** (lower = better, balances fit vs. simplicity).
- Conditional heteroscedasticity; further study of decomposition-residual noise (done in TP).

---

## 8. Suggested teaching sequence (mapping content → CM/TD/TP slots)

| Session | Content | Suggested activity |
|---|---|---|
| CM1 | §1 definitions + examples, §2 preprocessing | Show Airlines dataset raw vs log-transformed |
| CM2 | §3 decomposition, 3 models, 3 model-choice methods | Live band-method sketch on the board |
| TD1 | Buys-Ballot by hand on a small 3–4 year dataset | Exercise A below |
| CM3 | §4 trend: parametric vs moving average, formulas | Hand-compute a small moving average |
| TD2 | Moving average + trend line on paper | Exercise B below |
| CM4 | §5 seasonal correction + CVS, full worked example | Reproduce essence-aviation spreadsheet |
| TP1 | Same decomposition in Excel/R | Compare hand calc to software output |
| CM5 | §6.1–6.2 forecasting via decomposition + intro smoothing | — |
| TD3–4 | SES / Holt by hand, small numeric tables | Exercise C, D below |
| TP2–3 | Holt-Winters in software, error-metric sweep | Exercise E below |
| CM6 | §6.3–6.4 choosing constants, limitations, §7 preview | Wrap-up + project briefing |

---

## 9. Practice exercises (with worked solutions)

### Exercise A — Model choice (Buys-Ballot)
A company's quarterly revenue over 3 years gives these (mean, std-dev) pairs per year: (100, 24), (115, 25), (133, 25.2). Fit $s_Y = a\bar Y + b$ by eye or by least squares and decide: additive or multiplicative?

**Solution**: the standard deviation barely changes (24→25.2) while the mean grows by 33% — slope $a$ is close to 0 → **additive model**. (This mirrors the booklet's worked additive example almost exactly.)

### Exercise B — Moving average by hand
Given monthly data $x_1,\dots,x_6 = 10, 14, 18, 16, 20, 22$, compute the centered moving average of order $p=4$ at $t=3$ and $t=4$.

**Solution**: for $p=4$ (even), $m_{4,t} = \dfrac{\tfrac{x_{t-2}}{2}+x_{t-1}+x_t+x_{t+1}+\tfrac{x_{t+2}}{2}}{4}$.
- $m_{4,3} = \dfrac{\tfrac{10}{2}+14+18+16+\tfrac{20}{2}}{4} = \dfrac{5+14+18+16+10}{4} = \dfrac{63}{4} = 15.75$
- $m_{4,4} = \dfrac{\tfrac{14}{2}+18+16+20+\tfrac{22}{2}}{4} = \dfrac{7+18+16+20+11}{4} = \dfrac{72}{4} = 18$

### Exercise C — Seasonal coefficients & CVS (additive)
Quarterly data for 2 years: 2023 = (50, 80, 90, 55), 2024 = (54, 84, 94, 59). Suppose the order-4 moving average gives $\hat m_t \approx 69$ for every quarter (constant trend for simplicity). Compute the raw seasonal coefficient for Q2, then the CVS value for Q2 2024.

**Solution**: $x_t - \hat m_t$ for Q2: $80-69=11$ (2023), $84-69=15$ (2024) → average $\hat s_{Q2} = 13$. Assume after normalization $s^*_{Q2}=13$ (already ≈ centered here for simplicity). CVS: $x^*_{Q2,2024} = 84 - 13 = 71$.

### Exercise D — Simple exponential smoothing by hand
Data: $x_1=100, x_2=104, x_3=98, x_4=110$. Using $\beta=0.5$ and $\hat x_1(1)=x_1=100$, compute $\hat x_2(1), \hat x_3(1), \hat x_4(1)$ via the update rule.

**Solution**: $\hat x_T(1) = \beta\hat x_{T-1}(1)+(1-\beta)x_T$.
- $\hat x_2(1) = 0.5(100)+0.5(104) = 102$
- $\hat x_3(1) = 0.5(102)+0.5(98) = 100$
- $\hat x_4(1) = 0.5(100)+0.5(110) = 105$
So the forecast for period 5 is $\hat x_5 = 105$.

### Exercise E — Choosing $\beta$ objectively
Using the four forecasts you'd get from Exercise D-style calculations at $\beta=0.3$ and $\beta=0.7$ on the same data, which one has lower EQM against the actual next values? *(Have students actually run both and compare — this is best done in a spreadsheet/TP rather than by hand, mirroring Tableau 11–12 in the booklet.)*

### Exercise F (project-style, open-ended)
Give students a real quarterly or monthly dataset (economic indicator, weather, sales...). Ask them to: (1) plot it and pick additive vs. multiplicative using at least two of the three methods, (2) compute the moving average and trend line, (3) compute seasonal coefficients and the CVS, (4) forecast the next 2 periods two ways — decomposition-based and Holt-Winters — and compare using EQM on a held-out test period. This is essentially a compressed version of the 10h **Projet**.

---

## 10. Bibliography (from the booklet, for your own prep)

- Aragon, Y., *Séries temporelles avec R*, EDP Sciences, 2011.
- Aragon, Y., *Séries temporelles avec R : Méthodes et cas*, Springer, 2011.
- Bourbonnais, R. & Terraza, V., *Analyse des séries temporelles*, 5e éd., 2022.
- Box, G.E.P., Jenkins, G.M., Reinsel, G.C., *Time Series Analysis*, Wiley, 4th ed., 2008.
- Chatfield, C., *The Analysis of Time Series, an Introduction*, Chapman & Hall, 4th ed., 1989.
- Goldfarb, B. & Pardoux, C., *Introduction à la méthode statistique*, Dunod, 2011.
- Hamilton, J.D., *Time Series Analysis*, Princeton University Press, 1994.
- Lagnoux, A., *Statistique pour les Sciences Humaines II* (perso.math.univ-toulouse.fr/lagnoux/enseignements/).
- Monino, J.-L., *TD de statistique descriptive*, Dunod, 2017.
- Brockwell, P. & Davis, R., *Time Series: Theory and Methods*, Springer, 2nd ed., 1991.
