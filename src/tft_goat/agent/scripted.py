"""Adversaire scripté (heuristique) : joue des coups réfléchis, pas aléatoires.

Politique simple mais sensée façon TFT : choisir un augment quand proposé, acheter les unités
abordables, équiper les objets, poser les unités sur le board, monter de niveau / roller seulement
quand riche (préserver l'économie ~50 or), sinon passer. Bat nettement un joueur aléatoire et
sert de baseline de skill pour l'éval (et d'opposition crédible à l'entraînement).

Opère directement sur le GameState (c'est un adversaire, pas l'agent qui apprend via observations).
"""

from __future__ import annotations

import numpy as np

from ..env.actions import (
    BUY_SHOP_START,
    BUY_XP,
    EQUIP,
    FIELD_BENCH_START,
    N_AUGMENT_CHOICES,
    N_GOD_CHOICES,
    PASS,
    PICK_AUGMENT_START,
    PICK_GOD_START,
    REROLL,
    REROLL_AUGMENT,
    legal_mask,
)
from ..env.economy import SHOP_SIZE
from ..env.state import GameState, PlayerState

_BENCH_SLOTS = 9
ECON_FLOOR = 54  # ne dépense en XP/roll qu'au-dessus (garde l'intérêt max à 50)


def scripted_action(state: GameState, player: PlayerState) -> int:
    """Retourne une action légale réfléchie pour `player`."""
    mask = legal_mask(state, player)
    legal = set(np.flatnonzero(mask).tolist())

    # 1) choix forcé : augment. Si l'offre est faible (que du silver) et qu'il reste un reroll,
    #    reroll ; sinon prend le meilleur tier (prismatic > gold > silver).
    aug_choices = [i for i in range(N_AUGMENT_CHOICES) if PICK_AUGMENT_START + i in legal]
    if aug_choices:
        rank = {"prismatic": 3, "gold": 2, "silver": 1}
        def _tier_rank(i: int) -> int:
            aug = state.set_content.augments.get(player.augment_offer[i])
            return rank.get(aug.tier, 0) if aug else 0
        best = max(aug_choices, key=_tier_rank)
        if _tier_rank(best) <= 1 and REROLL_AUGMENT in legal:
            return REROLL_AUGMENT  # offre tout-silver : tente mieux
        return PICK_AUGMENT_START + best
    for i in range(N_GOD_CHOICES):
        if PICK_GOD_START + i in legal:
            return PICK_GOD_START + i
    # 2) acheter en priorisant les synergies : doublons (star-up) puis traits partagés
    buy_slots = [i for i in range(SHOP_SIZE) if BUY_SHOP_START + i in legal]
    if buy_slots:
        owned = {u.champion_api for u in player.all_units()}
        owned_traits: set[str] = set()
        for api in owned:
            ch = state.set_content.champions.get(api)
            if ch:
                owned_traits.update(ch.traits)

        def _score(i: int) -> int:
            api = player.shop[i]
            ch = state.set_content.champions.get(api)
            if ch is None:
                return -1
            s = 5 if api in owned else 0  # doublon -> progression vers 2/3 etoiles
            s += sum(1 for t in ch.traits if t in owned_traits)  # synergie de trait
            return s

        return BUY_SHOP_START + max(buy_slots, key=_score)
    # 3) équiper un objet si possible
    if EQUIP in legal:
        return EQUIP
    # 4) poser une unité du banc sur le board
    for i in range(_BENCH_SLOTS):
        if FIELD_BENCH_START + i in legal:
            return FIELD_BENCH_START + i
    # 5) monter de niveau si riche (préserve l'éco sinon)
    if BUY_XP in legal and player.gold >= ECON_FLOOR:
        return BUY_XP
    # 6) roller seulement si très riche
    if REROLL in legal and player.gold >= ECON_FLOOR:
        return REROLL
    return PASS
