"""Registre des sorts : sorts Set 17 (abilities_set17/) + defaut data-driven.

Chaque sort = fn(caster, allies, enemies, ctx). `ctx` (CombatContext) expose :
  ctx.target_of(caster) -> CombatUnit | None
  ctx.living_enemies(caster) / ctx.allies_of(caster) -> list
  ctx.enemies_in_radius(caster, r) -> list ; ctx.lowest_hp_enemy / highest_hp_enemy(caster)
  ctx.deal_magic / deal_physical / deal_true(caster, target, amount)
  ctx.shield_unit(unit, amount) ; ctx.heal(unit, amount) ; ctx.stun(target, duration)
  ctx.buff_attack_speed(unit, frac) ; ctx.buff_ad(unit, frac)
  caster.ability_value(name, default) -> valeur de variable data au niveau d'etoile courant
Couverture suivie dans docs/COMBAT_COVERAGE.md.
"""

from __future__ import annotations

from .ability_helpers import default_damage
from .abilities_set17 import SET17_ABILITIES


def default_ability(caster, allies, enemies, ctx) -> None:
    """Nuke mono-cible (magique) — defaut pour les sorts non encore implementes."""
    target = ctx.target_of(caster)
    if target is not None:
        ctx.deal_magic(caster, target, default_damage(caster))


def get_ability(api: str):
    return SET17_ABILITIES.get(api, default_ability)


IMPLEMENTED = set(SET17_ABILITIES)
