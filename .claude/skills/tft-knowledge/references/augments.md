# Augments — tiers, odds, reroll

## What augments are

Game-changing modifiers chosen during the game. Three are offered at each augment round and you
**pick one**. Augments come in three tiers (rising power): **Silver < Gold < Prismatic**.

## Augment rounds & offering

- Offered at **2-1, 3-2, 4-2** (Hyper Roll: 3-1, 5-2, 7-2) — the 1st, 2nd, 3rd augment choices.
- The offer is **random, independent, and different for every player**. You do **not** choose which
  augments appear — only which of the offered three you take.
- Each of the **3 slots is rolled independently** from the round's tier distribution, so a row can
  be mixed tiers (e.g. 2 silver + 1 gold).

## Tier odds per round (silver / gold / prismatic)

| Choice | Round | Silver | Gold | Prismatic |
|---|---|---|---|---|
| 1st | 2-1 | 28% | 62% | 10% |
| 2nd | 3-2 | 35% | 45% | 20% |
| 3rd | 4-2 | 6% | 74% | 20% |

These are the canonical TFT distribution odds (stable across Sets 14–17; 4-2 = 6/74/20 confirmed for
Set 17). TFT_GOAT: `env/rounds.py::AUGMENT_TIER_ODDS`, verified empirically to <0.5%.

## Reroll

- You may **reroll** the offered augments. **Cost = 2 gold** per reroll (re-rolls the row; each new
  augment is rolled fresh from the same round's tier odds).
- TFT_GOAT models reroll as the `REROLL_AUGMENT` action, legal while an offer is open and gold ≥ 2;
  it deducts 2 gold and re-samples (`env/actions.py::_reroll_augment`, `env/rounds.py::sample_augments`).
- (Real TFT historically also gave limited *free* per-slot rerolls in some sets; the project uses a
  simple 2-gold whole-row reroll.)

## Tier source (how the simulator knows an augment's tier)

CommunityDragon has **no clean `tier` field**. The reliable signal is the **icon filename**: the
roman numeral (`_I`/`_II`/`_III`) or arabic digit (`1`/`2`/`3`) just before the `.TFT_SetXX.tex`
suffix encodes the silver/gold/prismatic border Riot renders. I→silver, II→gold, III→prismatic.
TFT_GOAT: `data/augment_tiers.py::detect_tier` → `Augment.tier`. Resolves all 276 Set 17 augments
(silver 67 / gold 124 / prismatic 68, + 17 god augments).

## God augments (Set 17 only)

`*GodAugment*` augments are **Realm of the Gods boons**, NOT part of the silver/gold/prismatic
augment rounds. TFT_GOAT classifies them `tier="god"` and **excludes them from the regular augment
pool**. See `set17-space-gods.md`.

Sources: metatft / tftodds augment-distributions, TFT wiki "Augment", littlebuddybot Set 17 odds.
