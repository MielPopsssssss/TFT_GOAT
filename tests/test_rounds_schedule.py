"""Tests du schedule des rounds (Realm of the Gods, PvE/PvP)."""

from __future__ import annotations

from tft_goat.env.rounds import (
    PVE_OPENING,
    ROUNDS_PER_STAGE,
    STAGE_BASE_DAMAGE,
    is_god_round,
    is_pvp,
    round_in_stage,
    stage_base_damage,
    stage_of,
)


def _round_index(stage: int, round_in: int) -> int:
    """Index global du round `stage-round_in` (stage>=2)."""
    return PVE_OPENING + (stage - 2) * ROUNDS_PER_STAGE + (round_in - 1)


def test_god_vote_rounds_are_only_2_4_3_4_4_4():
    """Les Minor Blessings (votes) n'ont lieu qu'aux 2-4, 3-4, 4-4 — vérifié vs patch 17.4.

    Avant correction, is_god_round se déclenchait à CHAQUE x-4 (5-4, 6-4, 7-4 inclus) ;
    le vrai mécanisme n'a que 3 votes qui fixent le dieu aligné après 4-4.
    """
    god_rounds = {_round_index(s, 4) for s in (2, 3, 4)}
    # sanity : ces indices sont bien des x-4
    for idx in god_rounds:
        assert round_in_stage(idx) == 4
    assert {stage_of(idx) for idx in god_rounds} == {2, 3, 4}

    # exactement ces 3 rounds sur toute la partie (jusqu'au stage 8)
    fired = {idx for idx in range(PVE_OPENING + 6 * ROUNDS_PER_STAGE) if is_god_round(idx)}
    assert fired == god_rounds

    # explicitement : 5-4, 6-4, 7-4 ne sont PAS des rounds de vote
    for s in (5, 6, 7):
        assert not is_god_round(_round_index(s, 4))


def test_x4_rounds_are_non_pvp_at_all_stages():
    """Tous les x-4 restent non-PvP (carrousel/loot), même hors rounds de vote."""
    for s in (2, 3, 4, 5, 6, 7):
        assert not is_pvp(_round_index(s, 4))


def test_player_damage_base_table_verified_patch_17_4():
    """Base de dégâts joueur par stage — VÉRIFIÉ vs patch 17.4 (op.gg, 2026-06-08).

    Formule réelle : base_stage + 1 × (unités ennemies survivantes). Base confirmée
    {2:2, 3:5, 4:8, 5:10, 6:12, 7+:17}, per-unité PLAT = 1 (pas pondéré étoile).
    """
    assert STAGE_BASE_DAMAGE == {1: 0, 2: 2, 3: 5, 4: 8, 5: 10, 6: 12, 7: 17}
    # via la fonction (stage -> index global) : 2-1, 3-1, ... 7-1
    expected = {2: 2, 3: 5, 4: 8, 5: 10, 6: 12, 7: 17}
    for stage, base in expected.items():
        assert stage_base_damage(_round_index(stage, 1)) == base
    # stage 8+ retombe sur 17 (cap)
    assert stage_base_damage(_round_index(8, 1)) == 17
