# SAE 3.03 — Sujet 10 : débit du Nil (Nile) — solution R
# Lancer : Rscript solution.R
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")

y <- Nile
res <- run_pipeline(y, 20, OUT, name = "Nile", seasonal = FALSE, trend = "mean")
LOG <- res$log
ntr <- length(y) - 20
tr <- window(y, end = time(y)[ntr]); yt <- as.numeric(window(y, start = time(y)[ntr + 1]))
pt <- pettitt.test(as.numeric(tr)); brk <- as.numeric(pt$estimate[1])   # rupture après l'observation brk (1-based)
hdr("⭐ Pettitt (train) + ADF avant/après")
say(sprintf("rupture vers %d (p=%.2g)", time(tr)[min(brk + 1, ntr)], pt$p.value))
avant <- as.numeric(tr)[1:brk]; apres <- as.numeric(tr)[(brk + 1):ntr]
for (k in c("avant", "après")) {
  seg <- if (k == "avant") avant else apres
  say(sprintf("  ADF %s : p=%.3f   moyenne=%.1f", k, adf.test(seg)$p.value, mean(seg)))
}
for (k in c("LES sur toute la série d'entraînement", "LES sur la période post-rupture seule")) {
  seg <- if (k == "LES sur toute la série d'entraînement") tr else ts(apres, frequency = 1)
  m <- HoltWinters(seg, beta = FALSE, gamma = FALSE); mm <- metrics(yt, as.numeric(predict(m, n.ahead = 20)))
  say(sprintf("  %-42s alpha=%.3f RMSE=%.2f MAE=%.2f", k, m$alpha, mm["RMSE"], mm["MAE"]))
}
save_log()
