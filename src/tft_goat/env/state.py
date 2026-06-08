"""Etat mutable de l'environnement (pattern Gym).

Le *contenu* (SetContent) reste immuable ; l'etat de partie est mute in-place a chaque step.
La logique de calcul vit dans economy/shop/traits/combat (pures, testees isolement).
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..data.models import SetContent
from .economy import BENCH_CAP, SHOP_SIZE
from .shop import Pool


@dataclass
class BoardUnit:
    champion_api: str
    star: int = 1
    on_board: bool = False
    items: int = 0  # nombre d'objets completes equipes (0..3)
    item_apis: tuple[str, ...] = ()  # identites des objets (optionnel ; pour les procs moteur)

    @property
    def copies(self) -> int:
        """Nombre de copies 1-etoile que represente cette unite (pour le pool)."""
        return 3 ** (self.star - 1)


@dataclass
class PlayerState:
    agent_id: str
    gold: int = 0
    level: int = 1
    xp: int = 0
    hp: int = 100
    streak: int = 0  # >0 win streak, <0 loss streak
    shop: list[str | None] = field(default_factory=lambda: [None] * SHOP_SIZE)
    bench: list[BoardUnit] = field(default_factory=list)
    board: list[BoardUnit] = field(default_factory=list)
    alive: bool = True
    passed: bool = False  # a termine sa phase de planification ce round
    placement: int = 0  # rempli a l'elimination (1 = vainqueur)
    components: list[str] = field(default_factory=list)  # composants tenus (apiNames)
    augment_power: float = 0.0  # bonus cumule des augments (mitigation, resolvers non-moteur)
    augment_offer: list[str] = field(default_factory=list)  # augments proposes ce round
    chosen_augments: list[str] = field(default_factory=list)  # apiNames des augments choisis
    god_offer: list[str] = field(default_factory=list)  # Realm of the Gods : 3 champions au choix

    @property
    def board_cap(self) -> int:
        return self.level

    @property
    def board_champions(self) -> list[str]:
        return [u.champion_api for u in self.board]

    def all_units(self) -> list[BoardUnit]:
        return self.bench + self.board

    def bench_has_room(self) -> bool:
        return len(self.bench) < BENCH_CAP


@dataclass
class GameState:
    players: dict[str, PlayerState]
    pool: Pool
    set_content: SetContent
    rng: np.random.Generator
    round_index: int = 0

    def alive_players(self) -> list[PlayerState]:
        return [p for p in self.players.values() if p.alive]
