
## 2026-11-18 — sujet 01 corrigé
- EMS-1 « 10 données économiques » = 2.10 du doc = **a10** (anti-diabète, fpp2, juil. 1991–juin 2008), PAS FEDFUNDS. Dossier renommé `01_Economie_a10_antidiabete` (FEDFUNDS supprimé), énoncé/README/explication régénérés, R + Python OK.
- Bug corrigé dans `common.R` : les coefficients saisonniers étaient étiquetés par position calendaire mais pris dans l'ordre des observations (`dec$figure`) → décalage pour les séries qui ne commencent pas en position 1 (a10 : juillet ; Boulder, météo…). Maintenant `tapply(dec$seasonal, cycle(y), mean)`. Prévisions non touchées (déjà correctes).
- Restent à confirmer : VCOD-7 « 2.5 » = CO₂ dans le doc (dossier 13 = nottem, à remplacer) ; 04 → `sunspot.month`.
