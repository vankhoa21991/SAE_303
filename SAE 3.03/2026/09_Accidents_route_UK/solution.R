# SAE 3.03 — Sujet 09 : accidentés de la route UK (UKDriverDeaths) — solution R
# Lancer : Rscript solution.R
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")

y <- UKDriverDeaths
res <- run_pipeline(y, 24, OUT, name = "UKDriverDeaths")
LOG <- res$log
say(sprintf("Date de rupture trouvée par Pettitt : %.2f (loi : 31/01/1983)", res$info$break_time))
effect_of_break(y, length(y) - 24, res$F, "⭐ Effet estimé de la loi sur la ceinture")
save_log()
