# SAE 3.03 — Sujet 07 : précipitations journalières à Boulder, Colorado (1948-2013) — solution Python
# Lancer : /tmp/sae_venv/bin/python solution.py   (télécharge data/boulder-precip.csv si absent)
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")
os.makedirs(DATA, exist_ok=True)

# --- données : CSV journalier (doc SAE). HPCP en pouces ; 999.99 = NA ; plusieurs relevés/jour -> somme ; jours absents = secs.
f = os.path.join(DATA, "boulder-precip.csv")
if not os.path.exists(f):
    try:
        open(f, "w", encoding="utf-8").write(http_text(
            "https://raw.githubusercontent.com/ef2020/TextFiles/master/805333-precip-daily-1948-2013.csv"))
    except Exception:
        need_export(f)

d = pd.read_csv(f)
d["DATE"] = pd.to_datetime(d["DATE"], format="%Y%m%d %H:%M")
h = d["HPCP"].astype(float); h[h >= 900] = np.nan            # 999.99 = valeur manquante
d["val"] = h
day = d.groupby(d.DATE.dt.normalize())["val"].sum().fillna(0)  # somme des relevés du jour
full = pd.date_range(day.index.min(), day.index.max(), freq="D")
day = day.reindex(full, fill_value=0)                          # jours absents du fichier = jours secs

log = Log(OUT)
log.h("DONNÉES — précipitations journalières, Boulder CO (COOP 050843), pouces")
ann_t = day.resample("YE").sum()
log(f"Jours : {len(day)} ({day.index.min().date()} -> {day.index.max().date()}) ; jours secs : {100*(day==0).mean():.1f} % ; "
    f"médiane jour arrosé : {day[day>0].median():.3f} po ; total annuel médian : {ann_t.median():.1f} po")

# --- exploration au pas journalier (dataviz + ACF)
fig, ax = plt.subplots(2, 1, figsize=(12, 6))
ax[0].plot(day.index, day.values, lw=.4, c="tab:blue"); ax[0].set_ylabel("po/jour")
ax[0].set_title("Précipitation journalière à Boulder (po) — ~82 % de jours secs, pics très irréguliers")
doy = day.groupby(day.index.dayofyear).mean()
ax[1].plot(doy.index, doy.values); ax[1].set_ylabel("po")
ax[1].set_title("Dataviz : moyenne par jour de l'année (climatologie quotidienne) — pic printanier + monsoon d'été")
ax[1].set_xlabel("jour de l'année")
log.fig("00_journalier.png")

a = acf(day.values, nlags=800)
fig, ax = plt.subplots(figsize=(12, 3)); ax.stem(a[1:801], markerfmt=".", basefmt=" ")
for L in (365, 730): ax.axvline(L, ls=":", c="r")
ax.set_title("ACF journalière — pics à 365 et 730 jours (saisonnalité annuelle)")
log.fig("00_acf_journalier.png")

# --- série de travail : totaux mensuels (période 12) ; train = 1948-08 -> 2003-12, test = 2004-2013 (120 mois)
mon = day.resample("ME").sum()
ts = TS(mon.values, (mon.index[0].year, mon.index[0].month), 12, "pluie Boulder — total mensuel", "pouces")
res = run_pipeline(ts, 120, OUT, log=log)
log = res["log"]

# --- ⭐ climatologie mensuelle : jours secs par mois + stabilité par décennie
log.h("⭐ Climatologie mensuelle (série journalière)")
dd = (day.values == 0)
ps = pd.Series(dd, index=day.index).groupby(pd.Series(dd, index=day.index).index.month).mean() * 100
log("Proportion de jours secs par mois : " + "  ".join(f"{i:2d}={v:.0f}%" for i, v in ps.items()))

df = pd.DataFrame({"year": mon.index.year, "month": mon.index.month, "val": mon.values})
dec0 = (df.year // 10 * 10)
piv = df.pivot_table(index="month", columns=dec0, values="val")
cv = piv.std(axis=1, ddof=1) / piv.mean(axis=1)
log(f"Climatologie mensuelle par décennie : CV inter-décennies par mois — max {cv.max():.2f} (mois {cv.idxmax()}); "
    f"moyenne des CV = {cv.mean():.2f}. La saisonnalité est-elle stable sur 65 ans ?")
fig, ax = plt.subplots(figsize=(9, 4)); piv.plot(ax=ax, marker=".")
ax.set_title("Climatologie mensuelle par décennie (totaux mensuels, po)"); ax.set_xlabel("mois")
log.fig("07_decennies.png")

# --- ⭐ tests sur les totaux annuels (65 ans) : ADF / Mann-Kendall / Pettitt
log.h("⭐ Tests sur les totaux ANNUELS (65 ans)")
ann = ann_t.values
r = adfuller(ann)
log(f"ADF annuel : stat={r[0]:.3f}, p={r[1]:.4g} -> {'racine unitaire non rejetée' if r[1] > 0.05 else 'stationnaire'}")
mk = mann_kendall(ann)
log(f"Mann-Kendall annuel : Z={mk['Z']:.2f}, p={mk['p']:.4g} (tau={mk['tau']:.3f}) -> "
    f"{'tendance croissante' if mk['Z'] > 0 else 'tendance décroissante'}" if mk['p'] < 0.05 else
    f"Mann-Kendall annuel : Z={mk['Z']:.2f}, p={mk['p']:.4g} -> pas de tendance significative")
pt = pettitt(ann)
log(f"Pettitt annuel : K={pt['K']}, p={pt['p']:.4g}, changement possible après l'observation {pt['idx']+1} "
    f"(≈ année {int(day.index[0].year + pt['idx'])})")

# (le tableau de comparaison des méthodes vs naïf saisonnier est déjà dans la section ÉTAPE 8 du log)
log.save()
