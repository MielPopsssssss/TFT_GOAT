"""Realm of the Gods (Set 17) — les 9 dieux et leurs God Boons (data réelle CDragon).

Mécanique vérifiée vs patch 17.4 (eloboost24 + mobalytics + bunnymuffins) : 2 dieux tirés par
lobby au départ ; aux rounds 2-4 / 3-4 / 4-4 le joueur choisit un Minor Blessing de l'un des 2
dieux (= un vote) ; la majorité des 3 votes fixe le **dieu aligné**, qui octroie un **God Boon**
au 4-7. Les God Boons sont les 17 augments `*GodAugment*` de CDragon (tier="god", hors pool normal).

Ce module expose la data réelle (9 dieux + leurs boons) ; le flux vote/alignement vit dans
`env/rounds.py` + `env/actions.py`. Source statique = CommunityDragon (jamais inventé ici).
"""

from __future__ import annotations

from ..data.models import SetContent

# Les 9 dieux du Realm of the Gods. Le `token` est le fragment d'apiName CDragon
# (`TFT17_Augment_<token>GodAugment...`). Double-confirmé : table skill tft-knowledge ==
# les 17 GodAugments présents dans cdragon_17.4 (chaque dieu a >= 1 boon).
SET17_GODS: dict[str, str] = {
    "Soraka": "Soraka",
    "Yasuo": "Yasuo",
    "Ahri": "Ahri",
    "Thresh": "Thresh",
    "Kayle": "Kayle",
    "Varus": "Varus",
    "Evelynn": "Evelynn",
    "Ekko": "Ekko",
    "Aurelion Sol": "AurelionSol",
}

GOD_AUGMENT_TIER = "god"

# Cache mono-slot du mapping dieu -> boons : SetContent est immuable, le mapping ne change
# jamais pour un contenu donné. Évite de rescanner tous les augments à chaque alignement.
# UN SEUL slot (le dernier contenu vu) : borné par construction — un cache dict accumulait une
# entrée par TftEnv() créé (un par partie en self-play) et fuyait sans limite.
_BOONS_CACHE: tuple[SetContent, dict[str, list[str]]] | None = None


def god_boons(content: SetContent) -> dict[str, list[str]]:
    """Mappe chaque dieu -> liste des apiNames de ses God Boons (augments tier="god").

    Lit la vraie data : tout augment tier="god" dont l'apiName contient le token d'un dieu.
    Un apiName qui matche PLUSIEURS dieux est une donnée ambiguë -> erreur explicite (on ne
    devine jamais la data). Résultat mis en cache (mono-slot) — à traiter comme lecture seule.
    """
    global _BOONS_CACHE
    if _BOONS_CACHE is not None and _BOONS_CACHE[0] is content:
        return _BOONS_CACHE[1]
    boons: dict[str, list[str]] = {god: [] for god in SET17_GODS}
    for api, aug in content.augments.items():
        if aug.tier != GOD_AUGMENT_TIER:
            continue
        matched = [god for god, token in SET17_GODS.items() if token in api]
        if len(matched) > 1:
            raise ValueError(f"God augment ambigu : {api} matche plusieurs dieux {matched}")
        if matched:
            boons[matched[0]].append(api)
    _BOONS_CACHE = (content, boons)
    return boons


def choose_lobby_gods(rng) -> tuple[str, str]:
    """Tire les 2 dieux du lobby au départ de partie (mêmes pour tous les joueurs)."""
    pair = rng.choice(list(SET17_GODS), size=2, replace=False)
    return (str(pair[0]), str(pair[1]))


def aligned_god(votes: dict[str, int]) -> str | None:
    """Dieu aligné = celui avec le plus de votes ; None si aucun vote.

    En cas d'égalité, départage stable par ordre des dieux (déterministe).
    """
    if not votes or max(votes.values(), default=0) == 0:
        return None
    best = max(votes.values())
    for god in SET17_GODS:  # ordre stable
        if votes.get(god, 0) == best:
            return god
    return None
