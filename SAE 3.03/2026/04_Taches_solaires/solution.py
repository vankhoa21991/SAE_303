import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")

# --- A) EMS-4 : série MENSUELLE (cycle ≈ 11 ans = 132 mois, pas 12 !)
ts = from_rdataset("sunspots", name="sunspots mensuel", unit="nombre de taches")
m = Log(os.path.join(OUT, "mensuel_cycle132")); m.h("⭐ Quelle est la vraie période ?")
a = acf(ts.y, nlags=200); k = 100 + int(np.argmax(a[100:171])); m(f"Pic de l'ACF dans [100,170] : retard {k} mois = {k/12:.1f} ans")
d12 = seasonal_decompose(ts.y, model="additive", period=12)
m(f"Contresens du TP01 (période 12) : amplitude des coef. saisonniers = {d12.seasonal[:12].max()-d12.seasonal[:12].min():.2f} pour une moyenne de {ts.y.mean():.1f} -> saisonnalité annuelle négligeable")
m.save()
res = run_pipeline(ts, 120, os.path.join(OUT, "mensuel"), period=132, model="additive",
                   smooth_seasonal=False, sarima=False, max_p=2, max_q=2)
# --- B) VCOD-2 : série ANNUELLE 1700-1988
ta = from_rdataset("sunspot.year", name="sunspot.year", unit="nombre de taches")
res2 = run_pipeline(ta, 30, os.path.join(OUT, "annuel"), seasonal=False, max_p=9, max_q=1)
l = Log(os.path.join(OUT, "annuel")); l.lines = res2["log"].lines
l.h("⭐ PACF : ordre p de l'AR (retards significatifs)")
pc = pacf(ta.y, nlags=20); sig = [i for i in range(1, 21) if abs(pc[i]) > 1.96 / np.sqrt(ta.n)]
l("retards significatifs :", sig, "-> p proposé =", max(sig) if sig else 0); l.save()
