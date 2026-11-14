# SAE 3.03 — Sujet 05 : consommation de gaz UK trimestrielle (UKgas) — solution R
# Lancer : Rscript solution.R
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")

y <- UKgas
res <- run_pipeline(y, 8, OUT, name = "UKgas")
LOG <- res$log
brk <- res$info$pettitt$idx + 1                          # 1re observation après la rupture (1-based)
trend_break_compare(y, 8, 4, res$model, brk)
hw_compare(y, 8)
save_log()
