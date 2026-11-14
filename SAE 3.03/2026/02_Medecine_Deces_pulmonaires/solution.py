import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")

# --- données : exportées par solution.R (data/*.csv). Python lit les CSV.
out = {}
for nm in ["mdeaths", "fdeaths", "ldeaths"]:
    need_export(os.path.join(DATA, nm + ".csv")); out[nm] = from_csv(os.path.join(DATA, nm + ".csv"), nm, "décès")
# --- variante EMS-2 : hommes et femmes séparément
R = {}
for nm in ["mdeaths", "fdeaths"]:
    R[nm] = run_pipeline(out[nm], 24, os.path.join(OUT, nm))
cm = R["mdeaths"]["dec"].seasonal[:12] if hasattr(R["mdeaths"]["dec"], "seasonal") else None
cf = R["fdeaths"]["dec"].seasonal[:12]
log = Log(os.path.join(OUT, "comparaison_m_f"))
log.h("⭐ EMS-2 : coefficients saisonniers hommes vs femmes")
log("corrélation des profils saisonniers :", round(float(np.corrcoef(cm, cf)[0, 1]), 3))
log("mois de pic :", int(np.argmax(cm)) + 1, "(hommes)", int(np.argmax(cf)) + 1, "(femmes)")
log("amplitude (max-min) :", round(float(cm.max() - cm.min()), 1), "vs", round(float(cf.max() - cf.min()), 1))
log.save()
# --- variante VCOD-6 : total ; additif vs multiplicatif tranché par un critère chiffré
res = run_pipeline(out["ldeaths"], 24, os.path.join(OUT, "ldeaths"))
l2 = Log(os.path.join(OUT, "ldeaths")); l2.lines = res["log"].lines
compare_add_mult(out["ldeaths"], 12, l2); l2.save()
