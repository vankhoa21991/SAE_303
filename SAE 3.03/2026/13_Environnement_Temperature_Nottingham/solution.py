import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")

ts = from_rdataset("nottem", name="nottem", unit="°F")
res = run_pipeline(ts, 36, OUT, model="additive")
log = res["log"]; r = res["dec"].resid; r = r[~np.isnan(r)]
from statsmodels.tsa.ar_model import ar_select_order
log.h("⭐ Que reste-t-il dans les résidus ? (ordre AR par AIC)")
sel = ar_select_order(r, maxlag=6, ic="aic"); log("ordre AR sélectionné :", sel.ar_lags)
if sel.ar_lags: log("coefficients AR :", np.round(sel.model.fit().params, 3))
log.save()
