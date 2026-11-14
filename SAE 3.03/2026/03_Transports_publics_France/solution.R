# SAE 3.03 — Sujet 03 : transports publics France (retards trains, Kaggle) — solution R
# Lancer : Rscript solution.R
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")

f <- file.path(ROOT, "data", "kaggle_raw", "R_gatandubuc-public-transport-traffic-data-in-france", "Regularities_by_liaisons_Trains_France.csv")
d <- read.csv(f, check.names = FALSE)   # garde les noms d'origine (identiques à Python/pandas)
COL <- "Average delay of all arriving trains (min)"        # métrique choisie (à adapter !)
p <- as.POSIXlt(paste0(d$Period, "-01"), format = "%Y-%m-%d")   # %Y-%m seul est mal parsé par ce R
d$mi <- as.numeric(format(p, "%Y")) * 12 + as.numeric(format(p, "%m")) - 1
d$v <- d[[COL]]
g <- aggregate(v ~ mi, data = d, FUN = mean)               # moyenne sur toutes les liaisons
g <- g[order(g$mi), ]
full <- seq(min(g$mi), max(g$mi))
vals <- rep(NA_real_, length(full)); names(vals) <- as.character(full)
vals[as.character(g$mi)] <- g$v
vals <- na.interp(vals)                                    # réindexage complet + interpolation
yr0 <- floor(min(g$mi) / 12); mo0 <- min(g$mi) %% 12 + 1
y <- ts(as.numeric(vals), start = c(yr0, mo0), frequency = 12)
ntr <- (2019 - yr0) * 12 - mo0 + 1                         # train : jusqu'à déc. 2018
ntest <- length(y) - ntr
# 1) avec saisonnalité  2) sans (saisonnalité jugée faible) : comparer sur le test
SRT <- file.path(getwd(), "sorties_R")
a <- run_pipeline(y, ntest, file.path(SRT, "avec_saison"), name = "Retard moyen à l'arrivée (toutes liaisons)")
b <- run_pipeline(y, ntest, file.path(SRT, "sans_saison"), name = "Retard moyen à l'arrivée (toutes liaisons)", seasonal = FALSE)
init_out(file.path(getwd(), "sorties_R", "avec_saison")); LOG <- a$log
hdr("⭐ Résidus = événements ? (dates des 5 plus grands écarts de la décomposition)")
r <- a$dec$random; idx <- order(abs(ifelse(is.na(r), 0, r)))[(length(r) - 4):length(r)]
for (i in sort(idx)) say(sprintf("  %.2f  résidu=%.2f  (grève ? vacances ? COVID ?)", time(y)[i], r[i]))
save_log()
