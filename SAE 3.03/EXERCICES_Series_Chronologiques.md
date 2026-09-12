# SAE3.03 — Exercices d'entraînement (Séries Chronologiques)

*Compagnon du guide `GUIDE_ENSEIGNANT_Series_Chronologiques.md`. Exercices à faire à la main (papier/calculatrice), dans le même esprit que les TD. Les corrigés sont regroupés à la fin, séparés des énoncés, pour pouvoir distribuer ce fichier tel quel à des étudiants.*

**Comment l'utiliser** : fais chaque série d'exercices juste après avoir relu la section correspondante du guide. Ne regarde le corrigé qu'après avoir essayé — c'est la partie qui reconstruit vraiment l'intuition.

---

## Sommaire

0. Quiz de rappel rapide (théorie, sans calcul)
1. Choix du modèle (additif / multiplicatif)
2. Moyennes mobiles
3. Droite de tendance
4. Coefficients saisonniers & CVS
5. Prévision par décomposition
6. Lissage exponentiel simple (LES)
7. Lissage exponentiel double (Holt)
8. Holt-Winters
9. Choix de la constante de lissage
10. Exercice de synthèse (type projet)
11. **Corrigés**

---

## 0. Quiz de rappel rapide

Réponds en une phrase, sans regarder le guide. (Corrigés en §11.0)

1. Pourquoi l'ordre des observations est-il essentiel dans une série chronologique, contrairement à un échantillon statistique classique ?
2. Cite les trois composantes d'une série chronologique et donne leur symbole.
3. Quelle est la différence entre un modèle additif et un modèle multiplicatif ?
4. Pourquoi force-t-on les coefficients saisonniers à avoir une moyenne nulle (modèle additif) ou une moyenne égale à 1 (modèle multiplicatif) ?
5. Une moyenne mobile d'ordre $p$ élimine-t-elle toute saisonnalité, ou seulement celle de période $p$ ?
6. Pourquoi une moyenne mobile n'est-elle pas directement utilisable pour prévoir le futur ?
7. Que veut dire "$\beta$ proche de 1" pour un lissage exponentiel simple : prévision souple ou rigide ?
8. Cite un avantage et un inconvénient du lissage exponentiel par rapport à un modèle probabiliste (type ARIMA).
9. Pourquoi ne doit-on jamais évaluer une prévision sur les données ayant servi à l'ajuster ?
10. Le lissage de Holt (double) suppose quelle forme de tendance ? Et Holt-Winters saisonnier additif ?

---

## 1. Choix du modèle (méthode de Buys-Ballot)

### Exercice 1.1 — Facile
Ventes trimestrielles sur 3 ans donnent les couples (moyenne annuelle $\bar Y$, écart-type annuel $s_Y$) suivants : (200, 40), (240, 41), (290, 39).
Le modèle est-il additif ou multiplicatif ? Justifie sans calcul de régression, juste par lecture des chiffres.

### Exercice 1.2 — Régression complète
Sur 4 ans, on a : (100, 10), (130, 15), (160, 19), (190, 24).
a. Calcule $\bar{\bar Y}$ et $\bar{s_Y}$ (moyennes des deux colonnes).
b. Calcule la pente $a$ de la droite $s_Y = a\bar Y + b$ avec $a = \dfrac{\text{Cov}(\bar Y, s_Y)}{\text{Var}(\bar Y)}$.
c. Conclus : additif ou multiplicatif ?

### Exercice 1.3 — Lecture de graphique
On te montre un graphique où les pics et creux d'une série s'écartent de plus en plus l'un de l'autre au fil du temps (méthode de la bande : les deux lignes divergent). Quel modèle choisis-tu ? Cite une deuxième méthode (autre que la bande) qui confirmerait ton choix, et décris ce que tu observerais avec elle.

---

## 2. Moyennes mobiles

### Exercice 2.1 — Ordre impair
Soit $x_1,\dots,x_5 = 12, 15, 11, 18, 20$. Calcule la moyenne mobile centrée d'ordre $p=3$ en $t=2$, $t=3$ et $t=4$.

### Exercice 2.2 — Ordre pair
Soit $x_1,\dots,x_7 = 8, 12, 15, 10, 14, 18, 13$ (données trimestrielles, $p=4$). Calcule $m_{4,3}$, $m_{4,4}$ et $m_{4,5}$. Combien de valeurs de la série lisses sont "perdues" à chaque extrémité ?

### Exercice 2.3 — Comprendre les propriétés
Une série a une tendance exactement linéaire $x_t = 5 + 2t$ (sans bruit ni saisonnalité). Sans calcul, donne la valeur de $m_{5,10}$ (moyenne mobile d'ordre 5 en $t=10$). Quelle propriété du cours justifie ta réponse ?

### Exercice 2.4 — Effet sur la saisonnalité
Une série a une composante saisonnière de période 12 (mensuelle) superposée à une tendance constante. On calcule une moyenne mobile d'ordre $p=4$ (pas 12). La saisonnalité va-t-elle disparaître complètement ? Justifie.

---

## 3. Droite de tendance

### Exercice 3.1
Après calcul d'une moyenne mobile, on obtient les 5 points suivants (t, $m_{p,t}$) : (1, 20), (2, 23), (3, 27), (4, 29), (5, 34).
a. Calcule $\bar t$ et $\overline{m_{p,t}}$.
b. Calcule $\beta_1 = \dfrac{\text{Cov}(m_{p,t},t)}{\text{Var}(t)}$ puis $\beta_0$.
c. Donne l'équation de la droite de tendance et prédis la valeur tendancielle en $t=8$.

---

## 4. Coefficients saisonniers & CVS

### Exercice 4.1 — Modèle additif
Données trimestrielles sur 2 ans : 2023 = (40, 65, 70, 45), 2024 = (44, 69, 74, 49). La moyenne mobile d'ordre 4 donne $\hat m_t \approx 57$ pour tous les trimestres (tendance quasi constante, pour simplifier).
a. Calcule le coefficient saisonnier brut $\hat s_t$ pour chaque trimestre (moyenne de $x_t - \hat m_t$ sur les deux années).
b. Vérifie que la somme des 4 coefficients bruts n'est pas nécessairement nulle ; centre-les pour obtenir $s_t^*$.
c. Calcule la série CVS pour le T3 de chaque année.

### Exercice 4.2 — Modèle multiplicatif
Mêmes données que 4.1, mais on suppose un modèle multiplicatif avec $\hat m_t \approx 57$ constant.
a. Calcule les rapports $x_t/\hat m_t$ pour chaque trimestre-année.
b. Calcule le coefficient saisonnier brut $\hat s_t$ (moyenne des rapports par trimestre).
c. Normalise pour que la moyenne des 4 coefficients vaille 1.
d. Calcule la CVS pour le T2 2024.

---

## 5. Prévision par décomposition

### Exercice 5.1
On a estimé la droite de tendance $\hat m_t = 2.1t + 30$ et les coefficients saisonniers additifs centrés : $s_1^*=-4$, $s_2^*=3$, $s_3^*=6$, $s_4^*=-5$ (trimestres 1 à 4).
a. Prévoit $\hat x_{21}$ sachant que $t=21$ correspond au trimestre 1.
b. Prévoit $\hat x_{22}$ (trimestre 2).
c. Refais le calcul en supposant un modèle multiplicatif avec les mêmes $\hat m_t$ mais des coefficients $s_1^*=0.85$, $s_2^*=1.05$.

---

## 6. Lissage exponentiel simple (LES)

### Exercice 6.1
Données : $x_1=50, x_2=54, x_3=49, x_4=58, x_5=55$. Avec $\beta=0.6$ et $\hat x_1(1)=x_1=50$, calcule $\hat x_2(1)$ à $\hat x_5(1)$ par la formule récursive $\hat x_T(1) = \beta \hat x_{T-1}(1) + (1-\beta)x_T$. Quelle est la prévision pour la période 6 ?

### Exercice 6.2 — Comparaison de deux $\beta$
Reprends les mêmes données avec $\beta=0.2$ cette fois. Compare les trajectoires de $\hat x_T(1)$ obtenues avec $\beta=0.2$ et $\beta=0.6$ : laquelle réagit le plus vite aux variations de $x_t$ ? Relie ta réponse aux notions de prévision "souple" et "rigide".

---

## 7. Lissage exponentiel double (Holt)

### Exercice 7.1
Données mensuelles : $x_1=100, x_2=108$. Initialise $\hat a_2 = x_2-x_1$ et $\hat b_2=x_2$.
Avec $\beta=0.5$ et $x_3=118$ :
a. Calcule $\hat x_2(1) = \hat a_2 + \hat b_2$.
b. Calcule $\hat a_3$ et $\hat b_3$ avec les formules de mise à jour du cours.
c. Donne la prévision $\hat x_3(1)$.

---

## 8. Holt-Winters

### Exercice 8.1 — Conceptuel
Pour chacune des situations suivantes, indique quelle méthode de lissage exponentiel est adaptée (LES, Holt, Holt-Winters non saisonnier, ou Holt-Winters saisonnier additif) :
a. Ventes mensuelles globalement stables, sans tendance ni saison marquée.
b. Trafic aérien avec une nette tendance croissante, pas de saisonnalité (déjà désaisonnalisé).
c. Ventes trimestrielles avec tendance croissante ET pic récurrent chaque T4, d'amplitude à peu près constante d'une année sur l'autre.
d. Même cas que (c) mais où le pic de T4 devient de plus en plus grand à mesure que le niveau général augmente.

### Exercice 8.2 — Mise à jour saisonnière (additive)
Pour Holt-Winters saisonnier additif, écris de mémoire les trois équations de mise à jour ($\hat a_T$, $\hat b_T$, $\hat S_T$) et explique en une phrase chacune ce qu'elle "moyenne" (nouvelle évidence vs. ancienne croyance).

---

## 9. Choix de la constante de lissage

### Exercice 9.1
On a testé $\alpha=0.3$ et $\alpha=0.7$ sur une série et obtenu les erreurs de prévision suivantes (valeur réelle − prévision) sur 4 points test :

| $\alpha=0.3$ | 2, -1, 3, -2 |
|---|---|
| $\alpha=0.7$ | 5, -4, 1, 0 |

a. Calcule EM, EAM et EQM pour chaque $\alpha$.
b. Lequel des deux $\alpha$ choisirais-tu si tu optimises l'EQM ? Et si tu optimises l'EAM ?
c. Que signifierait un EM proche de 0 mais un EQM élevé ?

---

## 10. Exercice de synthèse (type mini-projet)

Choisis (ou invente) une série trimestrielle ou mensuelle de 3-4 ans (ex : ventes d'un produit saisonnier, consommation électrique, fréquentation d'un site). Sans utiliser de logiciel :

1. Trace-la (à la main ou sur papier millimétré) et détermine si le modèle est additif ou multiplicatif avec **deux méthodes** parmi les trois vues en cours.
2. Calcule une moyenne mobile centrée d'ordre égal à la période.
3. Ajuste une droite de tendance sur la moyenne mobile.
4. Calcule les coefficients saisonniers et la série CVS.
5. Prévois les 2 prochaines périodes par décomposition.
6. Calcule aussi une prévision par LES (choisis un $\beta$ "raisonnable" selon la méthode subjective) et compare les deux prévisions.

*C'est une version condensée du Projet (10h). Fais-le sur une petite série (12-16 points) pour que ça reste faisable à la main.*

---

## 11. Corrigés

### 11.0 — Quiz de rappel

1. Parce que la dépendance entre observations consécutives *est* l'information qu'on cherche à modéliser ; mélanger les points détruit ce lien (contrairement à un échantillon i.i.d. où l'ordre n'a pas de sens).
2. Tendance $m_t$, composante saisonnière $s_t$, résidu/aléa $e_t$.
3. Additif : l'amplitude saisonnière reste constante quel que soit le niveau de la série ($x_t=m_t+s_t+e_t$). Multiplicatif : l'amplitude saisonnière croît proportionnellement au niveau ($x_t=m_t\times s_t\times e_t$).
4. Pour lever l'ambiguïté : un décalage constant pourrait toujours être absorbé soit par la tendance, soit par la saisonnalité. Fixer la moyenne (0 ou 1) rend la décomposition unique.
5. Seulement celle de période $p$ (et ses multiples) ; une saisonnalité de période différente ne serait pas annulée.
6. Parce qu'elle "perd" $k$ points à chaque extrémité de la série (fenêtre non calculable près des bords) — donc pas de valeur disponible aux dates les plus récentes, là où on aurait justement besoin d'extrapoler.
7. Rigide (le lissage "oublie" lentement, il réagit peu aux nouvelles observations).
8. Avantage : peu coûteux, rapide, pas de ré-estimation complète à chaque nouvelle donnée. Inconvénient : pas d'optimalité garantie, pas d'intervalle de prévision (pas de cadre probabiliste).
9. Parce qu'un modèle ajusté sur les mêmes données qu'il prédit paraît toujours artificiellement bon (sur-ajustement) ; seul un test sur des données non vues mesure la vraie capacité prédictive.
10. Holt (double) suppose une tendance linéaire sans saison ($x_t=b+at+e_t$). Holt-Winters saisonnier additif suppose tendance linéaire + saison additive ($x_t=b+at+s_t+e_t$).

### 11.1 — Choix du modèle

**1.1** : l'écart-type reste presque constant (40→41→39) alors que la moyenne augmente nettement (200→290) → pente $a\approx 0$ → **modèle additif**.

**1.2**
a. $\bar{\bar Y} = \frac{100+130+160+190}{4}=145$, $\bar{s_Y}=\frac{10+15+19+24}{4}=17$.
b. Écarts $\bar Y-\bar{\bar Y}$: -45,-15,15,45 ; écarts $s_Y-\bar{s_Y}$: -7,-2,2,7.
Cov $\propto \sum(\bar Y_i-\bar{\bar Y})(s_{Y,i}-\bar{s_Y}) = (-45)(-7)+(-15)(-2)+15(2)+45(7) = 315+30+30+315=690$ (somme des produits, /4 pour la covariance = 172.5).
Var$(\bar Y) \propto \sum(\bar Y_i-\bar{\bar Y})^2 = 2025+225+225+2025=4500$ (/4 = 1125).
$a = 172.5/1125 \approx 0.153$.
c. $a\ne 0$, nettement positif → **modèle multiplicatif** (l'écart-type croît avec le niveau).

**1.3** : lignes qui divergent → **multiplicatif**. Deuxième méthode possible : méthode du profil — en superposant une courbe par année (axe x = trimestre 1 à 4), on observerait des pics de plus en plus prononcés au fil des années (au lieu de courbes parallèles).

### 11.2 — Moyennes mobiles

**2.1** ($p=3$, impair, $k=1$): $m_{3,t}=\frac{x_{t-1}+x_t+x_{t+1}}{3}$.
- $m_{3,2}=\frac{12+15+11}{3}=\frac{38}{3}\approx12.67$
- $m_{3,3}=\frac{15+11+18}{3}=\frac{44}{3}\approx14.67$
- $m_{3,4}=\frac{11+18+20}{3}=\frac{49}{3}\approx16.33$

**2.2** ($p=4$, pair, $k=2$): $m_{4,t}=\dfrac{\tfrac{x_{t-2}}{2}+x_{t-1}+x_t+x_{t+1}+\tfrac{x_{t+2}}{2}}{4}$.
- $m_{4,3}=\dfrac{4+12+15+10+7}{4}=\dfrac{38}{4}=9.5$ (avec $x_1/2=4$, $x_5/2=7$)
- $m_{4,4}=\dfrac{6+15+10+14+9}{4}=\dfrac{54}{4}=13.5$ (avec $x_2/2=6$, $x_6/2=9$)
- $m_{4,5}=\dfrac{7.5+10+14+18+6.5}{4}=\dfrac{56}{4}=14$ (avec $x_3/2=7.5$, $x_7/2=6.5$)
On perd $k=2$ points à chaque extrémité (ici : $t=1,2$ au début et $t=6,7$ à la fin ne peuvent pas être calculés avec $p=4$ sur seulement 7 points ; seuls $t=3,4,5$ sont calculables).

**2.3** : $m_{5,10} = 5+2(10) = 25$, exactement la valeur de la tendance en $t=10$. Propriété utilisée : une moyenne mobile **préserve exactement une tendance linéaire**.

**2.4** : Non, elle ne disparaît pas complètement. Une moyenne mobile d'ordre $p$ élimine uniquement la saisonnalité de période $p$ (et ses multiples). Ici $p=4 \ne 12$, donc la composante saisonnière de période 12 n'est pas annulée par construction — il faudrait $p=12$.

### 11.3 — Droite de tendance

**3.1**
a. $\bar t = 3$, $\overline{m_{p,t}} = \frac{20+23+27+29+34}{5}=26.6$.
b. Écarts $t-\bar t$: -2,-1,0,1,2 ; écarts $m-\overline m$: -6.6,-3.6,0.4,2.4,7.4.
Somme des produits: $(-2)(-6.6)+(-1)(-3.6)+0+1(2.4)+2(7.4) = 13.2+3.6+0+2.4+14.8=34$.
Somme des $(t-\bar t)^2 = 4+1+0+1+4=10$.
$\beta_1 = 34/10 = 3.4$. $\beta_0 = 26.6-3.4(3)=26.6-10.2=16.4$.
c. $\hat m_t = 3.4t+16.4$. En $t=8$: $\hat m_8 = 3.4(8)+16.4=27.2+16.4=43.6$.

### 11.4 — Coefficients saisonniers & CVS

**4.1**
a. Écarts $x_t-\hat m_t$ : T1: $40-57=-17$, $44-57=-13$ → moy $-15$. T2: $65-57=8$, $69-57=12$ → moy $10$. T3: $70-57=13$, $74-57=17$ → moy $15$. T4: $45-57=-12$, $49-57=-8$ → moy $-10$.
b. Somme des coefficients bruts: $-15+10+15-10=0$ → déjà centrés ici (cas favorable), donc $s_t^*=\hat s_t$: $s_1^*=-15, s_2^*=10, s_3^*=15, s_4^*=-10$.
c. CVS T3 : $x_{T3,2023}^* = 70-15=55$ ; $x_{T3,2024}^*=74-15=59$.

**4.2**
a. Rapports $x_t/57$: T1: $40/57\approx0.702$, $44/57\approx0.772$. T2: $65/57\approx1.140$, $69/57\approx1.211$. T3: $70/57\approx1.228$, $74/57\approx1.298$. T4: $45/57\approx0.789$, $49/57\approx0.860$.
b. Moyennes par trimestre : $\hat s_1\approx0.737$, $\hat s_2\approx1.175$, $\hat s_3\approx1.263$, $\hat s_4\approx0.825$.
c. Moyenne des 4 coefficients : $\bar s = (0.737+1.175+1.263+0.825)/4 \approx 1.000$ (déjà ≈1 ici) → $s_t^*\approx\hat s_t$ inchangés.
d. CVS T2 2024 : $x^*_{T2,2024}=69/1.175\approx58.7$.

### 11.5 — Prévision par décomposition

**5.1**
a. $\hat m_{21}=2.1(21)+30=44.1+30=74.1$. $\hat x_{21}=74.1+s_1^*=74.1-4=70.1$.
b. $\hat m_{22}=2.1(22)+30=46.2+30=76.2$. $\hat x_{22}=76.2+3=79.2$.
c. Multiplicatif : $\hat x_{21}=74.1\times0.85=62.985$ ; $\hat x_{22}=76.2\times1.05=80.01$.

### 11.6 — LES

**6.1** ($\beta=0.6$):
- $\hat x_2(1)=0.6(50)+0.4(54)=30+21.6=51.6$
- $\hat x_3(1)=0.6(51.6)+0.4(49)=30.96+19.6=50.56$
- $\hat x_4(1)=0.6(50.56)+0.4(58)=30.336+23.2=53.536$
- $\hat x_5(1)=0.6(53.536)+0.4(55)=32.1216+22=54.1216$
Prévision pour la période 6 : $\hat x_6\approx54.12$.

**6.2** ($\beta=0.2$, pour comparaison):
- $\hat x_2(1)=0.2(50)+0.8(54)=10+43.2=53.2$
- $\hat x_3(1)=0.2(53.2)+0.8(49)=10.64+39.2=49.84$
- $\hat x_4(1)=0.2(49.84)+0.8(58)=9.968+46.4=56.368$
- $\hat x_5(1)=0.2(56.368)+0.8(55)=11.2736+44=55.2736$
Avec $\beta=0.2$ (poids fort sur l'observation la plus récente), la série de prévisions colle de beaucoup plus près à $x_t$ que celle à $\beta=0.6$ — c'est le comportement "souple". $\beta=0.6$ lisse davantage et réagit plus lentement — comportement plus "rigide".

### 11.7 — Holt

**7.1**
a. $\hat x_2(1)=\hat a_2+\hat b_2 = 8+108=116$.
b. Avec $\beta=0.5$ : $\hat a_3=\hat a_2+(1-\beta)^2(x_3-\hat x_2(1)) = 8+(0.5)^2(118-116)=8+0.25(2)=8.5$.
$\hat b_3=\hat b_2+\hat a_2+(1-\beta^2)(x_3-\hat x_2(1)) = 108+8+(1-0.25)(2)=116+0.75(2)=116+1.5=117.5$.
c. $\hat x_3(1)=\hat b_3+\hat a_3=117.5+8.5=126$.

### 11.8 — Holt-Winters

**8.1** a. LES ; b. Holt (double, tendance seule) ; c. Holt-Winters saisonnier additif ; d. Holt-Winters saisonnier multiplicatif (hors programme dans ce cours, mais bonne réponse conceptuelle si vous l'aviez identifié).

**8.2** :
$\hat a_T=\beta(\hat b_T-\hat b_{T-1})+(1-\beta)\hat a_{T-1}$ — moyenne pondérée entre la variation de niveau la plus récente et l'ancienne estimation de pente.
$\hat b_T=\alpha(x_t-\hat S_{T-p})+(1-\alpha)(\hat b_{T-1}+\hat a_{T-1})$ — moyenne pondérée entre l'observation désaisonnalisée et la prévision de niveau faite la période précédente.
$\hat S_T=\gamma(x_t-\hat b_T)+(1-\gamma)\hat S_{T-p}$ — moyenne pondérée entre l'écart observé au niveau actuel et l'ancien coefficient saisonnier (une période plus tôt).

### 11.9 — Choix de la constante

**9.1**
a. $\alpha=0.3$ : erreurs $2,-1,3,-2$. EM $=(2-1+3-2)/4=2/4=0.5$. EAM $=(2+1+3+2)/4=8/4=2$. EQM $=(4+1+9+4)/4=18/4=4.5$.
$\alpha=0.7$ : erreurs $5,-4,1,0$. EM $=(5-4+1+0)/4=2/4=0.5$. EAM $=(5+4+1+0)/4=10/4=2.5$. EQM $=(25+16+1+0)/4=42/4=10.5$.
b. EQM plus faible pour $\alpha=0.3$ (4.5 < 10.5) → on choisirait $\alpha=0.3$. EAM aussi plus faible pour $\alpha=0.3$ (2 < 2.5) → même conclusion ici, les deux critères sont d'accord.
c. Un EM proche de 0 avec un EQM élevé signifierait que les erreurs positives et négatives se compensent en moyenne (pas de biais systématique) mais que leur amplitude individuelle est grande (forte variance des erreurs) — le modèle n'est pas biaisé mais reste imprécis/instable.

### 11.10 — Synthèse
Pas de corrigé unique : fais vérifier ta démarche (les 6 étapes) par un pair ou compare ta prévision par décomposition et ta prévision LES — si elles divergent beaucoup, questionne d'abord ton choix de modèle (étape 1) avant de questionner le calcul.

---

*Pour aller plus loin : refaire ces exercices avec un tableur ou en R/Python (calcul automatique des moyennes mobiles, régressions, lissages) — objet d'un futur script, une fois la théorie posée à la main.*
