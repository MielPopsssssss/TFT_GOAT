"""Tests de l'economie (fonctions pures)."""

from __future__ import annotations

from tft_goat.env.economy import (
    MAX_LEVEL,
    XP_BUY_COST,
    XP_PER_BUY,
    XP_TO_LEVEL,
    ROUND_XP,
    apply_xp,
    interest,
    round_income,
    sell_value,
    streak_bonus,
)


def test_interest_capped_at_5():
    assert interest(0) == 0
    assert interest(34) == 3
    assert interest(50) == 5
    assert interest(99) == 5  # plafond


def test_interest_boundaries_verified_patch_17_4():
    """Bornes exactes de l'interest — VÉRIFIÉ vs patch 17.4 (wiki/op.gg/lolchess unanimes).

    +1 par tranche de 10 banquée, cap +5 atteint pile à 50 gold.
    """
    assert interest(9) == 0  # <10 => aucun interest
    assert interest(10) == 1
    assert interest(49) == 4  # cap PAS encore atteint
    assert interest(50) == 5  # cap atteint pile à 50
    assert interest(1000) == 5  # plafonné


def test_streak_bonus_tiers():
    assert streak_bonus(0) == 0
    assert streak_bonus(1) == 0
    assert streak_bonus(2) == 1
    assert streak_bonus(4) == 2
    assert streak_bonus(7) == 3
    assert streak_bonus(-5) == 3  # loss streak compte aussi


def test_round_income():
    # 30 gold (interet 3) + streak 3 (+2) + base 5 = 10
    assert round_income(30, 3) == 5 + 3 + 2


def test_round_income_is_bounded_no_runaway():
    """Revenu/round plafonné = base 5 + interest 5 (cap) + streak 3 (cap) = 13, quel que soit l'or.

    Garde-fou anti-runaway éco : même à 1000 gold et streak 99, le revenu reste borné (l'or qui
    s'accumule en jeu aléatoire = thésaurisation par non-dépense, PAS un revenu cassé).
    """
    assert round_income(1000, 99) == 5 + 5 + 3
    assert round_income(0, 0) == 5  # plancher = base


def test_apply_xp_levels_up():
    # niveau 1, 0 xp, +2 xp : seuil L1->L2 = 2 => passe lvl 2, 0 xp restant
    level, xp = apply_xp(1, 0, 2)
    assert level == 2 and xp == 0


def test_apply_xp_multi_level():
    # niveau 1 (seuils 2 puis 2) + 4 xp d'un coup -> lvl 2 reste 2 (pas lvl 3 car besoin 2)
    level, xp = apply_xp(1, 0, 8)  # 8 = 2(->2) + 2(->3) + 4 reste
    assert level == 3 and xp == 4


def test_xp_constants_verified_patch_17_4():
    """Facts XP confirmes vs patch 17.4 (wiki LoL + tft.ninja + op.gg concordants)."""
    assert MAX_LEVEL == 10  # niveau max confirme (le row L11 des odds n'est pas atteignable)
    assert ROUND_XP == 2  # 2 XP passifs / round
    assert (XP_PER_BUY, XP_BUY_COST) == (4, 4)  # acheter 4 XP coute 4 gold


def test_xp_table_lower_increments_confirmed():
    """L1->L6 : code, tft.ninja et wiki concordent (2,2,6,10,20,36).

    NB : top-3 (L7->8, L8->9, L9->10) = 56/80/100 dans le code ; tft.ninja donne
    48/72/84 (valeurs d'anciens sets, guide marque "may be adjusted"). Désaccord non
    résolu faute de source officielle accessible (fandom 403, wiki SPA). Conservé tel
    quel — NE PAS flipper sans patch notes officiels. Voir FLAG dans economy.py.
    """
    assert XP_TO_LEVEL[1] == 2
    assert XP_TO_LEVEL[2] == 2
    assert XP_TO_LEVEL[3] == 6
    assert XP_TO_LEVEL[4] == 10
    assert XP_TO_LEVEL[5] == 20
    assert XP_TO_LEVEL[6] == 36


def test_xp_table_monotonic_and_complete():
    """Structure : XP requis non-décroissant et table couvre L1..MAX_LEVEL-1."""
    assert sorted(XP_TO_LEVEL) == list(range(1, MAX_LEVEL))
    vals = [XP_TO_LEVEL[lvl] for lvl in sorted(XP_TO_LEVEL)]
    assert vals == sorted(vals), "XP requis doit être non-décroissant"


def test_apply_xp_caps_at_max_level():
    """Au niveau max, l'XP ne déborde pas et reste à 0."""
    level, xp = apply_xp(MAX_LEVEL, 0, 999)
    assert level == MAX_LEVEL and xp == 0


def test_sell_value():
    assert sell_value(1, 1) == 1
    assert sell_value(1, 2) == 3  # 1-cost : pas de penalite
    assert sell_value(3, 1) == 3
    assert sell_value(3, 2) == 3 * 3 - 1  # 8
    assert sell_value(4, 3) == 4 * 9 - 1  # 35
