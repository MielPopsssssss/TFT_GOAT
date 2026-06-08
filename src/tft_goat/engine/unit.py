"""CombatUnit : etat runtime d'une unite, construit depuis les VRAIES stats.

Stats de base (data) -> star scaling -> effets d'items (reels, data) -> bonus de traits (reels).
Les semantiques d'effets (flat vs %) sont approximees a partir des cles CDragon (documente).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ..data.models import Champion, SetContent
from .config import ATTACK_WINDUP, BASE_AP, STAR_SCALE

# Bonus generique d'un objet « moyen » quand l'identite n'est pas connue (board env = compteur).
_GENERIC_ITEM = {"Health": 150.0, "AD": 0.15, "AP": 15.0, "Armor": 15.0, "MagicResist": 15.0}


@dataclass
class CombatUnit:
    champion_api: str
    star: int
    team: int
    max_hp: float
    hp: float
    ad: float
    ap: float
    attack_speed: float
    armor: float
    mr: float
    attack_range: int
    crit_chance: float
    crit_mult: float
    max_mana: float
    mana: float
    variables: dict[str, tuple[float, ...]] = field(default_factory=dict)
    role: str = ""  # role data (APTank, ADCarry, APReaper...) -> placement + ciblage
    pos: tuple[int, int] = (0, 0)
    alive: bool = True
    attack_cd: float = 0.0
    move_cd: float = 0.0
    target: "CombatUnit | None" = None  # cible persistante (gardee jusqu'a sa mort)
    shield: float = 0.0  # PV de bouclier (absorbe avant les PV)
    shield_expire: float = 0.0  # instant (s) d'expiration du bouclier
    stun_timer: float = 0.0  # secondes de stun restantes (>0 = ne peut pas agir)
    silence_timer: float = 0.0  # ne peut pas CAST (peut attaquer/bouger)
    disarm_timer: float = 0.0  # ne peut pas ATTAQUER (peut cast/bouger)
    untargetable_timer: float = 0.0  # ne peut pas etre cible
    mana_lock_timer: float = 0.0  # apres un cast : aucun gain de mana
    item_apis: tuple[str, ...] = ()  # identites d'objets equipes (pour les procs)
    can_ability_crit: bool = False  # vrai si IE/Jeweled Gauntlet -> les sorts peuvent critter
    damage_amp: float = 0.0  # amplification de degats sortants (0.1 = +10%) — s'additionne
    incoming_reduction: float = 0.0  # durability : reduction des degats SUBIS — cumul multiplicatif
    omnivamp: float = 0.0  # soigne ce % des degats infliges — s'additionne
    healing_reduction: float = 0.0  # Grievous Wounds sur cette unite (max actif)
    mana_regen: float = 0.0  # mana regen par seconde — s'additionne
    sunder: float = 0.0  # reduction d'armure subie (max actif)
    shred: float = 0.0  # reduction de RM subie (max actif)
    triggered: set = field(default_factory=set)  # procs a-usage-unique deja declenches

    def ability_value(self, name: str, default: float = 0.0) -> float:
        """Valeur d'une variable de sort au niveau d'etoile courant.

        Format CDragon : index 0 = placeholder, etoile s -> index s (1=1etoile...).
        """
        vals = self.variables.get(name)
        if not vals:
            return default
        return float(vals[min(self.star, len(vals) - 1)])


def _apply_effects(unit: CombatUnit, effects: dict[str, float]) -> None:
    """Applique des effets de STATS (cles CDragon -> attributs). Approximations documentees."""
    for key, v in effects.items():
        if v is None:
            continue
        k = key.lower()
        if k in ("health", "hp"):
            unit.max_hp += v
            unit.hp += v
        elif k == "armor":
            unit.armor += v
        elif k in ("magicresist", "mr"):
            unit.mr += v
        elif k == "ad":
            unit.ad *= 1.0 + v  # fraction (0.1 = +10%)
        elif k == "ap":
            unit.ap += v
        elif k in ("attackspeed", "as"):
            unit.attack_speed *= 1.0 + v
        elif k == "critchance":
            unit.crit_chance += v / 100.0 if v > 1 else v
        elif k == "mana":
            unit.max_mana += v


def build_unit(
    champion: Champion, star: int, team: int, content: SetContent,
    item_apis: tuple[str, ...] = (), generic_items: int = 0,
) -> CombatUnit:
    """Construit une unite de combat depuis les vraies stats."""
    st = champion.stats
    scale = STAR_SCALE.get(star, 1.0)
    hp = (st.hp if st else 500.0) * scale
    unit = CombatUnit(
        champion_api=champion.api_name, star=star, team=team,
        max_hp=hp, hp=hp,
        ad=(st.damage if st else 50.0) * scale,
        ap=BASE_AP,
        attack_speed=st.attack_speed if st else 0.6,
        armor=st.armor if st else 20.0,
        mr=st.magic_resist if st else 20.0,
        attack_range=int(st.attack_range) if (st and st.attack_range) else 1,
        crit_chance=st.crit_chance if st else 0.25,
        crit_mult=st.crit_multiplier if st else 1.4,
        max_mana=(st.mana if (st and st.mana) else 1e9),
        mana=(st.initial_mana if st else 0.0),
        variables=dict(champion.ability.variables) if champion.ability else {},
        role=champion.role or "",
        item_apis=tuple(item_apis),
        # IE / Jeweled Gauntlet debloquent le crit des sorts (les autos crittent deja a 25%)
        can_ability_crit=any(
            ("InfinityEdge" in a or "JeweledGauntlet" in a) for a in item_apis
        ),
    )
    for api in item_apis:  # items reels (identites connues)
        item = content.items.get(api)
        if item:
            _apply_effects(unit, item.effects)
    for _ in range(generic_items):  # items abstraits (compteur env)
        _apply_effects(unit, _GENERIC_ITEM)
    unit.attack_cd = ATTACK_WINDUP  # delai avant la 1re auto-attaque
    return unit
