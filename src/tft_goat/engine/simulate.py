"""Boucle de combat tick-par-tick entre deux boards (vraies stats)."""

from __future__ import annotations

import numpy as np

from ..data.models import SetContent
from ..env.combat import CombatResult
from ..env.state import BoardUnit
from .abilities import get_ability
from .augments_set17 import AUGMENT_REGISTRY
from .config import (
    ATTACK_SPEED_CAP,
    ATTACK_WINDUP,
    GRID_COLS,
    GRID_ROWS,
    MANA_LOCK_DURATION,
    MANA_ON_HIT_CAP,
    MANA_ON_HIT_POSTMIT,
    MANA_ON_HIT_PREMIT,
    MANA_PER_ATTACK,
    MAX_COMBAT_TICKS,
    MOVE_INTERVAL,
    ROWS_PER_TEAM,
    SHIELD_DEFAULT_DURATION,
    TICK_DT,
)
from .grid import distance, neighbors, step_toward
from .items_set17 import (
    ITEM_COMBAT_START,
    ITEM_HP_THRESHOLD,
    ITEM_ON_ATTACK,
    ITEM_ON_CAST,
    ITEM_ON_DAMAGED,
    ITEM_ON_TICK,
    ITEM_REVIVE,
)
from .trait_effects import apply_team_traits
from .unit import CombatUnit, build_unit


def _item_on_attack(u: CombatUnit, target: CombatUnit, ctx) -> None:
    for api in u.item_apis:
        hook = ITEM_ON_ATTACK.get(api)
        if hook:
            hook(u, target, ctx)


def _item_on_cast(u: CombatUnit, ctx) -> None:
    for api in u.item_apis:
        hook = ITEM_ON_CAST.get(api)
        if hook:
            hook(u, ctx)


class CombatContext:
    """API fournie aux sorts + gestion des degats/mana/morts."""

    def __init__(self, units: list[CombatUnit], rng: np.random.Generator):
        self.units = units
        self.rng = rng
        self.time = 0.0  # secondes ecoulees de combat (pour les durees)
        self._casting: CombatUnit | None = None  # unite en train de lancer son sort
        self._in_on_damaged = False  # garde anti-recursion (reflets mutuels type Bramble)

    def living_enemies(self, u: CombatUnit) -> list[CombatUnit]:
        return [e for e in self.units if e.alive and e.team != u.team]

    def _targetable_enemies(self, u: CombatUnit) -> list[CombatUnit]:
        return [e for e in self.living_enemies(u) if e.untargetable_timer <= 0]

    def target_of(self, u: CombatUnit) -> CombatUnit | None:
        # persistance : garde la cible tant qu'elle est vivante ET ciblable (comme le vrai TFT)
        if (u.target is not None and u.target.alive and u.target.team != u.team
                and u.target.untargetable_timer <= 0):
            return u.target
        enemies = self._targetable_enemies(u)
        if not enemies:
            u.target = None
            return None
        if "reaper" in u.role.lower():  # assassin -> focus le carry (plus bas frontline_score),
            lo = min(_frontline_score(e) for e in enemies)  # independant de la position (symetrique)
            candidates = [e for e in enemies if _frontline_score(e) == lo]
        else:  # par defaut : ennemi le plus proche (-> les tanks devant sont focus)
            near_d = min(distance(u.pos, e.pos) for e in enemies)
            candidates = [e for e in enemies if distance(u.pos, e.pos) == near_d]
        u.target = candidates[int(self.rng.integers(len(candidates)))]  # tie-break aleatoire
        return u.target

    def enemies_in_radius(self, u: CombatUnit, r: int) -> list[CombatUnit]:
        return [e for e in self._targetable_enemies(u) if distance(u.pos, e.pos) <= r]

    def allies_of(self, u: CombatUnit) -> list[CombatUnit]:
        return [a for a in self.units if a.alive and a.team == u.team and a is not u]

    def lowest_hp_enemy(self, u: CombatUnit) -> CombatUnit | None:
        enemies = self.living_enemies(u)
        return min(enemies, key=lambda e: e.hp) if enemies else None

    def highest_hp_enemy(self, u: CombatUnit) -> CombatUnit | None:
        enemies = self.living_enemies(u)
        return max(enemies, key=lambda e: e.hp) if enemies else None

    @staticmethod
    def _mitig(defense: float) -> float:
        return 100.0 / (100.0 + max(0.0, defense))

    def _amp(self, src: CombatUnit, raw: float) -> float:
        """Applique l'amplification de degats + le crit de sort (si cast IE/JG)."""
        raw *= 1.0 + getattr(src, "damage_amp", 0.0)
        if self._casting is src and src.can_ability_crit and self.rng.random() < src.crit_chance:
            raw *= src.crit_mult
        return raw

    def _apply(self, src: CombatUnit, tgt: CombatUnit, dmg: float, raw: float) -> None:
        dmg *= 1.0 - min(0.9, tgt.incoming_reduction)  # durability (cumul multiplicatif en amont)
        if tgt.shield > 0:  # le bouclier absorbe en premier
            absorbed = min(tgt.shield, dmg)
            tgt.shield -= absorbed
            dmg -= absorbed
        tgt.hp -= dmg  # dmg = degats reellement portes aux PV
        # mana en subissant des degats : 1% pre-mit + 7% post-mit, plafonne, sauf si mana-lock
        if tgt.mana_lock_timer <= 0:
            gain = min(MANA_ON_HIT_CAP, MANA_ON_HIT_PREMIT * raw + MANA_ON_HIT_POSTMIT * dmg)
            tgt.mana = min(tgt.max_mana, tgt.mana + gain)
        # omnivamp : l'attaquant se soigne d'un % des degats portes
        if src is not None and src.omnivamp > 0 and dmg > 0:
            self.heal(src, src.omnivamp * dmg)
        # proc « quand subit des degats » (ex. Bramble Vest reflect) — garde anti-recursion
        if src is not None and not self._in_on_damaged:
            self._in_on_damaged = True
            try:
                for api in tgt.item_apis:
                    hook = ITEM_ON_DAMAGED.get(api)
                    if hook:
                        hook(tgt, src, self)
            finally:
                self._in_on_damaged = False
        # proc de seuil de PV (ex. bouclier sous 60%), une seule fois
        if ITEM_HP_THRESHOLD and tgt.hp > 0:
            for api in tgt.item_apis:
                thr = ITEM_HP_THRESHOLD.get(api)
                if thr and api not in tgt.triggered and tgt.hp > 0 and tgt.hp / tgt.max_hp < thr[0]:
                    tgt.triggered.add(api)
                    thr[1](tgt, self)
        if tgt.hp <= 0:
            # revive (ex. Guardian Angel) : une seule fois, sinon mort
            for api in tgt.item_apis:
                rev = ITEM_REVIVE.get(api)
                if rev and ("revive:" + api) not in tgt.triggered:
                    tgt.triggered.add("revive:" + api)
                    rev(tgt, self)
                    break
            if tgt.hp <= 0:
                tgt.alive = False

    def deal_physical(self, src: CombatUnit, tgt: CombatUnit, raw: float) -> None:
        raw = self._amp(src, raw)
        eff_armor = tgt.armor * (1.0 - tgt.sunder)  # sunder = reduction d'armure (max actif)
        self._apply(src, tgt, raw * self._mitig(eff_armor), raw)

    def deal_magic(self, src: CombatUnit, tgt: CombatUnit, raw: float) -> None:
        raw = self._amp(src, raw)
        eff_mr = tgt.mr * (1.0 - tgt.shred)  # shred = reduction de RM (max actif)
        self._apply(src, tgt, raw * self._mitig(eff_mr), raw)

    def deal_true(self, src: CombatUnit, tgt: CombatUnit, raw: float) -> None:
        raw = self._amp(src, raw)
        self._apply(src, tgt, raw, raw)  # degats bruts (ignore armure/RM)

    def shield_unit(self, unit: CombatUnit, amount: float,
                    duration: float = SHIELD_DEFAULT_DURATION) -> None:
        unit.shield += amount  # les boucliers s'empilent
        unit.shield_expire = max(unit.shield_expire, self.time + duration)

    def heal(self, unit: CombatUnit, amount: float) -> None:
        if unit.alive:
            amount *= 1.0 - unit.healing_reduction  # Grievous Wounds
            unit.hp = min(unit.max_hp, unit.hp + amount)

    def stun(self, target: CombatUnit, duration: float) -> None:
        target.stun_timer = max(target.stun_timer, duration)

    def silence(self, target: CombatUnit, duration: float) -> None:
        target.silence_timer = max(target.silence_timer, duration)

    def disarm(self, target: CombatUnit, duration: float) -> None:
        target.disarm_timer = max(target.disarm_timer, duration)

    def make_untargetable(self, unit: CombatUnit, duration: float) -> None:
        unit.untargetable_timer = max(unit.untargetable_timer, duration)

    def add_durability(self, unit: CombatUnit, frac: float) -> None:
        # durability cumule MULTIPLICATIVEMENT : 1 - (1-a)(1-b)
        unit.incoming_reduction = 1.0 - (1.0 - unit.incoming_reduction) * (1.0 - frac)

    def apply_grievous(self, target: CombatUnit, frac: float) -> None:
        target.healing_reduction = max(target.healing_reduction, frac)  # max actif

    def sunder_armor(self, target: CombatUnit, frac: float) -> None:
        target.sunder = max(target.sunder, frac)  # max actif

    def shred_mr(self, target: CombatUnit, frac: float) -> None:
        target.shred = max(target.shred, frac)  # max actif

    def buff_attack_speed(self, unit: CombatUnit, frac: float) -> None:
        unit.attack_speed *= 1.0 + frac

    def buff_ad(self, unit: CombatUnit, frac: float) -> None:
        unit.ad *= 1.0 + frac


_COLS_CENTER = sorted(range(GRID_COLS), key=lambda c: abs(c - GRID_COLS // 2))  # centre -> bords
_COLS_CORNER = sorted(range(GRID_COLS), key=lambda c: -abs(c - GRID_COLS // 2))  # bords -> centre


def _lay(n: int, rows: list[int], cols: list[int]) -> list[tuple[int, int]]:
    """n hexes répartis sur `rows` (remplit une rangée selon `cols` avant de reculer)."""
    out, ri, ci = [], 0, 0
    for _ in range(n):
        out.append((rows[ri], cols[ci]))
        ci += 1
        if ci >= len(cols):
            ci, ri = 0, min(ri + 1, len(rows) - 1)
    return out


def _frontline_score(u: CombatUnit) -> float:
    """Priorite de placement (haut = plus devant), basee sur le ROLE (placement TFT habituel).

    Tanks devant pour absorber (les ennemis ciblent le plus proche), puis bruisers, puis assassins,
    puis casters, et les carrys (fragiles, longue portee) tout au fond.
    """
    r = u.role.lower()
    if "tank" in r:
        base = 100.0
    elif "fighter" in r:
        base = 70.0
    elif "reaper" in r:  # assassins : ni tank ni backline pure, plutot milieu
        base = 40.0
    elif "caster" in r:
        base = 20.0
    elif "carry" in r or "specialist" in r:
        base = 0.0
    else:
        base = 50.0  # role inconnu -> milieu
    base += (6 - u.attack_range) * 0.5  # melee -> un peu plus devant
    base += (u.max_hp + (u.armor + u.mr) * 10) / 2000.0  # tanky -> un peu plus devant
    return base


def _nearest_free_hex(target_pos: tuple[int, int], occupied: set) -> tuple[int, int] | None:
    best, best_d = None, 1 << 30
    for r in range(GRID_ROWS):
        for c in range(GRID_COLS):
            if (r, c) in occupied:
                continue
            d = distance((r, c), target_pos)
            if d < best_d:
                best, best_d = (r, c), d
    return best


def _assassin_dash(team: list[CombatUnit], ctx: "CombatContext") -> None:
    """Vrai dash d'assassin : au debut du combat, les Reapers se teleportent sur la backline
    ennemie (hex adjacent au carry vise) et verrouillent cette cible."""
    occupied = {u.pos for u in ctx.units if u.alive}
    for u in team:
        if "reaper" not in u.role.lower():
            continue
        target = ctx.target_of(u)  # ennemi le plus loin (= carry backline) pour les reapers
        if target is None:
            continue
        # choix du hex 180°-symetrique : voisin du carry le plus proche de SON propre camp
        # (team0 -> rangee la plus basse ; team1 -> la plus haute). Garde le miroir equitable.
        sign = 1 if u.team == 0 else -1
        free_nb = [nb for nb in neighbors(target.pos) if nb not in occupied]
        if free_nb:
            spot = min(free_nb, key=lambda nb: (sign * nb[0], abs(nb[1] - GRID_COLS // 2)))
        else:
            spot = _nearest_free_hex(target.pos, occupied)
        if spot is not None and spot != u.pos:
            occupied.discard(u.pos)
            occupied.add(spot)
            u.pos = spot
        u.target = target  # verrouille le carry


def _build_team(board: list[BoardUnit], team: int, content: SetContent) -> list[CombatUnit]:
    units: list[CombatUnit] = []
    for bu in board:
        champ = content.champions.get(bu.champion_api)
        if champ is None:
            continue
        units.append(build_unit(
            champ, bu.star, team, content,
            item_apis=tuple(getattr(bu, "item_apis", ()) or ()),
            generic_items=getattr(bu, "items", 0),
        ))
    apply_team_traits(units, content)
    # placement rôle-aware : moitie avant (tanks/bruisers) en rangees front, moitie arriere
    # (carrys/supports) en rangees back -> les ennemis (ciblage du + proche) focus les tanks.
    ordered = sorted(units, key=lambda u: -_frontline_score(u))
    half = (len(ordered) + 1) // 2
    # front : tanks au centre des rangees avant ; back : carrys dans les COINS (bords) des rangees arriere
    pos = _lay(half, [3, 2], _COLS_CENTER) + _lay(len(ordered) - half, [0, 1], _COLS_CORNER)
    for unit, p in zip(ordered, pos):
        # team1 = rotation 180deg exacte -> matchup miroir equitable
        unit.pos = p if team == 0 else (GRID_ROWS - 1 - p[0], GRID_COLS - 1 - p[1])
    return units


def _apply_combat_start(team: list[CombatUnit], enemies: list[CombatUnit],
                        augments: tuple[str, ...], content: SetContent, ctx) -> None:
    # procs d'items au debut de combat (auras, boucliers, regen)
    for u in team:
        for api in u.item_apis:
            hook = ITEM_COMBAT_START.get(api)
            if hook:
                hook(u, ctx)
    # effets d'augments de combat (variables reelles depuis la data)
    for aug_api in augments:
        fn = AUGMENT_REGISTRY.get(aug_api)
        if fn:
            aug = content.augments.get(aug_api)
            fn(team, enemies, ctx, aug.effects if aug else {})


def run_combat(
    board_a: list[BoardUnit], board_b: list[BoardUnit], content: SetContent,
    rng: np.random.Generator | None = None,
    augments_a: tuple[str, ...] = (), augments_b: tuple[str, ...] = (),
) -> CombatResult:
    rng = rng or np.random.default_rng()
    team0 = _build_team(board_a, 0, content)
    team1 = _build_team(board_b, 1, content)
    if not team0 and not team1:
        return CombatResult(winner=0, survivors=0)
    if not team0:
        return CombatResult(winner=1, survivors=len(team1))
    if not team1:
        return CombatResult(winner=0, survivors=len(team0))

    units = team0 + team1
    ctx = CombatContext(units, rng)
    _apply_combat_start(team0, team1, augments_a, content, ctx)
    _apply_combat_start(team1, team0, augments_b, content, ctx)
    _assassin_dash(team0, ctx)  # les assassins plongent sur la backline adverse au start
    _assassin_dash(team1, ctx)

    _CC = ("mana_lock_timer", "silence_timer", "disarm_timer", "untargetable_timer")
    ticks_per_second = max(1, int(round(1.0 / TICK_DT)))
    for tick in range(MAX_COMBAT_TICKS):
        ctx.time = tick * TICK_DT
        alive0 = [u for u in team0 if u.alive]
        alive1 = [u for u in team1 if u.alive]
        if not alive0 or not alive1:
            break
        for u in units:  # expiration des boucliers a duree
            if u.alive and u.shield > 0 and ctx.time >= u.shield_expire:
                u.shield = 0.0
        if tick % ticks_per_second == 0 and tick > 0:  # ~1/s : mana regen + procs periodiques
            for u in units:
                if not u.alive:
                    continue
                if u.mana_regen and u.mana_lock_timer <= 0:
                    u.mana = min(u.max_mana, u.mana + u.mana_regen)
                for api in u.item_apis:
                    hook = ITEM_ON_TICK.get(api)
                    if hook:
                        hook(u, ctx)
        occupied = {u.pos for u in units if u.alive}
        # ordre d'action randomise chaque tick : evite le biais « equipe 0 agit en premier ».
        for idx in rng.permutation(len(units)):
            u = units[idx]
            if not u.alive:
                continue
            u.attack_cd = max(0.0, u.attack_cd - TICK_DT)
            u.move_cd = max(0.0, u.move_cd - TICK_DT)
            for t in _CC:  # decrement des timers de CC / mana-lock
                setattr(u, t, max(0.0, getattr(u, t) - TICK_DT))
            if u.stun_timer > 0:  # etourdi : ne peut pas agir
                u.stun_timer = max(0.0, u.stun_timer - TICK_DT)
                continue
            # cast des que mana plein (sauf silence) ; le cast verrouille le mana ~1s
            if u.max_mana < 1e8 and u.mana >= u.max_mana and u.silence_timer <= 0:
                allies = team0 if u.team == 0 else team1
                ctx._casting = u  # le sort peut critter si IE/JG
                get_ability(u.champion_api)(u, [a for a in allies if a.alive and a is not u], ctx.living_enemies(u), ctx)
                ctx._casting = None
                _item_on_cast(u, ctx)
                u.mana = 0.0
                u.mana_lock_timer = MANA_LOCK_DURATION
                continue
            target = ctx.target_of(u)
            if target is None:
                continue
            if distance(u.pos, target.pos) <= u.attack_range:
                if u.attack_cd <= 0 and u.disarm_timer <= 0:  # desarme = ne peut pas attaquer
                    raw = u.ad
                    if rng.random() < u.crit_chance:
                        raw *= u.crit_mult
                    ctx.deal_physical(u, target, raw)
                    _item_on_attack(u, target, ctx)
                    u.attack_cd = 1.0 / min(ATTACK_SPEED_CAP, max(0.1, u.attack_speed))
                    if u.mana_lock_timer <= 0:
                        u.mana = min(u.max_mana, u.mana + MANA_PER_ATTACK)
            elif u.move_cd <= 0:
                nxt = step_toward(u.pos, target.pos, occupied)
                if nxt is not None:
                    occupied.discard(u.pos)
                    occupied.add(nxt)
                    u.pos = nxt
                    u.move_cd = MOVE_INTERVAL

    s0 = [u for u in team0 if u.alive]
    s1 = [u for u in team1 if u.alive]
    if len(s0) != len(s1):
        winner = 0 if len(s0) > len(s1) else 1
    else:
        hp0, hp1 = sum(u.hp for u in s0), sum(u.hp for u in s1)
        if hp0 == hp1:  # vraie egalite (ex. double-wipe) -> aleatoire, pas de biais equipe 0
            winner = int(rng.integers(2))
        else:  # egalite de survivants -> plus de PV total restant
            winner = 0 if hp0 > hp1 else 1
    # Vraie formule TFT : 1 degat par unite survivante (PLAT, pas pondere etoile) -> survivors.
    survivors = len(s0) if winner == 0 else len(s1)
    return CombatResult(winner=winner, survivors=survivors)
