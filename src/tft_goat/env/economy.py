"""Economie TFT : revenu, interets, streak, XP/level, valeur de revente. Fonctions pures.

Les tables (XP par niveau, paliers de streak) sont des constantes versionnees, comme les
shop odds.

AUDIT XP 2026-06-08 (vs patch 17.4) :
  - CONFIRME : niveau max = 10 ; 2 XP passifs/round ; achat 4 XP / 4 gold ;
    increments L1->L6 = 2, 2, 6, 10, 20, 36 (code == tft.ninja == wiki LoL).
  - DESACCORD NON RESOLU (top-3) : code = 56 / 80 / 100 pour L7->8, L8->9, L9->10 ;
    tft.ninja donne 48 / 72 / 84 (valeurs d'anciens sets, guide marque "may be adjusted").
    Sources officielles inaccessibles (fandom 403, wiki SPA, esportstales/op.gg sans la
    ligne). NE PAS flipper sans patch notes officiels : flipper = deviner. A reverifier
    quand une source fiable publie la table 17.4 complete.
  Impact : valeurs top-3 = realisme uniquement (l'env reste correct quel que soit le choix).
  Pins de regression : tests/test_economy.py::test_xp_* .
"""

from __future__ import annotations

BASE_INCOME = 5
MAX_INTEREST = 5  # plafonne a 50 gold (1 interet / 10 gold)
ROUND_XP = 2  # XP passive par round
XP_PER_BUY = 4
XP_BUY_COST = 4
REROLL_COST = 2
SHOP_SIZE = 5
BENCH_CAP = 9
MAX_LEVEL = 10

# Items & augments
COMPONENTS_PER_ITEM = 2
ITEMS_MAX = 3  # objets completes par unite
ITEM_BONUS = 0.5  # +50% de force d'unite par objet
AUGMENT_BONUS_RANGE = (0.05, 0.15)  # mitigation de degats ajoutee par augment choisi

# XP necessaire pour passer du niveau L au niveau L+1 (achat = 4 XP / 4 gold).
XP_TO_LEVEL: dict[int, int] = {
    1: 2,
    2: 2,
    3: 6,
    4: 10,
    5: 20,
    6: 36,
    7: 56,
    8: 80,
    9: 100,
}


def interest(gold: int) -> int:
    """Interets : 1 gold par tranche de 10, plafonne a MAX_INTEREST.

    VERIFIE vs patch 17.4 (2026-06-08, unanime wiki LoL / op.gg / lolchess) : +1/10 gold,
    cap +5 a partir de 50 gold banques.
    """
    return min(gold // 10, MAX_INTEREST)


def streak_bonus(streak: int) -> int:
    """Bonus de win/loss streak (|streak| en entree). Code actuel : 2->+1, 3-4->+2, 5+->+3.

    🟡 DISPUTE NON RESOLU (audit 2026-06-08) : les sources divergent sur le palier streak=3.
      - code : 3 -> +2
      - tftpad/lolchess(resume) : streak 2-3 -> +1, 4 -> +2, 5+ -> +3 (=> 3 devrait donner +1)
      - wiki LoL (extraction) : 3-4 -> +1, 5 -> +2, 6+ -> +3 (table encore differente)
    Extractions web non fiables (pages SPA, colonnes historiques du wiki). NE PAS flipper
    sans patch notes officiels : comportement conserve tel quel. Impact = realisme eco seul.
    A reverifier des qu'une source fiable publie la table streak 17.4.
    """
    s = abs(streak)
    if s < 2:
        return 0
    if s < 3:
        return 1
    if s < 5:
        return 2
    return 3


def round_income(gold: int, streak: int) -> int:
    """Revenu d'un round : base + interets + bonus de streak."""
    return BASE_INCOME + interest(gold) + streak_bonus(streak)


def xp_to_next(level: int) -> int | None:
    """XP requis pour atteindre le niveau suivant, ou None si niveau max."""
    return XP_TO_LEVEL.get(level)


def apply_xp(level: int, xp: int, gained: int) -> tuple[int, int]:
    """Ajoute `gained` XP et fait monter le(s) niveau(x). Retourne (level, xp restant)."""
    xp += gained
    while level < MAX_LEVEL:
        need = XP_TO_LEVEL[level]
        if xp < need:
            break
        xp -= need
        level += 1
    if level >= MAX_LEVEL:
        xp = 0
    return level, xp


def sell_value(cost: int, star: int) -> int:
    """Or rendu a la vente.

    1-cost : valeur pleine (1/3/9). 2+ cost : -1 gold des le 2-etoiles (regle TFT).
    """
    copies = 3 ** (star - 1)
    base = cost * copies
    if cost == 1 or star == 1:
        return base
    return base - 1
