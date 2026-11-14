# SAE 3.03 — Sujet 11 : météo ville (températures horaires Kaggle) — solution R
# Lancer : Rscript solution.R
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")

CITY <- "Minneapolis"; CITY2 <- "San Francisco"         # une ville + une comparaison (à adapter)
f <- file.path(ROOT, "data", "kaggle_raw", "L_selfishgene-historical-hourly-weather-data", "temperature.csv")
d <- read.csv(f, check.names = FALSE)   # garde les noms d'origine ("San Francisco", ...)
dt <- as.POSIXct(d$datetime, format = "%Y-%m-%d %H:%M:%S")
d$mi <- as.numeric(format(dt, "%Y")) * 12 + as.numeric(format(dt, "%m")) - 1

monthly <- function(col) {
  dd <- data.frame(mi = d$mi, v = d[[col]] - 273.15)    # K -> °C
  g <- aggregate(v ~ mi, data = dd, FUN = mean, na.rm = TRUE)
  g <- g[order(g$mi), ]
  full <- seq(min(g$mi), max(g$mi))
  vals <- rep(NA_real_, length(full)); names(vals) <- as.character(full)
  vals[as.character(g$mi)] <- g$v
  vals <- na.interp(vals)
  yr0 <- floor(min(g$mi) / 12); mo0 <- min(g$mi) %% 12 + 1
  ts(as.numeric(vals), start = c(yr0, mo0), frequency = 12)
}

tsm <- monthly(CITY)
cat("NA horaires :", sum(is.na(d[[CITY]])), "sur", nrow(d), "\n")
res <- run_pipeline(tsm, 12, OUT, name = paste("Température mensuelle", CITY), model = "additive")
LOG <- res$log
hdr("⭐ Effet de la granularité (cycle jour/nuit vs année)")
h <- tapply(d[[CITY]], as.numeric(format(dt, "%H")), mean, na.rm = TRUE)
say(sprintf("Cycle journalier : amplitude (max-min des moyennes horaires) = %.1f °C", diff(range(h))))
say(sprintf("Cycle annuel     : amplitude (max-min des moyennes mensuelles) = %.1f °C", diff(range(tsm))))
for (c in c(CITY, CITY2)) {
  s <- decompose(monthly(c), type = "additive")$figure
  say(sprintf("  %-15s amplitude saisonnière = %.1f °C", c, diff(range(s))))
}
save_log()
