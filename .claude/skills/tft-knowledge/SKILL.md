---
name: tft-knowledge
description: Authoritative reference for Teamfight Tactics (TFT) rules, numbers and Set 17 "Space Gods" data — game flow, economy, shop/augment odds, combat mechanics, the Realm of the Gods, and how TFT_GOAT sources its data. Use whenever a question, design decision, or simulator change depends on real TFT mechanics or numbers (augment tier odds, shop odds, XP/interest tables, mana/crit/CC rules, the Set 17 roster/traits, the god mechanic). Verify any number here against the live patch before relying on it.
---

# TFT Knowledge (Set 17 "Space Gods", patch 17.4)

Single source of truth for the **rules and numbers of TFT** as used by the TFT_GOAT simulator.
Static game data (champion stats, item effects, abilities, augment tiers) is **CommunityDragon**;
meta/performance stats are **datatft**; this skill captures the **mechanics and tables** that tie
them together.

> ⚠️ TFT changes every patch. Treat every number here as "true as of patch 17.4 (June 2026)".
> Before changing simulator behavior, re-verify against the live patch notes / wiki. Where sources
> disagree (noted inline), prefer the official Riot patch notes.

## When to use

- A simulator/RL change depends on a real rule or number (odds, costs, formulas, timings).
- Auditing whether the engine matches real TFT (combat, economy, augments, eliminations).
- Answering "how does X work in TFT?" or "what are the real odds of Y?".
- Onboarding to Set 17 specifics (roster, traits, the Realm of the Gods).

## Reference files (read the one you need)

| File | Contents |
|---|---|
| `references/game-flow.md` | Stage/round structure, PvE/PvP, augment rounds, carousel→Realm of the Gods, eliminations, player damage formula |
| `references/economy.md` | Gold income, interest, win/loss streak, XP-to-level table, level→max units, shop odds per level, reroll/XP costs, sell value |
| `references/augments.md` | Augment tiers (silver/gold/prismatic), per-round tier odds, reroll, god augments |
| `references/combat.md` | Combat start, mana & mana-lock, crit, attack-speed cap, armor/MR mitigation, CC, damage types, item proc categories, durability/omnivamp/grievous/sunder/shred |
| `references/set17-space-gods.md` | The Realm of the Gods mechanic, the 9 gods, blessings/alignment/boons, god artifacts; full Set 17 champion roster by cost + traits with breakpoints |
| `references/data-sources.md` | CommunityDragon / datatft / Riot match-v1: what each provides and how TFT_GOAT consumes them |

## Quick reference (the numbers people ask for most)

- **Augment rounds**: 2-1, 3-2, 4-2 (Hyper Roll: 3-1, 5-2, 7-2). 3 offered, pick 1, reroll = **2 gold**.
- **Augment tier odds** (silver / gold / prismatic): 2-1 = **28 / 62 / 10**, 3-2 = **35 / 45 / 20**,
  4-2 = **6 / 74 / 20**. Each of the 3 slots rolled independently. Offers are **per-player, random,
  different** for everyone.
- **Stage 1** = 3 PvE rounds (1-1…1-3). Stages 2+ = 7 rounds; x-4 = Realm of the Gods (carousel
  replacement), x-7 = PvE monsters; all other rounds PvP.
- **Interest**: +1 gold per 10 banked, **max +5** (cap at 50 gold). **Streak bonus**: 2→+1, 3-4→+2, 5+→+3.
- **Shop reroll** = 2 gold. **Buy XP** = 4 gold for 4 XP.
- **Crit**: every unit's **auto-attacks crit at 25%** base; **abilities can't crit** without
  Infinity Edge / Jeweled Gauntlet.
- **Mana**: gain on attack + on taking damage; **cast at full mana**; **~1 s mana-lock** after a cast.
- **Player damage** = stage base + 1 per surviving enemy unit. Base (Set 17): 2-x:2, 3-x:5, 4-x:8,
  5-x:10, 6-x:12, 7+:17.

Each reference file expands these with formulas, edge cases, and sources.
