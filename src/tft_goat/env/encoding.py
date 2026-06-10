"""Encodage des observations : GameState -> dict de tableaux numpy + espaces gym.

Inclut le « scouting » (etat resume des adversaires), central a TFT. Le masque d'actions
legales est fourni via `info` (convention compatible RLlib).
"""

from __future__ import annotations

import numpy as np
from gymnasium import spaces

from ..data.gods import SET17_GODS
from ..data.models import SetContent
from .actions import NUM_ACTIONS, legal_mask
from .economy import BENCH_CAP, MAX_LEVEL, SHOP_SIZE
from .state import GameState, PlayerState

MAX_BOARD = 10
MAX_OPP = 7
N_SCALARS = 10  # gold,level,xp,hp,streak,round,maxlvl,components,augment_power,augment_available
UNIT_FEATS = 3  # champ_idx, star, items

# Realm of the Gods : l'agent doit VOIR pour qui il vote (sinon le vote est du bruit).
# 9 (lobby one-hot) + 3 (slot d'offre : 0=vide, 1=dieu A, 2=dieu B) + 9 (votes /3)
# + 9 (dieu aligné one-hot) + 1 (boon présent). Ordre canonique = SET17_GODS.
_GOD_ORDER = tuple(SET17_GODS)
_N_GODS = len(_GOD_ORDER)
GOD_VOTE_SLOTS = 3
GOD_FEATS = _N_GODS + GOD_VOTE_SLOTS + _N_GODS + _N_GODS + 1  # = 31


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
                "gods": spaces.Box(0.0, 3.0, shape=(GOD_FEATS,), dtype=np.float32),
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

    def _gods_vec(self, state: GameState, p: PlayerState) -> np.ndarray:
        vec = np.zeros(GOD_FEATS, dtype=np.float32)
        lobby = tuple(state.lobby_gods)
        for god in lobby:  # lobby one-hot (toujours visible)
            if god in _GOD_ORDER:
                vec[_GOD_ORDER.index(god)] = 1.0
        base = _N_GODS
        for i, god in enumerate(p.god_offer_gods[:GOD_VOTE_SLOTS]):  # slots d'offre
            # invariant : _offer_gods ne tire QUE dans lobby_gods -> le 0 ne signifie
            # jamais « dieu hors lobby », uniquement « slot vide »
            if god in lobby:
                vec[base + i] = float(lobby.index(god) + 1)  # 1=dieu A, 2=dieu B
        base += GOD_VOTE_SLOTS
        for god, n in p.god_votes.items():  # votes cumulés, normalisés sur les 3 votes
            if god in _GOD_ORDER:
                vec[base + _GOD_ORDER.index(god)] = n / 3.0
        base += _N_GODS
        if p.aligned_god in _GOD_ORDER:  # dieu aligné one-hot
            vec[base + _GOD_ORDER.index(p.aligned_god)] = 1.0
        vec[-1] = 1.0 if p.god_boon else 0.0
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
            "gods": self._gods_vec(state, p),
        }

    def action_mask(self, state: GameState, agent: str) -> np.ndarray:
        return legal_mask(state, state.players[agent]).astype(np.int8)
