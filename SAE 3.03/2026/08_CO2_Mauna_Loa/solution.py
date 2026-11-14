import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")

f = os.path.join(DATA, "co2.csv")
if os.path.exists(f): ts = from_csv(f, "CO2 Mauna Loa", "ppm")
else:   # repli : données hebdomadaires de statsmodels moyennées par mois (≈ co2 de R, légèrement différent)
    w = sm.datasets.co2.load_pandas().data["co2"].interpolate().resample("MS").mean().loc["1959-01":"1997-12"]
    ts = TS(w.values, (1959, 1), 12, "CO2 Mauna Loa (repli statsmodels)", "ppm"); print("[!] repli statsmodels : lance solution.R pour la vraie série R co2")
res = run_pipeline(ts, 84, OUT, model="additive", trend="quad")
log = res["log"]; ntr = ts.n - 84; yt = ts.y[ntr:]
log.h("⭐ Tendance linéaire vs quadratique (décomposition, sur le test)")
for k in ["linear", "quad"]:
    m = metrics(yt, fc_decomposition(ts, ntr, 12, "additive", k)); log(f"  {k:7s} RMSE={m['RMSE']:.3f} MAE={m['MAE']:.3f}")
mod = ExponentialSmoothing(ts.y, trend="add", damped_trend=True, seasonal="add", seasonal_periods=12, initialization_method="estimated").fit()
fc = mod.forecast((2025 - 1997) * 12 + 12)
log(f"Extrapolation HW (série complète) : déc. 2025 ≈ {fc[-1]:.1f} ppm -> à comparer à la valeur NOAA/Scripps réelle (cherchez-la et commentez l'écart)")
log.save()
