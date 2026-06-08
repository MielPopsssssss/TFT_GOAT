# Game flow — stages, rounds, eliminations

## Stage / round structure

- A game is divided into **stages**; each stage has rounds labelled `stage-round` (e.g. `4-2`).
- **Stage 1 = 3 rounds** (1-1, 1-2, 1-3), all **PvE** (minions / "creeps"). No PvP in stage 1.
- **Stages 2+ = 7 rounds** each (x-1 … x-7).
- Round types within stages 2+:
  - **x-4 = Realm of the Gods** (Set 17's replacement for the carousel). See `set17-space-gods.md`.
  - **x-7 = PvE** monster round (Krugs/Wolves/Raptors → Elder Dragon-style boss at end stages).
  - **all other rounds = PvP** (combat vs another player's board).
- In TFT_GOAT this is encoded in `env/rounds.py`: `PVE_OPENING=3`, `ROUNDS_PER_STAGE=7`,
  `stage_of`, `round_in_stage`, `is_pvp` (False for stage 1, and for x-4 / x-7), `is_god_round` (x-4).

## Augment rounds

- Augments are offered at **2-1, 3-2, 4-2** (standard). In Hyper Roll: 3-1, 5-2, 7-2.
- See `augments.md` for tiers, odds and reroll.

## PvP matchmaking

- Each PvP round, living players are paired (you don't fight the same opponent repeatedly when
  avoidable). Odd player count → one player fights a **"ghost"** (a copy of another board); only the
  real player takes damage from a ghost loss.

## Player damage formula (loss of Tactician HP)

When you lose a PvP/PvE combat you lose Tactician HP equal to:

```
damage = stage_base_damage + 1 × (number of surviving enemy units)
```

- The per-unit term is **flat 1 per surviving unit** (NOT weighted by star level).
- **Set 17 stage base** (verified vs TFT Ninja): 2-x:2, 3-x:5, 4-x:8, 5-x:10, 6-x:12, 7+:17.
- Players start at **100 HP**. Reaching 0 eliminates you.
- TFT_GOAT: `STAGE_BASE_DAMAGE` + `_apply_damage` in `env/rounds.py`.

## Eliminations & placement

- A player at HP ≤ 0 is eliminated; **placement = number of players still alive** (lower-HP players
  die first in a multi-death round → higher/worse placement number).
- Final survivor = **1st place**.
- An eliminated player's champions return their copies to the **shared pool** (pool conservation).
- No traditional sudden-death in this model; ties broken by survivors then remaining HP.

## Board / bench

- **Board cap** = your level (max units you can field = current level).
- **Bench** = 9 slots. Units combine: **3 of the same champion at the same star → 1 unit one star
  higher** (1★→2★→3★). Star scaling is roughly ×1.8 HP/AD per star.

Sources: official Set 17 overview, TFT wiki "Game mechanics", TFT Ninja damage breakdown.
