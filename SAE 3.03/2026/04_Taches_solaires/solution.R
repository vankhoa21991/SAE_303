# SAE 3.03 — Sujet 04 : taches solaires (sunspots mensuel + sunspot.year annuel) — solution R
# Lancer : Rscript solution.R
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")

# --- A) EMS-4 : série MENSUELLE (cycle ≈ 11 ans = 132 mois, pas 12 !)
y <- sunspots
SRT <- file.path(getwd(), "sorties_R")
init_out(file.path(SRT, "mensuel_cycle132"))
hdr("⭐ Quelle est la vraie période ?")
a <- acf(as.numeric(y), lag.max = 200, plot = FALSE)$acf
k <- 100 + which.max(a[101:171])                          # pics de l'ACF entre retards 100 et 170
say(sprintf("Pic de l'ACF dans [100,170] : retard %d mois = %.1f ans", k, k / 12))
d12 <- decompose(y, type = "additive")
say(sprintf("Contresens du TP01 (période 12) : amplitude des coef. saisonniers = %.2f pour une moyenne de %.1f -> saisonnalité annuelle négligeable",
            diff(range(d12$figure)), mean(y)))
save_log()
res <- run_pipeline(y, 120, file.path(SRT, "mensuel"), name = "sunspots mensuel", period = 132, model = "additive",
                    smooth_seasonal = FALSE, sarima = FALSE)

# --- B) VCOD-2 : série ANNUELLE 1700-1988
ya <- sunspot.year
res2 <- run_pipeline(ya, 30, file.path(SRT, "annuel"), name = "sunspot.year", seasonal = FALSE, max_p = 9, max_q = 1)
LOG <- res2$log
hdr("⭐ PACF : ordre p de l'AR (retards significatifs)")
pc <- pacf(as.numeric(ya), lag.max = 20, plot = FALSE)$acf
sig <- which(abs(pc[2:21]) > 1.96 / sqrt(length(ya)))
say("retards significatifs : ", if (length(sig)) paste(sig, collapse = " ") else "-", " -> p proposé =", if (length(sig)) max(sig) else 0)
save_log()
