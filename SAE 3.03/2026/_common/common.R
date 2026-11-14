# SAE 3.03 — pipeline commun (R) : exploration, tests, décomposition, validation, prévision.
# Chaque dossier de sujet a un `solution.R` : à lancer DEPUIS le dossier du sujet (Rscript solution.R).
# Packages : install.packages(c("forecast","tseries"))   (le reste = base R)

suppressPackageStartupMessages({ library(forecast); library(tseries) })
options(warn = -1)
ROOT <- normalizePath(file.path(getwd(), "..", ".."))        # .../SAE 3.03

# ---------------------------------------------------------------- sorties
OUT <- NULL; LOG <- character()
# ATTENTION : modifie la variable globale OUT. Si on enchaîne plusieurs run_pipeline,
# recalculer les chemins depuis getwd() (cf. SRT dans les solution.R), pas depuis OUT.
init_out <- function(dir) { OUT <<- dir; dir.create(dir, showWarnings = FALSE, recursive = TRUE); LOG <<- character() }
say <- function(...) { s <- paste0(..., collapse = ""); cat(s, "\n"); LOG <<- c(LOG, s) }
hdr <- function(s) say("\n", strrep("=", 70), "\n", s, "\n", strrep("=", 70))
save_log <- function(tag = "") writeLines(LOG, file.path(OUT, paste0("resultats", tag, ".txt")))
png_open <- function(name, w = 1100, h = 800) png(file.path(OUT, name), width = w, height = h, res = 110)
export_csv <- function(x, file) {   # exporte une série R en CSV time,value (lu par solution.py)
  dir.create(dirname(file), showWarnings = FALSE, recursive = TRUE)
  write.csv(data.frame(time = as.numeric(time(x)), value = as.numeric(x)), file, row.names = FALSE)
}

# ---------------------------------------------------------------- tests
mann_kendall <- function(x) {
  n <- length(x); s <- 0
  for (i in 1:(n - 1)) s <- s + sum(sign(x[(i + 1):n] - x[i]))
  tt <- table(x); v <- (n * (n - 1) * (2 * n + 5) - sum(tt * (tt - 1) * (2 * tt + 5))) / 18
  z <- if (s == 0) 0 else (s - sign(s)) / sqrt(v)
  list(S = s, Z = z, p = 2 * (1 - pnorm(abs(z))), tau = s / (n * (n - 1) / 2))
}
pettitt <- function(x) {
  n <- length(x); r <- rank(x); u <- 2 * cumsum(r) - (1:n) * (n + 1)
  k <- max(abs(u)); list(K = k, idx = which.max(abs(u)), p = min(1, 2 * exp(-6 * k^2 / (n^3 + n^2))))
}
cycle_means <- function(y) { f <- frequency(y); if (f == 1) return(as.numeric(y)); m <- floor(length(y) / f)
  colMeans(matrix(as.numeric(y)[1:(m * f)], nrow = f)) }

# ---------------------------------------------------------------- étapes
explore <- function(y, name) {
  hdr("ÉTAPES 3-4 — DESCRIPTION & EXPLORATION")
  say(sprintf("Série : %s | n=%d | fréquence=%g | début=%s | fin=%.2f", name, length(y), frequency(y),
              paste(start(y), collapse = "/"), tail(time(y), 1)))
  say("summary : ", paste(names(summary(y)), round(summary(y), 2), collapse = " | "), " | sd=", round(sd(y), 2), " | NA=", sum(is.na(y)))
  blk <- if (frequency(y) > 1) frequency(y) else 10; nb <- floor(length(y) / blk)
  m <- matrix(as.numeric(y)[1:(nb * blk)], nrow = blk)
  g <- data.frame(debut = round(time(y)[seq(1, nb * blk, by = blk)]), moyenne = colMeans(m), sd = apply(m, 2, sd), min = apply(m, 2, min), max = apply(m, 2, max))
  say("Descripteurs par ", if (frequency(y) > 1) "cycle" else "décennie", " :"); say(paste(capture.output(print(round(head(g, 40), 2), row.names = FALSE)), collapse = "\n"))
  nl <- min(max(2 * frequency(y), 24), floor(length(y) / 3))
  png_open("01_exploration.png", 1100, 1000); par(mfrow = c(3, 1))
  plot(y, main = name, ylab = ""); acf(y, lag.max = nl, main = "ACF"); pacf(y, lag.max = min(nl, floor(length(y) / 2) - 1), main = "PACF"); dev.off()
}

run_tests <- function(y) {
  hdr("ÉTAPE 5 — TESTS")
  a <- adf.test(y); say(sprintf("ADF : stat=%.3f p=%.4f -> %s", a$statistic, a$p.value,
        if (a$p.value < .05) "stationnaire (rejette H0 racine unitaire)" else "NON stationnaire (H0 racine unitaire conservée)"))
  say(sprintf("ADF sur la série différenciée : p=%.4f", adf.test(diff(y))$p.value))
  use_cm <- frequency(y) > 1 && floor(length(y) / frequency(y)) >= 6
  mk <- mann_kendall(if (use_cm) cycle_means(y) else as.numeric(y))
  say(sprintf("Mann-Kendall (%s) : tau=%.3f Z=%.2f p=%.4g -> %s", if (use_cm) "moyennes par cycle" else "série brute", mk$tau, mk$Z, mk$p,
        if (mk$p < .05) paste("tendance", if (mk$S > 0) "croissante" else "décroissante") else "pas de tendance monotone significative"))
  pt <- pettitt(as.numeric(y)); tb <- time(y)[min(pt$idx + 1, length(y))]
  say(sprintf("Pettitt : K=%.0f p=%.4g -> %s", pt$K, pt$p, if (pt$p < .05) sprintf("rupture de niveau vers %.2f", tb) else "pas de rupture significative"))
  list(adf_p = a$p.value, mk = mk, pettitt = pt, break_time = tb)
}

choose_model <- function(y, period) {
  hdr("ÉTAPE 6a — CHOIX ADDITIF / MULTIPLICATIF (Buys-Ballot)")
  m <- floor(length(y) / period)
  if (m < 3 || period < 2) { say("Pas assez de cycles : additif par défaut."); return("additive") }
  Y <- matrix(as.numeric(y)[1:(m * period)], nrow = period)
  mean_c <- colMeans(Y); sd_c <- apply(Y, 2, sd); fit <- summary(lm(sd_c ~ mean_c))
  a <- fit$coefficients[2, 1]; p <- fit$coefficients[2, 4]
  say(sprintf("Régression sd = a*moyenne + b : a=%.4f  p=%.4f  (n cycles=%d)", a, p, m))
  if (!all(y > 0)) { mod <- "additive"; say("-> modèle retenu : ADDITIF   (série avec valeurs nulles/négatives : multiplicatif impossible)") }
  else if (a > 0 && p < .05) { mod <- "multiplicative"; say("-> modèle retenu : MULTIPLICATIF   (pente significativement > 0 => amplitude proportionnelle au niveau)") }
  else { mod <- "additive"; say("-> modèle retenu : ADDITIF   (pente non significative => amplitude indépendante du niveau)") }
  png_open("02_choix_modele.png", 1100, 450); par(mfrow = c(1, 2))
  plot(y, main = "Méthode de la bande (max/min par cycle)")
  tt <- time(y)[seq(1, m * period, by = period)]; lines(tt, apply(Y, 2, max), col = "red", type = "b"); lines(tt, apply(Y, 2, min), col = "green4", type = "b")
  plot(mean_c, sd_c, main = "Buys-Ballot", xlab = "moyenne du cycle", ylab = "écart-type"); abline(lm(sd_c ~ mean_c), col = "red"); dev.off()
  mod
}

decomposition <- function(y, model) {
  hdr(sprintf("ÉTAPE 6b — DÉCOMPOSITION (%s, période=%g)", model, frequency(y)))
  dec <- decompose(y, type = model); p <- frequency(y); seas <- dec$figure
  if (p == 12) {   # alignés sur le début de la série -> étiqueter par mois réel
    m0 <- start(y)[2]
    say("Coefficients saisonniers (mois:valeur) : ",
        paste(sprintf("%d:%+.3f", ((m0 + seq_len(p) - 2) %% 12) + 1, round(head(seas, p), 3)), collapse = " "))
  } else {
    say("Coefficients saisonniers : ", paste(round(head(seas, 24), 3), collapse = " "), if (p > 24) " ..." else "")
  }
  say("Contrôle de normalisation : ", if (model == "additive") "somme = " else "moyenne = ", round(if (model == "additive") sum(seas) else mean(seas), 4))
  cvs <- if (model == "additive") y - dec$seasonal else y / dec$seasonal
  w <- if (p %% 2 == 0) c(.5, rep(1, p - 1), .5) / p else rep(1, p) / p; h <- length(w) %/% 2
  for (t in (h + 1):(h + 3)) say(sprintf("  MM centrée à la main t=%d : %.3f | decompose : %.3f", t, sum(w * y[(t - h):(t + h)]), dec$trend[t]))
  png_open("03_decomposition.png", 1100, 900); plot(dec); dev.off()
  png_open("04_cvs.png", 1100, 400); plot(y, main = "Brute vs CVS", col = "grey50"); lines(cvs, col = "red"); legend("topleft", c("brute", "CVS"), col = c("grey50", "red"), lty = 1); dev.off()
  list(dec = dec, cvs = cvs)
}

validate <- function(y, dec, model) {
  hdr("ÉTAPE 7 — VALIDATION DES RÉSIDUS")
  r <- as.numeric(na.omit(dec$random)); if (model == "multiplicative") r <- r - 1
  lb <- Box.test(r, lag = min(10, floor(length(r) / 5)), type = "Ljung-Box")
  say(sprintf("moyenne résidus=%.4g sd=%.4g", mean(r), sd(r)))
  say(sprintf("Ljung-Box : p=%.4g -> %s", lb$p.value, if (lb$p.value < .05) "résidus autocorrélés (structure restante)" else "pas d'autocorrélation (bruit blanc plausible)"))
  sh <- shapiro.test(head(r, 5000)); say(sprintf("Shapiro-Wilk : p=%.4g -> %s", sh$p.value, if (sh$p.value < .05) "non normaux" else "normalité non rejetée"))
  ok <- which(!is.na(dec$random)); worst <- ok[order(-abs(r))[1:3]]
  say("3 observations les plus mal ajustées (temps, valeur) : ", paste(sprintf("(%.2f ; %.2f)", time(y)[worst], y[worst]), collapse = " "))
  png_open("05_residus.png", 1200, 400); par(mfrow = c(1, 3)); plot(r, type = "l", main = "résidus"); abline(h = 0, col = "red"); acf(r, main = "ACF des résidus"); qqnorm(r); qqline(r, col = "red"); dev.off()
}

# ---------------------------------------------------------------- prévision
metrics <- function(y, f) { e <- y - f; nz <- y != 0; c(RMSE = sqrt(mean(e^2)), MAE = mean(abs(e)), MAPE = mean(abs(e[nz] / y[nz])) * 100) }

fc_decomposition <- function(train, h, period, model, trend = "linear", start_fit = 1) {
  t0 <- as.numeric(time(train)); deg <- c(mean = 0, linear = 1, quad = 2)[[trend]]
  tf <- tail(t0, 1) + (1:h) / frequency(train); mult <- FALSE; sf <- rep(0, h)
  if (period < 2) cvs <- as.numeric(train)
  else {
    tr2 <- if (period != frequency(train)) ts(as.numeric(train), frequency = period) else train
    dec <- decompose(tr2, type = model); mult <- model == "multiplicative"
    cvs <- if (mult) as.numeric(tr2 / dec$seasonal) else as.numeric(tr2 - dec$seasonal)
    sf <- dec$figure[((length(train) + 0:(h - 1)) %% period) + 1]
  }
  ii <- start_fit:length(t0); X <- outer(t0[ii] - t0[1], 0:deg, "^"); b <- solve(crossprod(X), crossprod(X, cvs[ii]))
  base <- as.numeric(outer(tf - t0[1], 0:deg, "^") %*% b)
  if (period < 2) base else if (mult) base * sf else base + sf
}

fc_smoothing <- function(train, h, period, model, seasonal = TRUE) {
  specs <- if (seasonal && period > 1 && period <= 24) {
    if (model == "multiplicative") c("MNM", "MAM", "MAM") else c("ANA", "AAA", "AAA") } else c("ANN", "AAN", "AAN")
  damp <- c(FALSE, FALSE, TRUE)   # 3e candidat = tendance amortie (le amortissement se règle par damped=TRUE, pas dans le code du modèle)
  best <- NULL; bestsc <- Inf
  for (k in seq_along(specs)) {
    s <- specs[k]
    m <- tryCatch(ets(train, model = s, damped = damp[k], restrict = FALSE), error = function(e) NULL); if (is.null(m)) next
    sc <- if (is.finite(m$aicc)) m$aicc else m$aic
    say(sprintf("  ets %-5s%s AICc=%10.2f  alpha=%.3f beta=%s gamma=%s", s, if (damp[k]) "(amorti)" else "", sc, m$par["alpha"],
                if ("beta" %in% names(m$par)) round(m$par["beta"], 3) else "-", if ("gamma" %in% names(m$par)) round(m$par["gamma"], 3) else "-"))
    if (sc < bestsc) { best <- m; bestsc <- sc } }
  if (seasonal && period > 24) { hw <- HoltWinters(train, beta = FALSE); say("  HoltWinters (période longue) alpha=", round(hw$alpha, 3), " gamma=", round(hw$gamma, 3))
    return(list(name = "HoltWinters", f = as.numeric(predict(hw, n.ahead = h)))) }
  say("  -> lissage retenu (AICc minimal) : ", best$method)
  list(name = best$method, f = as.numeric(forecast(best, h = h)$mean))
}

fc_arima <- function(train, h, period, model, sarima = TRUE, max_p = 2, max_q = 2) {
  use_log <- model == "multiplicative" && all(train > 0); z <- if (use_log) log(train) else train
  d <- if (adf.test(z)$p.value < .05) 0 else 1; seas <- sarima && period >= 2 && period <= 24; D <- if (seas) 1 else 0
  sg <- if (seas) list(c(0, 1), c(1, 0), c(1, 1)) else list(c(0, 0)); best <- NULL
  for (p in 0:max_p) for (q in 0:max_q) for (s in sg) {
    m <- tryCatch(Arima(z, order = c(p, d, q), seasonal = if (seas) list(order = c(s[1], D, s[2]), period = period) else c(0, 0, 0),
                        include.constant = (d == 0 && D == 0)), error = function(e) NULL)
    if (!is.null(m) && (is.null(best) || m$aic < best$aic)) best <- m }
  if (is.null(best)) stop("ARIMA : aucun modèle de la grille n'a convergé")
  nm <- paste0("ARIMA", paste0("(", paste(best$arma[c(1, 6, 2)], collapse = ","), ")"), if (seas) sprintf("x(%d,%d,%d)[%d]", best$arma[3], best$arma[7], best$arma[4], period) else "", if (use_log) " sur log" else "")
  say("  modèle retenu (AIC minimal, d par ADF) : ", nm, "  AIC=", round(best$aic, 1))
  f <- as.numeric(forecast(best, h = h)$mean); list(name = nm, f = if (use_log) exp(f) else f)
}

forecasting <- function(y, n_test, period, model, trend = "linear", smooth_seasonal = TRUE, sarima = TRUE, max_p = 2, max_q = 2, tag = "") {
  hdr("ÉTAPE 8 — PRÉVISION (comparaison sur le jeu de test)")
  n <- length(y); ntr <- n - n_test
  train <- window(y, end = time(y)[ntr]); test <- window(y, start = time(y)[ntr + 1]); yt <- as.numeric(test)
  say(sprintf("train = %d obs. (jusqu'à %.2f) | test = %d obs. (de %.2f à %.2f)", ntr, time(y)[ntr], n_test, time(y)[ntr + 1], tail(time(y), 1)))
  F <- list(); F[["Décomposition"]] <- fc_decomposition(train, n_test, period, model, trend)
  say("Lissage exponentiel :"); s <- fc_smoothing(train, n_test, period, model, smooth_seasonal && period > 1); F[[paste("Lissage:", s$name)]] <- s$f
  say("Modèle ARIMA :"); a <- fc_arima(train, n_test, period, model, sarima, max_p, max_q); F[[a$name]] <- a$f
  if (period < 2 || !smooth_seasonal) F[["Naïf (dernière valeur)"]] <- rep(as.numeric(tail(train, 1)), n_test)
  else F[["Naïf saisonnier"]] <- as.numeric(tail(train, period))[((0:(n_test - 1)) %% period) + 1]
  tab <- t(sapply(F, function(f) metrics(yt, f))); tab <- round(tab[order(tab[, "RMSE"]), , drop = FALSE], 3)
  say(paste(capture.output(print(tab)), collapse = "\n")); say("==> meilleure méthode (RMSE) : ", rownames(tab)[1])
  write.csv(tab, file.path(OUT, paste0("comparaison_previsions", tag, ".csv")))
  png_open(paste0("06_previsions", tag, ".png"), 1100, 450); lo <- max(1, ntr - 4 * max(period, 5))
  tt <- as.numeric(time(y)); plot(tt[lo:n], as.numeric(y)[lo:n], type = "l", lwd = 2, xlab = "temps", ylab = "", main = "Prévisions sur le jeu de test", ylim = range(c(as.numeric(y)[lo:n], unlist(F))))
  for (i in seq_along(F)) lines(tt[(ntr + 1):n], F[[i]], col = i + 1, lwd = 1.5)
  abline(v = tt[ntr + 1], lty = 3); legend("topleft", c("observé", names(F)), col = c(1, seq_along(F) + 1), lty = 1, cex = .7); dev.off()
  list(F = F, table = tab, train = train, test = test)
}

run_pipeline <- function(y, n_test, outdir, name = "série", period = NULL, model = "auto", trend = "linear", smooth_seasonal = TRUE,
                         sarima = TRUE, max_p = 2, max_q = 2, seasonal = TRUE, tag = "", fresh_log = TRUE) {
  # fresh_log=FALSE : continuer le LOG global déjà initialisé (plusieurs parties dans un même resultats.txt)
  if (fresh_log) init_out(outdir) else { OUT <<- outdir; dir.create(OUT, showWarnings = FALSE, recursive = TRUE) }
  period <- if (seasonal) (if (is.null(period)) frequency(y) else period) else 1
  explore(y, name); info <- run_tests(y); dec <- NULL
  if (period > 1) {
    yy <- if (period != frequency(y)) ts(as.numeric(y), start = start(y), frequency = period) else y
    if (model == "auto") model <- choose_model(yy, period)
    d <- decomposition(yy, model); validate(y, d$dec, model); dec <- d$dec
  } else {
    model <- "additive"; hdr("Pas de saisonnalité : décomposition = tendance (régression) + résidus")
    t <- as.numeric(time(y)); fit <- lm(as.numeric(y) ~ t); r <- resid(fit)
    say(sprintf("Tendance linéaire : pente=%.4f ; sd résiduel=%.3f", coef(fit)[2], sd(r)))
    say(sprintf("Résidus — Ljung-Box p=%.4g, Shapiro p=%.4g", Box.test(r, 10, "Ljung-Box")$p.value, shapiro.test(head(r, 5000))$p.value))
  }
  fc <- forecasting(y, n_test, period, model, trend, smooth_seasonal && seasonal, sarima, max_p, max_q, tag)
  save_log(tag); c(list(info = info, model = model, period = period, dec = dec, log = LOG), fc)
}

# ---------------------------------------------------------------- outils d'extension (questions ⭐)
compare_add_mult <- function(y) {
  hdr("Additif vs multiplicatif — critère chiffré (reconstruction tendance ⊕ saison)")
  for (m in c("additive", "multiplicative")) {
    if (m == "multiplicative" && any(y <= 0)) { say("  multiplicatif impossible (valeurs <= 0)"); next }
    d <- decompose(y, type = m); fit <- if (m == "additive") d$trend + d$seasonal else d$trend * d$seasonal
    ok <- !is.na(fit); e <- as.numeric((y - fit)[ok])
    say(sprintf("  %-15s RMSE=%.3f  MAPE=%.2f%%  autocorr(1) des résidus=%.2f", m, sqrt(mean(e^2)), mean(abs(e / as.numeric(y)[ok])) * 100, cor(e[-1], e[-length(e)])))
  }
}
hw_compare <- function(y, n_test) {
  hdr("Holt-Winters multiplicatif brut vs additif sur log(y) (retransformé par exp)")
  n <- length(y); tr <- window(y, end = time(y)[n - n_test]); yt <- as.numeric(window(y, start = time(y)[n - n_test + 1]))
  f1 <- as.numeric(forecast(ets(tr, model = "MAM"), h = n_test)$mean)
  f2 <- exp(as.numeric(forecast(ets(log(tr), model = "AAA", damped = FALSE), h = n_test)$mean))
  for (k in c("HW multiplicatif (brut)", "HW additif sur log")) { m <- metrics(yt, if (grepl("brut", k)) f1 else f2); say(sprintf("  %-26s RMSE=%.3f MAE=%.3f MAPE=%.2f%%", k, m[1], m[2], m[3])) }
}
trend_break_compare <- function(y, n_test, period, model, start_fit) {
  hdr(sprintf("Tendance globale vs tendance ajustée après la rupture (obs. >= %d)", start_fit))
  n <- length(y); tr <- window(y, end = time(y)[n - n_test]); yt <- as.numeric(window(y, start = time(y)[n - n_test + 1]))
  for (k in c("tendance globale", "tendance post-rupture")) { s <- if (k == "tendance globale") 1 else start_fit
    m <- metrics(yt, fc_decomposition(tr, n_test, period, model, "linear", s)); say(sprintf("  %-24s RMSE=%.3f MAPE=%.2f%%", k, m[1], m[3])) }
}
effect_of_break <- function(y, ntr, F, label = "effet de l'événement") {
  hdr(paste0(label, " = (prévu sans l'événement) − (observé), sur le test"))
  yt <- as.numeric(y)[(ntr + 1):length(y)]
  for (k in names(F)) say(sprintf("  %-40s écart cumulé=%9.1f   soit %5.1f%% du prévu", k, sum(F[[k]] - yt), sum(F[[k]] - yt) / sum(F[[k]]) * 100))
}
segment_pettitt <- function(y, t, min_len = 60, level = 0, lo = 0) {
  if (length(y) < 2 * min_len) return(invisible())
  r <- pettitt(y)
  if (r$p < .05 && r$idx >= min_len && r$idx < length(y) - min_len) {
    say(strrep("  ", level), sprintf("rupture vers %.2f (p=%.3g)", t[lo + r$idx + 1], r$p))
    segment_pettitt(y[1:r$idx], t, min_len, level + 1, lo); segment_pettitt(y[(r$idx + 1):length(y)], t, min_len, level + 1, lo + r$idx)
  }
}
