"""God Boons du Realm of the Gods — les 11 restants (batch dédié, 17/17 couverts).

Le boon du dieu aligné est octroyé au 4-7 (cf. `data/gods.py` + `env/rounds.py`) puis
délivré ici via `chosen_augments`. Chaque fn applique les valeurs RÉELLES CDragon reçues
dans `variables` ; toute approximation est commentée inline et tracée dans
`docs/COMBAT_COVERAGE.md`. Trois boons sont des no-ops FIDÈLES : leur effet est purement
éco/joueur (couche env), inexistant en combat dans le vrai jeu — leur câblage env reste
un item de backlog dédié (« Décider du sort du God Boon hors moteur réel »).

Tests pin : tests/test_god_boons_engine.py (chaque chiffre référence sa source).
"""

from __future__ import annotations

# Réutilise l'abstraction d'item moyen du moteur (Kayle Scrapper) — même convention
# que le compteur `generic_items` du board env.
from ..unit import _GENERIC_ITEM, _apply_effects
from .batch_2 import _aurelion_sol_small_quest

# --- Ekko : item Anomaly (CDragon global `TFT17_EkkoOffering_AnomalyItem`, légitimement
# HORS setData — octroyé par le dieu, pas par le pool). Constantes en dur car inaccessibles
# via SetContent ; pinnées contre le JSON brut par test_ekko_anomaly_constants_pinned_*.
ANOMALY_TANK_HP = 1100.0  # "Tank: Gain @TankHP@ health"
ANOMALY_MARKSMAN_AS = 0.75  # "Marksman: +@MarksmanBonusAS@ attack speed"
ANOMALY_FIGHTER_ADAP = 35.0  # "Fighter: +@FighterAD@ AD / +@FighterAP@ AP"

# Soraka : PV tacticien manquants supposés au moment du boon (4-7) — le moteur de combat
# n'a pas le contexte joueur (même esprit que Ahri qui suppose niveau 9).
ASSUMED_MISSING_TAC_HP = 30.0

GOLDEN_HEX_API = "TFT17_Augment_YasuoGodAugment_GoldenHex"


def _combat_noop(team, enemies, ctx, variables) -> None:
    """No-op FIDÈLE : aucun effet combat dans le vrai jeu (effet éco/joueur, couche env)."""


def _large_quest_buildtime_noop(team, enemies, ctx, variables) -> None:
    """No-op ici : l'effet réel (« +1 to all non-unique traits ») est appliqué au BUILD des
    équipes (`simulate._build_team` -> `apply_team_traits(bonus_units=1)`), pas au start."""


def _aurelion_sol_parent(team, enemies, ctx, variables) -> None:
    # "Choose 1 of @NumQuestOptions@ quests" : le choix de quête n'est pas modélisé ->
    # approx quête Small (seule à effet combat immédiat), avec les variables du parent
    # (SmallQuestADAP). Medium = éco, Large = câblé au build (cf. simulate.py).
    _aurelion_sol_small_quest(team, enemies, ctx, variables)


def _soraka_boon(team, enemies, ctx, variables) -> None:
    # "team gains @HealthPerTacHealth@ Health for each missing player health" ; le
    # "+@Heal@ player health par combat" est de l'éco joueur (env), ignoré ici.
    hp = variables.get("HealthPerTacHealth", 0.0) * ASSUMED_MISSING_TAC_HP
    for u in team:
        u.max_hp += hp
        u.hp += hp


def _thresh_boon(team, enemies, ctx, variables) -> None:
    # "Each round, roll a die. Get a bonus based on that roll." — d6 réel (6 valeurs
    # d'effets dans la data). Seules 2 faces sont du combat (desc) : Health ({b386f143}=75)
    # et Attack Speed ({7eafa4c6}=0.06) ; les 4 autres = récompenses éco (no-op combat).
    if not team:
        return
    face = int(ctx.rng.integers(6))
    if face == 0:
        hp = variables.get("{b386f143}", 0.0)
        for u in team:
            u.max_hp += hp
            u.hp += hp
    elif face == 1:
        as_ = variables.get("{7eafa4c6}", 0.0)
        for u in team:
            ctx.buff_attack_speed(u, as_)


def _ekko_boon(team, enemies, ctx, variables) -> None:
    # "Gain the Anomaly, an item which grants units a powerful evolution depending on
    # their role." — posée sur l'unité la plus costaud (même approx que Golden Hex).
    # Rôles modélisés : *Tank -> +HP, *Carry -> Marksman (+AS) ; autres rôles ≈ Fighter
    # (+AD/+AP plats). Les évolutions Caster/Specialist (mécaniques à procs) sont
    # approximées en Fighter. Les Magnetic Removers sont de l'éco (ignorés).
    if not team:
        return
    u = max(team, key=lambda x: x.max_hp)
    if "Tank" in u.role:
        u.max_hp += ANOMALY_TANK_HP
        u.hp += ANOMALY_TANK_HP
    elif "Carry" in u.role:
        ctx.buff_attack_speed(u, ANOMALY_MARKSMAN_AS)
    else:
        u.ad += ANOMALY_FIGHTER_ADAP
        u.ap += ANOMALY_FIGHTER_ADAP


def _kayle_scrapper(team, enemies, ctx, variables) -> None:
    # "Combat start: Up to @NumComponents@ components temporarily turn into completed
    # items." — approx : +1 item générique (unit._GENERIC_ITEM) sur les NumComponents
    # unités les plus costauds (l'upgrade composant->complet ≈ un item moyen).
    # Removers/salvager = éco (ignorés).
    n = int(variables.get("NumComponents", 0.0))
    for u in sorted(team, key=lambda x: -x.max_hp)[:n]:
        _apply_effects(u, _GENERIC_ITEM)


def _golden_hex_fx(ctx) -> dict:
    """Valeurs réelles du Golden Hex lues dans la data via ctx.content (jamais en dur)."""
    if ctx.content is None:
        return {}
    aug = ctx.content.augments.get(GOLDEN_HEX_API)
    return dict(aug.effects) if aug else {}


def _apply_hex(u, ctx, fx: dict, mult: float) -> None:
    hp = fx.get("BonusHealth", 0.0) * mult
    u.max_hp += hp
    u.hp += hp
    ctx.buff_attack_speed(u, fx.get("AttackSpeed", 0.0) * mult)


def _yasuo_more_hexes(team, enemies, ctx, variables) -> None:
    # "Yasuo's hexes also affect adjacent units at @Effectiveness*100@% effectiveness."
    # Les hexes des Minor Blessings ne sont pas modélisés -> approx 1 hex (valeurs Golden
    # Hex, cf. _golden_hex batch_1) sur la plus costaud + 2 « adjacents » (les 2 suivantes
    # par PV) à Effectiveness. L'or-au-kill du hex est de l'éco (ignoré).
    if not team:
        return
    fx = _golden_hex_fx(ctx)
    eff = variables.get("Effectiveness", 0.0)
    ordered = sorted(team, key=lambda x: -x.max_hp)
    _apply_hex(ordered[0], ctx, fx, 1.0)
    for u in ordered[1:3]:
        _apply_hex(u, ctx, fx, eff)


def _yasuo_painted_power(team, enemies, ctx, variables) -> None:
    # "Increase the power of Yasuo's hexes by @Effectiveness*100@%." — approx 1 hex
    # (valeurs Golden Hex) amplifié sur la plus costaud. Le "+@GoldIfTwo@ gold si
    # seulement 2 hexes" est de l'éco (ignoré).
    if not team:
        return
    fx = _golden_hex_fx(ctx)
    u = max(team, key=lambda x: x.max_hp)
    _apply_hex(u, ctx, fx, 1.0 + variables.get("Effectiveness", 0.0))


REGISTRY = {
    "TFT17_Augment_AurelionSolGodAugment": _aurelion_sol_parent,
    "TFT17_Augment_AurelionSolGodAugment_BoonOfResurrection": _combat_noop,  # survie joueur (env)
    "TFT17_Augment_AurelionSolGodAugment_LargeQuest": _large_quest_buildtime_noop,
    "TFT17_Augment_AurelionSolGodAugment_MediumQuest": _combat_noop,  # anvil + or (éco)
    "TFT17_Augment_EkkoGodAugment": _ekko_boon,
    "TFT17_Augment_EvelynnGodAugment_BloodPrice": _combat_noop,  # shop contre PV (éco)
    "TFT17_Augment_KayleGodAugment_Scrapper": _kayle_scrapper,
    "TFT17_Augment_SorakaGodAugment": _soraka_boon,
    "TFT17_Augment_ThreshGodAugment": _thresh_boon,
    "TFT17_Augment_YasuoGodAugment_MoreHexes": _yasuo_more_hexes,
    "TFT17_Augment_YasuoGodAugment_PaintedPower": _yasuo_painted_power,
}
