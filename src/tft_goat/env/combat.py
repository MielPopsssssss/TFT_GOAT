"""Resolution de combat — interface enfichable + heuristique v0.

C'est LA couture du projet : `CombatResolver` est une interface stable. La v0 est une
heuristique « force de board » ; l'etape 4 branchera un surrogate neuronal entraine sur
match-v1 SANS toucher au reste de l'env.

Le resultat expose `winner` + `survivors` (unites du vainqueur encore debout) : c'est
exactement ce que les donnees post-game permettent d'apprendre. La conversion survivors ->
degats PV est une *regle de jeu* (rounds.py), pas du combat.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

import numpy as np

from ..data.models import SetContent
from ..data.stats_models import MetaStats
from .economy import ITEM_BONUS
from .state import BoardUnit
from .traits import active_traits

STAR_MULT = {1: 1, 2: 3, 3: 9}
TRAIT_WEIGHT = 3.0  # poids d'un palier de trait dans la force de board


@dataclass(frozen=True)
class CombatResult:
    winner: int  # 0 -> board_a, 1 -> board_b
    survivors: int  # unites du vainqueur encore en vie -> 1 degat joueur/unite (formule TFT reelle)


class CombatResolver(Protocol):
    def resolve(
        self,
        board_a: list[BoardUnit],
        board_b: list[BoardUnit],
        set_content: SetContent,
        rng: np.random.Generator,
        augments_a: tuple[str, ...] = (),
        augments_b: tuple[str, ...] = (),
    ) -> CombatResult: ...


def board_strength(
    board: list[BoardUnit], set_content: SetContent, meta_stats: MetaStats | None = None
) -> float:
    """Force heuristique : Σ cout×mult_etoile + bonus de traits actifs.

    Si `meta_stats` est fourni, chaque contribution est ponderee par la force reelle
    (placement moyen datatft) ; sinon comportement brut (cout×etoile), inchange.
    """
    strength = 0.0
    for unit in board:
        champ = set_content.champions.get(unit.champion_api)
        if champ is None:
            continue
        contrib = champ.cost * STAR_MULT.get(unit.star, 1)
        contrib *= 1.0 + ITEM_BONUS * getattr(unit, "items", 0)
        if meta_stats is not None:
            contrib *= meta_stats.unit_power(unit.champion_api)
        strength += contrib

    active = active_traits([u.champion_api for u in board], set_content)
    name_to_api = (
        {t.name: t.api_name for t in set_content.traits.values()} if meta_stats else {}
    )
    for name, tier in active.items():
        bonus = tier * TRAIT_WEIGHT
        if meta_stats is not None:
            api = name_to_api.get(name)
            if api is not None:
                bonus *= meta_stats.trait_power(api, tier)
        strength += bonus
    return strength


class HeuristicResolver:
    """Resolver v0 : probabiliste, pondere par la force de board.

    `meta_stats` (optionnel) ancre la force dans les vrais placements datatft.
    """

    def __init__(self, meta_stats: MetaStats | None = None):
        self.meta_stats = meta_stats

    def resolve(
        self,
        board_a: list[BoardUnit],
        board_b: list[BoardUnit],
        set_content: SetContent,
        rng: np.random.Generator,
        augments_a: tuple[str, ...] = (),
        augments_b: tuple[str, ...] = (),
    ) -> CombatResult:
        sa = board_strength(board_a, set_content, self.meta_stats)
        sb = board_strength(board_b, set_content, self.meta_stats)
        if sa == 0 and sb == 0:
            return CombatResult(winner=0, survivors=0)
        p_a = sa / (sa + sb) if (sa + sb) > 0 else 0.5
        winner = 0 if rng.random() < p_a else 1
        win_board = board_a if winner == 0 else board_b
        margin = abs(sa - sb) / (sa + sb)  # 0 (serre) .. 1 (ecrasant)
        survivors = max(1, round(len(win_board) * margin)) if win_board else 0
        return CombatResult(winner=winner, survivors=survivors)
