"""Génération de l'arbre docs/fiches/ : toutes les fiches + l'INDEX qui les lie."""

from __future__ import annotations

from pathlib import Path

from ..data.models import SetContent
from .render import render_augment, render_champion, render_item, render_trait
from .status import ability_implemented, augment_in_engine

_GROUPS = ("champions", "traits", "items", "augments")


def generate_all(content: SetContent, out_dir: Path | str) -> dict[str, dict[str, Path]]:
    """Écrit toutes les fiches sous `out_dir` et l'INDEX.md. Déterministe.

    Retourne {groupe: {apiName: Path}} pour chaque fiche écrite.
    """
    out = Path(out_dir)
    renderers = {
        "champions": (content.champions, render_champion),
        "traits": (content.traits, render_trait),
        "items": (content.items, render_item),
        "augments": (content.augments, render_augment),
    }
    paths: dict[str, dict[str, Path]] = {g: {} for g in _GROUPS}
    for group in _GROUPS:
        entities, renderer = renderers[group]
        (out / group).mkdir(parents=True, exist_ok=True)
        for api, entity in sorted(entities.items()):
            p = out / group / f"{api}.md"
            p.write_text(renderer(entity, content), encoding="utf-8")
            paths[group][api] = p
    (out / "INDEX.md").write_text(_render_index(content), encoding="utf-8")
    return paths


def _champ_line(api: str, content: SetContent) -> str:
    c = content.champions[api]
    status = "✅" if ability_implemented(api) else "🟡"
    return f"- [{c.name}](champions/{api}.md) {status}\n"


def _render_index(content: SetContent) -> str:
    champs = content.champions
    playable = [
        api for api, c in sorted(champs.items())
        if api.startswith(f"TFT{content.set_number}_") and 1 <= c.cost <= 5
    ]
    others = [api for api in sorted(champs) if api not in set(playable)]
    abilities_ok = sum(1 for api in playable if ability_implemented(api))
    aug_engine = sum(1 for api in sorted(content.augments) if augment_in_engine(api))
    god_augs = [api for api, a in sorted(content.augments.items()) if a.tier == "god"]

    md = (
        f"# Fiches d'audit — TFT Set {content.set_number} (patch {content.patch})\n\n"
        "> Index GÉNÉRÉ — **NE PAS ÉDITER À LA MAIN**. "
        "Régénérer : `.venv/bin/python -m scripts.generate_fiches`\n>\n"
        "> Légende : ✅ = implémenté dans le moteur réel · 🟡 = défaut générique / no-op / stats-only.\n"
        "> Chaque fiche est la vue auditable d'UNE entité : data CDragon + statut moteur.\n\n"
        "## Vue d'ensemble\n\n"
        f"- **Champions** : {len(champs)} fiches ({len(playable)} jouables — sorts moteur : "
        f"{abilities_ok} ✅ / {len(playable) - abilities_ok} 🟡)\n"
        f"- **Traits** : {len(content.traits)} fiches\n"
        f"- **Items** : {len(content.items)} fiches\n"
        f"- **Augments** : {len(content.augments)} fiches (effet combat moteur : {aug_engine} ✅) "
        f"— dont {len(god_augs)} God Boons\n\n"
    )

    md += "## Champions jouables (par coût)\n\n"
    for cost in (1, 2, 3, 4, 5):
        of_cost = [api for api in playable if champs[api].cost == cost]
        if not of_cost:
            continue
        md += f"### {cost} coût\n\n"
        for api in of_cost:
            md += _champ_line(api, content)
        md += "\n"
    if others:
        md += "## Autres unités (PvE / evergreen / spéciales)\n\n"
        for api in others:
            md += _champ_line(api, content)
        md += "\n"

    md += "## Traits\n\n"
    for api, t in sorted(content.traits.items()):
        bps = "/".join(str(b) for b in t.breakpoints) or "—"
        md += f"- [{t.name}](traits/{api}.md) ({bps})\n"
    md += "\n"

    components = [api for api, i in sorted(content.items.items()) if not i.composition]
    completed = [api for api, i in sorted(content.items.items()) if len(i.composition) == 2]
    other_items = [
        api for api in sorted(content.items)
        if api not in set(components) and api not in set(completed)
    ]
    md += "## Items\n\n### Composants / sans recette\n\n"
    for api in components:
        md += f"- [{content.items[api].name}](items/{api}.md)\n"
    md += "\n### Objets complets (recette 2 composants)\n\n"
    for api in completed:
        md += f"- [{content.items[api].name}](items/{api}.md)\n"
    if other_items:
        md += "\n### Autres\n\n"
        for api in other_items:
            md += f"- [{content.items[api].name}](items/{api}.md)\n"
    md += "\n"

    md += "## Augments\n\n"
    for tier in ("god", "prismatic", "gold", "silver"):
        of_tier = [api for api, a in sorted(content.augments.items()) if a.tier == tier]
        if not of_tier:
            continue
        md += f"### {tier} ({len(of_tier)})\n\n"
        for api in of_tier:
            status = "✅" if augment_in_engine(api) else "🟡"
            md += f"- [{content.augments[api].name}](augments/{api}.md) {status}\n"
        md += "\n"
    other_tiers = [
        api for api, a in sorted(content.augments.items())
        if a.tier not in ("god", "prismatic", "gold", "silver")
    ]
    if other_tiers:
        md += f"### autres tiers ({len(other_tiers)})\n\n"
        for api in other_tiers:
            status = "✅" if augment_in_engine(api) else "🟡"
            md += f"- [{content.augments[api].name}](augments/{api}.md) {status}\n"
        md += "\n"
    return md
