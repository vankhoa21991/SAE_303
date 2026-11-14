# SAE 3.03 — Sujet 01 : taux des fonds fédéraux (FEDFUNDS, FRED) — solution R
# Lancer : Rscript solution.R   (depuis n'importe quel dossier)
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")

# --- données : FRED (téléchargement), copie locale pour travailler hors-ligne
f <- file.path(DATA, "FEDFUNDS.csv")
if (!file.exists(f)) {
  ok <- tryCatch({ con <- url("https://fred.stlouisfed.org/graph/fredgraph.csv?id=FEDFUNDS"); d <- read.csv(con); close(con)
                   write.csv(d, f, row.names = FALSE); TRUE },
                 error = function(e) { message("[!] téléchargement FRED impossible : ", conditionMessage(e)); FALSE })
  if (!ok) stop("FEDFUNDS.csv introuvable dans data/ et téléchargement impossible (internet requis).")
}
d <- read.csv(f)
y <- ts(as.numeric(d[, 2]), start = c(1954, 7), frequency = 12)
ntr <- (2019 - 1954) * 12 - 6                      # train : jusqu'à déc. 2018
yy <- window(y, end = time(y)[ntr + 48])           # test : 2019-01 -> 2022-12
res <- run_pipeline(yy, 48, OUT, name = "FEDFUNDS", seasonal = FALSE, trend = "linear")
hdr("⭐ Segmentation récursive par Pettitt (ruptures successives)")
segment_pettitt(as.numeric(yy), as.numeric(time(yy)))
save_log()
