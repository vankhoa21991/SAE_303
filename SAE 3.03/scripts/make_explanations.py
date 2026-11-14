#!/usr/bin/env python3
"""SAE 3.03 — écrit `exemple_decomposition.md` dans chaque dossier de sujet de 2026/.

Les chiffres viennent des sorties R (`sorties_R/…`) : resultats.txt, exemple_chiffre.csv, coefficients.csv,
buys_ballot.csv, choix_modele.csv, comparaison_previsions.csv. Lancer d'abord `Rscript solution.R` dans chaque
dossier, puis : python3 scripts/make_explanations.py
Le sujet 05 (UKgas) a son explication écrite à la main : il est ignoré.
"""
import csv, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "2026"
MONTHS = "Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec".split()

SUBJECTS = {
 "01_Economie_FEDFUNDS": dict(title="FEDFUNDS — US federal funds rate", runs=[("FEDFUNDS monthly 1954–2022", ".")],
   context="Effective federal funds rate (the overnight interest rate between US banks), monthly from July 1954, cut at December 2022 for the exercise. Monetary policy makes it move by **regimes** (rise to 1981, long fall, near zero after 2008 and 2020, sharp hikes in 2022), not by calendar season.",
   watch=["No seasonality: the pipeline fits a trend line and looks at the residuals — and a single straight line is a poor description of several regimes.",
          "The test period (2019–2022) contains the Covid cut to ~0 and the 2022 hikes: every method is wrong there. That is the lesson, not a bug.",
          "MAPE is huge when the rate is close to 0 (division by a tiny observed value): read RMSE/MAE instead and say why."]),
 "02_Medecine_Deces_pulmonaires": dict(title="UK lung-disease deaths (mdeaths, fdeaths, ldeaths)", runs=[("mdeaths — men", "mdeaths"), ("fdeaths — women", "fdeaths"), ("ldeaths — both sexes", "ldeaths")],
   extra_dirs=["comparaison_m_f"],
   context="Monthly UK deaths from bronchitis, emphysema and asthma, 1974–1979 (72 months): `mdeaths` = men, `fdeaths` = women, `ldeaths` = total. Deaths peak in winter (cold, respiratory infections).",
   watch=["Only 6 cycles: every seasonal coefficient is the average of just 6 ratios, and the 24-month test set is a third of the data. State what so little data can and cannot prove.",
          "Early 1976 shows an unusually high winter peak: decide whether it is an outlier or a real event, and find a source for the explanation.",
          "Men and women have similar *shapes* but different *levels*: compare the coefficients (the ⭐ block), not the raw values."]),
 "03_Transports_publics_France": dict(title="French trains — average arrival delay (Option R)", runs=[("with seasonality (period 12)", "avec_saison"), ("without seasonality", "sans_saison")],
   context="Monthly average delay of all arriving trains (minutes), averaged over all connections of the Kaggle file `Regularities_by_liaisons_Trains_France.csv`, January 2015 → June 2020. Choose your own metric/connection in the report and document it.",
   watch=["The seasonality is weak on this metric (η² ≈ 0.13 in the dataset sheet): the two runs (with / without a seasonal term) let you check whether adding one actually helps on the test set.",
          "The test period contains the 2019–2020 strikes and the Covid lockdown: the biggest residuals are *events*, not noise. Date them and link them to real events.",
          "The averaging over connections hides missing data per line: document how gaps were filled."]),
 "04_Taches_solaires": dict(title="Sunspot numbers (monthly and annual)", runs=[("monthly, period 132", "mensuel"), ("annual 1700–1988", "annuel")], extra_dirs=["mensuel_cycle132"],
   context="Sunspot counts. The monthly series (`sunspots`, 1749–1983) and the annual series (`sunspot.year`, 1700–1988). The Sun has a ≈ 11-year activity cycle (Schwabe cycle) — **not** a yearly season.",
   watch=["`decompose()` with period 12 (as in TP01) is a misreading: there is no 12-month pattern. The ACF peaks near lag ≈ 130 months ≈ 11 years: that is the period to use (see the ⭐ block).",
          "The cycle length varies (9–14 years), so a fixed-period seasonal model is only an approximation.",
          "Smoothing without a seasonal term cannot reproduce the cycle: forecasts a decade ahead are nearly flat. An AR model of order ≈ 9 (PACF) does better."]),
 "06_Gaz_Australie": dict(title="Australian gas production (gas)", runs=[("monthly 1956–1995", ".")],
   context="Monthly Australian gas production, 1956 → August 1995 (476 observations, `forecast::gas`). Production exploded after the 1960s–70s.",
   watch=["The growth is faster than linear and the seasonal swing grows with it: multiplicative model, or work on log(y).",
          "The seasonal coefficients are not stable over 40 years (nearly flat in the 1950s–60s, large later): a single set of coefficients is a compromise.",
          "A level/trend break around 1970 (Pettitt): the global linear trend extrapolates badly."]),
 "07_Pluie_Boulder": dict(title="Boulder (Colorado) rainfall", runs=[("monthly totals 1948–2013", ".")],
   context="Daily precipitation at Boulder, Colorado (1948–2013; value 999.99 = missing). The daily file is aggregated into **monthly totals** (in inches) to apply the course methods.",
   watch=["Most days are dry and rain is very irregular: the seasonality is much weaker than for temperature, and the residuals are large and skewed.",
          "Missing-value code 999.99 must be turned into NA *before* summing, otherwise one bad value ruins a month.",
          "The daily ACF has peaks at 365 and 730 days (figure `00_acf_journalier.png`): seasonality exists, but it is buried in noise."]),
 "08_CO2_Mauna_Loa": dict(title="Atmospheric CO₂ at Mauna Loa (co2)", runs=[("monthly 1959–1997", ".")],
   context="Monthly CO₂ concentration near Mauna Loa (Hawaii), ppm, 1959–1997 — the Keeling curve. Photosynthesis in the northern hemisphere makes it dip every summer; fossil-fuel emissions make it rise.",
   watch=["The seasonal amplitude is constant while the level rises: **additive** model.",
          "The trend is slightly convex: a straight line leaves a curved pattern in the residuals; a quadratic trend does better (see ⭐).",
          "This is the TP example: do not stop at `decompose()` — compare methods on the 1991–97 test set and extrapolate."]),
 "09_Accidents_route_UK": dict(title="UK driver deaths (UKDriverDeaths)", runs=[("monthly 1969–1984", ".")],
   context="Monthly drivers killed or seriously injured in Great Britain, January 1969 → December 1984. The **seat-belt law came into force on 31 January 1983**.",
   watch=["The 24-month test set (1983–84) is entirely *after* the law: a model trained before it will over-forecast — the gap measures the effect of the law (⭐ block).",
          "Pettitt should detect a break close to January 1983; the oil crisis of 1973–74 also shows up as a dip.",
          "Seasonality: more accidents in winter (dark, bad weather)."]),
 "10_Debit_du_Nil": dict(title="Nile annual flow at Aswan (Nile)", runs=[("annual 1871–1970", ".")],
   context="Annual flow of the Nile at Aswan, 1871–1970, in 10⁸ m³. A well-known level shift appears around 1898–1899 (change of regime linked to dams and climate).",
   watch=["Annual data: no seasonality, so no coefficients — the structure is a **level shift**, not a straight-line trend. Pettitt is the right test.",
          "Fitting one LES on the whole series mixes two regimes; compare with a LES on the post-break part only (⭐ block).",
          "Every method has a similar RMSE: on such a series, 'beating' the naïve forecast is hard — say so honestly."]),
 "11_Meteo_ville_OptionL": dict(title="Monthly temperature of a US city (Option L)", runs=[("Minneapolis, monthly", ".")],
   context="Hourly temperature from the Kaggle 'Historical Hourly Weather Data' (kelvin, converted to °C), averaged by month: 62 months, October 2012 → November 2017, for one city (Minneapolis; compare with San Francisco in the ⭐ block).",
   watch=["Only 5 cycles and no significant trend: you cannot conclude anything about climate change from 5 years.",
          "Hourly gaps must be handled before averaging (missing hours, interpolation).",
          "Granularity matters: hourly data show the day/night cycle, monthly data the annual cycle — both are in the ⭐ block."]),
 "12_Champagne_OptionA": dict(title="Champagne sales (Option A)", runs=[("monthly 1964–1972", ".")],
   context="Monthly champagne sales (Perrin Frères), January 1964 → September 1972 (105 observations; the dataset sheet says ~108, document the difference). Sales peak every year-end (holidays).",
   watch=["Additive or multiplicative is a real debate here: the amplitude grows slowly. Check whether the three methods of the course agree.",
          "The ⭐ block compares both decompositions numerically and shows which Holt-Winters variant wins on the test set.",
          "Short series (8 full cycles): keep the test set to ~21 months."]),
 "13_Environnement_Temperature_Nottingham": dict(title="Nottingham temperatures (nottem)", runs=[("monthly 1920–1939", ".")],
   context="Average monthly air temperature at Nottingham Castle, °F, 20 years (1920–1939, 240 observations).",
   watch=["Very strong and stable annual cycle, no trend: **additive** (temperatures can be near 0 or negative in °C, so a percentage model makes no sense).",
          "Because the seasonal model fits so well, the interesting question is what is left in the residuals (⭐ block: AR order of the residuals).",
          "A degree-Fahrenheit coefficient is directly interpretable: '+2 °F above the annual mean'."]),
}


def read_csv(p):
    if not p.exists(): return None
    with open(p, encoding="utf-8") as f: return list(csv.DictReader(f))

def fnum(x, d=2):
    try: return f"{float(x):.{d}f}"
    except Exception: return str(x)

def grab(txt, pat, default=None):
    m = re.search(pat, txt); return m.group(1) if m else default

def pos_label(p, period):
    if period == 12: return MONTHS[p - 1]
    if period == 4: return f"Q{p}"
    return f"pos {p}"

def md_table(head, rows):
    return "\n".join(["| " + " | ".join(head) + " |", "|" + "---|" * len(head)] + ["| " + " | ".join(map(str, r)) + " |" for r in rows])

def pval_words(p, h0_rejected, h0_kept):
    return h0_rejected if p < 0.05 else h0_kept

def run_section(label, d, tag):
    txt = (d / "resultats.txt").read_text(encoding="utf-8")
    out = [f"## {tag}. Run: {label}\n"]
    nm = grab(txt, r"Série : (.*?) \|"); n = grab(txt, r"n=(\d+)"); fr = grab(txt, r"fréquence=([\d.]+)")
    st = grab(txt, r"début=([\d/]+)"); en = grab(txt, r"fin=([\d.]+)")
    summ = grab(txt, r"summary : (.*)")
    out.append(f"**Series**: {nm} — n = {n}, frequency = {fr} per cycle, from {st} to {en}.\n")
    if summ: out.append(f"Summary: `{summ.strip()}`\n")
    # ---- tests
    adf = grab(txt, r"ADF : p=([\d.e+-]+)"); mk = grab(txt, r"Mann-Kendall : p=([\d.e+-]+)"); pt = grab(txt, r"Pettitt : p=([\d.e+-]+) -> (.*)")
    pt_p = float(grab(txt, r"Pettitt : p=([\d.e+-]+)", "1")); pt_s = grab(txt, r"Pettitt : p=[\d.e+-]+ -> (.*)", "")
    out.append("### Tests (step 5)\n")
    rows = []
    if adf: rows.append(["ADF (stationarity)", adf, "stationary — H0 'unit root' rejected" if float(adf) < .05 else "**not** stationary — H0 'unit root' kept"])
    if mk: rows.append(["Mann-Kendall (trend)", mk, "significant monotone trend" if float(mk) < .05 else "no significant trend"])
    pt_en = re.sub(r"rupture de niveau vers", "level break around", pt_s.strip()).replace("pas de rupture significative", "no significant break")
    rows.append(["Pettitt (level break)", f"{pt_p:.3g}", pt_en])
    out.append(md_table(["Test", "p-value", "Reading (p < 0.05 ⇒ H0 rejected)"], rows))
    out.append("\nADF: H0 = the series has a unit root (is not stationary). Mann-Kendall: H0 = no trend. Pettitt: H0 = no change of level. "
               "A p-value below 0.05 rejects H0.\n")
    coef = read_csv(d / "coefficients.csv")
    if coef is None:
        out.append("### No seasonal decomposition\n")
        sl = grab(txt, r"pente=([-\d.]+)");
        out.append(f"This run has **no seasonal component** (annual data, or seasonality deliberately switched off). "
                   f"The pipeline therefore fits a straight line to the series: slope = **{sl}** per time unit. "
                   f"Without seasonal coefficients there is nothing to 'adjust': the structure is trend (or level shifts) + residual.\n")
        res = (grab(txt, r"(pente=.*)") or "").replace("pente", "slope").replace("sd résiduel", "residual sd")
        out.append(f"Residuals of the line: `{res}`\n")
        if pt_p < 0.05 and mk and float(mk) < 0.05:
            out.append("Mann-Kendall **and** Pettitt are both significant: on annual data this usually means a **level shift** (a step) rather than a steady slope — the straight line is only a rough summary. Look at the plot and the date given by Pettitt.\n")
        out.append("Interpretation: *Ljung-Box* tests whether residuals are autocorrelated (p < 0.05 ⇒ yes, structure left); *Shapiro* tests normality.\n")
        period = 1
    else:
        period = len(coef)
        bb = read_csv(d / "buys_ballot.csv"); cm = read_csv(d / "choix_modele.csv")[0]
        sugg = cm["modele"]; a = float(cm["pente"]); p = float(cm["p_value"])
        mod = {"additive": "additive", "multiplicative": "multiplicative"}.get(grab(txt, r"DÉCOMPOSITION \((\w+)"), sugg)   # modèle réellement utilisé
        out.append("### Additive or multiplicative? (step 6a — Buys-Ballot)\n")
        out.append("For each cycle compute the mean and the standard deviation, then regress `sd = a·mean + b`. "
                   "If `a` is significantly positive the swings grow with the level ⇒ multiplicative.\n")
        sel = bb[:3] + ([{"cycle": "…", "moyenne": "…", "ecart_type": "…"}] if len(bb) > 5 else []) + bb[-2:]
        out.append(md_table(["Cycle", "Mean", "Std"], [[r["cycle"], fnum(r["moyenne"]) if r["moyenne"] != "…" else "…", fnum(r["ecart_type"]) if r["ecart_type"] != "…" else "…"] for r in sel]))
        f0, f1 = bb[0], bb[-1]
        out.append(f"\nSlope **a = {a:.4f}**, p = {p:.4g}, {cm['n_cycles']} cycles ⇒ Buys-Ballot suggests **{sugg.upper()}**. "
                   + ("The spread grows with the level: seasonal effects are percentages of the trend." if sugg == "multiplicative" else "The spread does not grow significantly with the level: seasonal effects are constant amounts.")
                   + " (Figure `02_choix_modele.png`: band method on the left, Buys-Ballot on the right.)\n")
        if mod != sugg:
            out.append(f"**But `solution.R` imposes the {mod.upper()} model.** Do not hide the disagreement in your report: the slope may be statistically significant yet practically small "
                       f"(here the cycle standard deviation goes from {fnum(f0['ecart_type'])} to {fnum(f1['ecart_type'])} while the mean goes from {fnum(f0['moyenne'])} to {fnum(f1['moyenne'])}), "
                       f"so judge the *size* of the effect, the band plot, and the residuals of both decompositions before choosing. The tables below use the {mod} model.\n")
        ex = read_csv(d / "exemple_chiffre.csv")
        out.append("### Decomposition step by step (step 6b)\n")
        h = period // 2
        if period % 2 == 0:
            out.append(f"**Step A — centred moving average.** The period is p = {period} (even), so a window of {period} values has no centre. "
                       f"Use {period + 1} values with half weight on the two ends:\n\n```\nT_t = (0.5·y_(t-{h}) + y_(t-{h-1}) + … + y_(t+{h-1}) + 0.5·y_(t+{h})) / {period}\n```\n")
        else:
            out.append(f"**Step A — centred moving average.** p = {period} (odd): the plain average of the {period} values centred on t:\n\n```\nT_t = (y_(t-{h}) + … + y_(t+{h})) / {period}\n```\n")
        r0 = next((r for r in ex if r["tendance"] not in ("NA", "")), None)
        if r0 is not None and period <= 12:
            t0 = int(r0["t"]); ys = [float(r["y"]) for r in ex if t0 - h <= int(r["t"]) <= t0 + h]
            w = ([0.5] + [1] * (period - 1) + [0.5]) if period % 2 == 0 else [1] * period
            terms = " + ".join((f"0.5·{y:g}" if wi == 0.5 else f"{y:g}") for y, wi in zip(ys, w))
            val = sum(y * wi for y, wi in zip(ys, w)) / period
            out.append(f"By hand at t = {t0}: `T_{t0} = ({terms}) / {period} = {val:.3f}` — R gives **{float(r0['tendance']):.3f}** ✓\n")
        else:
            out.append(f"(With p = {period} the window is too long to write out; `ma(y, order={period}, centre=TRUE)` computes it and is compared with `decompose()` in the log.)\n")
        out.append(f"The first {h} and last {h} trend values do not exist (the window would run outside the data).\n")
        out.append(f"**Step B — remove the trend.** Compute `y_t / T_t` (multiplicative) or `y_t − T_t` (additive) — what is left is season + noise:\n")
        rr = [r for r in ex if r["tendance"] not in ("NA", "")][: min(period, 12)]
        out.append(md_table(["t", "time", "y_t", "T_t", "y/T" if mod == "multiplicative" else "y−T", "position"],
                            [[r["t"], r["temps"], fnum(r["y"]), fnum(r["tendance"]), fnum(r["ratio"], 3), pos_label(int(r["position"]), period)] for r in rr]))
        out.append("\n**Step C — average per position in the cycle, then normalise.** Collect all the ratios that belong to the same position and average them "
                   "(averaging cancels the noise), then force the coefficients to " + ("average exactly 1" if mod == "multiplicative" else "sum to 0") + ":\n")
        shown = coef if period <= 12 else coef[:6] + [{"position": "…", "brute": "…", "normalisee": "…", "n": "…"}] + coef[-2:]
        def meaning(c):
            if c == "…": return ""
            v = float(c)
            return (f"{(v-1)*100:+.0f}% vs trend" if mod == "multiplicative" else f"{v:+.1f} vs trend")
        out.append(md_table(["Position", "n ratios", "raw", "normalised (decompose)", "meaning"],
                            [[pos_label(int(r["position"]), period) if r["position"] != "…" else "…", r["n"], fnum(r["brute"], 4) if r["brute"] != "…" else "…", fnum(r["normalisee"], 4) if r["normalisee"] != "…" else "…", meaning(r["normalisee"])] for r in shown]))
        mraw = sum(float(r["brute"]) for r in coef) / period
        out.append(f"\nThe raw coefficients average {mraw:.4f}; they are rescaled to {'1' if mod == 'multiplicative' else '0'} so the season does not also move the overall level. "
                   f"Largest: **{pos_label(max(coef, key=lambda r: float(r['normalisee']))['position'] and int(max(coef, key=lambda r: float(r['normalisee']))['position']), period)}**, "
                   f"smallest: **{pos_label(int(min(coef, key=lambda r: float(r['normalisee']))['position']), period)}**.\n")
        rc = rr[0]
        cvs_formula = "y_t / S" if mod == "multiplicative" else "y_t − S"
        out.append(f"**Step D — seasonally adjusted series (CVS) and residual.** `CVS_t = {cvs_formula}`; the residual is what trend × season (or trend + season) does not explain. "
                   f"Example at t = {rc['t']}: y = {fnum(rc['y'])}, T = {fnum(rc['tendance'])}, S = {fnum(rc['coef'], 4)} ⇒ CVS = {fnum(rc['cvs'])}, residual = {fnum(rc['residu'], 4)} "
                   f"({'1 = perfect fit' if mod == 'multiplicative' else '0 = perfect fit'}).\n")
        v = grab(txt, r"(moyenne=.*Shapiro.*)")
        out.append("### Validation (step 7)\n")
        v = (v or "").replace("moyenne=", "mean=").replace("autocorrélés", "autocorrelated").replace("bruit blanc plausible", "plausibly white noise").replace("non normaux", "not normal").replace("normaux", "normal")
        out.append(f"`{v}`\n" if v else "")
        w3 = grab(txt, r"mal ajustées.*?: (.*)")
        if w3: out.append(f"Worst-fitted observations (time ; value): `{w3}` — look each one up: what happened at that date?\n")
        out.append("Ljung-Box p < 0.05 means the residuals are still autocorrelated (the decomposition left structure behind — often a seasonal pattern that drifts); Shapiro p < 0.05 means they are not perfectly normal.\n")
    # ---- forecast
    out.append("### Forecast (step 8)\n")
    split = grab(txt, r"(train = .*)")
    out.append(f"Split: `{split}`. Never evaluate a forecast on the data used to fit the model.\n")
    tab = read_csv(d / "comparaison_previsions.csv")
    if tab:
        key = list(tab[0].keys())[0]
        out.append(md_table(["Method", "RMSE", "MAE", "MAPE %"], [[r[key], fnum(r["RMSE"]), fnum(r["MAE"]), fnum(r["MAPE"], 1)] for r in tab]))
        best = tab[0][key]; names = [r[key] for r in tab]
        dec = next((i for i, nme in enumerate(names) if nme.startswith(("Décomposition", "Tendance seule"))), None)
        out.append(f"\nBest on the test set: **{best}** (RMSE {fnum(tab[0]['RMSE'])}). "
                   + (f"The {'decomposition' if coef is not None else 'trend-only'} method ranks {dec + 1} of {len(names)}. " if dec is not None else "")
                   + ("LES (simple smoothing) and LED (Holt) have **no seasonal term**: on a seasonal series they cannot reproduce the yearly pattern. "
                      "Holt-Winters adds it and updates it each period. " if coef is not None else
                      "There is no seasonality here, so LES (level only), LED (level + slope) and the trend line are the natural candidates; Holt-Winters is not used. ")
                   + "`auto.arima` is the optional autoregressive model. 'Naïf' repeats the last value (or the last cycle): any serious method must beat it.\n")
        al = grab(txt, r"(LES : alpha=.*)"); hw = grab(txt, r"(Holt-Winters : alpha=.*)"); ar = grab(txt, r"auto.arima : (.*)")
        smooth = "; ".join(x for x in [al, hw] if x)
        if smooth: out.append(f"Estimated smoothing constants: `{smooth}` (α close to 1 = the forecast follows the last observation; close to 0 = very smooth).\n")
        if re.search(r"alpha=1\.000", txt): out.append("An α (and/or β) of exactly 1.000 means the optimiser hit its boundary: the smoother just repeats the last observation/slope, which is a symptom of a model that does not fit the series (no seasonal term here).\n")
        if ar: out.append(f"Model chosen by `auto.arima`: `{ar.strip()}`.\n")
    # ---- extras ⭐
    after = txt.split("==> meilleure méthode (RMSE)")
    if len(after) > 1:
        extra = after[1].split("\n", 1)[1].strip() if "\n" in after[1] else ""
        extra = "\n".join(l for l in extra.splitlines() if not re.fullmatch(r"=+", l.strip()))
        if extra.strip(): out.append("### ⭐ Subject-specific question — results from the log\n\n```\n" + extra.strip() + "\n```\n")
    return "\n".join(out), period


def build(folder, cfg):
    out = [f"# {cfg['title']} — decomposition and forecasting explained\n",
           f"> Numbers below come from `solution.R` (folder `sorties_R/`). Companion to `ENONCE.md`. "
           f"The line-by-line theory with a full hand calculation is in `../05_Gaz_UK_UKgas/exemple_decomposition.md`; "
           f"here we apply the same method to **this** series.\n",
           "## 0. The method in 6 lines\n",
           "1. A series = trend T + seasonal S + residual R. **Additive**: Y = T + S + R. **Multiplicative**: Y = T × S × R.\n"
           "2. Choose with Buys-Ballot (does the within-cycle spread grow with the level?) and the band plot.\n"
           "3. Trend = centred moving average of one full cycle; seasonal coefficients = average of (y/T or y−T) per position, normalised (mean 1 or sum 0).\n"
           "4. CVS = y / S (or y − S); residual = what is left; validate it (autocorrelation, normality, big outliers).\n"
           "5. Forecast on a held-out test set: trend extrapolation × season, LES/LED/Holt-Winters, optional ARIMA; compare with RMSE/MAE/MAPE.\n"
           "6. Always compare with a naïve forecast.\n",
           "## 1. The data and its context\n", cfg["context"] + "\n"]
    tag = 2
    periods = []
    for label, sub in cfg["runs"]:
        d = ROOT / folder / "sorties_R" / (sub if sub != "." else "")
        s, per = run_section(label, d, tag); out.append(s); tag += 1; periods.append(per)
    for sub in cfg.get("extra_dirs", []):
        p = ROOT / folder / "sorties_R" / sub / "resultats.txt"
        if p.exists():
            body = "\n".join(l for l in p.read_text(encoding="utf-8").splitlines() if not re.fullmatch(r"=+", l.strip()))
            out.append(f"## {tag}. Extra results: `{sub}`\n\n```\n{body.strip()}\n```\n"); tag += 1
    out.append(f"## {tag}. What to watch for in this subject\n")
    out += [f"- {w}" for w in cfg["watch"]]
    out.append("\n**Generic mistakes**: using the additive default without checking Buys-Ballot; forgetting to normalise the coefficients; reading the CVS as the trend; "
               "evaluating on the training data; reporting an RMSE without a naïve reference; calling a model good while the residuals are still autocorrelated.\n")
    out.append(f"## {tag + 1}. Code and how to run\n")
    code = (ROOT / folder / "solution.R").read_text(encoding="utf-8")
    keep = [l for l in code.splitlines() if "run_pipeline" in l or "compare_add_mult" in l or "hw_compare" in l or "trend_break_compare" in l or "effect_of_break" in l or "segment_pettitt" in l]
    out.append("Core calls in `solution.R` (the pipeline itself is in `_common/common.R`, built from TP functions: `decompose`, `ma`, `HoltWinters`, `predict`, `adf.test`, `mk.test`, `pettitt.test`):\n\n```r\n" + "\n".join(keep[:8]) + "\n```\n")
    out.append(f"```bash\ncd \"{ROOT / folder}\"\nRscript solution.R      # sorties_R/\npython3 solution.py     # sorties_python/\n```\n")
    return "\n".join(out)


def main():
    for folder, cfg in SUBJECTS.items():
        txt = build(folder, cfg)
        (ROOT / folder / "exemple_decomposition.md").write_text(txt, encoding="utf-8")
        print(folder, len(txt.splitlines()), "lignes")


if __name__ == "__main__":
    main()
