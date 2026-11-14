import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")

# --- données : FRED (téléchargement), copie locale pour travailler hors-ligne
os.makedirs(DATA, exist_ok=True); f = os.path.join(DATA, "FEDFUNDS.csv")
try:
    txt = http_text("https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS"); open(f, "w").write(txt)
except Exception:
    pass
d = pd.read_csv(f)
full = TS(d.iloc[:, 1].astype(float).values, (1954, 7), 12, "FEDFUNDS", "% par an")
ntr = (2019 - 1954) * 12 - 6                      # train : jusqu'à déc. 2018
ts = full.sub(0, ntr + 48)                        # test : 2019-01 -> 2022-12
res = run_pipeline(ts, 48, OUT, seasonal=False, trend="linear")
# --- ⭐ segmentation récursive de Pettitt + qualité des prévisions en période de rupture
log = res["log"]; log.h("⭐ Segmentation récursive par Pettitt (ruptures successives)")
segment_pettitt(ts.y, ts.t(), log); log.save()
