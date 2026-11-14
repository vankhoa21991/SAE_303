# SAE 3.03 — Sujet 02 : décès pulmonaires UK (ldeaths/mdeaths/fdeaths, fpp2) — solution R
# Lancer : Rscript solution.R   (exporte aussi les CSV dans data/ pour solution.py)
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")

# --- données : séries fpp2, exportées en CSV pour Python
suppressPackageStartupMessages(library(fpp2))
for (nm in c("mdeaths", "fdeaths", "ldeaths")) export_csv(get(nm), file.path(DATA, paste0(nm, ".csv")))

# --- variante EMS-2 : hommes et femmes séparément
SRT <- file.path(getwd(), "sorties_R")
Rm <- run_pipeline(mdeaths, 24, file.path(SRT, "mdeaths"), name = "mdeaths")
Rf <- run_pipeline(fdeaths, 24, file.path(SRT, "fdeaths"), name = "fdeaths")
cm <- Rm$dec$figure; cf <- Rf$dec$figure           # coefficients saisonniers (12)
init_out(file.path(SRT, "comparaison_m_f"))
hdr("⭐ EMS-2 : coefficients saisonniers hommes vs femmes")
say("corrélation des profils saisonniers : ", round(cor(cm, cf), 3))
say("mois de pic : ", which.max(cm), " (hommes)  ", which.max(cf), " (femmes)")
say("amplitude (max-min) : ", round(diff(range(cm)), 1), " vs ", round(diff(range(cf)), 1))
save_log()

# --- variante VCOD-6 : total ; additif vs multiplicatif tranché par un critère chiffré
res <- run_pipeline(ldeaths, 24, file.path(SRT, "ldeaths"), name = "ldeaths")
LOG <- res$log
compare_add_mult(ldeaths)
save_log()
