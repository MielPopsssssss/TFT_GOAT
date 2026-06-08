"""Encodage des observations : GameState -> dict de tableaux numpy + espaces gym.

Inclut le « scouting » (etat resume des adversaires), central a TFT. Le masque d'actions
legales est fourni via `info` (convention compatible RLlib).
"""

from __future__ import annotations

import numpy as np
from gymnasium import spaces

from ..data.models import SetContent
from .actions import NUM_ACTIONS, legal_mask
from .economy import BENCH_CAP, MAX_LEVEL, SHOP_SIZE
from .state import GameState, PlayerState

MAX_BOARD = 10
MAX_OPP = 7
N_SCALARS = 10  # gold,level,xp,hp,streak,round,maxlvl,components,augment_power,augment_available
UNIT_FEATS = 3  # champ_idx, star, items


class Encoder:
    """Construit les index champion/trait une fois, puis encode les observations."""

    def __init__(self, set_content: SetContent):
        champs = sorted(set_content.champions.keys())
        # index 0 reserve a « vide » ; champions de 1 a N
        self.champ_index = {api: i + 1 for i, api in enumerate(champs)}
        self.n_champ = len(champs)
        traits = sorted(set_content.traits.keys())
        self.trait_index = {
            set_content.traits[api].name: i for i, api in enumerate(traits)
        }
        self.n_trait = len(traits)
        self._set_content = set_content

    # --- espaces -----------------------------------------------------------
    def observation_space(self) -> spaces.Dict:
        c = float(self.n_champ + 1)
        return spaces.Dict(
            {
                "scalars": spaces.Box(0.0, 1e4, shape=(N_SCALARS,), dtype=np.float32),
                "shop": spaces.Box(0.0, c, shape=(SHOP_SIZE,), dtype=np.float32),
                "bench": spaces.Box(0.0, c, shape=(BENCH_CAP, UNIT_FEATS), dtype=np.float32),
                "board": spaces.Box(0.0, c, shape=(MAX_BOARD, UNIT_FEATS), dtype=np.float32),
                "traits": spaces.Box(0.0, 10.0, shape=(self.n_trait,), dtype=np.float32),
                "opponents": spaces.Box(0.0, 1e4, shape=(MAX_OPP, 3), dtype=np.float32),
            }
        )

    def action_space(self) -> spaces.Discrete:
        return spaces.Discrete(NUM_ACTIONS)

    # --- encodage ----------------------------------------------------------
    def _units(self, units, n: int) -> np.ndarray:
        arr = np.zeros((n, UNIT_FEATS), dtype=np.float32)
        for i, u in enumerate(units[:n]):
            arr[i, 0] = self.champ_index.get(u.champion_api, 0)
            arr[i, 1] = u.star
            arr[i, 2] = u.items
        return arr

    def _traits_vec(self, player: PlayerState) -> np.ndarray:
        from .traits import active_traits

        vec = np.zeros(self.n_trait, dtype=np.float32)
        for name, tier in active_traits(player.board_champions, self._set_content).items():
            idx = self.trait_index.get(name)
            if idx is not None:
                vec[idx] = tier
        return vec

    def encode(self, state: GameState, agent: str) -> dict[str, np.ndarray]:
        p = state.players[agent]
        scalars = np.array(
            [p.gold, p.level, p.xp, p.hp, p.streak, state.round_index, MAX_LEVEL,
             len(p.components), p.augment_power, 1.0 if p.augment_offer else 0.0],
            dtype=np.float32,
        )
        shop = np.array(
            [self.champ_index.get(c, 0) if c else 0 for c in p.shop], dtype=np.float32
        )
        opp = np.zeros((MAX_OPP, 3), dtype=np.float32)
        others = [q for aid, q in sorted(state.players.items()) if aid != agent]
        for i, q in enumerate(others[:MAX_OPP]):
            opp[i] = [q.hp, q.level, len(q.board)]
        return {
            "scalars": scalars,
            "shop": shop,
            "bench": self._units(p.bench, BENCH_CAP),
            "board": self._units(p.board, MAX_BOARD),
            "traits": self._traits_vec(p),
            "opponents": opp,
        }

    def action_mask(self, state: GameState, agent: str) -> np.ndarray:
        return legal_mask(state, state.players[agent]).astype(np.int8)
