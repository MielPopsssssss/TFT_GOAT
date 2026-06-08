"""Joue une VRAIE partie 8 joueurs, séquence réelle, narrée stage par stage.

Combat = vrai moteur tick-par-tick (EngineResolver). Joueurs = politique scriptée (choix
réfléchis). Affiche chaque round (stage-round, type PvE/Augment/PvP), l'état des joueurs et les
éliminations, jusqu'au vainqueur.

Usage : .venv/bin/python -m tft_goat.scripts.play_game [seed]
"""

from __future__ import annotations

import sys

import numpy as np

from ..agent.scripted import scripted_action
from ..data.content import load_set
from ..engine.resolver import EngineResolver
from ..env.actions import PASS, apply_action
from ..env.rounds import (
    AUGMENT_ROUNDS,
    assign_eliminations,
    finalize_if_over,
    is_pvp,
    round_in_stage,
    stage_of,
    start_round,
)
from ..env.shop import Pool
from ..env.state import GameState, PlayerState
from ..env.traits import active_traits

N_PLAYERS = 8
ROUNDS_PER_STAGE = 7
MAX_ROUNDS = 120


def _label(round_index: int) -> str:
    return f"{stage_of(round_index)}-{round_in_stage(round_index)}"


def _round_type(round_index: int) -> str:
    if round_index in AUGMENT_ROUNDS:
        return "AUGMENT + PvP"
    if is_pvp(round_index):
        return "PvP"
    ris = round_in_stage(round_index)
    if stage_of(round_index) >= 2 and ris == 4:
        return "Realm of the Gods (1 champion / 3)"
    if stage_of(round_index) >= 2 and ris == 7:
        return "PvE (monstres)"
    return "PvE (creeps)"


def _short(api: str) -> str:
    return api.split("_")[-1]


_TIER_ICON = {"silver": "⚪", "gold": "🟡", "prismatic": "🟣", "god": "✨"}


def _fmt_augment(api: str, content) -> str:
    aug = content.augments.get(api)
    tier = aug.tier if aug else "?"
    name = (aug.name if aug and aug.name else _short(api))
    return f"{_TIER_ICON.get(tier, '·')}{tier[:4]}:{name}"


def _augment_offers_snapshot(state: GameState) -> dict[str, list[str]]:
    """Capture l'offre d'augment de chaque joueur AVANT qu'il ne choisisse (le pick la vide)."""
    return {a: list(p.augment_offer) for a, p in state.players.items() if p.augment_offer}


def _top_traits(player: PlayerState, content) -> str:
    active = active_traits(player.board_champions, content)
    if not active:
        return "-"
    top = sorted(active.items(), key=lambda kv: -kv[1])[:2]
    return ", ".join(f"{n} {t}" for n, t in top)


def _planning(state: GameState, player: PlayerState) -> None:
    for _ in range(60):  # garde-fou
        action = scripted_action(state, player)
        apply_action(state, player, action)
        if action == PASS:
            break


def play(seed: int = 0) -> None:
    content = load_set()
    rng = np.random.default_rng(seed)
    players = {f"player_{i}": PlayerState(agent_id=f"player_{i}") for i in range(N_PLAYERS)}
    state = GameState(players=players, pool=Pool(content), set_content=content, rng=rng)
    resolver = EngineResolver()

    print(f"=== PARTIE TFT Set 17 — 8 joueurs scriptés, vrai moteur (seed {seed}) ===\n")
    start_round(state)
    while state.round_index < MAX_ROUNDS:
        alive_before = {a for a, p in state.players.items() if p.alive}
        offers = _augment_offers_snapshot(state)  # avant les picks
        for p in state.alive_players():
            _planning(state, p)
        resolve_combat_engine(state, resolver)
        assign_eliminations(state)
        over = finalize_if_over(state)

        # narration du round
        rd, rtype = _label(state.round_index), _round_type(state.round_index)
        print(f"--- Round {rd}  [{rtype}] ---")
        if offers:  # round d'augment : montre l'offre (3 augments + tiers) et le choix de chacun
            for aid in sorted(offers):
                p = state.players[aid]
                proposed = "  |  ".join(_fmt_augment(a, content) for a in offers[aid])
                chosen = p.chosen_augments[-1] if p.chosen_augments else None
                pick = _fmt_augment(chosen, content) if chosen else "—"
                rerolled = "  🔄(reroll)" if chosen and chosen not in offers[aid] else ""
                print(f"  {_short(aid):9s} offre: {proposed}   →  choix: {pick}{rerolled}")
            print()
        ranking = sorted(state.players.values(), key=lambda p: (-p.alive, -p.hp))
        for p in ranking:
            if p.agent_id not in alive_before:
                continue  # deja mort avant ce round
            tag = ""
            if p.placement == 1:
                tag = "  🏆 VAINQUEUR"
            elif not p.alive:
                tag = f"  ☠ ELIMINE (place {p.placement})"
            print(f"  {_short(p.agent_id):9s} PV {max(p.hp,0):>3}  niv {p.level}  "
                  f"or {p.gold:>2}  board {len(p.board)} [{_top_traits(p, content)}]{tag}")
        print()
        if over:
            break
        state.round_index += 1
        start_round(state)

    winner = next((p for p in state.players.values() if p.placement == 1), None)
    print("=== CLASSEMENT FINAL ===")
    for p in sorted(state.players.values(), key=lambda p: p.placement):
        print(f"  {p.placement}. {_short(p.agent_id):9s} (niv {p.level})")
    if winner:
        print(f"\n🏆 Vainqueur : {_short(winner.agent_id)} en {state.round_index} rounds "
              f"(stage {_label(state.round_index)})")


def resolve_combat_engine(state: GameState, resolver) -> None:
    from ..env.rounds import resolve_combat

    resolve_combat(state, resolver)


if __name__ == "__main__":
    play(int(sys.argv[1]) if len(sys.argv) > 1 else 0)
