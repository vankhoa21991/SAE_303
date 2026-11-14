import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")

ts = from_rdataset("UKgas", name="UKgas", unit="millions de thermies")
res = run_pipeline(ts, 8, OUT)
log = res["log"]
brk = int(res["info"]["pettitt"]["idx"]) + 1
trend_break_compare(ts, ts.n - 8, 4, res["model"], brk, log)
hw_compare(ts, ts.n - 8, 4, log); log.save()
