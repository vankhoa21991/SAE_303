### SAÉ 3-03: Description et prévision de données temporelles – Cheat Sheet v3

This document provides a mathematically rigorous synthesis of time series analysis and forecasting as defined in the course 'SAÉ 3-03: Description et prévision de données temporelles'. It highlights essential formulas for decomposition, seasonality adjustment (CVS), autocorrelation, and forecasting.

#### 1. Fundamental Components and Models

A time series (série chronologique) is a sequence of observations $X_t$ where the temporal dependence between variables is the primary source of information. Classically, a series is decomposed into three components:

1. **Trend (Composante tendancielle/Trend):** $m_t$, the long-term persistent direction.
2. **Seasonality (Mouvement périodique/saisonnier):** $s_t$, phenomena repeating at regular intervals $p$.
3. **Residuals (Composante résiduelle/aléa):** $e_t$, irregular "noise" with a zero mean.

##### Composition Models

| Model Type | Equation | Usage |
|---|---|---|
| Additive | $X_t = m_t + s_t + e_t$ | Used when seasonal variation amplitude is constant regardless of the trend level. |
| Multiplicative | $X_t = m_t \times s_t \times e_t$ | Used when seasonal variation amplitude is proportional to the trend level. |
| Mixed | $X_t = m_t \times s_t + e_t$ | (Not studied in this course). |

#### 2. Model Selection Methods (Méthodes de choix du modèle)

| Method | Procedure | Criteria for Additive Model | Criteria for Multiplicative Model |
|---|---|---|---|
| Band Method (Méthode de la bande) | Plot lines through maxima and minima. | Lines are approximately parallel. | Lines diverge or converge (not parallel). |
| Profile Method (Méthode du profil) | Superimpose seasonal cycles. | Curves are approximately parallel. | Cycles accentuate (peaks/troughs widen). |
| Buys-Ballot Method | Linear regression of standard deviation $s_r$ against the mean $\bar{y}$. | $s_r = a\bar{y} + b$ where $a \approx 0$. | $a \neq 0$ (Standard deviation is a function of the mean). |

#### 3. Trend Estimation (Analyse de la tendance)

##### Non-Parametric: Centred Moving Averages (Moyennes mobiles centrées)

For a series of size $N$ and period $p$:

- **If $p$ is odd ($p = 2k+1$):**
$$m_{p,t} = \frac{1}{p} \sum_{i=-k}^{k} X_{t+i} = \frac{X_{t-k} + \dots + X_t + \dots + X_{t+k}}{p}$$

- **If $p$ is even ($p = 2k$):**
$$m_{p,t} = \frac{1}{p} \left( \frac{X_{t-k}}{2} + \sum_{i=-k+1}^{k-1} X_{t+i} + \frac{X_{t+k}}{2} \right) = \frac{\frac{X_{t-k}}{2} + \dots + X_t + \dots + \frac{X_{t+k}}{2}}{p}$$

##### Parametric: Trend Line (Droite de tendance)

If the moving average reveals a linear trend, the regression line $y = \beta_1 x + \beta_0$ is calculated:
$$\beta_1 = \frac{\text{cov}(m_{p,t}, t)}{\text{var}(t)}; \quad \beta_0 = \bar{m}_{p,t} - \beta_1 \bar{t}$$

#### 4. Seasonality and Seasonally Adjusted Series (CVS)

This section details the calculation of the Seasonally Adjusted Series (CVS - Série corrigée des variations saisonnières) and Residuals.

##### A. Additive Model (Modèle additif)

- **Trend estimate:** $\hat{m}_t$ (via moving averages or regression).
- **Raw seasonal coefficients:** $\hat{s}_j$ calculated as the arithmetic mean of $(X_t - \hat{m}_t)$ for each period $j$.
- **Normalised seasonal coefficients:** $s_j^* = \hat{s}_j - \bar{s}$, where $\bar{s} = \frac{1}{p} \sum_{i=1}^p \hat{s}_i$.
- *Property:* $\sum s_j^* = 0$.
- **Seasonally Adjusted Series (CVS):**
$$X_t^* = X_t - s_t^*$$
- **Additive Residuals:**
$$e_t = X_t^* - \hat{m}_t = X_t - \hat{m}_t - s_t^*$$

##### B. Multiplicative Model (Modèle multiplicatif)

- **Trend estimate:** $\hat{m}_t$.
- **Raw seasonal coefficients:** $\hat{s}_j$ calculated as the arithmetic mean of $\left(\frac{X_t}{\hat{m}_t}\right)$ for each period $j$.
- **Normalised seasonal coefficients:** $s_j^* = \frac{\hat{s}_j}{\bar{s}}$, where $\bar{s} = \frac{1}{p} \sum_{i=1}^p \hat{s}_i$.
- *Property:* Mean of $s_j^* = 1$.
- **Seasonally Adjusted Series (CVS):**
$$X_t^* = \frac{X_t}{s_t^*}$$
- **Multiplicative Residuals:**
$$e_t = \frac{X_t^*}{\hat{m}_t} = \frac{X_t}{\hat{m}_t \times s_t^*}$$

#### 5. Autocovariance and ACF (Indices de dépendance)

These metrics identify temporal dependence and stationarity (stationnarité).

- **Autocovariance function:**
$$\gamma(k) = \mathbb{E}\left[(X_t - \mu)(X_{t+k} - \mu)\right]$$
Estimator: $\hat{\gamma}(k) = \frac{1}{N} \sum_{t=1}^{N-k} (X_t - \bar{X})(X_{t+k} - \bar{X})$

- **Autocorrelation Function (ACF):**
$$\rho(k) = \frac{\gamma(k)}{\gamma(0)}$$
Estimator: $\hat{\rho}(k) = \frac{\hat{\gamma}(k)}{\hat{\gamma}(0)}$

- **Properties:**
  - $\rho(0) = 1$.
  - Symmetry: $\rho(k) = \rho(-k)$.
  - Bounds: $-1 \leq \rho(k) \leq 1$.
- **White Noise (Bruit blanc):** $\rho(k) \approx 0$ for all $k \neq 0$.

#### 6. Statistical Tests (Tests sur les séries)

| Test | Null Hypothesis ($H_0$) | Alternative Hypothesis ($H_1$) | Decision Rule |
|---|---|---|---|
| Augmented Dickey-Fuller (ADF) | Series is non-stationary. | Series is stationary. | Reject $H_0$ if $p\text{-value} < 0.05$. |
| Mann-Kendall | No trend exists. | Monotonic trend exists. | If $p\text{-value} < 0.05$ and $\tau > 0$, trend is increasing. |
| Pettitt | No change in central trend. | Presence of a rupture point. | Identifies date of shift in mean. |
| KPSS | Series is stationary. | Series is non-stationary. | Reject $H_0$ if $p\text{-value} < 0.05$. |

#### 7. Forecasting Methods (Prévision)

##### Parametric Modelling

A forecast $\hat{x}_{T+h}$ for horizon $h$ is built by combining trend and seasonality:

- **Additive:** $\hat{x}_{T+h} = \hat{m}_{T+h} + \hat{s}_{T+h}$
- **Multiplicative:** $\hat{x}_{T+h} = \hat{m}_{T+h} \times \hat{s}_{T+h}$, where $\hat{m}_{T+h} = a(T+h) + b$.

##### Exponential Smoothing (Lissage exponentiel)

1. **Simple Exponential Smoothing (LES/SES):** For series with no trend or seasonality.
   Update: $\hat{x}_T(h) = \beta x_T + (1 - \beta) \hat{x}_{T-1}(1)$, where $\beta$ is the smoothing constant.

2. **Holt's Double Exponential Smoothing (LED):** For series with a local linear trend but no seasonality.
   $$\hat{a}_T = \hat{a}_{T-1} + (1-\beta)^2 (x_T - \hat{x}_{T-1}(1))$$

3. **Holt-Winters (HW):** For series with trend and seasonality.
   **Additive Update Formulas:**
   - Level: $\hat{a}_T = \beta(x_T - \hat{s}_{T-p}) + (1-\beta)(\hat{a}_{T-1} + \hat{b}_{T-1})$
   - Trend: $\hat{b}_T = \alpha(\hat{a}_T - \hat{a}_{T-1}) + (1-\alpha)\hat{b}_{T-1}$
   - Seasonality: $\hat{s}_T = \gamma(x_T - \hat{a}_T) + (1-\gamma)\hat{s}_{T-p}$

#### 8. Validation Metrics (Indicateurs d'erreur)

To evaluate model quality, calculate the global magnitude of residuals $e_t = x_t - \hat{x}_t(1)$:

| Metric | Formula | Terminology |
|---|---|---|
| **Mean Error** | $EM = \frac{1}{N} \sum_{i=1}^N (x_{i+1} - \hat{x}_i(1))$ | Erreur Moyenne |
| **Mean Absolute Error** | $EAM = \frac{1}{N} \sum_{i=1}^N \left\lvert x_{i+1} - \hat{x}_i(1) \right\rvert$ | Erreur Absolue Moyenne |
| **Mean Squared Error** | $EQM = \frac{1}{N} \sum_{i=1}^N (x_{i+1} - \hat{x}_i(1))^2$ | Erreur Quadratique Moyenne |

*Note: For a well-adjusted model, $EM$ should be close to 0 and the $EQM$ should be minimised.*
