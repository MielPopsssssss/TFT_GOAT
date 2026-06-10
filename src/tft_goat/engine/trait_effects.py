"""Application des bonus de STATS des traits actifs (vraies variables data Set 17).

Gère le vocabulaire réel des clés (BonusArmor, BonusMR, Mountain_AS, Wolf_ADAP, Serpent_DR,
TeamwideResists, ...), distingue les effets **team-wide** (suffixe/préfixe Teamwide) des effets
réservés aux porteurs du trait, et **cumule** (chaque trait/tier s'ajoute ; durability multiplicatif).

Les effets NON-stat (invocations, exécutions, dégâts, durées, économie) et les clés obfusquées
({hex}) sont ignorés ici (long tail). Heuristique %/flat : valeur > 1 traitée comme pourcentage.
"""

from __future__ import annotations

import re

from ..data.models import SetContent
from ..env.traits import active_traits
from .unit import CombatUnit

# tokens de clés a IGNORER (non applicables comme stat plate sur l'unite).
# NB : « heal » n'est PAS dans cette liste — il est testé via _HEAL_NOT_HEALTH ci-dessous,
# car en substring brut il matchait aussi « health » et tuait la branche health->hp
# (aucun bonus HP de trait n'était appliqué — bug corrigé 2026-06-10).
_SKIP = (
    "round", "gold", "nummark", "duration", "threshold", "poison", "sharepercent",
    "interval", "numdeaths", "increaseper", "statincrease", "percenthealth", "executehp",
    "burst", "supermassive", "cashout", "stacks", "count", "mana", "omnivamp",
    # Clés *health* qui ne sont PAS des buffs de HP max (politique : jamais deviner) :
    "pvehp",          # flag PvE (Fiora unique) — PVEHP=1.0 doublerait ses HP en fraction
    "healthratio",    # ratio d'ability (Commander/Sona), pas un buff direct vérifié
    "shield_health",  # paramètre de bouclier Stargazer (8.0 = ni fraction ni flat sensé)
)

# « heal » non suivi de « th » : matche Heal/HealAmount/Huntress_Heal (soins, à skipper)
# mais PAS Health/HealthBonus (vraies stats HP).
_HEAL_NOT_HEALTH = re.compile(r"heal(?!th)")


def _pct(v: float) -> float:
    return v / 100.0 if abs(v) > 1.0 else v


def attrs_for(key: str) -> list[str]:
    """Liste des attributs de stat vises par une cle de trait (vide si non-stat).

    API publique : utilisee aussi par les fiches d'audit (fiches/status.py) pour afficher
    quelles variables de trait sont auto-appliquees par le moteur.
    """
    if key.startswith("{"):
        return []
    k = key.lower()
    if any(tok in k for tok in _SKIP) or _HEAL_NOT_HEALTH.search(k):
        return []
    attrs: list[str] = []
    if "adap" in k:
        attrs += ["ad", "ap"]
    else:
        if "ad" in k:
            attrs.append("ad")
        if "ap" in k:
            attrs.append("ap")
    if "resist" in k:
        attrs += ["armor", "mr"]
    if "armor" in k:
        attrs.append("armor")
    if "mr" in k or "magicresist" in k:
        attrs.append("mr")
    if "health" in k or k.endswith("hp") or "_hp" in k:
        attrs.append("hp")
    if "attackspeed" in k or k == "as" or "_as" in k or k.endswith("as"):
        attrs.append("as")
    if k.endswith("dr") or "_dr" in k or "damagereduction" in k or "durability" in k:
        attrs.append("dr")
    if k.endswith("da") or "_da" in k or "damageamp" in k:
        attrs.append("amp")
    return list(dict.fromkeys(attrs))


def _apply_stat(u: CombatUnit, attr: str, v: float) -> None:
    if attr == "hp":
        # Heuristique fraction/flat du module : |v| <= 1 = fraction de HP max (ex. Brawler
        # HealthBonus 0.25/0.45/0.65), sinon bonus plat (ex. Meeple BonusHealth 100..500).
        # Plusieurs fractions se COMPOSENT multiplicativement (max_hp*(1+a)*(1+b)) — commutatif,
        # donc indépendant de l'ordre d'application des traits.
        bonus = u.max_hp * v if abs(v) <= 1.0 else v
        u.max_hp += bonus
        u.hp += bonus
    elif attr == "armor":
        u.armor += v
    elif attr == "mr":
        u.mr += v
    elif attr == "ap":
        u.ap += v  # AP : ajout plat
    elif attr == "ad":
        u.ad *= 1.0 + _pct(v)
    elif attr == "as":
        u.attack_speed *= 1.0 + _pct(v)
    elif attr == "dr":
        u.incoming_reduction = 1.0 - (1.0 - u.incoming_reduction) * (1.0 - _pct(v))  # multiplicatif
    elif attr == "amp":
        u.damage_amp += _pct(v)  # additif


def apply_team_traits(
    units: list[CombatUnit], content: SetContent, *, bonus_units: int = 0
) -> None:
    """Calcule les traits actifs de l'equipe et applique leurs bonus de stats (cumul).

    `bonus_units` : champions virtuels ajoutes aux traits non-uniques presents
    (God Boon LargeQuest) — voir `env/traits.py::active_traits`.
    """
    if not units:
        return
    active = active_traits([u.champion_api for u in units], content, bonus_units=bonus_units)
    if not active:
        return
    by_name = {t.name: t for t in content.traits.values()}
    for trait_name, tier in active.items():
        trait = by_name.get(trait_name)
        if trait is None or not trait.effects:
            continue
        effs = sorted(trait.effects, key=lambda e: e.min_units)
        eff = effs[min(tier - 1, len(effs) - 1)]
        members = [
            u for u in units
            if (c := content.champions.get(u.champion_api)) and trait_name in c.traits
        ]
        for key, val in eff.variables.items():
            if not isinstance(val, (int, float)) or val == 0:
                continue
            targets = units if "teamwide" in key.lower() else members  # team-wide vs porteurs
            for attr in attrs_for(key):
                for u in targets:
                    _apply_stat(u, attr, float(val))
