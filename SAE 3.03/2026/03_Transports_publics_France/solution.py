import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")

f = os.path.join(ROOT, "data", "kaggle_raw", "R_gatandubuc-public-transport-traffic-data-in-france", "Regularities_by_liaisons_Trains_France.csv")
d = pd.read_csv(f, encoding="utf-8-sig")
COL = "Average delay of all arriving trains (min)"          # métrique choisie (à adapter !)
m = d.groupby("Period")[COL].mean()                         # moyenne sur toutes les liaisons
m.index = pd.PeriodIndex(m.index, freq="M"); m = m.reindex(pd.period_range(m.index.min(), m.index.max(), freq="M")).interpolate()
ts = TS(m.values, (m.index[0].year, m.index[0].month), 12, "Retard moyen à l'arrivée (toutes liaisons)", "min")
ntest = int(ts.n - (2019 - ts.start[0]) * 12 - (1 - ts.start[1]))
# 1) avec saisonnalité  2) sans (saisonnalité jugée faible) : comparer sur le test
a = run_pipeline(ts, ntest, os.path.join(OUT, "avec_saison"))
b = run_pipeline(ts, ntest, os.path.join(OUT, "sans_saison"), seasonal=False)
log = Log(os.path.join(OUT, "avec_saison")); log.lines = a["log"].lines
log.h("⭐ Résidus = événements ? (dates des 5 plus grands écarts de la décomposition)")
r = a["dec"].resid; idx = np.argsort(-np.nan_to_num(np.abs(r)))[:5]
for i in sorted(idx): log(f"  {ts.t()[i]:.2f}  résidu={r[i]:.2f}  (grève ? vacances ? COVID ?)")
log.save()
