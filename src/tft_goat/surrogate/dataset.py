"""Datasets pour le surrogate de combat.

- bootstrap : boards aleatoires + label = P(a gagne) du combat heuristique ancre (distillation).
- riot      : paires (board_i, board_j, y=placement_i<placement_j) depuis des parties match-v1.
"""

from __future__ import annotations

import numpy as np

from ..data.models import SetContent
from ..data.stats_models import MetaStats
from ..data.riot.models import Match
from ..env.combat import board_strength
from ..env.state import BoardUnit

_STAR_P = (0.7, 0.25, 0.05)  # proba 1★ / 2★ / 3★


_ITEM_P = (0.7, 0.15, 0.1, 0.05)  # proba 0/1/2/3 items


def _completed_item_pool(content: SetContent) -> list[str]:
    return [
        api for api, it in content.items.items()
        if len(it.composition) == 2 and "_Augment_" not in api and "Emblem" not in api
    ]


def sample_board(
    content: SetContent, rng: np.random.Generator, item_pool: list[str] | None = None
) -> list[BoardUnit]:
    """Board aleatoire : 1..9 champions (cout 1..5), etoiles + items ponderes.

    Si `item_pool` est fourni, les unites recoivent de vraies identites d'objets (pour que le
    moteur applique les procs reels lors de la generation de donnees).
    """
    pool = [api for api, c in content.champions.items() if 1 <= c.cost <= 5]
    k = int(rng.integers(1, 10))
    picks = rng.choice(pool, size=k, replace=True)
    stars = rng.choice([1, 2, 3], size=k, p=_STAR_P)
    items = rng.choice([0, 1, 2, 3], size=k, p=_ITEM_P)
    board = []
    for api, s, it in zip(picks, stars, items):
        item_apis = ()
        if item_pool and it > 0:
            item_apis = tuple(str(x) for x in rng.choice(item_pool, size=int(it)))
        board.append(BoardUnit(str(api), int(s), items=int(it), item_apis=item_apis))
    return board


def make_engine_dataset(
    content: SetContent, n_pairs: int, rng: np.random.Generator, samples: int = 1
) -> tuple[list[list[BoardUnit]], list[list[BoardUnit]], np.ndarray]:
    """Paires de boards + label = P(A gagne) selon le VRAI moteur de combat (verite terrain).

    `samples` runs par paire : 1 = label binaire (rapide), >1 = proba douce (moins bruite).
    """
    from ..engine.resolver import EngineResolver

    resolver = EngineResolver()
    item_pool = _completed_item_pool(content)
    boards_a, boards_b, labels = [], [], []
    for _ in range(n_pairs):
        a = sample_board(content, rng, item_pool)
        b = sample_board(content, rng, item_pool)
        wins = sum(resolver.resolve(a, b, content, rng).winner == 0 for _ in range(samples))
        boards_a.append(a)
        boards_b.append(b)
        labels.append(wins / samples)
    return boards_a, boards_b, np.array(labels, dtype=np.float32)


def make_bootstrap_dataset(
    content: SetContent, meta_stats: MetaStats | None, n_pairs: int, rng: np.random.Generator
) -> tuple[list[list[BoardUnit]], list[list[BoardUnit]], np.ndarray]:
    """Paires de boards + label de distillation = sa/(sa+sb)."""
    boards_a, boards_b, labels = [], [], []
    for _ in range(n_pairs):
        a = sample_board(content, rng)
        b = sample_board(content, rng)
        sa = board_strength(a, content, meta_stats)
        sb = board_strength(b, content, meta_stats)
        label = 0.5 if (sa + sb) == 0 else sa / (sa + sb)
        boards_a.append(a)
        boards_b.append(b)
        labels.append(label)
    return boards_a, boards_b, np.array(labels, dtype=np.float32)


def _board_from_participant(units) -> list[BoardUnit]:
    return [BoardUnit(u.character_id, max(1, u.tier), items=len(u.items)) for u in units]


def pairs_from_matches(
    matches: list[Match],
) -> tuple[list[list[BoardUnit]], list[list[BoardUnit]], np.ndarray]:
    """Paires (board_i, board_j, y=1 si i mieux classe que j) depuis des parties.

    Label = proxy de force de board relative (faute de combats round-par-round chez Riot).
    """
    boards_a, boards_b, labels = [], [], []
    for m in matches:
        parts = m.participants
        for i in range(len(parts)):
            for j in range(i + 1, len(parts)):
                pi, pj = parts[i], parts[j]
                if pi.placement == pj.placement:
                    continue
                boards_a.append(_board_from_participant(pi.units))
                boards_b.append(_board_from_participant(pj.units))
                labels.append(1.0 if pi.placement < pj.placement else 0.0)
    return boards_a, boards_b, np.array(labels, dtype=np.float32)
