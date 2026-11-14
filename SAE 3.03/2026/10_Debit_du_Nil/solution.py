import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")

ts = from_rdataset("Nile", name="Nile", unit="1e8 m3")
res = run_pipeline(ts, 20, OUT, seasonal=False, trend="mean")
log = res["log"]; ntr = ts.n - 20; yt = ts.y[ntr:]
pt = pettitt(ts.y[:ntr]); brk = pt["idx"] + 1
log.h("⭐ Pettitt (train) + ADF avant/après")
log(f"rupture vers {ts.t()[brk]:.0f} (p={pt['p']:.2g})")
for k, seg in [("avant", ts.y[:brk]), ("après", ts.y[brk:ntr])]: log(f"  ADF {k} : p={adfuller(seg)[1]:.3f}   moyenne={seg.mean():.1f}")
for k, tr in [("LES sur toute la série d'entraînement", ts.y[:ntr]), ("LES sur la période post-rupture seule", ts.y[brk:ntr])]:
    m = ExponentialSmoothing(tr, initialization_method="estimated").fit(); mm = metrics(yt, m.forecast(20))
    log(f"  {k:42s} alpha={m.params['smoothing_level']:.3f} RMSE={mm['RMSE']:.2f} MAE={mm['MAE']:.2f}")
log.save()
