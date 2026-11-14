# SAE 3.03 — Sujet 07 : précipitations journalières à Boulder, Colorado (1948-2013) — solution R
# Lancer : Rscript solution.R   (télécharge data/boulder-precip.csv si absent)
fa <- grep("^--file=", commandArgs(FALSE), value = TRUE)
setwd(if (length(fa)) dirname(normalizePath(sub("^--file=", "", fa[1]))) else getwd())
source(file.path(getwd(), "..", "_common", "common.R"))
OUT <- file.path(getwd(), "sorties_R"); DATA <- file.path(getwd(), "data")
dir.create(DATA, showWarnings = FALSE)

# --- données : CSV journalier (doc SAE). HPCP en pouces ; 999.99 = NA ; plusieurs relevés/jour -> somme ; jours absents = secs.
f <- file.path(DATA, "boulder-precip.csv")
if (!file.exists(f)) {
  ok <- tryCatch({
    con <- url("https://raw.githubusercontent.com/ef2020/TextFiles/master/805333-precip-daily-1948-2013.csv")
    on.exit(close(con)); writeLines(readLines(con, warn = FALSE), f); TRUE
  }, error = function(e) { message("[!] téléchargement Boulder impossible : ", conditionMessage(e)); FALSE })
  if (!ok) stop("boulder-precip.csv introuvable dans data/ et téléchargement impossible.")
}
d <- read.csv(f, check.names = FALSE)
dt <- as.POSIXct(d$DATE, format = "%Y%m%d %H:%M")
v <- d$HPCP; v[v >= 900] <- NA                        # 999.99 = valeur manquante
day <- tapply(v, as.Date(dt), sum, na.rm = TRUE)      # somme des relevés du jour
full <- seq(as.Date(min(as.Date(dt))), as.Date(max(as.Date(dt))), by = "day")
dayv <- setNames(as.numeric(day), as.character(names(day)))
dayv <- dayv[as.character(full)]; dayv[is.na(dayv)] <- 0   # jours absents du fichier = jours secs

init_out(OUT)
hdr("DONNÉES — précipitations journalières, Boulder CO (COOP 050843), pouces")
ann_t <- tapply(dayv, as.integer(format(full, "%Y")), sum)
say(sprintf("Jours : %d (%s -> %s) ; jours secs : %.1f %% ; médiane jour arrosé : %.3f po ; total annuel médian : %.1f po",
            length(dayv), full[1], full[length(full)], 100 * sum(dayv == 0) / length(dayv),
            median(dayv[dayv > 0]), median(ann_t)))

# --- exploration au pas journalier (dataviz + ACF)
png_open("00_journalier.png")
par(mfrow = c(2, 1))
plot(full, dayv, type = "l", lwd = .3, col = "steelblue", xlab = "", ylab = "po/jour",
     main = "Précipitation journalière à Boulder (po) — ~82 % de jours secs, pics très irréguliers")
doy <- tapply(dayv, as.integer(format(full, "%j")), mean)
plot(as.integer(names(doy)), doy, type = "l", xlab = "jour de l'année", ylab = "po",
     main = "Dataviz : moyenne par jour de l'année (climatologie quotidienne) — pic printanier + monsoon d'été")
dev.off()

png_open("00_acf_journalier.png")
acf(dayv, lag.max = 800, main = "ACF journalière — pics à 365 et 730 jours (saisonnalité annuelle)")
abline(v = c(365, 730), lty = 3, col = "red"); dev.off()

# --- série de travail : totaux mensuels (période 12) ; train = 1948-08 -> 2003-12, test = 2004-2013 (120 mois)
mon <- tapply(dayv, format(full, "%Y-%m"), sum)
ym <- strsplit(names(mon), "-"); yr <- as.integer(sapply(ym, `[`, 1)); mo <- as.integer(sapply(ym, `[`, 2))
ts_mon <- ts(as.numeric(mon), start = c(yr[1], mo[1]), frequency = 12)

res <- run_pipeline(ts_mon, 120, OUT, name = "pluie Boulder — total mensuel", fresh_log = FALSE)

# --- ⭐ climatologie mensuelle : jours secs par mois + stabilité par décennie
hdr("⭐ Climatologie mensuelle (série journalière)")
ps <- tapply(dayv == 0, as.integer(format(full, "%m")), mean) * 100
say(paste0("Proportion de jours secs par mois : ", paste(sprintf("%2d=%.0f%%", as.integer(names(ps)), ps), collapse = "  ")))

decade <- (yr %/% 10) * 10
piv <- tapply(mon, list(mo, decade), mean)            # lignes = mois, colonnes = décennies
cv <- apply(piv, 1, sd) / apply(piv, 1, mean)
say(sprintf("Climatologie mensuelle par décennie : CV inter-décennies par mois — max %.2f (mois %d) ; moyenne des CV = %.2f. La saisonnalité est-elle stable sur 65 ans ?",
            max(cv), which.max(cv), mean(cv)))
png_open("07_decennies.png")
x <- as.integer(rownames(piv)); cols <- rainbow(ncol(piv))
plot(x, as.numeric(piv[, 1]), type = "n", xlab = "mois", ylab = "po", xaxt = "n",
     main = "Climatologie mensuelle par décennie (totaux mensuels, po)")
axis(1, at = 1:12, labels = 1:12)
for (j in seq_len(ncol(piv))) lines(x, as.numeric(piv[, j]), col = cols[j], lwd = 1.5)
legend("topleft", colnames(piv), col = cols, lwd = 1.5, cex = .8); dev.off()

# --- ⭐ tests sur les totaux annuels (65 ans) : ADF / Mann-Kendall / Pettitt
hdr("⭐ Tests sur les totaux ANNUELS (65 ans)")
ann <- as.numeric(ann_t)
ad <- adf.test(ann)
say(sprintf("ADF annuel : stat=%.3f, p=%.4g -> %s", ad$statistic, ad$p.value,
            if (ad$p.value > 0.05) "racine unitaire non rejetée" else "stationnaire"))
mk <- mann_kendall(ann)
if (mk$p < 0.05) {
  say(sprintf("Mann-Kendall annuel : Z=%.2f, p=%.4g (tau=%.3f) -> tendance %s", mk$Z, mk$p, mk$tau, if (mk$Z > 0) "croissante" else "décroissante"))
} else {
  say(sprintf("Mann-Kendall annuel : Z=%.2f, p=%.4g -> pas de tendance significative", mk$Z, mk$p))
}
pt <- pettitt(ann)
say(sprintf("Pettitt annuel : K=%d, p=%.4g, changement possible après l'observation %d (≈ année %d)",
            pt$K, pt$p, pt$idx + 1, as.integer(format(full[1], "%Y")) + pt$idx))

# (le tableau de comparaison des méthodes vs naïf saisonnier est déjà dans la section ÉTAPE 8 du log)
save_log()
