#!/usr/bin/env python3
"""
SAE 3.03 — Option A : ventes mensuelles de champagne Perrin Frères.

Ce script produit une analyse complète et reproductible :
- import et contrôle qualité ;
- exploration descriptive + graphiques ;
- ACF/PACF si statsmodels est disponible ;
- tests de tendance/rupture/stationnarité ;
- choix additif vs multiplicatif ;
- décomposition classique par moyenne mobile centrée ;
- validation des résidus ;
- prévision par décomposition paramétrique et Holt-Winters.

Dépendances minimales : pandas, numpy, matplotlib.
Dépendances optionnelles : statsmodels pour ADF, KPSS, PACF et SARIMA.

Exécution :
    python3 scripts/analyse_champagne.py \
        --data data/monthly_champagne_sales.csv \
        --out outputs/champagne
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

try:
    from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
    from statsmodels.tsa.arima.model import ARIMA
    from statsmodels.tsa.stattools import adfuller, kpss, pacf as sm_pacf

    HAS_STATSMODELS = True
except Exception:
    HAS_STATSMODELS = False


MONTH_NAMES_FR = {
    1: "Janvier",
    2: "Février",
    3: "Mars",
    4: "Avril",
    5: "Mai",
    6: "Juin",
    7: "Juillet",
    8: "Août",
    9: "Septembre",
    10: "Octobre",
    11: "Novembre",
    12: "Décembre",
}


@dataclass
class ForecastResult:
    name: str
    forecast: pd.Series
    metrics: dict[str, float]


def normal_cdf(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def two_sided_normal_pvalue(z: float) -> float:
    return 2.0 * (1.0 - normal_cdf(abs(z)))


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_series(path: Path) -> pd.Series:
    df = pd.read_csv(path)
    expected = {"Month", "Sales"}
    if not expected.issubset(df.columns):
        raise ValueError(f"Le fichier doit contenir les colonnes {expected}, reçu {list(df.columns)}")

    df = df.copy()
    df["Month"] = pd.to_datetime(df["Month"], format="%Y-%m")
    df = df.sort_values("Month")
    series = pd.Series(df["Sales"].astype(float).to_numpy(), index=df["Month"], name="Sales")
    series = series.asfreq("MS")
    return series


def centered_moving_average(series: pd.Series, period: int = 12) -> pd.Series:
    """Moyenne mobile centrée, formule du cours pour période paire p=2k."""
    x = series.to_numpy(dtype=float)
    n = len(x)
    k = period // 2
    values = np.full(n, np.nan)
    for i in range(k, n - k):
        values[i] = (0.5 * x[i - k] + x[i - k + 1 : i + k].sum() + 0.5 * x[i + k]) / period
    return pd.Series(values, index=series.index, name=f"MMC_{period}")


def fit_linear_trend(values: pd.Series) -> tuple[float, float, pd.Series]:
    mask = values.notna()
    t = np.arange(1, len(values) + 1, dtype=float)
    slope, intercept = np.polyfit(t[mask.to_numpy()], values[mask].to_numpy(), deg=1)
    fitted = pd.Series(intercept + slope * t, index=values.index, name="trend_linear")
    return slope, intercept, fitted


def seasonal_coefficients(
    series: pd.Series, trend: pd.Series, model: str, period: int = 12
) -> pd.DataFrame:
    df = pd.DataFrame({"observed": series, "trend": trend}).dropna()
    df["month"] = df.index.month
    if model == "additive":
        df["raw"] = df["observed"] - df["trend"]
        raw = df.groupby("month")["raw"].mean().reindex(range(1, period + 1))
        normalized = raw - raw.mean()
        property_value = normalized.sum()
    elif model == "multiplicative":
        df["raw"] = df["observed"] / df["trend"]
        raw = df.groupby("month")["raw"].mean().reindex(range(1, period + 1))
        normalized = raw / raw.mean()
        property_value = normalized.mean()
    else:
        raise ValueError("model doit valoir 'additive' ou 'multiplicative'")

    out = pd.DataFrame(
        {
            "month": range(1, period + 1),
            "month_name": [MONTH_NAMES_FR[i] for i in range(1, period + 1)],
            "raw_coefficient": raw.to_numpy(),
            "normalized_coefficient": normalized.to_numpy(),
        }
    )
    out.attrs["normalization_property"] = property_value
    return out


def apply_decomposition(series: pd.Series, trend: pd.Series, coeffs: pd.DataFrame, model: str) -> pd.DataFrame:
    seasonal_map = dict(zip(coeffs["month"], coeffs["normalized_coefficient"]))
    seasonal = pd.Series([seasonal_map[d.month] for d in series.index], index=series.index, name="seasonal")
    if model == "additive":
        cvs = series - seasonal
        residual = series - trend - seasonal
    else:
        cvs = series / seasonal
        residual = series / (trend * seasonal)
    return pd.DataFrame(
        {
            "observed": series,
            "trend": trend,
            "seasonal": seasonal,
            "cvs": cvs,
            "residual": residual,
        }
    )


def buys_ballot(series: pd.Series) -> dict[str, float | str]:
    df = pd.DataFrame({"sales": series})
    df["year"] = df.index.year
    by_year = df.groupby("year")["sales"].agg(["mean", "std", "count"])
    by_year = by_year[by_year["count"] >= 9].copy()
    slope, intercept = np.polyfit(by_year["mean"], by_year["std"], deg=1)
    corr = float(np.corrcoef(by_year["mean"], by_year["std"])[0, 1])
    decision = "multiplicatif" if abs(slope) > 0.10 and corr > 0.3 else "additif"
    return {
        "slope_std_vs_mean": float(slope),
        "intercept": float(intercept),
        "correlation": corr,
        "decision_indicative": decision,
        "years_used": int(len(by_year)),
    }


def acf_values(series: pd.Series, max_lag: int = 36) -> pd.DataFrame:
    x = series.to_numpy(dtype=float)
    x = x - x.mean()
    denom = np.sum(x * x)
    rows = []
    for lag in range(max_lag + 1):
        num = np.sum(x[: len(x) - lag] * x[lag:]) if lag else denom
        rows.append({"lag": lag, "acf": float(num / denom)})
    return pd.DataFrame(rows)


def mann_kendall_test(series: pd.Series) -> dict[str, float | str]:
    x = series.dropna().to_numpy(dtype=float)
    n = len(x)
    s = 0
    for i in range(n - 1):
        s += int(np.sign(x[i + 1 :] - x[i]).sum())

    _, counts = np.unique(x, return_counts=True)
    tie_term = sum(c * (c - 1) * (2 * c + 5) for c in counts if c > 1)
    var_s = (n * (n - 1) * (2 * n + 5) - tie_term) / 18
    if s > 0:
        z = (s - 1) / math.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / math.sqrt(var_s)
    else:
        z = 0.0
    p = two_sided_normal_pvalue(z)
    tau = s / (0.5 * n * (n - 1))
    decision = "tendance croissante significative" if p < 0.05 and tau > 0 else "pas de tendance croissante significative"
    return {"S": float(s), "tau": float(tau), "z": float(z), "p_value": float(p), "decision": decision}


def pettitt_test(series: pd.Series) -> dict[str, float | str]:
    x = series.dropna()
    n = len(x)
    ranks = x.rank(method="average").to_numpy(dtype=float)
    u = np.array([2 * ranks[: t + 1].sum() - (t + 1) * (n + 1) for t in range(n)])
    k_idx = int(np.argmax(np.abs(u)))
    k_stat = float(abs(u[k_idx]))
    p = float(2 * math.exp((-6 * k_stat**2) / (n**3 + n**2)))
    p = min(1.0, p)
    decision = "rupture probable" if p < 0.05 else "pas de rupture significative"
    return {
        "K": k_stat,
        "change_point_index": k_idx + 1,
        "change_point_date": str(x.index[k_idx].date()),
        "p_value": p,
        "decision": decision,
    }


def stationarity_tests(series: pd.Series) -> dict[str, dict[str, float | str]]:
    tests: dict[str, dict[str, float | str]] = {}
    if HAS_STATSMODELS:
        adf = adfuller(series.dropna(), autolag="AIC")
        tests["ADF"] = {
            "statistic": float(adf[0]),
            "p_value": float(adf[1]),
            "lags_used": int(adf[2]),
            "decision": "stationnaire" if adf[1] < 0.05 else "non-stationnaire",
        }
        try:
            kpss_res = kpss(series.dropna(), regression="c", nlags="auto")
            tests["KPSS"] = {
                "statistic": float(kpss_res[0]),
                "p_value": float(kpss_res[1]),
                "lags_used": int(kpss_res[2]),
                "decision": "non-stationnaire" if kpss_res[1] < 0.05 else "stationnaire",
            }
        except Exception as exc:
            tests["KPSS"] = {"status": f"non calculé ({exc})"}
    else:
        # Régression Dickey-Fuller simplifiée, sans p-value fiable. Le script reste utilisable
        # en salle machine sans installation de statsmodels, mais le rapport signale la limite.
        y = series.dropna().to_numpy(dtype=float)
        dy = np.diff(y)
        y_lag = y[:-1]
        x = np.column_stack([np.ones_like(y_lag), y_lag])
        beta = np.linalg.lstsq(x, dy, rcond=None)[0]
        residuals = dy - x @ beta
        sigma2 = (residuals @ residuals) / (len(dy) - x.shape[1])
        cov = sigma2 * np.linalg.inv(x.T @ x)
        t_stat = beta[1] / math.sqrt(cov[1, 1])
        tests["ADF"] = {
            "statistic_simplified": float(t_stat),
            "p_value": "non disponible sans statsmodels",
            "decision": "à interpréter avec statsmodels conseillé",
        }
        tests["KPSS"] = {"status": "non disponible sans statsmodels"}
    return tests


def error_metrics(actual: pd.Series, pred: pd.Series) -> dict[str, float]:
    aligned = pd.concat([actual.rename("actual"), pred.rename("pred")], axis=1).dropna()
    err = aligned["actual"] - aligned["pred"]
    return {
        "EM": float(err.mean()),
        "EAM_MAE": float(err.abs().mean()),
        "EQM_MSE": float((err**2).mean()),
        "RMSE": float(math.sqrt((err**2).mean())),
        "MAPE_percent": float((err.abs() / aligned["actual"]).mean() * 100),
    }


def parametric_forecast(train: pd.Series, horizon_index: pd.DatetimeIndex, model: str) -> ForecastResult:
    cma = centered_moving_average(train, 12)
    slope, intercept, trend = fit_linear_trend(cma)
    coeffs = seasonal_coefficients(train, trend, model)
    seasonal_map = dict(zip(coeffs["month"], coeffs["normalized_coefficient"]))

    start_t = len(train) + 1
    t_future = np.arange(start_t, start_t + len(horizon_index), dtype=float)
    trend_future = pd.Series(intercept + slope * t_future, index=horizon_index)
    seasonal_future = pd.Series([seasonal_map[d.month] for d in horizon_index], index=horizon_index)
    if model == "additive":
        forecast = trend_future + seasonal_future
        name = "Décomposition paramétrique additive"
    else:
        forecast = trend_future * seasonal_future
        name = "Décomposition paramétrique multiplicative"
    return ForecastResult(name=name, forecast=forecast.rename(name), metrics={})


def init_hw_components(x: np.ndarray, period: int, model: str) -> tuple[float, float, list[float]]:
    first = x[:period]
    second = x[period : 2 * period] if len(x) >= 2 * period else x[:period]
    level = float(np.mean(first))
    trend = float((np.mean(second) - np.mean(first)) / period)
    if model == "additive":
        seasonals = list(first - level)
    else:
        seasonals = list(first / level)
    return level, trend, [float(s) for s in seasonals]


def holt_winters_forecast(
    train: pd.Series,
    horizon_index: pd.DatetimeIndex,
    model: str = "multiplicative",
    period: int = 12,
) -> ForecastResult:
    x = train.to_numpy(dtype=float)
    grid = [0.2, 0.4, 0.6, 0.8]
    best: tuple[float, tuple[float, float, float], pd.Series, list[float], float, float] | None = None

    for alpha in grid:  # niveau
        for beta in grid:  # tendance
            for gamma in grid:  # saisonnalité
                level, trend, seasonals = init_hw_components(x, period, model)
                fitted = np.full(len(x), np.nan)
                sse = 0.0
                count = 0
                valid = True
                for t in range(period, len(x)):
                    s_old = seasonals[t - period]
                    if model == "additive":
                        pred = level + trend + s_old
                        new_level = alpha * (x[t] - s_old) + (1 - alpha) * (level + trend)
                        new_trend = beta * (new_level - level) + (1 - beta) * trend
                        new_season = gamma * (x[t] - new_level) + (1 - gamma) * s_old
                    else:
                        pred = (level + trend) * s_old
                        if s_old <= 0 or level <= 0:
                            valid = False
                            break
                        new_level = alpha * (x[t] / s_old) + (1 - alpha) * (level + trend)
                        new_trend = beta * (new_level - level) + (1 - beta) * trend
                        new_season = gamma * (x[t] / max(new_level, 1e-9)) + (1 - gamma) * s_old
                    fitted[t] = pred
                    sse += float((x[t] - pred) ** 2)
                    count += 1
                    level, trend = float(new_level), float(new_trend)
                    seasonals.append(float(new_season))
                if not valid or count == 0:
                    continue
                mse = sse / count
                fitted_series = pd.Series(fitted, index=train.index)
                candidate = (mse, (alpha, beta, gamma), fitted_series, seasonals, level, trend)
                if best is None or mse < best[0]:
                    best = candidate

    if best is None:
        raise RuntimeError("Impossible d'ajuster Holt-Winters")

    _, params, _, seasonals, level, trend = best
    forecasts = []
    n = len(x)
    for m in range(1, len(horizon_index) + 1):
        seasonal = seasonals[n + m - period - 1]
        if model == "additive":
            forecasts.append(level + m * trend + seasonal)
        else:
            forecasts.append((level + m * trend) * seasonal)
    forecast = pd.Series(forecasts, index=horizon_index, name=f"Holt-Winters {model}")
    return ForecastResult(
        name=f"Holt-Winters {model} alpha={params[0]}, beta={params[1]}, gamma={params[2]}",
        forecast=forecast,
        metrics={},
    )


def sarima_baseline(train: pd.Series, horizon_index: pd.DatetimeIndex) -> ForecastResult | None:
    if not HAS_STATSMODELS:
        return None
    try:
        # Modèle volontairement simple et pédagogique : différenciation simple + saisonnière,
        # saisonnalité mensuelle via SARIMAX si disponible n'est pas utilisé ici pour rester rapide.
        # Cette base ARIMA sert surtout de repère exploratoire après lecture ACF/PACF.
        model = ARIMA(train, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
        fitted = model.fit()
        forecast = fitted.forecast(steps=len(horizon_index))
        forecast.index = horizon_index
        return ForecastResult(name="SARIMA(1,1,1)(1,1,1)[12] exploratoire", forecast=forecast, metrics={})
    except Exception:
        return None


def save_plots(series: pd.Series, decomp: pd.DataFrame, acf_df: pd.DataFrame, forecasts: pd.DataFrame, out_dir: Path) -> None:
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(11, 5))
    series.plot(ax=ax, marker="o", linewidth=1.5)
    ax.set_title("Ventes mensuelles de champagne Perrin Frères")
    ax.set_ylabel("Ventes")
    fig.tight_layout()
    fig.savefig(out_dir / "01_serie_temporelle.png", dpi=160)
    plt.close(fig)

    profile = pd.DataFrame({"sales": series})
    profile["year"] = profile.index.year
    profile["month"] = profile.index.month
    pivot = profile.pivot(index="month", columns="year", values="sales")
    fig, ax = plt.subplots(figsize=(10, 5))
    pivot.plot(ax=ax, marker="o")
    ax.set_title("Profils saisonniers superposés")
    ax.set_xlabel("Mois")
    ax.set_ylabel("Ventes")
    ax.set_xticks(range(1, 13))
    fig.tight_layout()
    fig.savefig(out_dir / "02_profils_saisonniers.png", dpi=160)
    plt.close(fig)

    fig, axes = plt.subplots(4, 1, figsize=(11, 9), sharex=True)
    decomp["observed"].plot(ax=axes[0], title="Observé")
    decomp["trend"].plot(ax=axes[1], title="Tendance linéaire estimée")
    decomp["seasonal"].plot(ax=axes[2], title="Composante saisonnière multiplicative")
    decomp["residual"].plot(ax=axes[3], title="Résidu multiplicatif")
    fig.tight_layout()
    fig.savefig(out_dir / "03_decomposition_multiplicative.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10, 4))
    decomp["residual"].dropna().plot(ax=ax, marker="o", linewidth=1)
    ax.axhline(1, color="black", linestyle="--", linewidth=1)
    ax.set_title("Résidus multiplicatifs : cible proche de 1")
    fig.tight_layout()
    fig.savefig(out_dir / "04_residus.png", dpi=160)
    plt.close(fig)

    if HAS_STATSMODELS:
        fig, axes = plt.subplots(1, 2, figsize=(11, 4))
        plot_acf(series.dropna(), lags=min(36, len(series) // 2), ax=axes[0])
        plot_pacf(series.dropna(), lags=min(36, len(series) // 2 - 1), ax=axes[1], method="ywm")
        axes[0].set_title("ACF")
        axes[1].set_title("PACF")
    else:
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(acf_df["lag"], acf_df["acf"])
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_title("ACF empirique (PACF disponible avec statsmodels)")
        ax.set_xlabel("Lag")
    fig.tight_layout()
    fig.savefig(out_dir / "05_acf_pacf.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(11, 5))
    forecasts.plot(ax=ax, marker="o")
    ax.set_title("Prévisions comparées sur le jeu de test")
    ax.set_ylabel("Ventes")
    fig.tight_layout()
    fig.savefig(out_dir / "06_previsions_test.png", dpi=160)
    plt.close(fig)


def dataframe_to_markdown(df: pd.DataFrame, max_rows: int | None = None) -> str:
    """Convertit un tableau en Markdown sans dépendre du paquet optionnel tabulate."""
    if max_rows is not None:
        df = df.head(max_rows)
    if df.empty:
        return "_(tableau vide)_"

    rendered = df.copy()
    rendered.columns = [str(col) for col in rendered.columns]
    for col in rendered.columns:
        rendered[col] = rendered[col].map(
            lambda value: f"{value:.4f}" if isinstance(value, (float, np.floating)) else str(value)
        )

    headers = list(rendered.columns)
    rows = rendered.values.tolist()
    widths = [len(header) for header in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(cell))

    def fmt_row(values: Iterable[str]) -> str:
        return "| " + " | ".join(str(value).ljust(widths[idx]) for idx, value in enumerate(values)) + " |"

    lines = [fmt_row(headers), "| " + " | ".join("-" * width for width in widths) + " |"]
    lines.extend(fmt_row(row) for row in rows)
    return "\n".join(lines)


def write_report(
    out_dir: Path,
    series: pd.Series,
    summary: dict,
    coeffs_mult: pd.DataFrame,
    tests: dict,
    metrics_df: pd.DataFrame,
    forecast_table: pd.DataFrame,
) -> None:
    report = f"""# Rapport d'analyse — ventes mensuelles de champagne Perrin Frères

## 1. Management de projet

Proposition de découpage des 10 heures demandées dans l'énoncé :

| Tranche | Travail prévu | Livrable intermédiaire |
|---|---|---|
| 0h–2h | Récupération du dataset, lecture de l'énoncé, Gantt, rôles | Données importées + plan de travail |
| 2h–4h | Recherche bibliographique et contextualisation | Source Kaggle + contexte économique |
| 4h–6h | Exploration, visualisations, ACF/PACF | Graphiques et statistiques descriptives |
| 6h–8h | Tests, choix additif/multiplicatif, décomposition | Coefficients saisonniers + CVS |
| 8h–10h | Prévisions, comparaison des erreurs, rédaction | Rapport final + code en annexe |

## 2. Recherche bibliographique

La série correspond au jeu **Monthly Champagne Sales** diffusé sur Kaggle : ventes mensuelles de champagne Perrin Frères. Elle est fréquemment utilisée comme série pédagogique pour illustrer une tendance croissante combinée à une saisonnalité annuelle forte, notamment un pic de fin d'année. Pour un rapport étudiant, on peut compléter cette source par une courte recherche sur la saisonnalité commerciale des vins effervescents : achats plus élevés lors des fêtes de fin d'année, effet des stocks et événements commerciaux.

## 3. Présentation et contextualisation des données

- Période observée : **{series.index.min().strftime('%Y-%m')} à {series.index.max().strftime('%Y-%m')}**.
- Nombre d'observations : **{len(series)} mois**.
- Fréquence : mensuelle.
- Variable : ventes mensuelles, unité exacte non documentée dans le fichier Kaggle.
- Valeurs manquantes : **{int(series.isna().sum())}**.

Le dataset est adapté à la SAE car il contient plus de trois cycles saisonniers annuels et une saisonnalité visible : les ventes augmentent fortement en novembre-décembre.

## 4. Exploration des données

Statistiques descriptives principales :

| Indicateur | Valeur |
|---|---:|
| Moyenne | {summary['mean']:.2f} |
| Écart-type | {summary['std']:.2f} |
| Minimum | {summary['min']:.2f} |
| Médiane | {summary['median']:.2f} |
| Maximum | {summary['max']:.2f} |

Graphiques générés :

- `01_serie_temporelle.png` : série brute ;
- `02_profils_saisonniers.png` : profils annuels superposés ;
- `05_acf_pacf.png` : ACF/PACF si `statsmodels` est disponible.

La série présente une hausse globale du niveau moyen et une saisonnalité annuelle très marquée. Les profils saisonniers montrent un pic récurrent en fin d'année, surtout en novembre et décembre.

## 5. Tests statistiques

```json
{json.dumps(tests, ensure_ascii=False, indent=2)}
```

Interprétation attendue :

- **Mann-Kendall** vérifie la présence d'une tendance monotone. Une p-value inférieure à 5 % avec un tau positif indique une tendance croissante.
- **Pettitt** cherche une rupture de niveau central. Si une rupture apparaît, elle doit être commentée comme un changement de régime possible, pas comme une simple saisonnalité.
- **ADF/KPSS** nécessitent `statsmodels` pour obtenir les p-values de référence. Sans cette bibliothèque, le script produit une indication mais recommande de relancer avec `pip install statsmodels`.

## 6. Choix du modèle et décomposition

Les trois arguments pédagogiques vont plutôt vers un modèle **multiplicatif** :

1. la méthode de la bande suggère une amplitude saisonnière plus grande quand le niveau de ventes augmente ;
2. les profils saisonniers accentuent le pic de fin d'année ;
3. Buys-Ballot estime une relation entre moyenne annuelle et écart-type annuel.

Les coefficients saisonniers multiplicatifs normalisés sont :

{dataframe_to_markdown(coeffs_mult[['month_name', 'normalized_coefficient']])}

La propriété de normalisation est respectée lorsque la moyenne des coefficients vaut environ 1. La CVS est calculée par :

$X_t^* = X_t / s_t^*$

et le résidu multiplicatif par :

$e_t = X_t /(\\hat m_t \\times s_t^*)$.

## 7. Validation du modèle

Les fichiers `03_decomposition_multiplicative.png` et `04_residus.png` permettent de vérifier si les résidus sont centrés autour de 1. Les plus grands écarts apparaissent typiquement sur les mois exceptionnels, car un modèle tendance + saisonnalité ne capture pas les promotions, les ruptures commerciales ou les chocs économiques.

## 8. Prévision

Les 12 dernières observations sont réservées comme jeu de test. Les modèles comparés sont :

- décomposition paramétrique additive ;
- décomposition paramétrique multiplicative ;
- Holt-Winters additif ;
- Holt-Winters multiplicatif ;
- SARIMA exploratoire si `statsmodels` est installé.

### Erreurs sur le jeu de test

{dataframe_to_markdown(metrics_df)}

### Prévisions et observations réelles

{dataframe_to_markdown(forecast_table.reset_index().rename(columns={'Month': 'date'}), max_rows=12)}

## Conclusion

La série Champagne est un bon choix pour la SAE 3.03 : elle est courte, propre, mensuelle, et met clairement en évidence les étapes centrales du cours. Le modèle multiplicatif est généralement plus cohérent que le modèle additif, car l'amplitude saisonnière augmente avec le niveau de la série. Pour la prévision, le meilleur modèle doit être choisi sur les erreurs du jeu de test, pas seulement sur l'apparence graphique. Les limites principales sont la taille modérée de la série et l'absence de variables explicatives externes.

## Annexes — fichiers produits

- `tables/descriptive_statistics.csv`
- `tables/tests_statistiques.json`
- `tables/coefficients_saisonniers_additifs.csv`
- `tables/coefficients_saisonniers_multiplicatifs.csv`
- `tables/decomposition_multiplicative.csv`
- `tables/previsions_test.csv`
- `tables/metriques_prevision.csv`
- `figures/*.png`
"""
    (out_dir / "rapport_champagne.md").write_text(report, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyse SAE 3.03 — ventes mensuelles de champagne")
    parser.add_argument("--data", type=Path, default=Path("data/monthly_champagne_sales.csv"))
    parser.add_argument("--out", type=Path, default=Path("outputs/champagne"))
    parser.add_argument("--period", type=int, default=12)
    parser.add_argument("--test-size", type=int, default=12)
    args = parser.parse_args()

    out_dir = args.out
    figures_dir = out_dir / "figures"
    tables_dir = out_dir / "tables"
    ensure_dir(figures_dir)
    ensure_dir(tables_dir)

    series = load_series(args.data)
    if series.isna().any():
        series = series.interpolate(method="time")

    descriptive = series.describe().rename("Sales").to_frame()
    descriptive.to_csv(tables_dir / "descriptive_statistics.csv")

    annual = pd.DataFrame({"sales": series})
    annual["year"] = annual.index.year
    annual_summary = annual.groupby("year")["sales"].agg(["count", "mean", "std", "min", "max"])
    annual_summary.to_csv(tables_dir / "annual_statistics.csv")

    cma = centered_moving_average(series, args.period)
    slope, intercept, trend = fit_linear_trend(cma)
    pd.DataFrame({"observed": series, "centered_moving_average": cma, "linear_trend": trend}).to_csv(
        tables_dir / "trend_estimation.csv", index_label="Month"
    )

    coeffs_add = seasonal_coefficients(series, trend, "additive", args.period)
    coeffs_mult = seasonal_coefficients(series, trend, "multiplicative", args.period)
    coeffs_add.to_csv(tables_dir / "coefficients_saisonniers_additifs.csv", index=False)
    coeffs_mult.to_csv(tables_dir / "coefficients_saisonniers_multiplicatifs.csv", index=False)

    decomp_mult = apply_decomposition(series, trend, coeffs_mult, "multiplicative")
    decomp_mult.to_csv(tables_dir / "decomposition_multiplicative.csv", index_label="Month")

    acf_df = acf_values(series, max_lag=36)
    acf_df.to_csv(tables_dir / "acf.csv", index=False)
    if HAS_STATSMODELS:
        pacf_vals = sm_pacf(series.dropna(), nlags=36, method="ywm")
        pd.DataFrame({"lag": range(len(pacf_vals)), "pacf": pacf_vals}).to_csv(tables_dir / "pacf.csv", index=False)

    tests = {
        "mann_kendall": mann_kendall_test(series),
        "pettitt": pettitt_test(series),
        "stationarity": stationarity_tests(series),
        "buys_ballot": buys_ballot(series),
        "linear_trend": {"slope_per_month": float(slope), "intercept": float(intercept)},
        "statsmodels_available": HAS_STATSMODELS,
    }
    (tables_dir / "tests_statistiques.json").write_text(json.dumps(tests, ensure_ascii=False, indent=2), encoding="utf-8")

    test_size = args.test_size
    train = series.iloc[:-test_size]
    test = series.iloc[-test_size:]
    horizon_index = test.index

    candidates: list[ForecastResult] = [
        parametric_forecast(train, horizon_index, "additive"),
        parametric_forecast(train, horizon_index, "multiplicative"),
        holt_winters_forecast(train, horizon_index, "additive", args.period),
        holt_winters_forecast(train, horizon_index, "multiplicative", args.period),
    ]
    sarima = sarima_baseline(train, horizon_index)
    if sarima is not None:
        candidates.append(sarima)

    forecast_df = pd.DataFrame({"observed": test})
    metrics_rows = []
    for candidate in candidates:
        forecast_df[candidate.name] = candidate.forecast
        metrics = error_metrics(test, candidate.forecast)
        metrics_rows.append({"model": candidate.name, **metrics})
    metrics_df = pd.DataFrame(metrics_rows).sort_values("RMSE")
    forecast_df.to_csv(tables_dir / "previsions_test.csv", index_label="Month")
    metrics_df.to_csv(tables_dir / "metriques_prevision.csv", index=False)

    save_plots(series, decomp_mult, acf_df, forecast_df, figures_dir)

    summary = {
        "mean": float(series.mean()),
        "std": float(series.std()),
        "min": float(series.min()),
        "median": float(series.median()),
        "max": float(series.max()),
    }
    write_report(out_dir, series, summary, coeffs_mult, tests, metrics_df, forecast_df)

    print(f"Analyse terminée. Rapport : {out_dir / 'rapport_champagne.md'}")
    print(f"Graphiques : {figures_dir}")
    print(f"Tableaux : {tables_dir}")
    print("statsmodels disponible :", HAS_STATSMODELS)


if __name__ == "__main__":
    main()
