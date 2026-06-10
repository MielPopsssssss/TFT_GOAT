"""Tests pin du pathing équitable (`grid.step_toward`) et de la symétrie miroir du moteur.

Root cause investiguée (2026-06-10) : (1) les tie-breaks de `step_toward` dépendaient de
l'ordre fixe des listes de voisins (parité odd-r) -> deux marcheurs en positions miroirs
prenaient des chemins différents = biais structurel d'équipe (miroir parfait perdu 0.00
par team0 en synthétique, 0.29-0.39 en comps réelles) ; (2) le sidestep à distance égale
n'avait pas de mémoire -> oscillation A<->B infinie derrière sa propre frontline (tank
backline : 1er coup à 24.1s au lieu de 3.1s pour son jumeau miroir).

Fix : départage rng des égalités (cf. learning seat-equity : « toujours une clé de
départage rng ») + exclusion de la case précédente au sidestep (flanking émergent).
"""

from __future__ import annotations

import numpy as np
import pytest

from tft_goat.data.models import Champion, SetContent, Stats
from tft_goat.engine.grid import step_toward
from tft_goat.engine.simulate import run_combat
from tft_goat.env.state import BoardUnit


def _stats(**kw):
    base = dict(hp=2000.0, armor=50.0, magic_resist=50.0, damage=80.0, attack_speed=0.8,
                mana=60.0, initial_mana=0.0, crit_chance=0.25, crit_multiplier=1.4,
                attack_range=1.0)
    base.update(kw)
    return Stats(**base)


@pytest.fixture(scope="module")
def mirror_content() -> SetContent:
    champs = {
        "tank": Champion(api_name="tank", name="tank", cost=2, traits=(),
                         stats=_stats(hp=3500.0, damage=60.0)),
        "mel": Champion(api_name="mel", name="mel", cost=5, traits=(),
                        stats=_stats(attack_range=1.0)),
    }
    return SetContent(patch="test", set_number=17, champions=champs,
                      traits={}, items={}, augments={})


def test_sidestep_never_returns_to_previous_cell():
    """Le jam exact observé : à (2,3) visant (4,3), frontlines occupées, l'unité venait
    de (2,2). Sans mémoire elle re-sidestep sur (2,2) -> ping-pong infini. Avec `prev`,
    elle doit prendre l'autre sidestep (2,4) et contourner."""
    occupied = {(3, 2), (3, 3), (4, 3), (4, 4)}  # scrum : alliés + ennemis au contact
    nxt = step_toward((2, 3), (4, 3), occupied, prev=(2, 2))
    assert nxt == (2, 4)  # jamais (2,2) = la case d'où l'on vient


def test_step_toward_rng_breaks_ties():
    """Deux voisins strictement plus proches et symétriques autour de la ligne de visée :
    le départage doit être rng (les deux apparaissent), pas l'ordre de liste des voisins."""
    rng = np.random.default_rng(0)
    seen = {step_toward((0, 3), (4, 3), set(), rng=rng) for _ in range(100)}
    assert len(seen) >= 2  # ordre fixe = toujours la même case ; rng = plusieurs


def test_step_toward_legacy_signature_still_works():
    """Compat : l'appel positionnel historique (sans rng/prev) reste déterministe valide."""
    nxt = step_toward((0, 0), (4, 4), set())
    assert nxt is not None


@pytest.mark.parametrize("seed", [0, 1, 2])
def test_mirror_combat_is_fair(mirror_content, seed):
    """Miroir parfait (mêmes 4 unités des deux côtés) : win rate team0 ~ 0.50.

    Bande N-aware (cf. learning seat-equity) : N=200, sigma=0.5/sqrt(200)=0.035,
    bande à 4 sigma = [0.36, 0.64]. Avec le bug : 0.00 (échec franc). Multi-seeds :
    un seed « chanceux » ne doit pas masquer un biais structurel résiduel."""
    board = [BoardUnit("tank", 2) for _ in range(3)] + [BoardUnit("mel", 2)]
    rng = np.random.default_rng(seed)
    n = 200
    wins = sum(
        run_combat(board, board, mirror_content, rng).winner == 0 for _ in range(n)
    )
    assert 0.36 <= wins / n <= 0.64
