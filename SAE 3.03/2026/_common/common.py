"""SAE 3.03 — pipeline commun (Python) : exploration, tests, décomposition, validation, prévision.

Chaque dossier de sujet a un `solution.py` qui charge SA série puis appelle `run_pipeline(...)`.
Dépendances : numpy pandas scipy matplotlib statsmodels   (pip install numpy pandas scipy matplotlib statsmodels)
Les tests de Mann-Kendall et de Pettitt sont réimplémentés ici (courts, lisibles, à comprendre).
"""
from __future__ import annotations
import io, os, urllib.request, warnings
from dataclasses import dataclass
import numpy as np, pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller, acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.stats.diagnostic import acorr_ljungbox

warnings.filterwarnings("ignore")
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # .../SAE 3.03


# ------------------------------------------------------------------ série
@dataclass
class TS:
    y: np.ndarray
    start: tuple          # (année, période)   ex. (1959, 1)
    freq: int             # observations par cycle (12 mensuel, 4 trimestriel, 1 annuel…)
    name: str
    unit: str = ""

    @property
    def n(self): return len(self.y)

    def t(self):          # axe temporel décimal, comme time() en R
        return self.start[0] + (self.start[1] - 1) / self.freq + np.arange(self.n) / self.freq

    def sub(self, i0, i1):
        s = self.start[0] * self.freq + (self.start[1] - 1) + i0
        return TS(self.y[i0:i1], (s // self.freq, s % self.freq + 1), self.freq, self.name, self.unit)


def _infer(time, values, name, unit=""):
    time = np.asarray(time, float)
    freq = int(round(1 / np.median(np.diff(time))))
    yr = int(np.floor(time[0] + 1e-9))
    per = int(round((time[0] - yr) * freq)) + 1
    return TS(np.asarray(values, float), (yr, per), freq, name, unit)


def from_rdataset(item, package="datasets", name=None, col="value", unit=""):
    """Série R chargée depuis le dépôt Rdatasets (équivalent du jeu de données R)."""
    d = sm.datasets.get_rdataset(item, package).data
    if col in d.columns and "time" in d.columns:
        return _infer(d["time"], d[col], name or item, unit)
    return d


def from_csv(path, name, unit=""):
    """CSV `time,value` exporté par solution.R (export des séries R) — ou séries de même format."""
    d = pd.read_csv(path)
    return _infer(d["time"], d["value"], name, unit)


def need_export(path):
    if not os.path.exists(path):
        raise SystemExit(f"[!] {path} introuvable : lance d'abord `Rscript solution.R` (il exporte la série R en CSV), "
                         "ou place ici un CSV avec les colonnes time,value.")


def http_text(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return urllib.request.urlopen(req, timeout=30).read().decode()


# ------------------------------------------------------------------ sorties
class Log:
    def __init__(self, outdir):
        os.makedirs(outdir, exist_ok=True)
        self.outdir, self.lines = outdir, []

    def __call__(self, *a):
        s = " ".join(str(x) for x in a)
        print(s); self.lines.append(s)

    def h(self, s): self("\n" + "=" * 70 + "\n" + s + "\n" + "=" * 70)

    def save(self):
        with open(os.path.join(self.outdir, "resultats.txt"), "w", encoding="utf-8") as f:
            f.write("\n".join(self.lines))

    def fig(self, name):
        plt.tight_layout(); plt.savefig(os.path.join(self.outdir, name), dpi=110); plt.close()


# ------------------------------------------------------------------ tests
def mann_kendall(x):
    x = np.asarray(x, float); n = len(x)
    s = np.sign(x[None, :] - x[:, None])[np.triu_indices(n, 1)].sum()
    _, c = np.unique(x, return_counts=True)
    var = (n * (n - 1) * (2 * n + 5) - np.sum(c * (c - 1) * (2 * c + 5))) / 18
    z = (s - np.sign(s)) / np.sqrt(var) if s != 0 else 0.0
    return dict(S=s, Z=z, p=2 * (1 - stats.norm.cdf(abs(z))), tau=s / (n * (n - 1) / 2))


def pettitt(x):
    x = np.asarray(x, float); n = len(x)
    r = stats.rankdata(x)
    u = 2 * np.cumsum(r) - np.arange(1, n + 1) * (n + 1)
    k = np.abs(u).max(); idx = int(np.abs(u).argmax())
    return dict(K=k, idx=idx, p=min(1.0, 2 * np.exp(-6 * k**2 / (n**3 + n**2))))


def cycle_means(ts):
    if ts.freq == 1: return ts.y
    m = ts.n // ts.freq
    return ts.y[: m * ts.freq].reshape(m, ts.freq).mean(axis=1)


def run_tests(ts, log):
    log.h("ÉTAPE 5 — TESTS")
    r = adfuller(ts.y, autolag="AIC", regression="ct" if ts.n > 30 else "c")
    log(f"ADF (constante+tendance) : stat={r[0]:.3f}  p={r[1]:.4f}  -> "
        + ("stationnaire (rejette H0 racine unitaire)" if r[1] < 0.05 else "NON stationnaire (H0 racine unitaire conservée)"))
    d1 = adfuller(np.diff(ts.y), autolag="AIC")
    log(f"ADF sur la série différenciée : p={d1[1]:.4f}")
    cm = cycle_means(ts) if ts.freq > 1 and ts.n // ts.freq >= 6 else ts.y
    mk = mann_kendall(cm)
    log(f"Mann-Kendall ({'moyennes par cycle' if cm is not ts.y else 'série brute'}) : tau={mk['tau']:.3f} Z={mk['Z']:.2f} p={mk['p']:.4g} -> "
        + ("tendance " + ("croissante" if mk['S'] > 0 else "décroissante") if mk['p'] < 0.05 else "pas de tendance monotone significative"))
    pt = pettitt(ts.y); tb = ts.t()[min(pt["idx"] + 1, ts.n - 1)]
    log(f"Pettitt : K={pt['K']:.0f} p={pt['p']:.4g} -> " + (f"rupture de niveau vers {tb:.2f}" if pt["p"] < 0.05 else "pas de rupture significative"))
    return dict(adf_p=r[1], mk=mk, pettitt=pt, break_time=tb)


# ------------------------------------------------------------------ exploration
def explore(ts, log):
    log.h("ÉTAPES 3-4 — DESCRIPTION & EXPLORATION")
    y = ts.y
    log(f"Série : {ts.name} ({ts.unit}) | n={ts.n} | fréquence={ts.freq} | début={ts.start} | fin≈{ts.t()[-1]:.2f}")
    log(f"min={y.min():.2f} q1={np.percentile(y,25):.2f} médiane={np.median(y):.2f} moyenne={y.mean():.2f} q3={np.percentile(y,75):.2f} max={y.max():.2f} sd={y.std(ddof=1):.2f}  NA={int(np.isnan(y).sum())}")
    blk = ts.freq if ts.freq > 1 else 10
    nb = ts.n // blk
    g = pd.DataFrame({"bloc": np.repeat(np.arange(nb), blk), "y": y[: nb * blk]}).groupby("bloc")["y"].agg(["mean", "std", "min", "max"])
    g.index = [f"{ts.t()[i*blk]:.0f}" for i in g.index]
    log(f"Descripteurs par {'cycle' if ts.freq>1 else 'décennie'} :\n" + g.round(2).head(40).to_string())
    nl = min(max(2 * ts.freq, 24), ts.n // 3)
    fig, ax = plt.subplots(3, 1, figsize=(10, 9))
    ax[0].plot(ts.t(), y, lw=.8); ax[0].set_title(f"{ts.name}"); ax[0].set_xlabel("temps")
    ax[1].stem(acf(y, nlags=nl, missing="drop")[1:], markerfmt=".", basefmt=" "); ax[1].axhline(1.96/np.sqrt(ts.n), ls="--", c="r"); ax[1].axhline(-1.96/np.sqrt(ts.n), ls="--", c="r"); ax[1].set_title("ACF")
    ax[2].stem(pacf(y, nlags=min(nl, ts.n // 2 - 1))[1:], markerfmt=".", basefmt=" "); ax[2].axhline(1.96/np.sqrt(ts.n), ls="--", c="r"); ax[2].axhline(-1.96/np.sqrt(ts.n), ls="--", c="r"); ax[2].set_title("PACF")
    log.fig("01_exploration.png")
    a = acf(y, nlags=nl)
    pk = [i for i in range(2, len(a) - 1) if a[i] > a[i-1] and a[i] > a[i+1] and a[i] > 1.96/np.sqrt(ts.n)]
    log(f"Pics locaux significatifs de l'ACF aux retards : {pk[:8]}  (la période = premier grand pic récurrent)")


# ------------------------------------------------------------------ choix additif / multiplicatif
def choose_model(ts, period, log):
    log.h("ÉTAPE 6a — CHOIX ADDITIF / MULTIPLICATIF (Buys-Ballot)")
    m = ts.n // period
    if m < 3 or period < 2:
        log("Pas assez de cycles/saisonnalité : modèle additif par défaut."); return "additive"
    Y = ts.y[: m * period].reshape(m, period)
    mean, sd = Y.mean(1), Y.std(1, ddof=1)
    res = stats.linregress(mean, sd)
    log(f"Régression sd = a*moyenne + b : a={res.slope:.4f}  p={res.pvalue:.4f}  (n cycles={m})")
    cv = (sd / mean)
    log(f"Coefficient de variation moyen sd/moyenne = {np.nanmean(cv):.3f} (sd des CV = {np.nanstd(cv):.3f}; sd des sd = {sd.std():.2f})")
    ok = bool(np.all(ts.y > 0))
    if not ok:
        mod = "additive"
        log("-> modèle retenu : ADDITIF   (série avec valeurs nulles/négatives : multiplicatif impossible)")
    elif res.slope > 0 and res.pvalue < 0.05:
        mod = "multiplicative"
        log("-> modèle retenu : MULTIPLICATIF   (pente significativement > 0 => amplitude proportionnelle au niveau)")
    else:
        mod = "additive"
        log("-> modèle retenu : ADDITIF   (pente non significative => amplitude indépendante du niveau)")
    # visuel : bandes
    fig, ax = plt.subplots(1, 2, figsize=(10, 4))
    ax[0].plot(ts.t(), ts.y, lw=.6); ax[0].plot(ts.t()[: m*period][::period], Y.max(1), "r.-"); ax[0].plot(ts.t()[: m*period][::period], Y.min(1), "g.-"); ax[0].set_title("Méthode de la bande (max/min par cycle)")
    ax[1].scatter(mean, sd); xs = np.linspace(mean.min(), mean.max(), 10); ax[1].plot(xs, res.intercept + res.slope * xs, "r"); ax[1].set_xlabel("moyenne du cycle"); ax[1].set_ylabel("écart-type"); ax[1].set_title("Buys-Ballot")
    log.fig("02_choix_modele.png")
    return mod


# ------------------------------------------------------------------ décomposition
def decomposition(ts, period, model, log, label="complète"):
    log.h(f"ÉTAPE 6b — DÉCOMPOSITION ({model}, période={period}, {label})")
    dec = seasonal_decompose(ts.y, model=model, period=period, extrapolate_trend=0)
    seas = dec.seasonal[:period]
    if period == 12:   # alignés sur le début de la série -> étiqueter par mois réel
        m0 = ts.start[1]
        log("Coefficients saisonniers (mois:valeur) :",
            " ".join(f"{((m0 - 1 + i) % 12) + 1}:{v:+.3f}" for i, v in enumerate(np.round(seas, 3))))
    else:
        log("Coefficients saisonniers (cycle) :", np.round(seas[:min(period, 24)], 3), "..." if period > 24 else "")
    log(f"Contrôle de normalisation : {'somme' if model=='additive' else 'moyenne'} = {seas.sum() if model=='additive' else seas.mean():.4f}")
    cvs = ts.y - dec.seasonal if model == "additive" else ts.y / dec.seasonal
    # --- calcul à la main de 3 valeurs de moyenne mobile centrée (à comparer au logiciel)
    p, y = period, ts.y
    w = np.r_[0.5, np.ones(p - 1), 0.5] / p if p % 2 == 0 else np.ones(p) / p
    h = len(w) // 2
    for i in range(h, h + 3):
        mm = float(np.dot(w, y[i - h: i + h + 1]))
        log(f"  MM centrée à la main t={i+1} : {mm:.3f} | statsmodels : {dec.trend[i]:.3f}")
    fig, ax = plt.subplots(4, 1, figsize=(10, 9), sharex=True)
    for a, s, t in zip(ax, [ts.y, dec.trend, dec.seasonal, dec.resid], ["série", "tendance (MM)", "saisonnalité", "résidus"]):
        a.plot(ts.t(), s, lw=.7); a.set_ylabel(t)
    log.fig("03_decomposition.png")
    plt.figure(figsize=(10, 3.5)); plt.plot(ts.t(), ts.y, lw=.6, label="brute"); plt.plot(ts.t(), cvs, lw=.8, label="CVS"); plt.legend(); plt.title("Série brute vs corrigée des variations saisonnières")
    log.fig("04_cvs.png")
    return dec, cvs


def validate(ts, dec, model, log):
    log.h("ÉTAPE 7 — VALIDATION DES RÉSIDUS")
    r = dec.resid[~np.isnan(dec.resid)]
    r = r if model == "additive" else r - 1  # multiplicatif : résidus autour de 1
    lb = acorr_ljungbox(r, lags=[min(10, len(r)//5)], return_df=True)
    sh = stats.shapiro(r[:5000])
    log(f"moyenne résidus={r.mean():.4g}  sd={r.std(ddof=1):.4g}")
    log(f"Ljung-Box : p={lb['lb_pvalue'].iloc[0]:.4g} -> " + ("résidus autocorrélés (structure restante)" if lb['lb_pvalue'].iloc[0] < .05 else "pas d'autocorrélation (bruit blanc plausible)"))
    log(f"Shapiro-Wilk : p={sh.pvalue:.4g} -> " + ("non normaux" if sh.pvalue < .05 else "normalité non rejetée"))
    ok = ~np.isnan(dec.resid)
    idx = np.where(ok)[0][np.argsort(-np.abs(r))[:3]]
    log("3 observations les plus mal ajustées :", [(round(float(ts.t()[i]), 2), round(float(ts.y[i]), 2)) for i in idx])
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.5))
    ax[0].plot(r, lw=.6); ax[0].axhline(0, c="r"); ax[0].set_title("résidus")
    ax[1].stem(acf(r, nlags=min(30, len(r)//3))[1:], markerfmt=".", basefmt=" "); ax[1].set_title("ACF des résidus")
    sm.qqplot(r, line="s", ax=ax[2]); ax[2].set_title("QQ-plot")
    log.fig("05_residus.png")


# ------------------------------------------------------------------ prévision
def metrics(y, f):
    y, f = np.asarray(y, float), np.asarray(f, float)
    e = y - f; nz = y != 0
    return dict(RMSE=float(np.sqrt(np.mean(e**2))), MAE=float(np.mean(np.abs(e))), MAPE=float(np.mean(np.abs(e[nz] / y[nz])) * 100))


def fc_decomposition(ts, ntr, period, model, trend="linear", start_fit=0):
    tr = ts.sub(0, ntr)
    if period < 2:
        cvs = tr.y; seas = lambda idx: np.zeros(len(idx))
        mult = False
    else:
        dec = seasonal_decompose(tr.y, model=model, period=period, extrapolate_trend=0)
        sc = dec.seasonal[:period]; mult = model == "multiplicative"
        cvs = tr.y / dec.seasonal if mult else tr.y - dec.seasonal
        seas = lambda idx: sc[np.asarray(idx) % period]
    t = ts.t(); deg = {"mean": 0, "linear": 1, "quad": 2}[trend]
    coef = np.polyfit(t[start_fit:ntr] - t[0], cvs[start_fit:], deg)
    idx = np.arange(ntr, ts.n); base = np.polyval(coef, t[idx] - t[0])
    if period < 2: return base
    return base * seas(idx) if mult else base + seas(idx)


def fc_smoothing(ts, ntr, period, model, log, seasonal=True):
    tr = ts.sub(0, ntr).y; h = ts.n - ntr
    cands = {"LES": dict(trend=None), "Holt": dict(trend="add"), "Holt amorti": dict(trend="add", damped_trend=True)}
    if seasonal and period > 1:
        s = "mul" if model == "multiplicative" else "add"
        cands = {"HW (sans tendance)": dict(trend=None, seasonal=s, seasonal_periods=period),
                 "HW tendance": dict(trend="add", seasonal=s, seasonal_periods=period),
                 "HW tendance amortie": dict(trend="add", damped_trend=True, seasonal=s, seasonal_periods=period)}
    best = None
    for k, kw in cands.items():
        try:
            m = ExponentialSmoothing(tr, initialization_method="estimated" if period < 30 else "heuristic", **kw).fit()
            sc = m.aicc if np.isfinite(m.aicc) else m.aic
            log(f"  {k:22s} AICc={sc:10.2f}  SSE={m.sse:.1f}  alpha={m.params['smoothing_level']:.3f} beta={m.params.get('smoothing_trend', float('nan')) if kw.get('trend') else float('nan'):.3f} gamma={m.params.get('smoothing_seasonal', float('nan')) if 'seasonal' in kw else float('nan'):.3f}")
            if best is None or sc < best[0]: best = (sc, k, m)
        except Exception as e:
            log(f"  {k}: échec ({str(e)[:60]})")
    log(f"  -> lissage retenu (AICc minimal) : {best[1]}")
    return best[1], np.asarray(best[2].forecast(h))


def fc_arima(ts, ntr, period, model, log, sarima=True, max_p=2, max_q=2):
    tr = ts.sub(0, ntr).y; h = ts.n - ntr
    use_log = model == "multiplicative" and np.all(ts.y > 0)
    z = np.log(tr) if use_log else tr
    d = 0 if adfuller(z)[1] < .05 else 1
    seas = sarima and 2 <= period <= 24
    D = 1 if seas else 0
    grid = [(p, q) for p in range(max_p + 1) for q in range(max_q + 1)]
    sgrid = [(0, 1), (1, 0), (1, 1)] if seas else [(0, 0)]
    best = None
    for p, q in grid:
        for P, Q in sgrid:
            try:
                m = SARIMAX(z, order=(p, d, q), seasonal_order=(P, D, Q, period if seas else 0), trend="c" if d == 0 and D == 0 else None).fit(disp=False)
                if best is None or m.aic < best[0]: best = (m.aic, (p, d, q), (P, D, Q), m)
            except Exception:
                pass
    name = f"ARIMA{best[1]}" + (f"x{best[2]}[{period}]" if seas else "") + (" sur log" if use_log else "")
    log(f"  modèle retenu (AIC minimal, d par ADF) : {name}  AIC={best[0]:.1f}")
    f = np.asarray(best[3].forecast(h))
    return name, np.exp(f) if use_log else f


def forecasting(ts, n_test, period, model, log, trend="linear", smooth_seasonal=True, sarima=True, max_p=2, max_q=2, tag=""):
    log.h("ÉTAPE 8 — PRÉVISION (comparaison sur le jeu de test)")
    ntr = ts.n - n_test
    log(f"train = {ntr} obs. (jusqu'à {ts.t()[ntr-1]:.2f}) | test = {n_test} obs. (de {ts.t()[ntr]:.2f} à {ts.t()[-1]:.2f})")
    yt = ts.y[ntr:]
    F = {}
    F["Décomposition"] = fc_decomposition(ts, ntr, period, model, trend)
    log("Lissage exponentiel :"); k, F["Lissage"] = fc_smoothing(ts, ntr, period, model, log, smooth_seasonal)
    F[f"Lissage: {k}"] = F.pop("Lissage")
    log("Modèle ARIMA :"); k2, F[k2] = fc_arima(ts, ntr, period, model, log, sarima, max_p, max_q)
    F["Naïf (dernière valeur)" if period < 2 or not smooth_seasonal else "Naïf saisonnier"] = (
        np.repeat(ts.y[ntr - 1], n_test) if period < 2 or not smooth_seasonal else ts.y[ntr - period: ntr][np.arange(n_test) % period])
    rows = {k: metrics(yt, v) for k, v in F.items()}
    tab = pd.DataFrame(rows).T.round(3).sort_values("RMSE")
    log(tab.to_string()); log(f"==> meilleure méthode (RMSE) : {tab.index[0]}")
    tab.to_csv(os.path.join(log.outdir, f"comparaison_previsions{tag}.csv"))
    plt.figure(figsize=(11, 4.5)); lo = max(0, ntr - 4 * max(period, 5))
    plt.plot(ts.t()[lo:], ts.y[lo:], "k", lw=1.2, label="observé")
    for k, v in F.items(): plt.plot(ts.t()[ntr:], v, lw=1, label=k)
    plt.axvline(ts.t()[ntr], c="gray", ls=":"); plt.legend(fontsize=7); plt.title("Prévisions sur le jeu de test")
    log.fig(f"06_previsions{tag}.png")
    return F, tab


# ------------------------------------------------------------------ pipeline
def run_pipeline(ts, n_test, outdir, period=None, model="auto", trend="linear", smooth_seasonal=True,
                 sarima=True, max_p=2, max_q=2, seasonal=True, tag="", log=None):
    """seasonal=False : pas de saisonnalité (série annuelle, bourse, etc.) -> décomposition = tendance seule.
    log : Log existant pour continuer le même fichier resultats.txt (sinon en crée un)."""
    if log is None: log = Log(outdir)
    period = (period or ts.freq) if seasonal else 1
    explore(ts, log); info = run_tests(ts, log)
    if period > 1:
        model = choose_model(ts, period, log) if model == "auto" else model
        dec, cvs = decomposition(ts, period, model, log); validate(ts, dec, model, log)
    else:
        model = "additive"; log.h("Pas de saisonnalité : décomposition = tendance (régression) + résidus")
        t = ts.t(); c = np.polyfit(t - t[0], ts.y, 1); r = ts.y - np.polyval(c, t)
        log(f"Tendance linéaire : pente={c[0]:.4f} par unité de temps ; écart-type résiduel={r.std(ddof=1):.3f}")
        lb = acorr_ljungbox(r, lags=[10], return_df=True)
        log(f"Résidus autour de la droite — Ljung-Box p={lb['lb_pvalue'].iloc[0]:.4g}, Shapiro p={stats.shapiro(r[:5000]).pvalue:.4g}")
        dec = None
    F, tab = forecasting(ts, n_test, period, model, log, trend, smooth_seasonal and seasonal, sarima, max_p, max_q, tag)
    log.save()
    return dict(log=log, info=info, model=model, period=period, dec=dec, F=F, table=tab, n_train=ts.n - n_test)


# ------------------------------------------------------------------ outils d'extension (questions ⭐)
def compare_add_mult(ts, period, log):
    log.h("Additif vs multiplicatif — critère chiffré (reconstruction tendance ⊕ saison)")
    for m in ["additive", "multiplicative"]:
        if m == "multiplicative" and not np.all(ts.y > 0): log("  multiplicatif impossible (valeurs <= 0)"); continue
        d = seasonal_decompose(ts.y, model=m, period=period, extrapolate_trend=0); ok = ~np.isnan(d.trend)
        fit = d.trend + d.seasonal if m == "additive" else d.trend * d.seasonal
        e = (ts.y - fit)[ok]
        log(f"  {m:15s} RMSE={np.sqrt(np.mean(e**2)):.3f}  MAPE={np.mean(np.abs(e / ts.y[ok])) * 100:.2f}%  autocorr(1) des résidus={np.corrcoef(e[:-1], e[1:])[0,1]:.2f}")


def hw_compare(ts, ntr, period, log):
    log.h("Holt-Winters multiplicatif brut vs additif sur log(y) (retransformé par exp)")
    tr, yt = ts.sub(0, ntr).y, ts.y[ntr:]; h = len(yt)
    f1 = ExponentialSmoothing(tr, trend="add", seasonal="mul", seasonal_periods=period, initialization_method="estimated").fit().forecast(h)
    f2 = np.exp(ExponentialSmoothing(np.log(tr), trend="add", seasonal="add", seasonal_periods=period, initialization_method="estimated").fit().forecast(h))
    for k, f in [("HW multiplicatif (brut)", f1), ("HW additif sur log", f2)]:
        m = metrics(yt, f); log(f"  {k:26s} RMSE={m['RMSE']:.3f} MAE={m['MAE']:.3f} MAPE={m['MAPE']:.2f}%")


def trend_break_compare(ts, ntr, period, model, start_fit, log):
    log.h(f"Tendance globale vs tendance ajustée après la rupture (obs. >= {start_fit})")
    yt = ts.y[ntr:]
    for k, s in [("tendance globale", 0), ("tendance post-rupture", start_fit)]:
        m = metrics(yt, fc_decomposition(ts, ntr, period, model, "linear", s)); log(f"  {k:24s} RMSE={m['RMSE']:.3f} MAPE={m['MAPE']:.2f}%")


def effect_of_break(ts, ntr, F, log, label="effet de l'événement"):
    log.h(f"{label} = (prévu sans l'événement) − (observé), sur le test")
    yt = ts.y[ntr:]
    for k, f in F.items():
        log(f"  {k:40s} écart cumulé={np.sum(f - yt):9.1f}   soit {np.sum(f - yt) / np.sum(f) * 100:5.1f}% du prévu")


def segment_pettitt(y, t, log, min_len=60, level=0, lo=0):
    """Segmentation récursive par Pettitt (ruptures successives)."""
    if len(y) < 2 * min_len: return
    r = pettitt(y)
    if r["p"] < 0.05 and min_len <= r["idx"] < len(y) - min_len:
        log("  " * level + f"rupture vers {t[lo + r['idx'] + 1]:.2f} (p={r['p']:.3g})")
        segment_pettitt(y[: r["idx"] + 1], t, log, min_len, level + 1, lo)
        segment_pettitt(y[r["idx"] + 1:], t, log, min_len, level + 1, lo + r["idx"] + 1)
