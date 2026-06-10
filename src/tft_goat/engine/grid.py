"""Grille hexagonale (offset odd-r) : distance, voisins, pas vers une cible.

Coordonnees (row, col). Conversion en cube pour la distance hexagonale exacte.
"""

from __future__ import annotations

from .config import GRID_COLS, GRID_ROWS

# Voisins odd-r : dependent de la parite de la ligne.
_NEIGHBORS_EVEN = [(-1, 0), (-1, -1), (0, -1), (0, 1), (1, -1), (1, 0)]
_NEIGHBORS_ODD = [(-1, 1), (-1, 0), (0, -1), (0, 1), (1, 0), (1, 1)]


def _to_cube(row: int, col: int) -> tuple[int, int, int]:
    x = col - (row - (row & 1)) // 2
    z = row
    y = -x - z
    return x, y, z


def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
    ax, ay, az = _to_cube(*a)
    bx, by, bz = _to_cube(*b)
    return (abs(ax - bx) + abs(ay - by) + abs(az - bz)) // 2


def in_bounds(row: int, col: int) -> bool:
    return 0 <= row < GRID_ROWS and 0 <= col < GRID_COLS


def neighbors(pos: tuple[int, int]) -> list[tuple[int, int]]:
    row, col = pos
    deltas = _NEIGHBORS_ODD if (row & 1) else _NEIGHBORS_EVEN
    out = []
    for dr, dc in deltas:
        nr, nc = row + dr, col + dc
        if in_bounds(nr, nc):
            out.append((nr, nc))
    return out


def step_toward(
    src: tuple[int, int], dst: tuple[int, int], occupied: set[tuple[int, int]],
    *, rng=None, prev: tuple[int, int] | None = None,
) -> tuple[int, int] | None:
    """Voisin libre de `src` se rapprochant de `dst`.

    Priorite : voisin strictement plus proche ; sinon sidestep a egale distance (anti-blocage
    derriere les allies) ; None seulement si vraiment aucune case libre utile.

    Les EGALITES sont departagees par `rng` : l'ordre fixe des listes de voisins depend de
    la parite odd-r, donc deux marcheurs en positions MIROIRS faisaient des choix differents
    -> biais structurel d'equipe mesurable (miroir parfait perdu 0.00/0.29-0.39 par team0 ;
    cf. tests/test_pathing_symmetry.py). Sans rng (legacy), premier trouve (deterministe).

    Le sidestep ne revient jamais sur `prev` (case d'ou l'on vient) : sans memoire, une
    unite bloquee oscillait A<->B indefiniment derriere sa frontline (1er coup a 24s au
    lieu de 3s) au lieu de contourner.
    """
    cur = distance(src, dst)
    closer: list[tuple[int, int]] = []
    best_d = cur
    for nb in neighbors(src):
        if nb in occupied:
            continue
        d = distance(nb, dst)
        if d < best_d:
            closer, best_d = [nb], d
        elif closer and d == best_d:
            closer.append(nb)
    if closer:
        if rng is not None and len(closer) > 1:
            return closer[int(rng.integers(len(closer)))]
        return closer[0]
    side = [
        nb for nb in neighbors(src)  # sidestep : meme distance, pour contourner un blocage
        if nb not in occupied and nb != prev and distance(nb, dst) == cur
    ]
    if side:
        if rng is not None and len(side) > 1:
            return side[int(rng.integers(len(side)))]
        return side[0]
    return None
