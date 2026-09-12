# Glossaire des symboles mathématiques — comment les lire en français

*Document de référence pour lire à voix haute et comprendre les notations utilisées dans la SAÉ 3.03 (séries chronologiques). Pensé pour quelqu'un qui maîtrise les maths mais pas le vocabulaire français associé. Toutes les lectures proposées sont celles qu'un enseignant ou un étudiant français dirait à l'oral.*

---

## 1. Notation générale (indices, exposants, accents)

| Symbole | Comment le lire à voix haute | Signification |
|---|---|---|
| $X_t$ | "X indice t" | La valeur de la variable $X$ à l'instant $t$. Le petit caractère en bas s'appelle un **indice** (subscript). |
| $X_{t+h}$ | "X indice t plus h" | Valeur de $X$, $h$ pas de temps après $t$. |
| $X_{t-k}$ | "X indice t moins k" | Valeur de $X$, $k$ pas de temps avant $t$. |
| $x^2$ | "x au carré" | Exposant 2 (puissance). |
| $x^n$ | "x puissance n" | Exposant général. |
| $\hat{m}_t$ | "m chapeau, indice t" | Le **chapeau** (^) au-dessus d'une lettre signifie "valeur **estimée**" (par opposition à la vraie valeur théorique). |
| $\bar{y}$ | "y barre" | La **barre** au-dessus d'une lettre signifie "**moyenne** de y". |
| $\bar{t}$ | "t barre" | Moyenne des valeurs de $t$. |
| $s_j^*$ | "s indice j, étoile" | L'**étoile** (*) signifie ici "coefficient **normalisé**" — une convention propre à ce cours, pas une règle universelle. |
| $X_t^*$ | "X indice t, étoile" | Série corrigée / ajustée (ici : série corrigée des variations saisonnières, CVS). |
| $\tilde{x}$ | "x tilde" | Le **tilde** (~) indique souvent une autre transformation (médiane, valeur modifiée) — variante moins utilisée dans ce cours. |
| $x'$ | "x prime" | Une variante de $x$, souvent une dérivée ou une deuxième version. |

**Règle générale de lecture** : on lit toujours de gauche à droite, en disant "indice" pour ce qui descend et "puissance" ou "exposant" pour ce qui monte. Le chapeau se lit toujours en dernier après la lettre : "m chapeau" et pas "chapeau m".

---

## 2. Opérations et relations

| Symbole | Comment le lire | Signification |
|---|---|---|
| $+$ | "plus" | Addition. |
| $-$ | "moins" | Soustraction. |
| $\times$ | "fois" ou "multiplié par" | Multiplication. |
| $\frac{a}{b}$ | "a sur b" | Fraction : $a$ divisé par $b$. |
| $\sum$ | "somme" | Symbole sigma majuscule : signifie "somme de". |
| $\sum_{i=-k}^{k}$ | "somme, pour i allant de moins k à k" | On additionne un terme pour chaque valeur de $i$, de $-k$ jusqu'à $k$. |
| $\sum_{i=1}^{N}$ | "somme, pour i allant de 1 à N" | Idem, de $1$ à $N$. |
| $=$ | "égal" | Égalité. |
| $\approx$ | "environ égal à" ou "à peu près égal à" | Égalité approximative. |
| $\neq$ | "différent de" | Non-égalité. |
| $\leq$ | "inférieur ou égal à" | Plus petit ou égal. |
| $\geq$ | "supérieur ou égal à" | Plus grand ou égal. |
| $<$ | "strictement inférieur à" | Plus petit (strict). |
| $>$ | "strictement supérieur à" | Plus grand (strict). |
| $\lvert x \rvert$ | "valeur absolue de x" | Distance de $x$ à zéro, toujours positive. |
| $\left( \dots \right)$ | "parenthèse... fin de parenthèse" (souvent non dit à l'oral, juste une pause) | Regroupe des termes. |
| $\dots$ | "points de suspension" ou "et ainsi de suite" | Continuation d'une liste ou d'une somme. |
| $\cdot$ | "fois" (multiplication discrète) | Utilisé parfois à la place de $\times$ dans les notations condensées. |

---

## 3. Lettres grecques utilisées dans ce cours

Les lettres grecques servent à nommer des **paramètres** ou des **coefficients**, jamais des données brutes. En français, on prononce le nom de la lettre, pas le son de la lettre latine la plus proche.

| Symbole | Nom en français | Prononciation | Rôle dans le cours |
|---|---|---|---|
| $\alpha$ | alpha | "al-fa" | Paramètre de lissage (niveau) dans Holt/Holt-Winters. |
| $\beta$ | bêta | "bé-ta" | Coefficient de la droite de tendance ($\beta_1$, $\beta_0$), ou constante de lissage selon le contexte. |
| $\gamma$ | gamma | "ga-ma" | Autocovariance $\gamma(k)$, ou paramètre de lissage saisonnier dans Holt-Winters. |
| $\mu$ | mu | "mu" (comme "mur" sans le r) | Moyenne théorique (espérance) d'une série. |
| $\rho$ | rhô | "ro" | Autocorrélation $\rho(k)$. |
| $\sigma$ | sigma | "sig-ma" | Écart-type (parfois $\sigma^2$ pour la variance). |
| $\tau$ | tau | "to" | Statistique du test de Mann-Kendall (tau de Kendall). |

**Astuce** : à l'oral, un professeur français dira "alpha", "bêta", "gamma"... jamais "a", "b", "c". Si vous entendez "bêta un" ou "bêta zéro", cela correspond à $\beta_1$ et $\beta_0$.

---

## 4. Symboles statistiques (espérance, variance, covariance)

| Symbole | Comment le lire | Signification |
|---|---|---|
| $\mathbb{E}[X]$ | "espérance de X" | Moyenne théorique attendue de la variable $X$. |
| $\text{var}(X)$ | "variance de X" | Mesure de dispersion autour de la moyenne. |
| $\text{cov}(X, Y)$ | "covariance de X et Y" | Mesure de la variation commune entre deux variables. |
| $\gamma(k)$ | "gamma de k" | Autocovariance au retard (décalage) $k$. |
| $\rho(k)$ | "rhô de k" | Autocorrélation au retard $k$ — c'est $\gamma(k)$ normalisée. |
| $\hat{\gamma}(k)$ | "gamma chapeau de k" | Estimateur (calculé sur les données) de l'autocovariance. |
| $\hat{\rho}(k)$ | "rhô chapeau de k" | Estimateur de l'autocorrélation. |

---

## 5. Symboles spécifiques aux séries temporelles (ce cours)

| Symbole | Comment le lire | Signification |
|---|---|---|
| $X_t$ | "X indice t" | Valeur observée de la série au temps $t$. |
| $m_t$ | "m indice t" | Composante de **tendance** au temps $t$ ("m" pour *moyenne mobile* ou *modèle*). |
| $s_t$ | "s indice t" | Composante **saisonnière** au temps $t$ ("s" pour *saisonnier*). |
| $e_t$ | "e indice t" | **Résidu** (bruit, erreur) au temps $t$. |
| $\hat{m}_t$ | "m chapeau, indice t" | Tendance **estimée**. |
| $\hat{s}_j$ | "s chapeau, indice j" | Coefficient saisonnier **brut estimé** pour la période $j$ (ex : le mois $j$). |
| $s_j^*$ | "s indice j, étoile" | Coefficient saisonnier **normalisé**. |
| $X_t^*$ | "X indice t, étoile" | Série **CVS** : "corrigée des variations saisonnières". |
| $p$ | "p" | La **période** de saisonnalité (ex : $p=12$ pour des données mensuelles). |
| $N$ | "grand N" | Le nombre total d'observations dans la série. |
| $k$ | "k" | Généralement la moitié de la période ($p = 2k$ ou $p = 2k+1$), ou un décalage (lag) dans l'ACF. |
| $m_{p,t}$ | "m indice p, t" | Moyenne mobile d'ordre $p$, calculée au temps $t$. |
| $\hat{x}_{T+h}$ | "x chapeau, indice T plus h" | **Prévision** de $x$ à l'horizon $h$, à partir du dernier point observé $T$. |
| $\hat{x}_T(h)$ | "x chapeau de T, entre parenthèses h" | Notation alternative : prévision faite à l'instant $T$, pour $h$ pas dans le futur. |
| $H_0$ | "H indice zéro" | **Hypothèse nulle** d'un test statistique. |
| $H_1$ | "H indice un" | **Hypothèse alternative**. |
| $p\text{-value}$ | "p-valeur" (ou "petit p") | Probabilité utilisée pour accepter/rejeter $H_0$ (seuil habituel : 0,05). |

---

## 6. Lire une formule complète à voix haute — exemples du cours

### Moyenne mobile centrée (période impaire)

$$m_{p,t} = \frac{1}{p} \sum_{i=-k}^{k} X_{t+i}$$

**Lecture** : *"m indice p, t, est égal à un sur p, fois la somme, pour i allant de moins k à k, de X indice t plus i."*

### Droite de tendance

$$\beta_1 = \frac{\text{cov}(m_{p,t}, t)}{\text{var}(t)}$$

**Lecture** : *"bêta un est égal à la covariance de m indice p t et t, sur la variance de t."*

### Coefficient saisonnier normalisé (modèle additif)

$$s_j^* = \hat{s}_j - \bar{s}$$

**Lecture** : *"s indice j étoile est égal à s chapeau indice j, moins s barre."*

### Série corrigée des variations saisonnières (modèle multiplicatif)

$$X_t^* = \frac{X_t}{s_t^*}$$

**Lecture** : *"X indice t étoile est égal à X indice t, sur s indice t étoile."*

### Autocorrélation

$$\rho(k) = \frac{\gamma(k)}{\gamma(0)}$$

**Lecture** : *"rhô de k est égal à gamma de k, sur gamma de zéro."*

### Prévision paramétrique multiplicative

$$\hat{x}_{T+h} = \hat{m}_{T+h} \times \hat{s}_{T+h}$$

**Lecture** : *"x chapeau, indice T plus h, est égal à m chapeau, indice T plus h, fois s chapeau, indice T plus h."*

---

## 7. Vocabulaire français utile (au-delà des symboles)

| Terme français | Signification / équivalent |
|---|---|
| **Série chronologique** / **série temporelle** | *Time series* |
| **Tendance** | *Trend* |
| **Saisonnalité** | *Seasonality* |
| **Résidu** / **aléa** | *Residual* / *noise* |
| **Moyenne mobile** | *Moving average* |
| **Moyenne mobile centrée** | *Centered moving average* |
| **Droite de tendance** | *Trend line* (régression linéaire de la tendance) |
| **Coefficient saisonnier** | *Seasonal coefficient/factor* |
| **CVS** (série corrigée des variations saisonnières) | *Seasonally adjusted series* |
| **Stationnarité** | *Stationarity* |
| **Rupture** | *Change point / break* |
| **Lissage exponentiel** | *Exponential smoothing* |
| **Prévision** | *Forecast* |
| **Horizon (de prévision)** | *Forecast horizon* |
| **Écart-type** | *Standard deviation* |
| **Retard** / **décalage** (en ACF) | *Lag* |
| **Bruit blanc** | *White noise* |
| **Test de stationnarité** | *Stationarity test* |
| **Seuil** (de décision, souvent 5 %) | *Threshold* |

---

## Notes

- Ce glossaire couvre les symboles présents dans `SAÉ 3-03 Time Series Forecasting Cheat Sheet - v3.md`. S'il apparaît un symbole non listé ici (ex. dans un TD ou un exercice), il suffit de repérer sa famille (indice, exposant, lettre grecque, opérateur) pour appliquer les mêmes règles de lecture.
- Les conventions de notation ($*$ pour "normalisé", chapeau pour "estimé") sont propres à ce cours — un autre enseignant ou un autre manuel pourrait utiliser des symboles différents pour les mêmes idées.
