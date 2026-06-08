# Economy — gold, interest, streaks, XP, shop odds

## Gold income each PvP round

```
income = base(5) + interest + streak_bonus + win_bonus
```

- **Base**: 5 gold per round (after the early rounds ramp up).
- **Interest**: +1 gold per 10 gold banked, **capped at +5** (so banking 50 gold = max interest).
- **Win/loss streak bonus** (Set 17): streak length **2 → +1**, **3-4 → +2**, **5+ → +3**.
  Win streaks and loss streaks both grant the bonus (lose-streaking is a legit econ strategy).
- **Win bonus**: +1 gold for winning a PvP combat.

TFT_GOAT: `env/economy.py` → `round_income`, interest cap, streak table.

## Leveling

- You gain a small amount of **passive XP** each round, and can **Buy XP = 4 gold for 4 XP**.
- **Level cap = 10** (Set 17). Board cap (units you can field) = your level.
- **XP required to reach the next level** (cumulative-per-level, real TFT):

| Level | XP to next |
|---|---|
| 2 | 2 |
| 3 | 6 |
| 4 | 10 |
| 5 | 20 |
| 6 | 36 |
| 7 | 48 |
| 8 | 76 |
| 9 | 84 |

> ⚠️ TFT_GOAT's `XP_TO_LEVEL` is flagged as a placeholder in code and is slightly off at 8→9 and
> 9→10 — use the table above as the real reference.

## Shop

- **Shop size** = 5 slots. **Reroll the shop = 2 gold**. Buying a champion costs its tier cost (1-5).
- Champions are drawn per-slot from a **cost-tier probability table that depends on your level**.
- **Shop odds by level** (% chance per slot for a 1/2/3/4/5-cost champion):

| Level | 1-cost | 2-cost | 3-cost | 4-cost | 5-cost |
|---|---|---|---|---|---|
| 1 | 100 | 0 | 0 | 0 | 0 |
| 2 | 100 | 0 | 0 | 0 | 0 |
| 3 | 75 | 25 | 0 | 0 | 0 |
| 4 | 55 | 30 | 15 | 0 | 0 |
| 5 | 45 | 33 | 20 | 2 | 0 |
| 6 | 30 | 40 | 25 | 5 | 0 |
| 7 | 19 | 30 | 35 | 15 | 1 |
| 8 | 18 | 25 | 32 | 22 | 3 |
| 9 | 10 | 20 | 25 | 35 | 10 |
| 10 | 5 | 10 | 20 | 40 | 25 |

> ⚠️ **Sources disagree on levels 7/8/9** (esportstales vs tftactics vs tftacademy differ by a few
> %). The table above follows the more commonly cited values; TFT_GOAT's `data/odds.py::SHOP_ODDS`
> uses a near-identical table. If precision matters, copy the exact numbers from the live patch notes.

## Champion pool (shared across all 8 players)

Copies available per champion, by cost (Set 17):

| Cost | Copies per champion | Distinct champions |
|---|---|---|
| 1 | 30 | ~15 |
| 2 | 25 | ~13 |
| 3 | 18 | ~13 |
| 4 | 10 | ~14 |
| 5 | 9 | ~10 |

- Buying / rolling does **not** consume copies you don't take; the pool only shrinks when copies are
  **held** by players. Selling/eliminations return copies. This is why contested comps "dry up".
- TFT_GOAT: `data/odds.py::POOL_SIZES`, `env/shop.py::roll_shop` (pool-aware weighting).

## Selling

- Selling returns gold roughly equal to what you paid: full cost for 1-cost or any 1★ unit;
  for cost ≥ 2 multi-star units it's (cost × 3^(star-1)) − 1 (a 1-gold penalty). 5-costs are special-cased.
- TFT_GOAT: `env/economy.py::sell_value`.

Sources: TFT wiki "Gold"/"Experience"/"Shop", tftactics.gg rolling chances, esportstales odds tables.
