# SAE 3.03 — Sujet 01 : ventes de produits anti-diabète en Australie (a10, fpp2) — solution R
# Lancer : Rscript solution.R   (exporte aussi data/a10.csv pour solution.py)
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")

# --- données : a10 (package fpp2) = dépenses mensuelles du PBS, produits anti-diabète (ATC A10), juil. 1991 - juin 2008
suppressPackageStartupMessages(library(fpp2))
y <- a10
export_csv(y, file.path(DATA, "a10.csv"))            # lu par solution.py
res <- run_pipeline(y, 24, OUT, name = "a10 anti-diabète (M$)")   # test = 24 derniers mois (juil. 2006 - juin 2008)
LOG <- res$log
compare_add_mult(y)                                   # ⭐ additif vs multiplicatif tranché par un critère chiffré
hw_compare(y, 24)                                     # ⭐ Holt-Winters multiplicatif brut vs additif sur log(y)
hdr("⭐ Rupture de tendance ?")
say("Pettitt (série brute) : voir ÉTAPE 5 — la croissance accélère-t-elle ? comparer tendance globale et tendance post-rupture :")
trend_break_compare(y, 24, 12, res$model, max(2, as.integer(res$info$pettitt$idx) + 1))
say("-> La méthode de choix (Buys-Ballot) avait retenu : ", res$model)
save_log()
