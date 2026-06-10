"""TftEnv — environnement PettingZoo ParallelEnv (8 joueurs) pour le macro-jeu TFT.

Chaque step = une micro-action par agent (achat, roll, level, deplacement, PASS). Quand tous
les vivants ont PASS (ou cap de planification atteint), le combat est resolu via le
CombatResolver injecte, les revenus tombent, le round avance, les morts sont elimines.
Recompense terminale = placement (1er -> +1 ... 8e -> -1).
"""

from __future__ import annotations

import numpy as np
from pettingzoo import ParallelEnv

from ..data.content import load_set
from ..data.gods import choose_lobby_gods
from ..data.models import SetContent
from ..data.stats_models import MetaStats
from .actions import NUM_ACTIONS, PASS, apply_action, legal_mask
from .combat import CombatResolver, HeuristicResolver
from .encoding import Encoder
from .rounds import (
    assign_eliminations,
    finalize_if_over,
    resolve_combat,
    start_round,
)
from .shop import Pool
from .state import GameState, PlayerState

N_PLAYERS = 8
MAX_PLANNING_STEPS = 50  # garde-fou anti-boucle dans une phase de planification
MAX_ROUNDS = 100  # garde-fou dur de fin de partie


def placement_reward(placement: int) -> float:
    """1er -> +1.0, 8e -> -1.0 (lineaire)."""
    return (4.5 - placement) / 3.5


class TftEnv(ParallelEnv):
    metadata = {"name": "tft_goat_v0"}

    def __init__(
        self,
        set_content: SetContent | None = None,
        resolver: CombatResolver | None = None,
        meta_stats: MetaStats | None = None,
    ):
        self.set_content = set_content or load_set()
        self.resolver = resolver or HeuristicResolver(meta_stats)
        self.encoder = Encoder(self.set_content)
        self.possible_agents = [f"player_{i}" for i in range(N_PLAYERS)]
        self._state: GameState | None = None
        self._phase_steps = 0
        self._done: set[str] = set()

    # --- espaces -----------------------------------------------------------
    def observation_space(self, agent: str):
        return self.encoder.observation_space()

    def action_space(self, agent: str):
        return self.encoder.action_space()

    # --- reset -------------------------------------------------------------
    def reset(self, seed: int | None = None, options: dict | None = None):
        rng = np.random.default_rng(seed)
        players = {aid: PlayerState(agent_id=aid) for aid in self.possible_agents}
        self._state = GameState(
            players=players, pool=Pool(self.set_content),
            set_content=self.set_content, rng=rng, round_index=0,
            lobby_gods=choose_lobby_gods(rng),  # 2 dieux tirés pour tout le lobby
        )
        self.agents = list(self.possible_agents)
        self._phase_steps = 0
        self._done = set()
        start_round(self._state)
        obs = {a: self.encoder.encode(self._state, a) for a in self.agents}
        infos = {a: {"action_mask": self.encoder.action_mask(self._state, a)} for a in self.agents}
        return obs, infos

    # --- step --------------------------------------------------------------
    def step(self, actions: dict[str, int]):
        state = self._state
        acting = list(self.agents)
        rewards = {a: 0.0 for a in acting}
        terminations = {a: False for a in acting}
        truncations = {a: False for a in acting}

        # 1) appliquer une micro-action par agent. Coercition d'une action illegale : vers PASS
        # si PASS est legal, sinon vers la PREMIERE action legale — jamais vers un PASS aveugle,
        # qui permettrait de sauter un choix force (offre de dieu/augment, mask[PASS]=False).
        for a in acting:
            p = state.players[a]
            if p.passed:
                continue
            try:
                act = int(actions.get(a, PASS))
            except (TypeError, ValueError):  # payload malformé (frontière de confiance)
                act = PASS
            mask = legal_mask(state, p)
            if act < 0 or act >= NUM_ACTIONS or not mask[act]:
                act = PASS if mask[PASS] else int(np.flatnonzero(mask)[0])
            apply_action(state, p, act)

        self._phase_steps += 1
        planning_done = (
            all(p.passed for p in state.alive_players())
            or self._phase_steps >= MAX_PLANNING_STEPS
        )

        game_over = False
        if planning_done:
            resolve_combat(state, self.resolver)
            assign_eliminations(state)
            game_over = finalize_if_over(state)
            if state.round_index >= MAX_ROUNDS and not game_over:
                game_over = self._truncate_by_hp(state)
            if not game_over:
                state.round_index += 1
                start_round(state)
                self._phase_steps = 0

        # 2) recompenses/terminaisons des nouveaux elimines
        for a in acting:
            p = state.players[a]
            if p.placement > 0 and a not in self._done:
                rewards[a] = placement_reward(p.placement)
                terminations[a] = True
                self._done.add(a)

        # 3) observations (sur les agents du debut de step) puis retrait des termines
        obs = {a: self.encoder.encode(state, a) for a in acting}
        infos = {a: {"action_mask": self.encoder.action_mask(state, a)} for a in acting}
        self.agents = [a for a in acting if not terminations[a] and not truncations[a]]
        return obs, rewards, terminations, truncations, infos

    def _truncate_by_hp(self, state: GameState) -> bool:
        """Fin forcee : classe les vivants restants par PV decroissants."""
        alive = sorted(state.alive_players(), key=lambda p: -p.hp)
        place = 1
        for p in alive:
            p.placement = place
            p.alive = False
            place += 1
        return True

    def render(self):
        return None
