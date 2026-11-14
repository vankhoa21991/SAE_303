#!/usr/bin/env python3
"""
SAE 3.03 — Génère une fiche PDF (via HTML) par option de dataset, tenant sur une seule
page, avec le graphique de diagnostic (tendance + profil saisonnier) intégré. Construite
à partir de :
  - DATASETS_Kaggle_Projet.md (nom, caractéristiques, URL complète de chaque option)
  - DESCRIPTIONS (ci-dessous) : description factuelle courte de ce que mesure la série
  - scripts/plots/_summary.md (colonnes détectées, période, N observations)
  - scripts/plots/_trend_seasonality.md (tendance / saisonnalité mesurées)
  - scripts/plots/<option>.png (le graphique lui-même, intégré en base64)

Utilisation :
    python3 scripts/make_dataset_fiches.py
    python3 scripts/make_dataset_fiches.py --only A,F

Sortie : SAE 3.03/fiches_datasets/<lettre>_fiche.html et .pdf
"""

from __future__ import annotations

import argparse
import base64
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent  # SAE 3.03/
GUIDE = ROOT / "DATASETS_Kaggle_Projet.md"
SUMMARY = ROOT / "scripts" / "plots" / "_summary.md"
TRENDSEAS = ROOT / "scripts" / "plots" / "_trend_seasonality.md"
PLOTS_DIR = ROOT / "scripts" / "plots"
OUT_DIR = ROOT / "fiches_datasets"

# Description factuelle : de quoi parle réellement la série (contenu, source, période),
# reconstituée à partir de la page Kaggle "About Dataset" / "About this file" de chaque option.
DESCRIPTIONS: dict[str, str] = {
    "A": "Nombre de ventes mensuelles de champagne (maison Perrin Frères), de janvier 1964 à "
         "septembre 1972 — 105 observations.",
    "B": "Consommation électrique mensuelle d'un foyer (puissance active/réactive, tension, "
         "sous-comptages), agrégée depuis le jeu UCI « Individual Household Electric Power "
         "Consumption », d'environ 2006 à 2022.",
    "D": "Prix de vente moyen d'un avocat Hass et volumes vendus (par code produit PLU), par région "
         "des États-Unis — données de caisse hebdomadaires de la Hass Avocado Board.",
    "E": "Ventes hebdomadaires par magasin et par rayon pour 45 magasins Walmart (US) — jeu de la "
         "compétition Kaggle « Walmart Recruiting - Store Sales Forecasting » — avec variables "
         "économiques associées (CPI, taux de chômage, prix du carburant, indicateur jours fériés).",
    "F": "Consommation électrique (mégawatts), au pas de 15/30/60 min selon le pays, pour 15 pays "
         "d'Europe de l'Ouest, données ENTSO-E Transparency Platform, janvier 2015 à août 2020.",
    "H": "Série de ventes du commerce de détail aux États-Unis (US Census Bureau), diffusée via "
         "l'API FRED (Federal Reserve Economic Database).",
    "K": "Charge électrique horaire (mégawatts) de plusieurs zones du réseau PJM Interconnection, "
         "gestionnaire de réseau couvrant 13 États du nord-est / centre-est des États-Unis + DC.",
    "L": "Variables météorologiques horaires (température, humidité, pression…) pour 30 villes "
         "d'Amérique du Nord et 6 villes israéliennes, ~5 ans de données, collectées via l'API "
         "OpenWeatherMap.",
    "M": "Nombre de vues quotidiennes pour environ 145 000 pages Wikipédia, du 1er juillet 2015 au "
         "31 décembre 2016 — jeu de la compétition Kaggle/Google « Web Traffic Time Series "
         "Forecasting ».",
    "R": "Régularité mensuelle des TGV par liaison et validations quotidiennes de titres de "
         "transport en Île-de-France — données ouvertes SNCF / Île-de-France Mobilités.",
    "T": "Puissance maximale disponible (MW) de chacun des 58 réacteurs nucléaires français, au pas "
         "de 30 minutes, de janvier 2015 à décembre 2021 — déclarations réglementaires d'EDF.",
    "U": "Consommation quotidienne d'électricité et de gaz (MW) par région française, croisée avec "
         "la météo régionale (Open-Meteo), de 2013 à 2024 — sources RTE / GRDF via data.gouv.fr.",
}


def parse_options(text: str) -> dict[str, dict]:
    blocks = re.split(r"\n(?=## Option [A-Z] )", text)
    options: dict[str, dict] = {}
    for block in blocks:
        m = re.match(r"## Option ([A-Z]) [—-]+\s*(.+)", block)
        if not m:
            continue
        letter, title = m.group(1), m.group(2).strip()
        body = block.split("\n", 1)[1] if "\n" in block else ""
        body = re.split(r"\n## ", body)[0]  # coupe avant la prochaine section de niveau 2
        options[letter] = {"title": title, "body": body}
    return options


def parse_md_table(text: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| Option"):
            continue
        cols = [c.strip() for c in line.strip("|").split("|")]
        if not cols:
            continue
        letter = cols[0].split("—")[0].strip()
        if len(letter) == 1 and letter.isalpha():
            rows[letter] = cols
    return rows


def find_plot(letter: str) -> Path | None:
    matches = sorted(PLOTS_DIR.glob(f"{letter}_*.png"))
    return matches[0] if matches else None


def img_data_uri(path: Path) -> str:
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{b64}"


def extract_dataset_line(body_md: str) -> dict | None:
    """Isole la ligne '**Dataset** : Nom · Fréquence/taille · [texte](url)' pour en tirer
    le nom, les caractéristiques annoncées et l'URL complète de la page Kaggle."""
    m = re.search(r"^\*\*Dataset\*\*\s*:\s*(.+)$", body_md, re.MULTILINE)
    if not m:
        return None

    content = m.group(1).strip()
    parts = [p.strip() for p in content.split(" · ")]
    link_m = re.search(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", parts[-1])
    if link_m:
        url = link_m.group(2)
        parts = parts[:-1]
    else:
        url = None

    name = parts[0] if parts else content
    meta = " · ".join(parts[1:]) if len(parts) > 1 else ""
    return {"name": name, "meta": meta, "url": url}


def build_html(letter: str, title: str, body_md: str, summ_row: list[str] | None,
                trend_row: list[str] | None, plot_path: Path | None) -> str:
    dataset_info = extract_dataset_line(body_md)

    if dataset_info:
        meta_html = f"<p>{dataset_info['meta']}</p>" if dataset_info["meta"] else ""
        if dataset_info["url"]:
            url_html = (
                f'<p class="dataset-url">🔗 <a href="{dataset_info["url"]}">{dataset_info["url"]}</a></p>'
            )
        else:
            url_html = ""
        dataset_html = f"""<div class="dataset-box">
  <div class="dataset-name">{dataset_info['name']}</div>
  {meta_html}
  {url_html}
</div>"""
    else:
        dataset_html = ""

    description = DESCRIPTIONS.get(letter, "")
    description_html = f'<p class="data-description">{description}</p>' if description else ""

    if plot_path is not None:
        img_html = f'<img src="{img_data_uri(plot_path)}" alt="Graphique diagnostic {letter}">'
    else:
        img_html = "<p><em>Graphique non disponible (dataset non téléchargé ou non détecté).</em></p>"

    stats_html = ""
    if summ_row and len(summ_row) >= 7:
        stats_html += f"<tr><th>Colonne date détectée</th><td>{summ_row[3]}</td></tr>\n"
        stats_html += f"<tr><th>Colonne(s) valeur</th><td>{summ_row[4]}</td></tr>\n"
        stats_html += f"<tr><th>Nombre de points (mensuel)</th><td>{summ_row[5]}</td></tr>\n"
        stats_html += f"<tr><th>Période couverte</th><td>{summ_row[6]}</td></tr>\n"

    return f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>Option {letter} — {title}</title>
<style>
  @page {{ size: A4; margin: 10mm 12mm; }}
  * {{ box-sizing: border-box; }}
  body {{ font-family: Georgia, "Times New Roman", serif; margin: 0; color: #1a1a1a;
          line-height: 1.35; font-size: 10.5pt; }}
  h1 {{ font-size: 1.5em; border-bottom: 3px solid #16324f; padding-bottom: 6px; margin: 0 0 10px 0; }}
  .badge {{ display:inline-block; background:#16324f; color:#fff; padding:3px 12px;
            border-radius:5px; font-size:0.55em; vertical-align:middle; margin-right:12px; }}
  h2 {{ color:#16324f; font-size: 1.05em; margin: 12px 0 6px 0; border-left: 4px solid #16324f;
        padding-left: 8px; }}
  table {{ border-collapse: collapse; width: 100%; margin: 6px 0; font-size: 0.92em; }}
  th, td {{ border: 1px solid #ccc; padding: 4px 9px; text-align: left; vertical-align: top; }}
  th {{ background: #eef2f6; width: 210px; }}
  tr:nth-child(even) td {{ background: #fafafa; }}
  img {{ max-width: 100%; max-height: 95mm; width: auto; height: auto; border: 1px solid #ddd;
         margin: 6px auto; display: block; }}
  code {{ background: #f3f3f3; padding: 1px 5px; border-radius: 3px; font-size: 0.9em; }}
  .dataset-box {{ background: #fffaf0; border: 1px solid #e3d5b8; border-radius: 6px;
                  padding: 8px 14px; margin: 0 0 8px 0; }}
  .dataset-name {{ font-size: 1.1em; font-weight: bold; color: #16324f; margin-bottom: 2px; }}
  .dataset-box p {{ margin: 3px 0; }}
  .dataset-url a {{ word-break: break-all; color: #0b5394; }}
  .data-description {{ margin: 4px 0 10px 0; font-size: 1.02em; }}
</style>
</head>
<body>
<h1><span class="badge">Option {letter}</span>{title}</h1>

<div class="dataset-box">
  <div class="dataset-name">{dataset_info['name'] if dataset_info else title}</div>
  {f'<p>{dataset_info["meta"]}</p>' if dataset_info and dataset_info['meta'] else ''}
  {f'<p class="dataset-url">🔗 <a href="{dataset_info["url"]}">{dataset_info["url"]}</a></p>' if dataset_info and dataset_info['url'] else ''}
</div>
{description_html}

<h2>Caractéristiques mesurées</h2>
<table>
{stats_html}
</table>

<h2>Graphique de diagnostic</h2>
{img_html}

</body>
</html>
"""


def html_to_pdf(html_path: Path, pdf_path: Path) -> None:
    cmd = [
        "google-chrome", "--headless", "--disable-gpu", "--no-sandbox",
        "--run-all-compositor-stages-before-draw", "--virtual-time-budget=6000",
        f"--print-to-pdf={pdf_path}", "--no-pdf-header-footer",
        f"file://{html_path.resolve()}",
    ]
    subprocess.run(cmd, capture_output=True, check=False)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--only", type=str, default="")
    args = parser.parse_args()

    options = parse_options(GUIDE.read_text(encoding="utf-8"))
    summary_rows = parse_md_table(SUMMARY.read_text(encoding="utf-8")) if SUMMARY.exists() else {}
    trend_rows = parse_md_table(TRENDSEAS.read_text(encoding="utf-8")) if TRENDSEAS.exists() else {}

    letters = sorted(options.keys())
    if args.only:
        wanted = {x.strip().upper() for x in args.only.split(",") if x.strip()}
        letters = [l for l in letters if l in wanted]

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for letter in letters:
        opt = options[letter]
        plot_path = find_plot(letter)
        html = build_html(
            letter, opt["title"], opt["body"],
            summary_rows.get(letter), trend_rows.get(letter), plot_path,
        )
        out_html = OUT_DIR / f"{letter}_fiche.html"
        out_html.write_text(html, encoding="utf-8")

        out_pdf = OUT_DIR / f"{letter}_fiche.pdf"
        html_to_pdf(out_html, out_pdf)
        ok = out_pdf.exists() and out_pdf.stat().st_size > 1000
        print(f"[{letter}] {opt['title']} -> {out_pdf.name} ({'OK' if ok else 'ECHEC'})")


if __name__ == "__main__":
    main()
