# SAE 3.03 — Sujet 13 : températures de Nottingham (nottem) — solution R
# Lancer : Rscript solution.R
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")

y <- nottem
res <- run_pipeline(y, 36, OUT, name = "nottem", model = "additive")
LOG <- res$log
r <- as.numeric(na.omit(res$dec$random))
hdr("⭐ Que reste-t-il dans les résidus ? (ordre AR par AIC)")
best <- NULL
for (p in 0:6) { m <- tryCatch(arima(r, order = c(p, 0, 0), method = "ML"), error = function(e) NULL)
                 if (!is.null(m) && (is.null(best) || m$aic < best$aic)) best <- m }
say("ordre AR sélectionné : ", best$arma[1])
if (best$arma[1] > 0) say("coefficients AR : ", paste(round(coef(best)[seq_len(best$arma[1])], 3), collapse = " "))
save_log()
