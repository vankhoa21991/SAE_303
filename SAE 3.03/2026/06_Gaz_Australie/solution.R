# SAE 3.03 — Sujet 06 : production de gaz australienne (gas, forecast) — solution R
# Lancer : Rscript solution.R
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")

y <- gas
ntest <- length(y) - (1994 - 1956) * 12                  # test : 1994-01 -> 1995-08
res <- run_pipeline(y, ntest, OUT, name = "gas (Australie)")
LOG <- res$log
hdr("⭐ Les coefficients saisonniers sont-ils stables ? (amplitude par décennie)")
for (dd in list(c(1956, 1970), c(1970, 1980), c(1980, 1990), c(1990, 1995))) {
  a0 <- dd[1]; b0 <- dd[2]
  i0 <- (a0 - 1956) * 12 + 1; i1 <- min(length(y), (b0 - 1956) * 12)
  if (i1 - i0 + 1 >= 24) {
    seg <- window(y, start = time(y)[i0], end = time(y)[i1])
    d <- decompose(seg, type = "multiplicative")
    say(sprintf("  %d-%d : max/min des coef. = %.2f", a0, b0, max(d$figure) / min(d$figure)))
  }
}
hw_compare(y, ntest)
brk <- res$info$pettitt$idx + 1                          # 1re observation après la rupture (1-based)
trend_break_compare(y, ntest, 12, res$model, brk)
save_log()
