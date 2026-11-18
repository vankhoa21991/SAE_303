# SAE 3.03 — Sujet 01 : ventes de produits anti-diabète en Australie (a10) — solution Python
# Lancer : python3 solution.py   (lit data/a10.csv exporté par `Rscript solution.R`)
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")

f = os.path.join(DATA, "a10.csv")
need_export(f)
ts = from_csv(f, "a10 anti-diabète", "M$")
res = run_pipeline(ts, 24, OUT)                       # test = 24 derniers mois
log = res["log"]
compare_add_mult(ts, 12, log)
hw_compare(ts, ts.n - 24, 12, log)
log.h("⭐ Rupture de tendance ?")
brk = int(res["info"]["pettitt"]["idx"]) + 1
trend_break_compare(ts, ts.n - 24, 12, res["model"], brk, log)
log("-> Buys-Ballot avait retenu :", res["model"]); log.save()
