"""Contenu de set synthetique, petit et deterministe.

Utilise pour les tests et l'entrainement rapide (sans dependre du snapshot CDragon ~24 MB).
"""

from __future__ import annotations

from .models import Augment, Champion, Item, SetContent, Trait, TraitEffect


def _trait(api: str, name: str, breakpoints: tuple[int, ...]) -> Trait:
    effects = tuple(
        TraitEffect(min_units=bp, max_units=bp + 1, style=i + 1)
        for i, bp in enumerate(breakpoints)
    )
    return Trait(api_name=api, name=name, effects=effects)


def _champ(api: str, cost: int, traits: tuple[str, ...]) -> Champion:
    return Champion(api_name=api, name=api, cost=cost, traits=traits)


def build_sample_content() -> SetContent:
    traits = {
        "T_Brawler": _trait("T_Brawler", "Brawler", (2, 4, 6)),
        "T_Mage": _trait("T_Mage", "Mage", (3, 5)),
    }
    champions = {
        "c1": _champ("c1", 1, ("Brawler",)),
        "c2": _champ("c2", 1, ("Brawler", "Mage")),
        "c3": _champ("c3", 2, ("Mage",)),
        "c4": _champ("c4", 2, ("Brawler",)),
        "c5": _champ("c5", 3, ("Brawler",)),
        "c6": _champ("c6", 3, ("Mage",)),
        "c7": _champ("c7", 4, ("Brawler", "Mage")),
        "c8": _champ("c8", 5, ("Mage",)),
    }
    # 2 composants de base + 1 objet complet (recette) pour tester le système d'items
    items = {
        "cmp_bf": Item(api_name="cmp_bf", name="BF", composition=()),
        "cmp_bow": Item(api_name="cmp_bow", name="Bow", composition=()),
        "it_combined": Item(api_name="it_combined", name="Combined",
                            composition=("cmp_bf", "cmp_bow"), effects={"AD": 0.5}),
    }
    # quelques augments avec tiers varies + 1 God Augment (doit etre exclu du pool regulier)
    augments = {
        f"aug_s{i}": Augment(api_name=f"aug_s{i}", name=f"Silver{i}", tier="silver")
        for i in range(4)
    }
    augments.update(
        {f"aug_g{i}": Augment(api_name=f"aug_g{i}", name=f"Gold{i}", tier="gold") for i in range(4)}
    )
    augments.update(
        {f"aug_p{i}": Augment(api_name=f"aug_p{i}", name=f"Prism{i}", tier="prismatic")
         for i in range(4)}
    )
    augments["GodAugment_test"] = Augment(api_name="GodAugment_test", name="God", tier="god")
    return SetContent(
        patch="test", set_number=0,
        champions=champions, traits=traits, items=items, augments=augments,
    )
