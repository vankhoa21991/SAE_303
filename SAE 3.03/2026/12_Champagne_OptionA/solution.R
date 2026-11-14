# SAE 3.03 — Sujet 12 : ventes de champagne françaises (Option A) — solution R
# Lancer : Rscript solution.R
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")

d <- read.csv(file.path(ROOT, "data", "monthly_champagne_sales.csv"))
dtm <- as.Date(paste0(d$Month, "-01"))
y <- ts(as.numeric(d$Sales), start = c(as.integer(format(dtm[1], "%Y")), as.integer(format(dtm[1], "%m"))), frequency = 12)
cat("n =", length(y), "(105 obs. et non 108 : à documenter)\n")
res <- run_pipeline(y, 21, OUT, name = "Ventes de champagne")
LOG <- res$log
compare_add_mult(y)
hw_compare(y, 21)
say("-> La méthode de choix (Buys-Ballot) avait retenu : ", res$model, " : confirmée ou non par le test ci-dessus ?")
save_log()
