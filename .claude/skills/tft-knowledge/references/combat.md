# Combat mechanics

Combat is an auto-battle on a hex grid. Units acquire a target, move toward it, auto-attack in range,
gain mana, and **cast their ability when mana is full**.

## Targeting & positioning

- Default targeting = **nearest enemy**; target is **persistent** (kept until it dies), reducing jitter.
- Typical placement: **tanks/bruisers front-center**, **carries/casters/supports back**, carries in
  the **backline corners**. TFT_GOAT scores units by role (`_frontline_score`) to place them.
- **Assassins (Reapers)** dash at combat start to the enemy **backline carry** (lowest frontline score).

## Auto-attacks & damage

- Attack cadence = **attack speed** (attacks/sec), **capped at 5.0**.
- Three damage types: **physical** (reduced by Armor), **magic** (reduced by Magic Resist), **true**
  (ignores resistances).
- **Mitigation formula**: `damage_taken = raw × 100 / (100 + resist)` (armor for physical, MR for
  magic). 100 armor = take 50%; 200 = 33%, etc.
- **Crit**: **every unit's auto-attacks crit at 25% base** for ×1.4 damage. **Abilities do NOT crit**
  unless the unit holds **Infinity Edge** or **Jeweled Gauntlet** (which unlock ability crit).

## Mana

- Units gain mana **per auto-attack** and **when taking damage** (~1% of pre-mitigation + ~7% of
  post-mitigation damage, capped per hit ~42.5).
- At **full mana → cast ability**, then mana resets.
- **Mana-lock**: for ~**1 second** after casting, a unit gains **no mana** (prevents instant re-cast).
- Some units start with partial mana (`initialMana`).

## Crowd control & debuffs

- **Stun** (can't act), **Silence** (can't cast, can attack/move), **Disarm** (can't attack, can
  cast/move), **Untargetable** (excluded from targeting). All are timed.
- **Sunder** (reduce Armor), **Shred** (reduce MR), **Grievous Wounds** (reduce healing). The active
  strongest value applies (not additive across sources).

## Items & augments in combat

- **Stat items** apply their numeric effects at unit construction (HP/AD%/AP/Armor/MR/AS/crit/mana).
- **Item procs** (special effects) hook combat events: on-being-hit (e.g. Bramble Vest reflects),
  on-tick (e.g. Dragon's Claw % max HP/s, Spirit Visage % missing HP/s), HP-threshold (e.g. Sterak's,
  Edge of Night, Protector's Vow, Zhonya's), combat-start (durability).
- **Durability** (incoming damage reduction) stacks **multiplicatively**; **damage amp** and
  **omnivamp** stack additively.
- Set 17 renamed many classic item apiNames to *different* Set 17 items (e.g. `RunaansHurricane` =
  Kraken's Fury, `GuardianAngel` = Edge of Night, `FrozenHeart` = Protector's Vow). Always check the
  Set 17 effect, not the legacy name. **No standard Set 17 item revives** (GA became Edge of Night).

## Traits

- Active traits apply real stat bonuses (armor/HP/MR/AS/AD/AP/DR/damage-amp) at their breakpoints,
  some team-wide, some only to trait members; bonuses **stack cumulatively**.

TFT_GOAT implements all of the above in `engine/` (tick-by-tick) as the `EngineResolver`; a learned
`CombatNet` surrogate approximates it for fast self-play. See `docs/COMBAT_COVERAGE.md` for fidelity.

Sources: TFT wiki "Damage"/"Mana"/"Critical strike"/"Armor", Set 17 patch notes, in-game testing.
