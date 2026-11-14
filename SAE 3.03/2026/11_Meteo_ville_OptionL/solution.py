import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_common"))
from common import *
OUT = os.path.join(HERE, "sorties_python")
DATA = os.path.join(HERE, "data")

CITY, CITY2 = "Minneapolis", "San Francisco"        # une ville + une comparaison (à adapter)
f = os.path.join(ROOT, "data", "kaggle_raw", "L_selfishgene-historical-hourly-weather-data", "temperature.csv")
d = pd.read_csv(f, parse_dates=["datetime"], index_col="datetime") - 273.15      # K -> °C (l'index est exclu du calcul)
def monthly(c):
    s = d[c].resample("MS").mean().interpolate()
    return TS(s.values, (s.index[0].year, s.index[0].month), 12, f"Température mensuelle {c}", "°C")
ts = monthly(CITY)
print("NA horaires :", int(d[CITY].isna().sum()), "sur", len(d))
res = run_pipeline(ts, 12, OUT, model="additive")
log = res["log"]
log.h("⭐ Effet de la granularité (cycle jour/nuit vs année)")
h = d[CITY].groupby(d.index.hour).mean(); log(f"Cycle journalier : amplitude (max-min des moyennes horaires) = {h.max()-h.min():.1f} °C")
log(f"Cycle annuel     : amplitude (max-min des moyennes mensuelles) = {ts.y.max()-ts.y.min():.1f} °C")
for c in [CITY, CITY2]:
    s = seasonal_decompose(monthly(c).y, model="additive", period=12).seasonal[:12]; log(f"  {c:15s} amplitude saisonnière = {s.max()-s.min():.1f} °C")
log.save()
