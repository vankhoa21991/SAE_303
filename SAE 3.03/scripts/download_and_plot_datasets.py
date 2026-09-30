#!/usr/bin/env python3
"""
SAE 3.03 — Télécharge tous les jeux de données listés dans DATASETS_Kaggle_Projet.md
et produit, pour chacun, un ou plusieurs graphiques de diagnostic (tendance / saisonnalité)
afin d'aider l'enseignant à juger rapidement si une série est exploitable par un binôme.

Ce script est un outil de TRIAGE, pas une analyse finale : la détection de la colonne
date et de la colonne valeur est automatique (heuristique) faute de connaître à l'avance
la structure exacte de chaque fichier Kaggle. Vérifier visuellement chaque graphique.

Prérequis :
    - Le CLI `kaggle` installé et authentifié (~/.kaggle/kaggle.json ou variables
      d'environnement KAGGLE_USERNAME / KAGGLE_KEY). Voir :
      https://github.com/Kaggle/kaggle-cli/blob/main/docs/README.md#authentication
    - pandas, matplotlib

Utilisation :
    python3 scripts/download_and_plot_datasets.py
    python3 scripts/download_and_plot_datasets.py --only A,D,J        # sous-ensemble
    python3 scripts/download_and_plot_datasets.py --no-download       # re-tracer sans retélécharger
    python3 scripts/download_and_plot_datasets.py --list              # liste les options détectées et quitte

Sorties :
    scripts/kaggle_data/<lettre>_<slug>/   — données brutes téléchargées (cache, réutilisé si présent)
    scripts/plots/<lettre>_<slug>.png      — graphique de diagnostic (tendance + profil saisonnier)
    scripts/plots/_summary.md              — tableau récapitulatif (statut, colonnes détectées, etc.)
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
DEFAULT_MD = HERE.parent / "DATASETS_Kaggle_Projet.md"
DEFAULT_DATA_DIR = HERE.parent / "data" / "kaggle_raw"
DEFAULT_PLOTS_DIR = HERE / "plots"

# Réutilise directement les données déjà présentes dans le repo pour éviter un
# téléchargement inutile (et pour que le script produise au moins un résultat
# même sans identifiants Kaggle configurés).
LOCAL_OVERRIDES: dict[str, Path] = {
    "piyushagni5/monthly-sales-of-french-champagne": HERE.parent / "data" / "monthly_champagne_sales.csv",
}

FULL_DATE_NAME_CANDIDATES = [
    "date", "datetime", "ds", "time", "timestamp", "period", "dt", "year_month", "date_time",
    "start", "start_time", "start_date", "ts", "ts_utc", "tbin_utc",
]
YEAR_NAME_CANDIDATES = ["year", "annee", "année"]
MONTH_NAME_CANDIDATES = ["month", "mois"]
DAY_NAME_CANDIDATES = ["day", "jour"]
ID_LIKE_HINTS = [
    "id", "index", "unnamed", "code", "lat", "lon", "longitude", "latitude",
    "store", "dept", "nbr", "num", "station_id", "zone",
]

MAX_ROWS_READ = 300_000  # borne de sécurité pour garder le script rapide sur les gros fichiers
MAX_CSV_PER_DATASET = 4  # nombre max de fichiers CSV traités par dataset (évite l'explosion sur les archives à 30 fichiers)
MAX_ZIP_BYTES_TO_EXTRACT = 1_000_000_000  # 1 Go — au-delà, on n'extrait pas automatiquement (cf. MeteoNet)


@dataclass
class DatasetEntry:
    letter: str
    title: str
    url: str
    ref_type: str  # "dataset" ou "competition"
    ref: str
    slug: str = field(init=False)

    def __post_init__(self) -> None:
        safe = re.sub(r"[^a-zA-Z0-9]+", "-", self.ref).strip("-").lower()
        self.slug = f"{self.letter}_{safe}"


@dataclass
class DiagnosticResult:
    entry: DatasetEntry
    status: str  # ok | download_failed | no_data_found | no_date_column | no_numeric_column | error
    detail: str = ""
    file_used: str = ""
    date_col: str = ""
    value_cols: str = ""
    n_obs: int = 0
    date_min: str = ""
    date_max: str = ""
    plot_path: str = ""


def parse_dataset_guide(md_path: Path) -> list[DatasetEntry]:
    """Extrait chaque `## Option X — Titre` et son lien Kaggle depuis le fichier markdown."""
    text = md_path.read_text(encoding="utf-8")
    blocks = re.split(r"\n(?=## Option [A-Z] )", text)
    entries: list[DatasetEntry] = []
    for block in blocks:
        header_match = re.match(r"## Option ([A-Z]) [—-]+\s*(.+)", block)
        if not header_match:
            continue
        letter, title = header_match.group(1), header_match.group(2).strip()
        url_match = re.search(r"\]\((https://www\.kaggle\.com/[^)]+)\)", block)
        if not url_match:
            continue
        url = url_match.group(1)
        ref_type, ref = _parse_kaggle_url(url)
        entries.append(DatasetEntry(letter=letter, title=title, url=url, ref_type=ref_type, ref=ref))
    return entries


def _parse_kaggle_url(url: str) -> tuple[str, str]:
    path = url.split("kaggle.com/", 1)[1].split("?")[0].rstrip("/")
    parts = [p for p in path.split("/") if p not in ("datasets", "data")]
    if not parts:
        return "unknown", path
    if parts[0] in ("c", "competitions"):
        return "competition", parts[1] if len(parts) > 1 else parts[0]
    return "dataset", "/".join(parts[:2]) if len(parts) >= 2 else parts[0]


def check_kaggle_auth() -> bool:
    import os
    kaggle_dir = Path.home() / ".kaggle"
    if (kaggle_dir / "kaggle.json").exists():
        return True
    if (kaggle_dir / "access_token").exists():  # kaggle CLI 2.x browser login flow
        return True
    if os.environ.get("KAGGLE_USERNAME") and os.environ.get("KAGGLE_KEY"):
        return True
    return False


def download_entry(entry: DatasetEntry, dest_dir: Path, has_auth: bool) -> tuple[bool, str]:
    """Télécharge (et décompresse) un dataset/compétition Kaggle. Idempotent : ne re-télécharge pas
    si des fichiers sont déjà présents dans dest_dir."""

    if entry.ref in LOCAL_OVERRIDES:
        src = LOCAL_OVERRIDES[entry.ref]
        if not src.exists():
            return False, f"fichier local attendu introuvable : {src}"
        dest_dir.mkdir(parents=True, exist_ok=True)
        target = dest_dir / src.name
        if not target.exists():
            shutil.copy2(src, target)
        return True, f"réutilisé depuis le repo local ({src})"

    existing_csvs = list(dest_dir.rglob("*.csv")) if dest_dir.exists() else []
    if existing_csvs:
        return True, f"déjà présent en cache ({len(existing_csvs)} fichier(s) CSV)"

    if not has_auth:
        return False, "identifiants Kaggle non configurés (~/.kaggle/kaggle.json manquant)"

    dest_dir.mkdir(parents=True, exist_ok=True)
    if entry.ref_type == "dataset":
        cmd = ["kaggle", "datasets", "download", "-d", entry.ref, "-p", str(dest_dir), "--unzip"]
    elif entry.ref_type == "competition":
        cmd = ["kaggle", "competitions", "download", "-c", entry.ref, "-p", str(dest_dir)]
    else:
        return False, f"type de référence Kaggle non reconnu pour l'URL {entry.url}"

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    except subprocess.TimeoutExpired:
        return False, "téléchargement interrompu (timeout 30 min)"

    if result.returncode != 0:
        stderr = (result.stderr or result.stdout or "").strip()
        return False, f"échec kaggle CLI : {stderr[-400:]}"

    # Les compétitions ne supportent pas toujours --unzip : on décompresse nous-mêmes.
    # Garde-fou : ce zipfile.extractall() n'a aucune limite de temps contrairement au
    # subprocess ci-dessus — un zip trop volumineux peut bloquer le script indéfiniment.
    skipped_large = []
    for zpath in list(dest_dir.glob("*.zip")):
        if zpath.stat().st_size > MAX_ZIP_BYTES_TO_EXTRACT:
            skipped_large.append(zpath.name)
            continue
        try:
            with zipfile.ZipFile(zpath) as zf:
                zf.extractall(dest_dir)
            zpath.unlink()
        except zipfile.BadZipFile:
            pass

    # Un deuxième passage : certains datasets contiennent des zips imbriqués.
    for zpath in list(dest_dir.rglob("*.zip")):
        if zpath.stat().st_size > MAX_ZIP_BYTES_TO_EXTRACT:
            skipped_large.append(zpath.name)
            continue
        try:
            with zipfile.ZipFile(zpath) as zf:
                zf.extractall(zpath.parent)
            zpath.unlink()
        except zipfile.BadZipFile:
            pass

    if skipped_large:
        return False, (
            f"archive(s) trop volumineuse(s) pour extraction automatique "
            f"(> {MAX_ZIP_BYTES_TO_EXTRACT // (1024*1024)} Mo) : {', '.join(skipped_large)} — "
            f"télécharger/extraire manuellement si ce dataset est retenu"
        )

    return True, "téléchargé avec succès"


SUPPORTED_EXTENSIONS = (".csv", ".xlsx", ".xls", ".parquet")


def try_concat_split_files(dest_dir: Path) -> tuple[pd.DataFrame, str] | None:
    """Certains datasets sont livrés en un fichier CSV par année (ex: donnees_elec_2008.csv,
    donnees_elec_2009.csv, ...). Analyser un seul de ces fichiers ne montrerait qu'une seule
    année — sans tendance ni saisonnalité visible. Si plusieurs CSV du même dossier partagent
    en grande partie les mêmes colonnes (un fichier peut avoir quelques colonnes en plus/moins
    d'une année à l'autre), on les concatène sur leurs colonnes communes."""
    csvs = sorted(dest_dir.rglob("*.csv"))
    if len(csvs) < 2 or len(csvs) > 30:  # 30 = garde-fou contre les archives à centaines de fichiers
        return None
    frames = []
    ref_cols: set[str] | None = None
    per_file_cap = max(1000, MAX_ROWS_READ // len(csvs))
    for p in csvs:
        try:
            df = read_any_table(p, nrows=per_file_cap)
        except Exception:
            return None
        cols = set(df.columns)
        if ref_cols is None:
            ref_cols = cols
        else:
            overlap = len(cols & ref_cols) / max(len(cols), len(ref_cols))
            if overlap < 0.8:
                return None  # schémas trop différents : pas une série multi-fichiers homogène
            ref_cols &= cols
        frames.append(df)
    combined = pd.concat(frames, ignore_index=True, join="inner")
    return combined, f"{len(csvs)} fichiers concaténés (colonnes communes)"


def pick_files_to_inspect(dest_dir: Path) -> list[Path]:
    files: list[Path] = []
    for ext in SUPPORTED_EXTENSIONS:
        files.extend(dest_dir.rglob(f"*{ext}"))
    if not files:
        return []
    def sort_key(p: Path) -> tuple[int, int]:
        is_train = 0 if "train" in p.name.lower() else 1
        try:
            size = -p.stat().st_size
        except OSError:
            size = 0
        return (is_train, size)
    files.sort(key=sort_key)
    return files[:MAX_CSV_PER_DATASET]


def read_any_table(path: Path, nrows: int | None = MAX_ROWS_READ) -> pd.DataFrame:
    """Charge un fichier CSV/Excel/Parquet en DataFrame, avec repli d'encodage pour les CSV
    contenant des caractères accentués non-UTF-8 (fréquent dans les fichiers français)."""
    suffix = path.suffix.lower()
    if suffix == ".csv":
        last_exc: Exception | None = None
        # 1) Chemin rapide : moteur C, séparateur ',' par défaut — couvre l'immense majorité
        #    des fichiers et reste rapide même sur des CSV larges (centaines de colonnes).
        for encoding in ("utf-8", "latin-1", "cp1252"):
            try:
                df = pd.read_csv(path, nrows=nrows, low_memory=False, encoding=encoding)
                if df.shape[1] > 1:
                    return df
                last_exc = None  # une seule colonne = separateur probablement mal deviné
                break
            except UnicodeDecodeError as exc:
                last_exc = exc
                continue
            except Exception as exc:  # noqa: BLE001 — ex: nombre de champs incohérent
                last_exc = exc
                break

        # 2) Repli lent : sep=None + moteur python pour détecter un séparateur non standard
        #    (ex: ';' dans un fichier français) ou absorber des lignes malformées.
        for encoding in ("utf-8", "latin-1", "cp1252"):
            try:
                return pd.read_csv(
                    path, nrows=nrows, encoding=encoding,
                    sep=None, engine="python", on_bad_lines="skip",
                )
            except Exception as exc:  # noqa: BLE001 — encodage ou délimiteur en cause, on retente
                last_exc = exc
                continue
        raise last_exc or ValueError("lecture CSV impossible (encodage/délimiteur non détecté)")
    if suffix in (".xlsx", ".xls"):
        return pd.read_excel(path, sheet_name=0, nrows=nrows)
    if suffix == ".parquet":
        # Colonnaire et généralement compact : on charge tout plutôt que de risquer un
        # échantillon non représentatif de la plage temporelle réelle.
        return pd.read_parquet(path, engine="pyarrow")
    raise ValueError(f"extension non supportée : {suffix}")


def _find_col(lower_cols: dict[str, str], candidates: list[str], exact_only: bool = False) -> str | None:
    for cand in candidates:
        for col, low in lower_cols.items():
            if low == cand:
                return col
    if exact_only:
        return None
    for cand in candidates:
        for col, low in lower_cols.items():
            if cand in low:
                return col
    return None


def _parse_plain_column(df: pd.DataFrame, col: str) -> pd.Series:
    """Parse une colonne comme date, SANS jamais laisser pandas interpréter un entier nu
    comme un nombre de nanosecondes depuis 1970 (piège classique avec des colonnes
    'month'/'day' à valeur 1-12 ou 1-31)."""
    s = df[col]
    if pd.api.types.is_numeric_dtype(s):
        # Un entier "nu" (ex: mois 1-12) n'est pas une date exploitable seul.
        return pd.Series(pd.NaT, index=s.index)
    return pd.to_datetime(s, errors="coerce", format="mixed")


def _is_plausible_datetime(parsed: pd.Series, min_valid_ratio: float = 0.6,
                            check_span_collapse: bool = True) -> bool:
    valid = parsed.dropna()
    if len(parsed) == 0 or len(valid) / len(parsed) < min_valid_ratio:
        return False
    if len(valid) < 3:
        return False
    years = valid.dt.year
    if not years.between(1900, 2100).mean() >= 0.9:
        return False
    if check_span_collapse:
        span = valid.max() - valid.min()
        # Rejette le cas classique où un petit entier (ex: mois 1-12) a été interprété comme
        # des nanosecondes depuis epoch : toutes les dates s'écrasent alors en < 1 seconde.
        # Ne s'applique qu'aux colonnes "brutes" (voir appelants) : une date construite via
        # un combo année[+mois[+jour]] n'est par construction pas sujette à ce piège, et un
        # fichier ne couvrant qu'une seule année/mois y est légitimement sujet à un span nul.
        if span < pd.Timedelta(seconds=1):
            return False
    return True


DateSpec = "str | tuple"  # str = nom de colonne unique ; tuple = ('combo', year_col, month_col|None, day_col|None)


def resolve_datetime(df: pd.DataFrame, spec) -> pd.Series:
    if isinstance(spec, tuple) and spec[0] == "combo":
        _, year_col, month_col, day_col = spec
        parts = {
            "year": pd.to_numeric(df[year_col], errors="coerce"),
            "month": pd.to_numeric(df[month_col], errors="coerce") if month_col else 1,
            "day": pd.to_numeric(df[day_col], errors="coerce") if day_col else 1,
        }
        return pd.to_datetime(parts, errors="coerce")
    return _parse_plain_column(df, spec)


def detect_date_spec(df: pd.DataFrame):
    lower_cols = {c: c.lower() for c in df.columns}

    # 1) Colonne date complète nommée explicitement (ex: "Date", "timestamp"...).
    for cand in FULL_DATE_NAME_CANDIDATES:
        col = _find_col(lower_cols, [cand], exact_only=True)
        if col and _is_plausible_datetime(resolve_datetime(df, col)):
            return col
    for cand in FULL_DATE_NAME_CANDIDATES:
        col = _find_col(lower_cols, [cand], exact_only=False)
        if col and _is_plausible_datetime(resolve_datetime(df, col)):
            return col

    # 2) Colonnes séparées Année [+ Mois [+ Jour]] (ex: dataset avec YEAR, MONTH).
    year_col = _find_col(lower_cols, YEAR_NAME_CANDIDATES, exact_only=True)
    month_col = _find_col(lower_cols, MONTH_NAME_CANDIDATES, exact_only=True)
    day_col = _find_col(lower_cols, DAY_NAME_CANDIDATES, exact_only=True)
    if year_col and month_col:
        spec = ("combo", year_col, month_col, day_col)
        if _is_plausible_datetime(resolve_datetime(df, spec), check_span_collapse=False):
            return spec
    if year_col and not month_col:
        # Données annuelles seules (ex: "annee" sans mois) : pas de saisonnalité possible,
        # mais utile comme série de tendance (cf. LakeHuron dans le cours). Peut légitimement
        # ne couvrir qu'une seule année (span nul) si le fichier est un extrait mono-année.
        spec = ("combo", year_col, None, None)
        if _is_plausible_datetime(resolve_datetime(df, spec), min_valid_ratio=0.6, check_span_collapse=False):
            return spec

    # 3) Repli : tenter de parser chaque colonne texte et garder la meilleure.
    # NB : depuis pandas 2.x/3.x avec l'inférence de type "string" activée, une colonne
    # textuelle n'a plus forcément dtype == object — il faut un test plus robuste.
    best_col, best_ratio = None, 0.0
    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]) or df[col].dtype == object:
            sample = df[col].dropna().head(300)
            if sample.empty:
                continue
            parsed = pd.to_datetime(sample, errors="coerce", format="mixed")
            if not _is_plausible_datetime(parsed, min_valid_ratio=0.5):
                continue
            ratio = parsed.notna().mean()
            if ratio > best_ratio:
                best_ratio, best_col = ratio, col
    if best_col is not None and best_ratio > 0.7:
        return best_col
    return None


def try_wide_date_columns(df: pd.DataFrame) -> tuple[pd.DataFrame, str, str] | None:
    """Détecte le format 'large' où les dates sont des NOMS DE COLONNES plutôt que des valeurs
    de ligne (ex: Page, 2015-07-01, 2015-07-02, ... — cas du dataset Wikipedia Web Traffic).
    Si détecté, transforme (melt) en format long et agrège (somme) toutes les lignes par date
    pour produire une série unique exploitable par le reste du pipeline."""
    str_cols = [c for c in df.columns if isinstance(c, str)]
    date_like: list[str] = []
    for c in str_cols:
        parsed = pd.to_datetime(c, errors="coerce", format="mixed")
        if pd.notna(parsed):
            date_like.append(c)
    if len(date_like) < 10 or len(date_like) < 0.5 * len(df.columns):
        return None

    id_cols = [c for c in df.columns if c not in date_like]
    if not id_cols:
        return None
    id_col = id_cols[0]

    melted = df[[id_col] + date_like].melt(id_vars=[id_col], var_name="_wide_date", value_name="_value")
    melted["_value"] = pd.to_numeric(melted["_value"], errors="coerce")
    agg = melted.groupby("_wide_date", as_index=False)["_value"].sum()
    return agg, "_wide_date", "_value"


def date_spec_label(spec) -> str:
    if isinstance(spec, tuple) and spec[0] == "combo":
        parts = [c for c in spec[1:] if c]
        return "+".join(parts) + " (combiné)"
    return str(spec)


def detect_value_columns(df: pd.DataFrame, date_spec, max_cols: int = 3) -> list[str]:
    if isinstance(date_spec, tuple):
        used_cols = {c for c in date_spec[1:] if c}
    else:
        used_cols = {date_spec}
    numeric_cols = [
        c for c in df.select_dtypes(include="number").columns
        if c not in used_cols and not any(hint in c.lower() for hint in ID_LIKE_HINTS)
    ]
    if not numeric_cols:
        return []
    variances = df[numeric_cols].var(numeric_only=True).sort_values(ascending=False)
    return list(variances.head(max_cols).index)


def build_series(df: pd.DataFrame, date_spec, value_col: str) -> pd.Series:
    tmp = df.copy()
    tmp["_dt"] = resolve_datetime(tmp, date_spec)
    tmp = tmp.dropna(subset=["_dt", value_col])
    tmp = tmp.set_index("_dt").sort_index()
    grouped = tmp[value_col].groupby(level=0).mean()
    monthly = grouped.resample("MS").mean()
    return monthly.dropna()


def plot_diagnostic(entry: DatasetEntry, df_full: pd.DataFrame, date_spec, value_cols: list[str],
                     out_path: Path) -> tuple[int, str, str]:
    n_series = len(value_cols)
    fig, axes = plt.subplots(n_series, 2, figsize=(12, 3.6 * n_series), squeeze=False)
    fig.suptitle(f"{entry.letter} — {entry.title}\n({entry.ref})", fontsize=12, fontweight="bold")

    total_obs = 0
    date_min_overall, date_max_overall = None, None

    for i, value_col in enumerate(value_cols):
        series = build_series(df_full, date_spec, value_col)

        ax_line, ax_profile = axes[i][0], axes[i][1]
        if series.empty:
            ax_line.text(0.5, 0.5, "pas de données exploitables", ha="center", va="center")
            ax_profile.axis("off")
            continue

        total_obs = max(total_obs, len(series))
        if date_min_overall is None or series.index.min() < date_min_overall:
            date_min_overall = series.index.min()
        if date_max_overall is None or series.index.max() > date_max_overall:
            date_max_overall = series.index.max()

        series.plot(ax=ax_line, marker=".", linewidth=1.2)
        ax_line.set_title(f"{value_col} — série mensualisée (moyenne)")
        ax_line.set_xlabel("")

        span_years = (series.index.max() - series.index.min()).days / 365.25
        if span_years >= 1.5 and len(series) >= 18:
            prof = pd.DataFrame({"value": series, "year": series.index.year, "month": series.index.month})
            pivot = prof.pivot_table(index="month", columns="year", values="value")
            pivot.plot(ax=ax_profile, marker="o", legend=False, linewidth=1)
            ax_profile.set_title("Profils saisonniers superposés (par année)")
            ax_profile.set_xlabel("Mois")
            ax_profile.set_xticks(range(1, 13))
        else:
            ax_profile.text(0.5, 0.5, "historique trop court\npour un profil saisonnier fiable\n(< ~2 ans)",
                             ha="center", va="center", fontsize=9)
            ax_profile.axis("off")

    fig.tight_layout(rect=(0, 0, 1, 0.94))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=140)
    plt.close(fig)

    date_min_str = date_min_overall.strftime("%Y-%m") if date_min_overall is not None else ""
    date_max_str = date_max_overall.strftime("%Y-%m") if date_max_overall is not None else ""
    return total_obs, date_min_str, date_max_str


def process_entry(entry: DatasetEntry, data_dir: Path, plots_dir: Path, has_auth: bool,
                   do_download: bool) -> DiagnosticResult:
    dest_dir = data_dir / entry.slug
    result = DiagnosticResult(entry=entry, status="error")

    if do_download:
        ok, detail = download_entry(entry, dest_dir, has_auth)
        if not ok:
            result.status = "download_failed"
            result.detail = detail
            return result
    elif not dest_dir.exists():
        result.status = "download_failed"
        result.detail = "pas de cache local (relancer sans --no-download)"
        return result

    csv_files = pick_files_to_inspect(dest_dir)
    if not csv_files:
        result.status = "no_data_found"
        result.detail = "aucun fichier CSV/Excel/Parquet trouvé après extraction"
        return result

    # Tenter d'abord une concaténation multi-fichiers (ex: un CSV par année) : donne une vue
    # bien plus utile qu'un seul fichier isolé quand le dataset est fragmenté ainsi.
    candidates: list[tuple[Path, pd.DataFrame]] = []
    concat_result = try_concat_split_files(dest_dir)
    if concat_result is not None:
        combined_df, concat_note = concat_result
        candidates.append((Path(f"<{concat_note}>"), combined_df))

    last_reason = ""
    for csv_path in csv_files:
        try:
            candidates.append((csv_path, read_any_table(csv_path)))
        except Exception as exc:  # noqa: BLE001 — on veut continuer sur l'entrée suivante
            last_reason = f"lecture impossible ({csv_path.name}) : {exc}"

    for csv_path, df in candidates:
        if df.empty or df.shape[1] < 2:
            last_reason = f"{csv_path.name} : fichier vide ou trop peu de colonnes"
            continue

        wide_result = try_wide_date_columns(df)
        if wide_result is not None:
            df, date_spec, value_col = wide_result
            value_cols = [value_col]
        else:
            date_spec = detect_date_spec(df)
            if date_spec is None:
                last_reason = f"{csv_path.name} : aucune colonne date détectée"
                continue
            value_cols = detect_value_columns(df, date_spec)
            if not value_cols:
                last_reason = f"{csv_path.name} : aucune colonne numérique exploitable détectée"
                continue

        out_path = plots_dir / f"{entry.slug}.png"
        try:
            n_obs, date_min, date_max = plot_diagnostic(entry, df, date_spec, value_cols, out_path)
        except Exception as exc:  # noqa: BLE001
            last_reason = f"{csv_path.name} : erreur lors du tracé ({exc})"
            continue

        if n_obs == 0:
            last_reason = f"{csv_path.name} : série vide après nettoyage/agrégation"
            continue

        result.status = "ok"
        result.detail = f"fichier retenu parmi {len(candidates)} candidat(s)"
        try:
            result.file_used = str(csv_path.relative_to(data_dir))
        except ValueError:
            result.file_used = csv_path.name  # candidat synthétique (concaténation multi-fichiers)
        result.date_col = date_spec_label(date_spec)
        result.value_cols = ", ".join(value_cols)
        result.n_obs = n_obs
        result.date_min = date_min
        result.date_max = date_max
        result.plot_path = str(out_path.relative_to(plots_dir.parent))
        return result

    result.status = "no_date_column" if "date" in last_reason else "no_numeric_column"
    result.detail = last_reason or "aucun fichier exploitable"
    return result


def write_summary(results: list[DiagnosticResult], plots_dir: Path) -> None:
    lines = [
        "# Résumé du triage des datasets Kaggle — SAE 3.03",
        "",
        "*Généré automatiquement par `scripts/download_and_plot_datasets.py`. "
        "Vérifier visuellement chaque graphique avant de valider une option pour un binôme.*",
        "",
        "| Option | Statut | Fichier retenu | Colonne date | Colonne(s) valeur | N obs (mensuel) | Période | Détail |",
        "|---|---|---|---|---|---:|---|---|",
    ]
    status_fr = {
        "ok": "✅ OK",
        "download_failed": "⛔ échec téléchargement",
        "no_data_found": "⚠️ pas de CSV trouvé",
        "no_date_column": "⚠️ pas de colonne date",
        "no_numeric_column": "⚠️ pas de colonne numérique",
        "error": "⛔ erreur",
    }
    for r in results:
        lines.append(
            f"| {r.entry.letter} — {r.entry.title} | {status_fr.get(r.status, r.status)} | "
            f"`{r.file_used}` | {r.date_col} | {r.value_cols} | {r.n_obs} | "
            f"{r.date_min}–{r.date_max} | {r.detail} |"
        )
    lines.append("")
    lines.append("## Légende des statuts")
    lines.append("- **OK** : un graphique a été généré (`plots/<option>.png`) — à valider visuellement.")
    lines.append("- **échec téléchargement** : identifiants Kaggle manquants, compétition dont les règles "
                  "n'ont pas été acceptées sur le site, ou dataset introuvable/renommé.")
    lines.append("- **pas de CSV / pas de colonne détectée** : la détection automatique n'a pas trouvé de "
                  "structure exploitable — inspecter le fichier manuellement.")
    (plots_dir / "_summary.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--md", type=Path, default=DEFAULT_MD, help="Chemin du fichier DATASETS_Kaggle_Projet.md")
    parser.add_argument("--data-dir", type=Path, default=DEFAULT_DATA_DIR, help="Dossier de cache des données brutes")
    parser.add_argument("--plots-dir", type=Path, default=DEFAULT_PLOTS_DIR, help="Dossier de sortie des graphiques")
    parser.add_argument("--only", type=str, default="", help="Lettres d'options à traiter, ex: A,D,J")
    parser.add_argument("--no-download", action="store_true", help="Ne pas télécharger, utiliser le cache existant")
    parser.add_argument("--list", action="store_true", help="Lister les options détectées dans le .md et quitter")
    args = parser.parse_args()

    entries = parse_dataset_guide(args.md)
    if not entries:
        print(f"Aucune option trouvée dans {args.md}", file=sys.stderr)
        sys.exit(1)

    if args.list:
        for e in entries:
            print(f"{e.letter} [{e.ref_type}] {e.ref:60s} — {e.title}")
        return

    if args.only:
        wanted = {x.strip().upper() for x in args.only.split(",") if x.strip()}
        entries = [e for e in entries if e.letter in wanted]

    has_auth = check_kaggle_auth()
    if not has_auth and not args.no_download:
        print(
            "⚠️  Aucun identifiant Kaggle détecté (~/.kaggle/kaggle.json ou variables "
            "KAGGLE_USERNAME/KAGGLE_KEY). Les téléchargements échoueront pour tout ce qui "
            "n'est pas déjà en cache local. Voir : "
            "https://github.com/Kaggle/kaggle-cli/blob/main/docs/README.md#authentication\n",
            file=sys.stderr,
        )

    results: list[DiagnosticResult] = []
    for entry in entries:
        print(f"[{entry.letter}] {entry.title} ({entry.ref_type}: {entry.ref}) ...", end=" ", flush=True)
        try:
            res = process_entry(entry, args.data_dir, args.plots_dir, has_auth, do_download=not args.no_download)
        except Exception as exc:  # noqa: BLE001 — ne jamais interrompre le run global
            res = DiagnosticResult(entry=entry, status="error", detail=str(exc))
        print(res.status, "-", res.detail)
        results.append(res)

    write_summary(results, args.plots_dir)
    ok_count = sum(1 for r in results if r.status == "ok")
    print(f"\nTerminé : {ok_count}/{len(results)} graphiques générés dans {args.plots_dir}")
    print(f"Résumé : {args.plots_dir / '_summary.md'}")


if __name__ == "__main__":
    main()
