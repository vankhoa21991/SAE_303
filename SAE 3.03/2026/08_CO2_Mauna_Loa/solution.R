# SAE 3.03 — Sujet 08 : CO2 Mauna Loa (co2, R) — solution R
# Lancer : Rscript solution.R   (exporte aussi data/co2.csv pour solution.py)
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")

# --- données : co2 de R (Mauna Loa, 1959-1997) ; quelques NA -> interpolés, export CSV pour Python
co2i <- co2
i <- which(is.na(co2))
if (length(i)) co2i[i] <- approx(time(co2), as.numeric(co2), xout = time(co2)[i])$y
export_csv(co2i, file.path(DATA, "co2.csv"))

res <- run_pipeline(co2i, 84, OUT, name = "CO2 Mauna Loa", model = "additive", trend = "quad")
LOG <- res$log
hdr("⭐ Tendance linéaire vs quadratique (décomposition, sur le test)")
ntr <- length(co2i) - 84
tr <- window(co2i, end = time(co2i)[ntr]); yt <- as.numeric(window(co2i, start = time(co2i)[ntr + 1]))
for (k in c("linear", "quad")) { m <- metrics(yt, fc_decomposition(tr, 84, 12, "additive", k)); say(sprintf("  %-7s RMSE=%.3f MAE=%.3f", k, m["RMSE"], m["MAE"])) }
mod <- ets(co2i, model = "AAAd")                       # HW additif, tendance amortie (4e caractère = amorti)
fc <- as.numeric(forecast(mod, h = (2025 - 1997) * 12 + 12)$mean)
say(sprintf("Extrapolation HW (série complète) : déc. 2025 ≈ %.1f ppm -> à comparer à la valeur NOAA/Scripps réelle (cherchez-la et commentez l'écart)", fc[length(fc)]))
save_log()
