# SAE 3.03 — pipeline commun en R, version simple (même fonctions que les TP01 à TP04).
#   exploration : summary, sd, plot, acf, pacf        tests : adf.test, mk.test, pettitt.test
#   choix du modèle : Buys-Ballot (lm sd ~ moyenne)    décomposition : decompose, ma
#   validation : Box.test, shapiro.test, qqnorm        prévision : lm (tendance) + HoltWinters + predict
# Lancer un sujet : depuis son dossier, `Rscript solution.R`.
# Packages : install.packages(c("forecast", "tseries", "trend"))

suppressPackageStartupMessages({ library(forecast); library(tseries); library(trend) })
options(warn = -1)
ROOT <- normalizePath(file.path(getwd(), "..", ".."))   # .../SAE 3.03

# ---------------------------------------------------------------- sorties (log texte + PNG)
OUT <- NULL; LOG <- character()
init_out <- function(dir) { OUT <<- dir; dir.create(dir, showWarnings = FALSE, recursive = TRUE); LOG <<- character() }
say  <- function(...) { s <- paste0(..., collapse = ""); cat(s, "\n"); LOG <<- c(LOG, s) }
hdr  <- function(s) say("\n", strrep("=", 70), "\n", s, "\n", strrep("=", 70))
save_log <- function(tag = "") writeLines(LOG, file.path(OUT, paste0("resultats", tag, ".txt")))
png_open <- function(name, w = 1100, h = 800) png(file.path(OUT, name), width = w, height = h, res = 110)
export_csv <- function(x, file) {   # série R -> CSV (time,value) lu par solution.py
  dir.create(dirname(file), showWarnings = FALSE, recursive = TRUE)
  write.csv(data.frame(time = as.numeric(time(x)), value = as.numeric(x)), file, row.names = FALSE)
}
with_period <- function(y, p) if (p != frequency(y)) ts(as.numeric(y), start = start(y), frequency = p) else y
rmse <- function(obs, pred) sqrt(mean((obs - pred)^2))
metrics <- function(obs, pred) c(RMSE = rmse(obs, pred), MAE = mean(abs(obs - pred)), MAPE = mean(abs((obs - pred)[obs != 0] / obs[obs != 0])) * 100)

# ---------------------------------------------------------------- étape 4 : exploration (TP01-TP02)
explore <- function(y, name) {
  hdr("ÉTAPES 3-4 — DESCRIPTION & EXPLORATION")
  say(sprintf("Série : %s | n=%d | fréquence=%g | début=%s | fin=%.2f", name, length(y), frequency(y), paste(start(y), collapse = "/"), tail(time(y), 1)))
  say("summary : ", paste(names(summary(y)), round(summary(y), 2), collapse = " | "), " | sd=", round(sd(y), 2), " | NA=", sum(is.na(y)))
  png_open("01_exploration.png", 1100, 1000); par(mfrow = c(3, 1))
  plot(y, main = name, ylab = ""); acf(y, lag.max = min(max(2 * frequency(y), 24), length(y) %/% 3), main = "ACF")
  pacf(y, lag.max = min(max(2 * frequency(y), 24), length(y) %/% 3), main = "PACF"); dev.off()
  if (frequency(y) > 1) {   # boxplot par cycle et par position dans le cycle (comme TP02)
    png_open("01b_boxplots.png", 1100, 450); par(mfrow = c(1, 2))
    boxplot(as.numeric(y) ~ floor(time(y)), main = "Par année", xlab = "", ylab = ""); boxplot(as.numeric(y) ~ cycle(y), main = "Par position dans le cycle"); dev.off()
  }
}

# ---------------------------------------------------------------- étape 5 : tests (TP04)
run_tests <- function(y) {
  hdr("ÉTAPE 5 — TESTS")
  a <- adf.test(y)
  say(sprintf("ADF : p=%.4f -> %s", a$p.value, if (a$p.value < .05) "stationnaire (H0 racine unitaire rejetée)" else "NON stationnaire"))
  mk <- mk.test(as.numeric(y))
  say(sprintf("Mann-Kendall : p=%.4g -> %s", mk$p.value, if (mk$p.value < .05) "tendance significative" else "pas de tendance significative"))
  pt <- pettitt.test(as.numeric(y)); idx <- as.numeric(pt$estimate[1]); tb <- time(y)[min(idx + 1, length(y))]
  say(sprintf("Pettitt : p=%.4g -> %s", pt$p.value, if (pt$p.value < .05) sprintf("rupture de niveau vers %.2f", tb) else "pas de rupture significative"))
  list(adf_p = a$p.value, mk_p = mk$p.value, pettitt = list(idx = idx, p = pt$p.value), break_time = tb)
}

# ---------------------------------------------------------------- étape 6 : modèle + décomposition (TP02, TP04)
choose_model <- function(y, period) {   # Buys-Ballot : écart-type de chaque cycle ~ moyenne du cycle
  hdr("ÉTAPE 6a — CHOIX ADDITIF / MULTIPLICATIF (Buys-Ballot)")
  cyc <- (seq_along(y) - 1) %/% period; full <- cyc < max(cyc) | length(y) %% period == 0
  moy <- tapply(as.numeric(y)[full], cyc[full], mean); et <- tapply(as.numeric(y)[full], cyc[full], sd)
  fit <- summary(lm(et ~ moy)); a <- fit$coefficients[2, 1]; p <- fit$coefficients[2, 4]
  say(sprintf("sd = a*moyenne + b : a=%.4f, p=%.4f (%d cycles)", a, p, length(moy)))
  mod <- if (a > 0 && p < .05 && all(y > 0)) "multiplicative" else "additive"
  write.csv(data.frame(cycle = as.integer(names(moy)) + 1, moyenne = as.numeric(moy), ecart_type = as.numeric(et)), file.path(OUT, "buys_ballot.csv"), row.names = FALSE)
  write.csv(data.frame(pente = a, p_value = p, n_cycles = length(moy), modele = mod), file.path(OUT, "choix_modele.csv"), row.names = FALSE)
  say("-> modèle retenu : ", toupper(mod), "  (pente significativement > 0 => amplitude proportionnelle au niveau)")
  png_open("02_choix_modele.png", 1100, 450); par(mfrow = c(1, 2))
  plot(y, main = "Méthode de la bande (max / min de chaque cycle)", ylab = "")   # bande parallèle = additif ; en éventail = multiplicatif
  tc <- tapply(time(y)[full], cyc[full], min); lines(tc, tapply(as.numeric(y)[full], cyc[full], max), col = "red", type = "b", pch = 20)
  lines(tc, tapply(as.numeric(y)[full], cyc[full], min), col = "green4", type = "b", pch = 20)
  plot(moy, et, main = "Buys-Ballot : écart-type vs moyenne du cycle", xlab = "moyenne du cycle", ylab = "écart-type"); abline(lm(et ~ moy), col = "red"); dev.off()
  mod
}

decomposition <- function(y, model, tt = as.numeric(time(y))) {
  hdr(sprintf("ÉTAPE 6b — DÉCOMPOSITION (%s, période=%g)", model, frequency(y)))
  dec <- decompose(y, type = model); p <- frequency(y)
  say("Coefficients saisonniers : ", paste(round(head(dec$figure, 24), 3), collapse = " "), if (p > 24) " ...")
  say("Contrôle : ", if (model == "additive") "somme = " else "moyenne = ", round(if (model == "additive") sum(dec$figure) else mean(dec$figure), 4))
  mm <- ma(y, order = p, centre = TRUE); h <- p %/% 2   # moyenne mobile centrée "à la main" (comme TP02) vs decompose
  for (t in (h + 1):(h + 3)) say(sprintf("  MM t=%d : ma()=%.3f | decompose=%.3f", t, mm[t], dec$trend[t]))
  cvs <- if (model == "additive") y - dec$seasonal else y / dec$seasonal
  # tableaux chiffrés (lus par scripts/make_explanations.py pour écrire exemple_decomposition.md)
  ratio <- if (model == "additive") y - dec$trend else y / dec$trend; pos <- as.integer(cycle(y)); raw <- tapply(as.numeric(ratio), pos, mean, na.rm = TRUE)
  write.csv(data.frame(position = seq_along(raw), brute = as.numeric(raw), normalisee = dec$figure, n = as.numeric(tapply(!is.na(ratio), pos, sum))), file.path(OUT, "coefficients.csv"), row.names = FALSE)
  rows <- 1:(h + min(2 * p, 12))
  write.csv(data.frame(t = rows, temps = round(tt[rows], 2), y = as.numeric(y)[rows], tendance = as.numeric(dec$trend)[rows], ratio = as.numeric(ratio)[rows], position = pos[rows],
                       coef = dec$figure[pos[rows]], cvs = as.numeric(cvs)[rows], residu = as.numeric(dec$random)[rows]), file.path(OUT, "exemple_chiffre.csv"), row.names = FALSE)
  png_open("03_decomposition.png", 1100, 900); plot(dec); dev.off()
  png_open("04_cvs.png", 1100, 400); plot(y, col = "grey50", main = "Série brute vs CVS"); lines(cvs, col = "red"); dev.off()
  dec
}

# ---------------------------------------------------------------- étape 7 : résidus (TP04)
validate <- function(y, dec, model) {
  hdr("ÉTAPE 7 — VALIDATION DES RÉSIDUS")
  r <- as.numeric(na.omit(dec$random)); if (model == "multiplicative") r <- r - 1
  lb <- Box.test(r, lag = 10, type = "Ljung-Box"); sh <- shapiro.test(head(r, 5000))
  say(sprintf("moyenne=%.4g sd=%.4g | Ljung-Box p=%.4g (%s) | Shapiro p=%.4g (%s)", mean(r), sd(r), lb$p.value,
              if (lb$p.value < .05) "autocorrélés" else "bruit blanc plausible", sh$p.value, if (sh$p.value < .05) "non normaux" else "normaux"))
  ok <- which(!is.na(dec$random)); worst <- ok[order(-abs(r))[1:3]]
  say("3 observations les moins bien ajustées (temps ; valeur) : ", paste(sprintf("(%.2f ; %.2f)", time(y)[worst], y[worst]), collapse = " "))
  png_open("05_residus.png", 1200, 400); par(mfrow = c(1, 3)); plot(r, type = "l", main = "résidus"); abline(h = 0, col = "red")
  acf(r, main = "ACF des résidus"); qqnorm(r); qqline(r, col = "red"); dev.off()
}

# ---------------------------------------------------------------- étape 8 : prévisions (TP03-TP04)
# (a) tendance (lm sur la série CVS) + coefficients saisonniers
fc_decomposition <- function(train, h, period, model, trend = "linear", start_fit = 1) {
  deg <- c(mean = 0, linear = 1, quad = 2)[[trend]]; n <- length(train)
  if (period < 2) { cvs <- as.numeric(train); sf <- rep(0, h); mult <- FALSE }
  else { tr2 <- with_period(train, period); d <- decompose(tr2, type = model); mult <- model == "multiplicative"
         cvs <- if (mult) as.numeric(tr2 / d$seasonal) else as.numeric(tr2 - d$seasonal); sf <- d$figure[((n + 0:(h - 1)) %% period) + 1] }
  i <- start_fit:n; b <- lm.fit(outer(i, 0:deg, "^"), cvs[i])$coefficients   # tendance polynomiale de degré deg
  base <- as.numeric(outer(n + 1:h, 0:deg, "^") %*% b)
  if (mult) base * sf else base + sf
}

forecasting <- function(y, n_test, period, model, trend = "linear", smooth_seasonal = TRUE, arima = TRUE, max_p = 2, max_q = 2, tag = "") {
  hdr("ÉTAPE 8 — PRÉVISION (comparaison sur le jeu de test)")
  n <- length(y); train <- window(y, end = time(y)[n - n_test]); test <- window(y, start = time(y)[n - n_test + 1]); obs <- as.numeric(test)
  say(sprintf("train = %d obs. | test = %d obs. (de %.2f à %.2f)", n - n_test, n_test, time(y)[n - n_test + 1], tail(time(y), 1)))
  F <- list(); F[[if (period < 2) "Tendance seule (lm)" else "Décomposition (tendance + saison)"]] <- fc_decomposition(train, n_test, period, model, trend)
  # lissage exponentiel : LES, LED et, si saisonnier, Holt-Winters (comme TP03/TP04)
  les <- HoltWinters(train, beta = FALSE, gamma = FALSE); F[["LES"]] <- as.numeric(predict(les, n.ahead = n_test))
  led <- HoltWinters(train, gamma = FALSE);              F[["LED (Holt)"]] <- as.numeric(predict(led, n.ahead = n_test))
  say(sprintf("LES : alpha=%.3f | LED : alpha=%.3f beta=%.3f", les$alpha, led$alpha, led$beta))
  if (smooth_seasonal && period > 1 && period <= 24) {
    hw <- HoltWinters(train, seasonal = if (model == "multiplicative") "multiplicative" else "additive")
    F[["Holt-Winters"]] <- as.numeric(predict(hw, n.ahead = n_test))
    say(sprintf("Holt-Winters : alpha=%.3f beta=%.3f gamma=%.3f", hw$alpha, hw$beta, hw$gamma))
  }
  if (arima) {   # optionnel (hors cours) : auto.arima ; lambda=0 = travail sur le log si multiplicatif
    fit <- tryCatch(auto.arima(train, max.p = max_p, max.q = max_q, seasonal = (period > 1 && period <= 24), lambda = if (model == "multiplicative") 0 else NULL), error = function(e) NULL)
    if (!is.null(fit)) { nm <- sub("^Regression with ", "", as.character(fit)); say("auto.arima : ", nm); F[[nm]] <- as.numeric(forecast(fit, h = n_test)$mean) }
  }
  F[["Naïf"]] <- if (period > 1 && smooth_seasonal) as.numeric(tail(train, period))[((0:(n_test - 1)) %% period) + 1] else rep(as.numeric(tail(train, 1)), n_test)
  tab <- t(sapply(F, function(f) metrics(obs, f))); tab <- round(tab[order(tab[, "RMSE"]), , drop = FALSE], 3)
  say(paste(capture.output(print(tab)), collapse = "\n")); say("==> meilleure méthode (RMSE) : ", rownames(tab)[1])
  write.csv(tab, file.path(OUT, paste0("comparaison_previsions", tag, ".csv")))
  png_open(paste0("06_previsions", tag, ".png"), 1100, 450); lo <- max(1, n - n_test - 4 * max(period, 5)); tt <- as.numeric(time(y))
  plot(tt[lo:n], as.numeric(y)[lo:n], type = "l", lwd = 2, xlab = "temps", ylab = "", main = "Prévisions sur le jeu de test", ylim = range(c(as.numeric(y)[lo:n], unlist(F))))
  for (i in seq_along(F)) lines(tt[(n - n_test + 1):n], F[[i]], col = i + 1, lwd = 1.5)
  legend("topleft", c("observé", names(F)), col = c(1, seq_along(F) + 1), lty = 1, cex = .7); dev.off()
  list(F = F, table = tab, train = train, test = test)
}

# ---------------------------------------------------------------- pipeline complet
run_pipeline <- function(y, n_test, outdir, name = "série", period = NULL, model = "auto", trend = "linear", smooth_seasonal = TRUE,
                         sarima = TRUE, max_p = 2, max_q = 2, seasonal = TRUE, tag = "", fresh_log = TRUE) {
  if (fresh_log) init_out(outdir) else { OUT <<- outdir; dir.create(outdir, showWarnings = FALSE, recursive = TRUE) }
  period <- if (seasonal) (if (is.null(period)) frequency(y) else period) else 1
  explore(y, name); info <- run_tests(y); dec <- NULL
  if (period > 1) {
    yy <- with_period(y, period); chosen <- choose_model(yy, period)   # toujours calculé (informatif)
    if (model == "auto") model <- chosen else say("-> modèle IMPOSÉ dans solution.R : ", toupper(model), " (Buys-Ballot suggérait ", toupper(chosen), ")")
    dec <- decomposition(yy, model, as.numeric(time(y))); validate(y, dec, model)
  } else {
    model <- "additive"; hdr("Pas de saisonnalité : tendance (lm) + résidus")
    t <- as.numeric(time(y)); fit <- lm(as.numeric(y) ~ t); r <- resid(fit)
    say(sprintf("pente=%.4f ; sd résiduel=%.3f ; Ljung-Box p=%.4g ; Shapiro p=%.4g", coef(fit)[2], sd(r), Box.test(r, 10, "Ljung-Box")$p.value, shapiro.test(head(r, 5000))$p.value))
  }
  fc <- forecasting(y, n_test, period, model, trend, smooth_seasonal && seasonal, sarima, max_p, max_q, tag)
  save_log(tag); c(list(info = info, model = model, period = period, dec = dec, log = LOG), fc)
}

# ---------------------------------------------------------------- outils pour les questions ⭐
compare_add_mult <- function(y) {   # additif vs multiplicatif : erreur de reconstruction chiffrée
  hdr("Additif vs multiplicatif — critère chiffré")
  for (m in c("additive", "multiplicative")) {
    if (m == "multiplicative" && any(y <= 0)) { say("  multiplicatif impossible (valeurs <= 0)"); next }
    d <- decompose(y, type = m); fit <- if (m == "additive") d$trend + d$seasonal else d$trend * d$seasonal; e <- as.numeric((y - fit)[!is.na(fit)])
    say(sprintf("  %-15s RMSE=%.3f  MAPE=%.2f%%  autocorr(1) résidus=%.2f", m, sqrt(mean(e^2)), mean(abs(e / as.numeric(y)[!is.na(fit)])) * 100, cor(e[-1], e[-length(e)])))
  }
}
hw_compare <- function(y, n_test) {   # Holt-Winters multiplicatif brut vs additif sur log(y)
  hdr("Holt-Winters multiplicatif brut vs additif sur log(y)")
  n <- length(y); tr <- window(y, end = time(y)[n - n_test]); obs <- as.numeric(window(y, start = time(y)[n - n_test + 1]))
  f1 <- as.numeric(predict(HoltWinters(tr, seasonal = "multiplicative"), n.ahead = n_test))
  f2 <- exp(as.numeric(predict(HoltWinters(log(tr)), n.ahead = n_test)))
  for (k in c("HW multiplicatif (brut)", "HW additif sur log")) { m <- metrics(obs, if (grepl("brut", k)) f1 else f2); say(sprintf("  %-26s RMSE=%.3f MAE=%.3f MAPE=%.2f%%", k, m[1], m[2], m[3])) }
}
trend_break_compare <- function(y, n_test, period, model, start_fit) {   # tendance globale vs post-rupture
  hdr(sprintf("Tendance globale vs ajustée après la rupture (obs. >= %d)", start_fit))
  n <- length(y); tr <- window(y, end = time(y)[n - n_test]); obs <- as.numeric(window(y, start = time(y)[n - n_test + 1]))
  for (k in c("tendance globale", "tendance post-rupture")) { m <- metrics(obs, fc_decomposition(tr, n_test, period, model, "linear", if (k == "tendance globale") 1 else start_fit)); say(sprintf("  %-24s RMSE=%.3f MAPE=%.2f%%", k, m[1], m[3])) }
}
effect_of_break <- function(y, ntr, F, label = "effet de l'événement") {   # prévu sans l'événement - observé
  hdr(paste0(label, " = (prévu sans l'événement) - (observé), sur le test"))
  obs <- as.numeric(y)[(ntr + 1):length(y)]
  for (k in names(F)) say(sprintf("  %-40s écart cumulé=%9.1f  soit %5.1f%% du prévu", k, sum(F[[k]] - obs), sum(F[[k]] - obs) / sum(F[[k]]) * 100))
}
segment_pettitt <- function(y, t, min_len = 60, level = 0, lo = 0) {   # Pettitt récursif (ruptures successives)
  if (length(y) < 2 * min_len) return(invisible())
  pt <- pettitt.test(y); idx <- as.numeric(pt$estimate[1])
  if (pt$p.value < .05 && idx >= min_len && idx < length(y) - min_len) {
    say(strrep("  ", level), sprintf("rupture vers %.2f (p=%.3g)", t[lo + idx + 1], pt$p.value))
    segment_pettitt(y[1:idx], t, min_len, level + 1, lo); segment_pettitt(y[(idx + 1):length(y)], t, min_len, level + 1, lo + idx)
  }
}
