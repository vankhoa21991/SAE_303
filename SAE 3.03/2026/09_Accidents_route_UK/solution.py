import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")

ts = from_rdataset("UKDriverDeaths", name="UKDriverDeaths", unit="conducteurs tués/blessés")
res = run_pipeline(ts, 24, OUT)
log = res["log"]; log(f"Date de rupture trouvée par Pettitt : {res['info']['break_time']:.2f} (loi : 31/01/1983)")
effect_of_break(ts, ts.n - 24, res["F"], log, "⭐ Effet estimé de la loi sur la ceinture")
log.save()
