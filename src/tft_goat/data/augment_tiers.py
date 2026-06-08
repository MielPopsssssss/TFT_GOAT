"""Detection du tier d'un augment (Silver / Gold / Prismatic) — la vraie qualite TFT.

CommunityDragon n'expose pas de champ `tier` propre, MAIS l'icone d'augment encode le tier
de facon fiable : le fichier est nomme avec le chiffre romain (`_I`/`_II`/`_III`) ou arabe
(`1`/`2`/`3`) du tier, juste avant le suffixe `.TFT_SetXX.tex`. C'est le meme indicateur que
Riot utilise pour rendre la bordure argent/or/prismatique de l'augment en jeu.

Tiers : I/1 = Silver, II/2 = Gold, III/3 = Prismatic.
Les augments lies aux dieux (Realm of the Gods, `*GodAugment*`) ne sont PAS des picks
silver/gold/prismatic des rounds 2-1/3-2/4-2 : ce sont des boons du mecanisme du set. On les
classe `god` pour les EXCLURE du pool d'augments reguliers.
"""

from __future__ import annotations

import re

SILVER = "silver"
GOLD = "gold"
PRISMATIC = "prismatic"
GOD = "god"  # boon Realm of the Gods — hors pool regulier

_ROMAN = {"I": SILVER, "II": GOLD, "III": PRISMATIC}
_DIGIT = {"1": SILVER, "2": GOLD, "3": PRISMATIC}

# Le token de tier apparait juste avant un point (`..._II.TFT_Set17.tex`, `...3.tex`).
_ROMAN_RE = re.compile(r"(III|II|I)(?=\.)")
_DIGIT_RE = re.compile(r"([123])(?=\.)")


def detect_tier(api_name: str, icon: str | None) -> str:
    """Retourne le tier d'un augment depuis son apiName + le chemin de son icone CDragon."""
    if "GodAugment" in api_name:
        return GOD
    ic = icon or ""
    m = _ROMAN_RE.search(ic)
    if m:
        return _ROMAN[m.group(1)]
    m = _DIGIT_RE.search(ic)
    if m:
        return _DIGIT[m.group(1)]
    icl = ic.lower()  # filet de securite : mot explicite dans le chemin
    for word in (PRISMATIC, GOLD, SILVER):
        if word in icl:
            return word
    return GOLD  # defaut : Gold (tier le plus courant) — jamais atteint sur la data Set 17 actuelle
