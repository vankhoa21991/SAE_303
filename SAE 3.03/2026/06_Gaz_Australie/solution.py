import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")

ts = from_rdataset("gas", "forecast", name="gas (Australie)", unit="")
ntest = ts.n - ((1994 - 1956) * 12)            # test : 1994-01 -> 1995-08
res = run_pipeline(ts, ntest, OUT)
log = res["log"]; brk = int(res["info"]["pettitt"]["idx"]) + 1
log.h("⭐ Les coefficients saisonniers sont-ils stables ? (amplitude par décennie)")
for a, b in [(1956, 1970), (1970, 1980), (1980, 1990), (1990, 1995)]:
    i0, i1 = (a - 1956) * 12, min(ts.n, (b - 1956) * 12)
    if i1 - i0 >= 24:
        d = seasonal_decompose(ts.y[i0:i1], model="multiplicative", period=12); log(f"  {a}-{b} : max/min des coef. = {d.seasonal[:12].max()/d.seasonal[:12].min():.2f}")
hw_compare(ts, ts.n - ntest, 12, log); trend_break_compare(ts, ts.n - ntest, 12, res["model"], brk, log); log.save()
