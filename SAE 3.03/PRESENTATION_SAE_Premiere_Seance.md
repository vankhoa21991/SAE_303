# SAE3.03 — Préparer la première séance (présentation du sujet aux étudiants)

*Document de préparation pour l'enseignant, en vue de la première séance de lancement de la SAE3.03 "Description et prévision de données temporelles" (IUT SD, 2025-2026). Contient : le résumé du sujet, un script de présentation orale, une proposition de présentation personnelle, et une FAQ anticipant les questions des étudiants. Tout est en français, prêt à être utilisé tel quel ou adapté.*

---

## 1. Résumé du sujet de la SAE (ce que dit l'énoncé)

### 1.1 La tâche (en une phrase)

> Un jeu de données temporelles est donné. Le groupe a la charge de le **présenter**, l'**analyser**, le **décomposer**, et de **proposer une prédiction**.

### 1.2 Les 8 étapes clés du projet

| # | Étape | Contenu attendu |
|---|---|---|
| 1 | **Management de projet** | Diagramme de Gantt sur 10h (par tranches de 2h) ; répartition des rôles dans le groupe ; mise en place d'un espace de travail commun (Drive, GitHub, Overleaf…) |
| 2 | **Recherche bibliographique** | Vérifier si la série (ou une série similaire) a déjà été étudiée par quelqu'un d'autre — et le documenter en bibliographie |
| 3 | **Présenter et contextualiser les données** | Source des données, période d'étude, unité des variables, présence attendue d'une saisonnalité, etc. |
| 4 | **Explorer les données** | Descripteurs statistiques, visualisation à différents pas de temps (journalier/mensuel/annuel), dataviz de la série (radial line graph ou autre), fonctions ACF et PACF (PACF optionnelle) |
| 5 | **Tests sur la série** | Test de stationnarité (Dickey-Fuller augmenté), test de tendance, test de Pettitt (changement de tendance centrale), autres tests au choix |
| 6 | **Choisir un modèle de décomposition** | Additif ou multiplicatif ; extraire la tendance ; calculer les coefficients saisonniers si besoin ; produire la série CVS |
| 7 | **Valider le modèle** | Analyse des résidus (graphiques/tableaux commentés), repérer les valeurs mal ajustées |
| 8 | **Prédire** | Prévisions à court terme par (a) une méthode paramétrique (tendance + coefficients saisonniers) **et** (b) une méthode de lissage |

**Point d'attention pédagogique** : l'énoncé mentionne aussi, en 1.3, une modélisation par un modèle autorégressif (**AR, MA, ARMA, ARIMA, SARIMA**), les fonctions ACF/PACF aidant à choisir ce modèle — plus, en option, une méthode de machine learning. C'est **au-delà** de ce que couvre le cours de décomposition/lissage exponentiel (voir `GUIDE_ENSEIGNANT_Series_Chronologiques.md`, qui s'arrête aux méthodes de lissage). À anticiper : soit ce point est traité dans un autre cours du semestre (SAE ou CM complémentaire), soit il faudra donner aux étudiants un minimum de repères sur ARIMA en séance, soit préciser explicitement que c'est acceptable de rester au niveau décomposition + lissage pour la partie obligatoire, l'ARIMA restant à explorer en autonomie. **À clarifier avant la séance** (voir §5, "Ce que je dois vérifier avant de me lancer").

### 1.3 Groupes & outils

- **Groupes de 2 personnes**
- Outils au choix, mais **R ou Python conseillés**
- Modèle autorégressif à choisir en s'appuyant sur ACF/PACF (AR, MA, ARMA, ARIMA, SARIMA)
- Optionnel : une autre méthode, ou une méthode de machine learning

### 1.4 Livrables

- **Temps imparti : 10h** (le Gantt de l'étape 1 doit couvrir ces 10h, par tranches de 2h)
- Un **rapport** sur le travail effectué :
  - Structure conseillée = suivre les 8 étapes clés
  - **Maximum 12 pages** (hors annexes)
  - **Le code doit être mis en annexe** (ne compte pas dans les 12 pages)
  - La bibliographie (étape 2) s'ajoute également hors 12 pages
- Un **badge** associé à la SAE
- **Dépôt sur Moodle, au format PDF**, avec les noms de fichiers imposés :
  - `Nom1_Nom2_rapport_SAE303.pdf`
  - `Nom_Badge_SAE303.pdf`
- **Date limite de dépôt** : à confirmer/rappeler avec la date officielle de l'année en cours (le document source portait une annotation manuscrite `2025-01-12 23h59`, probablement relative à une session précédente — **vérifier la date exacte de cette année avant la séance**, cf. §5)

### 1.5 Jeux de données proposés en exemple

L'énoncé illustre le type de séries mobilisables (probablement une liste dans laquelle chaque groupe pioche, ou des exemples de la forme attendue pour "présenter et contextualiser les données") :

| Dataset | Description | Remarque |
|---|---|---|
| **wineind** (`forecast`) | Ventes totales de vin par les viticulteurs australiens (bouteilles < 1L), janvier 1980 – août 1994 | Présentée comme série **sans saisonnalité** dans le document — à vérifier en séance, car `wineind` est en réalité connue pour avoir une saisonnalité annuelle marquée ; bon point de débat/vérification avec les étudiants (§4) |
| **FEDFUNDS** | Taux des fonds fédéraux américains (taux mensuel), Réserve fédérale US | Nécessite un téléchargement externe (fred.stlouisfed.org) ; bon exemple de série économique sans saisonnalité forte mais avec tendance/ruptures marquées |
| **EuStockMarkets** (colonne FTSE) | Cours de clôture quotidiens de 4 bourses européennes (DAX, SMI, CAC, FTSE) — on s'intéresse ici au FTSE (Royaume-Uni) | Série financière quotidienne, pas de saisonnalité calendaire classique, utile pour illustrer stationnarité/non-stationnarité |
| **gold** (`fpp2`) | Cours quotidiens de l'or le matin (USD), 1er janvier 1985 – 31 mars 1989 | ⚠️ pas nativement au format `ts` — bon exercice de mise en forme des données avant analyse |
| **LakeHuron** | Niveau annuel (en pieds) du lac Huron, 1875–1972 | Classique de Brockwell & Davis ; série annuelle donc **pas de saisonnalité infra-annuelle possible** — bon exemple pour discuter tendance seule / rupture de régime |

*(Ce tableau peut être mis en parallèle avec `DATASETS_Kaggle_Projet.md`, qui propose des alternatives Kaggle si les étudiants veulent/doivent choisir eux-mêmes une série plutôt que d'utiliser une série imposée.)*

---

## 2. Script de présentation orale — premher séance

*But : un déroulé que je peux suivre (ou juste garder sous les yeux) pendant les 10-15 premières minutes de la séance, avant de laisser les groupes démarrer. À adapter à l'oral, ce n'est pas à lire mot pour mot.*

### 2.1 Introduction / accroche (2 min)

> "Bonjour à tous. Aujourd'hui on démarre la SAE3.03, dix heures consacrées à un exercice très concret : prendre une série de données dans le temps — des ventes, un taux d'intérêt, un cours de bourse — et répondre à une question simple mais qui demande une vraie méthode : **qu'est-ce qui va se passer ensuite ?**
>
> C'est le même type de travail que fait un analyste financier, un responsable logistique qui prévoit un stock, ou un data scientist qui prévoit un pic de trafic. La méthode qu'on va utiliser est éprouvée et se retrouve partout une fois qu'on sait la reconnaître."

### 2.2 Présentation personnelle (2-3 min)

> "Je me présente rapidement : je m'appelle XYZ, je suis data scientist en poste, actuellement dans une entreprise d'e-commerce. Avant ça, j'ai travaillé comme data scientist et ingénieur IA dans plusieurs entreprises et sur des domaines assez différents : l'automobile, l'imagerie médicale, et maintenant l'e-commerce. 
>
> C'est ma première fois à encadrer cette SAE. Si vous avez des questions n'hesite pas de le demander. Et je ne souhaite pas que vous parler quand je parle, apres je vais vous donner le temps pour poser des questions
>
> N'hésitez pas à me poser des questions à tout moment, y compris des questions bêtes — sur ce genre de projet, il n'y a jamais de mauvaise question, seulement des hypothèses qu'on n'a pas vérifiées. Et si une question me sort de mon domaine de confort, je vous le dirai aussi honnêtement plutôt que d'inventer une réponse.
>
> Aujourd'hui, mon rôle n'est pas de vous donner la réponse, mais de vous aider à structurer votre démarche et à ne pas rester bloqués sur un point technique — un peu comme je le ferais avec un collègue junior en entreprise. Allons-y."

### 2.3 Cadrage du module (3-4 min)

> "Pour resituer : cette SAE s'appuie sur ce qu'on a vu en cours — la décomposition d'une série en tendance, saisonnalité et résidu, et les méthodes de lissage exponentiel. Le but ici n'est pas de refaire le cours, c'est de l'appliquer sur une vraie série, en autonomie, en groupe de deux, et de rendre un rapport professionnel dessus.
>
> Le déroulé suit 8 étapes que vous retrouverez dans l'énoncé : gestion de projet, recherche biblio, présentation des données, exploration, tests statistiques, décomposition, validation du modèle, et enfin prédiction. Ce n'est pas une liste à cocher dans le désordre — c'est un peu un pipeline, chaque étape s'appuie sur la précédente."

### 2.4 Parcourir les livrables et contraintes (3 min)

> "Quelques points très concrets à retenir tout de suite :
> - Vous avez **10 heures**, à répartir vous-même dans le temps — d'où le diagramme de Gantt demandé en première étape. Ce n'est pas un détail administratif, c'est ce qui vous évite d'arriver à la dernière heure sans avoir fait la partie prédiction.
> - Le rapport final fait **12 pages maximum**, le code va en annexe. Ça veut dire : soyez synthétiques, ne collez pas 40 lignes de sortie R dans le corps du texte, interprétez.
> - Groupes de **2 personnes**, outil **R ou Python** conseillé (libre à vous d'utiliser autre chose si vous justifiez).
> - Le dépôt se fait sur Moodle, au format PDF, avec la nomenclature de fichier imposée — je vous la remets à l'écran/sur Moodle."

### 2.5 Lien avec le cours (2-3 min)

> "Concrètement, les étapes 4 à 8 de l'énoncé, c'est exactement ce qu'on a fait ensemble en cours et en TD, mais sur des jeux de données jouets. Là vous allez le refaire sur une vraie série, avec du vrai bruit, des vraies décisions à prendre — notamment est-ce que le modèle est additif ou multiplicatif, ce qui n'est pas toujours évident au premier coup d'œil sur des données réelles.
>
> Un point à anticiper : l'énoncé mentionne aussi des modèles autorégressifs — AR, ARMA, ARIMA, SARIMA. [ADAPTER SELON VOTRE DÉCISION — voir §5] : soit on n'a pas eu le temps de les voir en cours, et je vous donne quelques repères aujourd'hui / je vous renvoie à telle ressource ; soit c'est volontairement laissé en autonomie/optionnel pour ceux qui veulent aller plus loin."

### 2.6 Lancement (2 min)

> "Je vous laisse maintenant vous mettre en groupe de deux, choisir/récupérer votre jeu de données, et démarrer par l'étape 1 : le Gantt et la répartition des rôles. Je circule dans la salle si vous avez des questions, n'hésitez pas à m'appeler."

### 2.7 Pendant que les groupes travaillent (le reste de la séance)

*C'est la phase la plus longue — les groupes sont en autonomie sur l'étape 1 (Gantt/rôles), puis démarrent l'étape 2-3 (biblio, contextualisation) si le temps le permet sur cette première séance. Votre rôle change : vous n'êtes plus devant la classe, vous circulez.*

- **Circuler activement plutôt qu'attendre qu'on vous appelle.** Beaucoup de groupes n'osent pas lever la main en première séance — passez voir chaque binôme dans les 15-20 premières minutes, même juste pour valider que le jeu de données choisi est adapté (cf. critères en §5 de la checklist, ou `DATASETS_Kaggle_Projet.md`).
- **Répondre par des questions plutôt que par la réponse directe**, surtout sur le choix additif/multiplicatif ou le choix de dataset : *"Qu'est-ce que tu observes sur le graphique qui te fait pencher pour l'un ou l'autre ?"* plutôt que trancher à leur place — c'est cohérent avec le message donné en 2.2 ("mon rôle n'est pas de vous donner la réponse").
- **Repérer tôt les groupes qui partent sur un dataset à risque** (trop peu de cycles saisonniers, trop de valeurs manquantes, série multivariée non filtrée) — mieux vaut le dire dès la première séance qu'après plusieurs heures de travail dessus.
- **Point de passage informel à mi-séance** (si la séance dure plusieurs heures) : un rapide tour visuel ou oral pour vérifier que chaque groupe a bien avancé sur l'étape 1 et est en train d'attaquer l'étape 2/3, sans que ce soit noté ou formel — juste pour recaler ceux qui seraient partis dans la mauvaise direction.

### 2.8 Clôture de la séance (dernières 5-10 min)

> "On s'arrête là pour aujourd'hui. Avant de partir, un rapide tour : est-ce que chaque groupe a bien choisi son jeu de données et a un Gantt, même provisoire ? [Lever de main ou tour de table rapide.]
>
> Pour la suite : vous retrouverez les ressources du cours — le guide, les exercices corrigés, et la liste des jeux de données alternatifs — sur [Moodle / l'espace partagé]. N'hésitez pas à m'écrire si vous êtes bloqués avant la prochaine séance plutôt que d'attendre.
>
> Rappel de la deadline du rapport et du badge : [donner la date confirmée, cf. checklist §5]. À la prochaine séance, je m'attends à ce que les étapes 1 à 3 soient bouclées pour qu'on puisse avancer sur l'exploration et les tests."

**Après la séance (pour vous)** : notez rapidement les groupes qui semblent en difficulté ou sur un dataset fragile, pour les recontacter en priorité à la prochaine séance plutôt que de redécouvrir le problème sur place.

---

## 3. Variante courte de la présentation personnelle

*Le texte complet est désormais intégré directement en §2.2 ci-dessus (dans le déroulé de la séance). Gardez cette version courte sous la main si le temps est serré ou si vous devez vous représenter plus tard dans le semestre (ex. auprès d'un autre groupe/créneau) :*

> "Bonjour, je suis XYZ, data scientist dans l'e-commerce, avec une expérience passée en automobile et en imagerie médicale. C'est ma première fois à encadrer une SAE — je n'ai pas beaucoup d'expérience d'enseignement, mais j'espère que mon expérience terrain pourra vous être utile. Je suis là pour vous accompagner sur la méthode, pas pour vous donner les réponses — donc posez toutes vos questions, même celles qui vous semblent évidentes."

---

## 4. Questions probables des étudiants — et éléments de réponse

### Sur l'organisation

**Q : Peut-on choisir notre binôme ?**
R : *(à trancher selon la politique du département — préciser avant la séance : libre, imposé, ou tirage au sort.)*

**Q : Peut-on choisir notre propre jeu de données, ou est-il imposé ?**
R : Si l'énoncé propose une liste (§1.5 ci-dessus), préciser si c'est une liste fermée ou des exemples parmi d'autres possibles. Si libre choix : rappeler les critères de qualité d'une série (voir `DATASETS_Kaggle_Projet.md` : au moins 3 cycles saisonniers complets si saisonnalité étudiée, peu de valeurs manquantes, licence compatible).

**Q : Le diagramme de Gantt, ça doit être un vrai outil (Excel, GanttProject) ou un simple tableau suffit ?**
R : Un tableau simple avec les tranches de 2h et les tâches suffit largement ; l'objectif est de montrer une répartition réfléchie du temps, pas la maîtrise d'un logiciel de gestion de projet.

**Q : "Espace de travail en commun", ça veut dire quoi concrètement ?**
R : N'importe quel outil de partage (Drive, GitHub, Overleaf, Notion…) permettant aux deux membres du binôme de travailler sur les mêmes documents sans s'envoyer des fichiers par mail. Ce n'est pas noté en soi, mais évite les problèmes de version à la fin.

### Sur le contenu statistique

**Q : Comment on sait si notre série est additive ou multiplicative ?**
R : Rappeler les 3 méthodes vues en cours (méthode de la bande, méthode du profil, méthode de Buys-Ballot — régression écart-type/moyenne). Renvoyer à `GUIDE_ENSEIGNANT_Series_Chronologiques.md` §3 et à `EXERCICES_Series_Chronologiques.md` §1 pour s'entraîner.

**Q : Et si notre série n'a pas de saisonnalité du tout (comme `wineind` présentée ici, ou LakeHuron) ?**
R : C'est un résultat valide en soi ! Il faut alors le montrer (test/graphique à l'appui), et adapter la suite : pas de coefficients saisonniers à calculer, la décomposition se réduit à tendance + résidu, et côté prévision on peut comparer une régression de tendance simple à un lissage exponentiel simple (LES) ou double (Holt) plutôt qu'à Holt-Winters.

**Q : C'est quoi le test de Dickey-Fuller / le test de Pettitt, on ne les a pas vus en cours ?**
R : *(À anticiper selon ce qui a été couvert.)* Dickey-Fuller augmenté teste si la série est stationnaire (pas de tendance/racine unitaire) ; Pettitt teste s'il y a une rupture dans le niveau moyen de la série à un instant donné. Si non vus en cours, prévoir soit un mini-apport en séance, soit indiquer clairement que la fonction existe "clé en main" dans R (`tseries::adf.test`, `trend::pettitt.test`) et que l'important est de savoir interpréter la p-value, pas de refaire la démonstration mathématique.

**Q : ARIMA/SARIMA, on doit vraiment le faire ?**
R : Se référer à la décision prise en §5 avant la séance — préciser explicitement le niveau d'exigence (obligatoire / bonus / hors-cadre-de-cette-SAE) pour éviter le flou qui inquiète les étudiants.

**Q : Quelle est la différence entre les coefficients saisonniers et la série CVS ?**
R : Les coefficients saisonniers résument "de combien telle saison dévie en moyenne" ; la CVS, c'est la série d'origine *débarrassée* de cette déviation saisonnière (donc tendance + résidu seulement). Voir `GUIDE_ENSEIGNANT_Series_Chronologiques.md` §5 pour des exemples chiffrés complets.

**Q : On doit faire les deux méthodes de prévision (décomposition ET lissage), ou on choisit ?**
R : L'énoncé (étape 8) demande explicitement les deux : une méthode paramétrique par décomposition, et une méthode de lissage — c'est justement l'intérêt pédagogique, pouvoir comparer.

### Sur le rapport et l'évaluation

**Q : 12 pages, ça inclut les graphiques ?**
R : Oui, tout ce qui est dans le corps du rapport compte (texte + figures + tableaux), seuls le code et la bibliographie sont hors limite.

**Q : Peut-on utiliser ChatGPT/un LLM pour nous aider ?**
R : *(À trancher selon la politique du département — précisez la position avant la séance : autorisé avec citation, toléré pour du code mais pas pour l'analyse, interdit, etc. C'est une question quasi systématique aujourd'hui, mieux vaut y répondre frontalement dès le lancement.)*

**Q : Comment sera noté le rapport ? Il y a une grille ?**
R : Si une grille de notation existe, la présenter maintenant. Sinon, indiquer au minimum les critères qualitatifs : rigueur méthodologique à chaque étape, qualité de l'interprétation (pas seulement des graphiques bruts), clarté de la rédaction, cohérence entre modèle choisi et prévisions produites.

**Q : Le "badge", c'est quoi exactement ?**
R : *(À préciser selon le référentiel BUT/compétences de votre établissement — généralement une auto-évaluation ou une preuve de compétence associée à la SAE, à documenter séparément du rapport.)*

---

## 5. Ce que je dois vérifier avant de me lancer

*Checklist personnelle — à faire avant la séance, pas pendant.*

- [ ] **Date limite exacte** de dépôt sur Moodle pour l'année en cours (le document source portait une date manuscrite `2025-01-12 23h59`, probablement d'une session antérieure — confirmer la date réelle 2025-2026)
- [ ] **Politique sur les groupes** : libre, imposé ou tiré au sort ?
- [ ] **Jeux de données** : liste fermée imposée, ou les datasets listés en §1.5 ne sont que des *exemples* de format attendu et les étudiants doivent en choisir/apporter un autre (auquel cas, avoir `DATASETS_Kaggle_Projet.md` sous la main à leur proposer) ?
- [ ] **Niveau d'exigence sur AR/MA/ARMA/ARIMA/SARIMA** : ont-ils été vus dans un autre cours du semestre ? Sont-ils obligatoires, bonus, ou hors périmètre réel de cette SAE malgré leur mention dans l'énoncé ?
- [ ] **Tests statistiques (Dickey-Fuller, Pettitt)** : ont-ils été couverts en cours/TD ? Si non, prévoir un support minimal (fiche ou 5 minutes d'explication) plutôt que de les découvrir dans l'énoncé sans repère.
- [ ] **Grille de notation** existante ou à communiquer / à construire.
- [ ] **Politique sur l'usage des IA génératives** pour la rédaction/le code.
- [ ] **Définition exacte du "badge"** attendu par le référentiel de compétences.
- [ ] Vérifier que `wineind` est bien présentée comme "sans saisonnalité" dans l'énoncé officiel (dans la doc R standard, `wineind` a une saisonnalité annuelle connue) — si c'est une coquille de l'énoncé, ça vaut le coup de le signaler en séance plutôt que de laisser les étudiants se fier aveuglément au sous-titre.

---

## 6. Ressources déjà disponibles pour ce module

À mentionner aux étudiants ou à garder sous la main pendant que vous circulez dans la salle :

- `GUIDE_ENSEIGNANT_Series_Chronologiques.md` — théorie complète (décomposition, moyennes mobiles, CVS, lissage exponentiel) avec exemples chiffrés
- `EXERCICES_Series_Chronologiques.md` — exercices d'entraînement à la main, avec corrigés, pour revoir un point avant de l'appliquer sur la vraie série du projet
- `DATASETS_Kaggle_Projet.md` — alternative de jeux de données si besoin de choisir/varier les séries entre binômes

*(Script/notebook R ou Python d'automatisation : pas encore fait, explicitement pour plus tard.)*
