"""Pool de champions partage + tirage du shop.

Le pool est partage entre les 8 joueurs : acheter une copie la retire du pool (plus rare
pour les autres), la revendre la rend. Roller le shop ne consomme PAS le pool (les unites
affichees ne sont retirees qu'a l'achat).
"""

from __future__ import annotations

import numpy as np

from ..data.models import SetContent
from ..data.odds import pool_size, roll_odds
from .economy import SHOP_SIZE

COSTS = (1, 2, 3, 4, 5)


class Pool:
    """Compteur de copies restantes par champion, indexe par cout."""

    def __init__(self, set_content: SetContent):
        self._remaining: dict[str, int] = {}
        self._by_cost: dict[int, list[str]] = {c: [] for c in COSTS}
        # Seules les unités jouables du set (préfixe TFT<set>_) entrent dans le pool achetable.
        # Les unités PvE/evergreen (TFT_BlueGolem, TFT9_SLIME_Crab, TFT_TrainingDummy...) ont
        # cost=1 dans setData mais NE sont PAS vendues en boutique → exclues (sinon pool 1-cost
        # pollué à 18 au lieu de 15 + un Training Dummy pouvait apparaître dans le shop).
        playable_prefix = f"TFT{set_content.set_number}_"
        champs = list(set_content.champions.values())
        # Filtre appliqué seulement si le préfixe du set existe (contenu réel) ; sinon (contenu
        # synthétique de test, set_number=0) on garde tout — pas de pollution PvE à filtrer.
        apply_filter = any(c.api_name.startswith(playable_prefix) for c in champs)
        for champ in champs:
            if champ.cost not in self._by_cost:
                continue  # ignore les unites hors 1..5 (invocations, etc.)
            if apply_filter and not champ.api_name.startswith(playable_prefix):
                continue  # unité PvE/evergreen, pas dans le pool de boutique
            self._remaining[champ.api_name] = pool_size(champ.cost)
            self._by_cost[champ.cost].append(champ.api_name)

    def remaining(self, champion: str) -> int:
        return self._remaining.get(champion, 0)

    def champions_of_cost(self, cost: int) -> list[str]:
        return self._by_cost.get(cost, [])

    def take(self, champion: str) -> bool:
        """Retire une copie (achat). False si indisponible."""
        if self._remaining.get(champion, 0) <= 0:
            return False
        self._remaining[champion] -= 1
        return True

    def give_back(self, champion: str, copies: int = 1) -> None:
        """Rend des copies au pool (vente)."""
        if champion in self._remaining:
            self._remaining[champion] += copies

    def total_remaining(self) -> int:
        return sum(self._remaining.values())


def _pick_cost(level: int, rng: np.random.Generator) -> int:
    odds = roll_odds(level)
    costs = list(odds.keys())
    probs = np.array([odds[c] for c in costs], dtype=float)
    return int(rng.choice(costs, p=probs))


def roll_shop(level: int, pool: Pool, rng: np.random.Generator) -> list[str | None]:
    """Tire SHOP_SIZE slots ponderes par les copies restantes (sans consommer le pool)."""
    slots: list[str | None] = []
    for _ in range(SHOP_SIZE):
        cost = _pick_cost(level, rng)
        champs = [c for c in pool.champions_of_cost(cost) if pool.remaining(c) > 0]
        if not champs:
            slots.append(None)
            continue
        weights = np.array([pool.remaining(c) for c in champs], dtype=float)
        weights /= weights.sum()
        slots.append(str(rng.choice(champs, p=weights)))
    return slots
