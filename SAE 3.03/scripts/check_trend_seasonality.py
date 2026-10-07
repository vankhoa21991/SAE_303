#!/usr/bin/env python3
"""
SAE 3.03 — Vérifie quantitativement, pour chaque dataset déjà téléchargé/diagnostiqué
par download_and_plot_datasets.py, s'il présente une TENDANCE et/ou une SAISONNALITÉ
suffisamment nettes pour être exploitable dans le cadre de la SAE (décomposition +
prévision). Réutilise la détection date/valeur déjà construite (évite de redétecter
une colonne différente à chaque script).

Pas de dépendance à scipy (cassé dans cet environnement — conflit ABI numpy/scipy) :
le test de tendance (Mann-Kendall) et la force de saisonnalité (eta²) sont calculés
à la main avec numpy/pandas uniquement.

Utilisation :
    python3 scripts/check_trend_seasonality.py
    python3 scripts/check_trend_seasonality.py --only A,D,K

Sortie :
    scripts/plots/_trend_seasonality.md
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from download_and_plot_datasets import (  # noqa: E402
    DEFAULT_DATA_DIR,
    DEFAULT_MD,
    parse_dataset_guide,
    pick_files_to_inspect,
    try_concat_split_files,
    read_any_table,
    try_wide_date_columns,
    detect_date_spec,
    detect_value_columns,
    build_series,
)


def mann_kendall(series: pd.Series) -> dict:
    """Test de Mann-Kendall (tendance monotone), implémentation manuelle sans scipy."""
    x = series.dropna().to_numpy(dtype=float)
    n = len(x)
    if n < 8:
        return {"n": n, "S": None, "tau": None, "z": None, "p_value": None, "decision": "trop peu de points"}

    s = 0
    for i in range(n - 1):
        s += int((x[i + 1:] > x[i]).sum()) - int((x[i + 1:] < x[i]).sum())

    counts = pd.Series(x).value_counts().to_numpy()
    tie_term = sum(c * (c - 1) * (2 * c + 5) for c in counts if c > 1)
    var_s = (n * (n - 1) * (2 * n + 5) - tie_term) / 18
    if var_s <= 0:
        z = 0.0
    elif s > 0:
        z = (s - 1) / math.sqrt(var_s)
    elif s < 0:
        z = (s + 1) / math.sqrt(var_s)
    else:
        z = 0.0

    p_value = 2.0 * (1.0 - 0.5 * (1.0 + math.erf(abs(z) / math.sqrt(2.0))))
    tau = s / (0.5 * n * (n - 1))
    if p_value < 0.05 and tau > 0:
        decision = "tendance croissante"
    elif p_value < 0.05 and tau < 0:
        decision = "tendance décroissante"
    else:
        decision = "pas de tendance significative"
    return {"n": n, "S": s, "tau": tau, "z": z, "p_value": p_value, "decision": decision}


def seasonal_strength(series: pd.Series) -> dict:
    """Force de la saisonnalité mensuelle via eta² = variance inter-mois / variance totale.
    Nécessite au moins 2 cycles annuels complets pour être interprétable."""
    s = series.dropna()
    years_span = (s.index.max() - s.index.min()).days / 365.25 if len(s) > 1 else 0
    by_month = s.groupby(s.index.month)

    if by_month.ngroups < 6:
        # Donnees annuelles (ou quasi) : la saisonnalite mensuelle n'est pas mesurable
        # par construction, quelle que soit la duree couverte en annees.
        return {"eta2": None, "years_span": years_span,
                "decision": "données annuelles : saisonnalité mensuelle non mesurable"}

    if years_span < 1.8 or len(s) < 20:
        return {"eta2": None, "years_span": years_span, "decision": "historique trop court (< ~2 ans)"}

    overall_mean = s.mean()
    total_ss = ((s - overall_mean) ** 2).sum()
    between_ss = sum(len(g) * (g.mean() - overall_mean) ** 2 for _, g in by_month)
    eta2 = float(between_ss / total_ss) if total_ss > 0 else 0.0

    if eta2 >= 0.4:
        decision = "saisonnalité forte"
    elif eta2 >= 0.15:
        decision = "saisonnalité modérée"
    else:
        decision = "saisonnalité faible/absente"
    return {"eta2": eta2, "years_span": years_span, "decision": decision}


def get_primary_series(entry, data_dir: Path) -> tuple[pd.Series, str] | None:
    """Reconstruit la série principale (même logique que download_and_plot_datasets.py :
    essaie la concaténation multi-fichiers en premier, sinon le meilleur fichier seul)."""
    dest_dir = data_dir / entry.slug
    if not dest_dir.exists():
        return None

    candidates: list[tuple[str, pd.DataFrame]] = []
    concat_result = try_concat_split_files(dest_dir)
    if concat_result is not None:
        df, note = concat_result
        candidates.append((note, df))

    for p in pick_files_to_inspect(dest_dir):
        try:
            candidates.append((p.name, read_any_table(p)))
        except Exception:
            continue

    for label, df in candidates:
        if df.empty or df.shape[1] < 2:
            continue
        wide_result = try_wide_date_columns(df)
        if wide_result is not None:
            df, date_spec, value_col = wide_result
        else:
            date_spec = detect_date_spec(df)
            if date_spec is None:
                continue
            value_cols = detect_value_columns(df, date_spec, max_cols=1)
            if not value_cols:
                continue
            value_col = value_cols[0]
        series = build_series(df, date_spec, value_col)
        if not series.empty:
            return series, f"{label} / {value_col}"
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--md", type=Path, default=DEFAULT_MD)
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR)
    parser.add_argument("--only", type=str, default="")
    parser.add_argument("--out", type=Path, default=HERE / "plots" / "_trend_seasonality.md")
    args = parser.parse_args()

    entries = parse_dataset_guide(args.md)
    if args.only:
        wanted = {x.strip().upper() for x in args.only.split(",") if x.strip()}
        entries = [e for e in entries if e.letter in wanted]

    rows = []
    for entry in entries:
        result = get_primary_series(entry, args.data_dir)
        if result is None:
            rows.append({
                "letter": entry.letter, "title": entry.title, "status": "pas de données locales",
                "n": 0, "span": "", "trend": "", "trend_p": "", "season": "", "season_eta2": "",
                "verdict": "⛔ non évalué",
            })
            print(f"[{entry.letter}] {entry.title} ... pas de données locales")
            continue

        series, source_label = result
        mk = mann_kendall(series)
        ss = seasonal_strength(series)

        has_trend = mk["p_value"] is not None and mk["p_value"] < 0.05
        has_season = ss["eta2"] is not None and ss["eta2"] >= 0.15

        if has_trend and has_season:
            verdict = "✅ bon (tendance + saisonnalité)"
        elif has_trend or has_season:
            verdict = "⚠️ partiel (un seul des deux)"
        else:
            verdict = "❌ faible (ni tendance ni saisonnalité nette)"

        trend_str = mk["decision"] if mk["p_value"] is None else f"{mk['decision']} (p={mk['p_value']:.4f})"
        season_str = ss["decision"] if ss["eta2"] is None else f"{ss['decision']} (eta2={ss['eta2']:.2f})"

        rows.append({
            "letter": entry.letter, "title": entry.title, "status": "ok",
            "n": mk["n"], "span": f"{ss['years_span']:.1f} ans" if ss["years_span"] else "",
            "trend": trend_str, "trend_p": mk["p_value"], "season": season_str,
            "season_eta2": ss["eta2"], "verdict": verdict, "source": source_label,
        })
        print(f"[{entry.letter}] {entry.title} ... n={mk['n']}, {mk['decision']}, {ss['decision']} -> {verdict}")

    lines = [
        "# Tendance et saisonnalité — verification quantitative des datasets Kaggle",
        "",
        "*Genere par `scripts/check_trend_seasonality.py`. Tendance = test de Mann-Kendall "
        "(p<0.05 = tendance significative). Saisonnalite = eta2 (part de variance expliquee "
        "par le mois ; >=0.15 = saisonnalite exploitable, >=0.40 = forte). Necessite au moins "
        "~2 ans d'historique pour evaluer la saisonnalite.*",
        "",
        "| Option | N (mois) | Periode | Tendance | Saisonnalite | Verdict |",
        "|---|---:|---|---|---|---|",
    ]
    for r in rows:
        if r["status"] != "ok":
            lines.append(f"| {r['letter']} — {r['title']} | - | - | - | - | {r['verdict']} |")
            continue
        lines.append(
            f"| {r['letter']} — {r['title']} | {r['n']} | {r['span']} | {r['trend']} | "
            f"{r['season']} | {r['verdict']} |"
        )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nRésumé écrit dans {args.out}")


if __name__ == "__main__":
    main()
