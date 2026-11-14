import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")

d = pd.read_csv(os.path.join(ROOT, "data", "monthly_champagne_sales.csv"))
ts = TS(d["Sales"].astype(float).values, (1964, 1), 12, "Ventes de champagne", "bouteilles")
print("n =", ts.n, "(105 obs. et non 108 : à documenter)")
res = run_pipeline(ts, 21, OUT)
log = res["log"]; compare_add_mult(ts, 12, log); hw_compare(ts, ts.n - 21, 12, log)
log("-> La méthode de choix (Buys-Ballot) avait retenu :", res["model"], ": confirmée ou non par le test ci-dessus ?"); log.save()
