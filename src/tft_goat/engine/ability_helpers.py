"""Helpers partages pour les sorts (importables par les batches sans import circulaire)."""

from __future__ import annotations

from .unit import CombatUnit


def default_damage(caster: CombatUnit) -> float:
    """Degats par defaut = 1re variable 'damage' de la data, scalee par AP."""
    for name in caster.variables:
        if "damage" in name.lower():
            return caster.ability_value(name) * (caster.ap / 100.0)
    return caster.ad * 2.0
