"""Rendu markdown d'une fiche (champion / trait / item / augment).

Tout est déterministe : mêmes données -> mêmes octets (les fiches vivent dans git,
un diff propre = un vrai changement de data ou de moteur).
"""

from __future__ import annotations

import re

from ..data.models import Augment, Champion, Item, SetContent, Trait
from ..engine.config import STAR_SCALE
from .status import (
    ability_implemented,
    augment_in_engine,
    god_of_augment,
    item_proc_hooks,
    trait_var_attrs,
)

_HTML_TAG = re.compile(r"<[^>]+>")
_ICON_TOKEN = re.compile(r"%i:[^%]+%")  # icônes inline CDragon (ex. %i:scaleAP%)


def fmt(x: float) -> str:
    """Format compact d'une valeur de jeu : 700.0 -> '700', 0.6000000238 -> '0.6'."""
    return format(x, "g")


def _strip_html(text: str) -> str:
    """Nettoie une desc CDragon : tags HTML, icônes %i:...%, espaces insécables.

    Les placeholders `@Variable@` sont CONSERVÉS : ils référencent les variables data
    listées dans la fiche (auditables ligne à ligne).
    """
    text = _HTML_TAG.sub("", text)
    text = _ICON_TOKEN.sub("", text)
    text = text.replace("&nbsp;", " ")
    text = re.sub(r"\s*\(\s*\)", "", text)  # parenthèses vidées par le retrait des icônes
    return text.strip()


def _header(title: str, kind: str, content: SetContent) -> str:
    return (
        f"# {title} — fiche {kind}\n\n"
        f"> Fiche GÉNÉRÉE depuis CommunityDragon patch {content.patch} — "
        f"**NE PAS ÉDITER À LA MAIN**.\n"
        f"> Régénérer : `.venv/bin/python -m scripts.generate_fiches`\n\n"
    )


def _trait_links(champ: Champion, content: SetContent) -> str:
    """Champion.traits contient des NOMS d'affichage -> liens vers les fiches (apiName)."""
    by_name = {t.name: api for api, t in content.traits.items()}
    parts = []
    for name in champ.traits:
        api = by_name.get(name)
        parts.append(f"[{name}](../traits/{api}.md)" if api else name)
    return ", ".join(parts) if parts else "—"


def _is_playable(champ: Champion, content: SetContent) -> bool:
    return champ.api_name.startswith(f"TFT{content.set_number}_") and 1 <= champ.cost <= 5


def render_champion(champ: Champion, content: SetContent) -> str:
    md = _header(champ.name, "champion", content)
    md += f"- **apiName** : `{champ.api_name}`\n"
    md += f"- **Coût** : {champ.cost}\n"
    md += f"- **Traits** : {_trait_links(champ, content)}\n"
    md += f"- **Rôle** : {champ.role or '—'}\n"
    md += f"- **Jouable (pool boutique)** : {'oui' if _is_playable(champ, content) else 'non (PvE/evergreen/spécial)'}\n\n"

    s = champ.stats
    if s is not None:
        md += "## Stats\n\n"
        md += "| Stat | 1★ | 2★ | 3★ |\n|---|---|---|---|\n"
        md += f"| HP | {fmt(s.hp)} | {fmt(s.hp * STAR_SCALE[2])} | {fmt(s.hp * STAR_SCALE[3])} |\n"
        md += (
            f"| Dégâts d'attaque | {fmt(s.damage)} | {fmt(s.damage * STAR_SCALE[2])} "
            f"| {fmt(s.damage * STAR_SCALE[3])} |\n"
        )
        md += f"| Vitesse d'attaque | {fmt(s.attack_speed)} | = | = |\n"
        md += f"| Armure | {fmt(s.armor)} | = | = |\n"
        md += f"| Résistance magique | {fmt(s.magic_resist)} | = | = |\n"
        md += f"| Mana (initial/max) | {fmt(s.initial_mana)} / {fmt(s.mana)} | = | = |\n"
        md += f"| Portée | {fmt(s.attack_range)} | = | = |\n"
        md += f"| Crit (chance × multi) | {fmt(s.crit_chance)} × {fmt(s.crit_multiplier)} | = | = |\n\n"

    a = champ.ability
    if a is not None:
        md += f"## Sort — {a.name}\n\n"
        if ability_implemented(champ.api_name):
            md += "**Statut moteur** : ✅ implémenté (`engine/abilities_set17`)\n\n"
        else:
            md += "**Statut moteur** : 🟡 défaut générique (nuke magique mono-cible)\n\n"
        if a.desc:
            md += f"{_strip_html(a.desc)}\n\n"
        if a.variables:
            md += "### Variables (valeurs data par niveau)\n\n| Variable | Valeurs |\n|---|---|\n"
            for key in sorted(a.variables):
                vals = " / ".join(fmt(v) for v in a.variables[key])
                md += f"| `{key}` | {vals} |\n"
            md += "\n"
    return md


def render_trait(trait: Trait, content: SetContent) -> str:
    md = _header(trait.name, "trait", content)
    md += f"- **apiName** : `{trait.api_name}`\n"
    bps = " / ".join(str(b) for b in trait.breakpoints) or "—"
    md += f"- **Paliers d'activation** : {bps}\n\n"

    if trait.effects:
        md += "## Paliers\n\n| Min unités | Max | Style | Variables |\n|---|---|---|---|\n"
        for e in sorted(trait.effects, key=lambda e: e.min_units):
            var_list = ", ".join(f"`{k}`={fmt(v)}" for k, v in sorted(e.variables.items())) or "—"
            md += f"| {e.min_units} | {e.max_units} | {e.style} | {var_list} |\n"
        md += "\n"

    # Statut moteur : quelles variables sont auto-appliquées en stats par apply_team_traits ?
    keys = sorted({k for e in trait.effects for k in e.variables})
    md += "## Statut moteur\n\n"
    if not keys:
        md += "Aucune variable de palier (trait sans effet numérique en data).\n\n"
    else:
        md += "| Variable | Application moteur |\n|---|---|\n"
        for k in keys:
            attrs = trait_var_attrs(k)
            if attrs:
                md += f"| `{k}` | ✅ stat auto-appliquée ({', '.join(attrs)}) |\n"
            else:
                md += f"| `{k}` | 🟡 non-stat — effet appliqué uniquement si codé (long-tail) |\n"
        md += "\n"

    holders = [
        (c.name, api) for api, c in sorted(content.champions.items())
        if trait.name in c.traits
    ]
    if holders:
        md += "## Champions avec ce trait\n\n"
        for name, api in holders:
            md += f"- [{name}](../champions/{api}.md)\n"
        md += "\n"
    return md


def render_item(item: Item, content: SetContent) -> str:
    md = _header(item.name, "item", content)
    md += f"- **apiName** : `{item.api_name}`\n"
    if len(item.composition) == 2:
        comps = " + ".join(
            f"[{content.items[c].name}](../items/{c}.md)" if c in content.items else f"`{c}`"
            for c in item.composition
        )
        md += f"- **Recette** : {comps}\n"
    elif not item.composition:
        md += "- **Type** : composant de base (ou item sans recette)\n"
    else:
        md += f"- **Composition** : {', '.join(f'`{c}`' for c in item.composition)}\n"
    md += f"- **Unique** : {'oui' if item.unique else 'non'}\n"
    if item.tags:
        md += f"- **Tags** : {', '.join(item.tags)}\n"
    if item.associated_traits:
        md += f"- **Traits associés** : {', '.join(item.associated_traits)}\n"
    if item.incompatible_traits:
        md += f"- **Traits incompatibles** : {', '.join(item.incompatible_traits)}\n"
    md += "\n"

    if item.effects:
        md += "## Effets (stats data)\n\n| Effet | Valeur |\n|---|---|\n"
        for k, v in sorted(item.effects.items()):
            md += f"| `{k}` | {fmt(v)} |\n"
        md += "\n> Les effets numériques sont auto-appliqués par le moteur quand l'identité de l'item est connue.\n\n"

    hooks = item_proc_hooks(item.api_name)
    md += "## Proc spécial moteur\n\n"
    if hooks:
        md += f"✅ proc codé — hooks : {', '.join(f'`{h}`' for h in hooks)}\n"
    else:
        md += "🟡 stats uniquement — aucun proc spécial codé (cf. docs/COMBAT_COVERAGE.md)\n"
    return md


def render_augment(aug: Augment, content: SetContent) -> str:
    md = _header(aug.name, "augment", content)
    md += f"- **apiName** : `{aug.api_name}`\n"
    md += f"- **Tier** : {aug.tier}\n"
    god = god_of_augment(aug)
    if god is not None:
        md += f"- **God Boon** : boon du dieu **{god}** (Realm of the Gods, hors pool normal)\n"
    if aug.associated_traits:
        md += f"- **Traits associés** : {', '.join(aug.associated_traits)}\n"
    md += "\n"

    if aug.desc:
        md += f"{_strip_html(aug.desc)}\n\n"
    if aug.effects:
        md += "## Effets (data)\n\n| Effet | Valeur |\n|---|---|\n"
        for k, v in sorted(aug.effects.items()):
            md += f"| `{k}` | {fmt(v)} |\n"
        md += "\n"

    md += "## Statut combat moteur\n\n"
    if augment_in_engine(aug.api_name):
        md += "✅ effet combat codé (`engine/augments_set17`)\n"
    else:
        md += (
            "🟡 no-op en combat — soit augment éco/loot (no-op correct), soit effet combat "
            "non encore implémenté (cf. docs/COMBAT_COVERAGE.md, TODOS.md)\n"
        )
    return md
