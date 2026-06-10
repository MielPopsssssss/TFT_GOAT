"""Garde-fou de réalisme : la durée de partie doit rester dans une bande réaliste.

Vrai TFT : une partie 8 joueurs finit vers stage 6-7. Avant la correction de la mitigation
augment erronée des dégâts joueur, le sim finissait ~stage 7.8 (médiane 8-2) — largement trop.
Ce test (jeu aléatoire seedé) attrape une régression qui re-gonflerait/écraserait la durée.
"""

from __future__ import annotations

import numpy as np

from tft_goat.env.rounds import stage_of
from tft_goat.env.tft_env import TftEnv

N_GAMES = 60


def _final_stage(seed: int) -> int:
    env = TftEnv()
    obs, infos = env.reset(seed=seed)
    rng = np.random.default_rng(seed)
    while env.agents:
        acts = {
            a: int(rng.choice(np.flatnonzero(infos[a]["action_mask"])))
            for a in env.agents
        }
        obs, r, term, trunc, infos = env.step(acts)
    return stage_of(env._state.round_index)


def test_average_game_length_is_realistic():
    """Stage final moyen dans [6.0, 7.3] — réaliste vs vrai TFT (~6.5-7).

    NB : jeu aléatoire => léger sur-allongement résiduel (boards sous-remplis) ; la borne
    haute tolère cet artefact. Une régression de la formule de dégâts joueur sortirait de la bande.
    """
    stages = [_final_stage(s) for s in range(N_GAMES)]
    avg = sum(stages) / len(stages)
    assert 6.0 <= avg <= 7.3, f"stage final moyen {avg:.2f} hors bande réaliste [6.0, 7.3]"


def test_level_progression_matches_real_tft():
    """La courbe niveau-par-stage suit le vrai TFT — garde-fou éco/XP (2026-06-08).

    Bandes vérifiées (sim random vs typique réel) : S3 ~5-6, S5 ~7-8, S7 ~8-9. Un drift de la
    table XP ou des revenus ferait sortir la courbe de ces bandes.
    """
    from collections import defaultdict

    from tft_goat.env.rounds import round_in_stage

    lvl_at_stage = defaultdict(list)
    for seed in range(40):
        env = TftEnv()
        obs, infos = env.reset(seed=seed)
        rng = np.random.default_rng(seed)
        seen = set()
        while env.agents:
            stt = env._state
            stg = stage_of(stt.round_index)
            if round_in_stage(stt.round_index) == 1 and stg not in seen:
                seen.add(stg)
                for p in stt.alive_players():
                    lvl_at_stage[stg].append(p.level)
            acts = {
                a: int(rng.choice(np.flatnonzero(infos[a]["action_mask"])))
                for a in env.agents
            }
            obs, r, term, trunc, infos = env.step(acts)

    def avg(stg):
        return sum(lvl_at_stage[stg]) / len(lvl_at_stage[stg])

    assert 5.0 <= avg(3) <= 6.5, f"niveau S3 {avg(3):.1f} hors bande"
    assert 6.5 <= avg(5) <= 8.0, f"niveau S5 {avg(5):.1f} hors bande"
    assert 7.5 <= avg(7) <= 9.0, f"niveau S7 {avg(7):.1f} hors bande"


def test_better_placement_correlates_with_higher_level():
    """Cohérence macro : mieux on place, plus haut on monte (placement ↔ progression).

    Observé stable : place 1 ≈ 8.4, place 8 ≈ 7.7. Une régression cassant le lien
    combat→survie→progression aplatirait ou inverserait ce gradient.
    """
    from collections import defaultdict

    lvl_by_place = defaultdict(list)
    for seed in range(40):
        env = TftEnv()
        obs, infos = env.reset(seed=seed)
        rng = np.random.default_rng(seed)
        last_lvl = {a: 1 for a in env.possible_agents}
        while env.agents:
            for a in env.possible_agents:
                if env._state.players[a].alive:
                    last_lvl[a] = env._state.players[a].level
            acts = {
                a: int(rng.choice(np.flatnonzero(infos[a]["action_mask"])))
                for a in env.agents
            }
            obs, r, term, trunc, infos = env.step(acts)
        for a, p in env._state.players.items():
            lvl_by_place[p.placement].append(last_lvl[a])

    def avg(pl):
        return sum(lvl_by_place[pl]) / len(lvl_by_place[pl])

    top = (avg(1) + avg(2)) / 2
    bottom = (avg(7) + avg(8)) / 2
    assert top > bottom + 0.2, f"top {top:.2f} pas > bottom {bottom:.2f} : gradient cassé"
