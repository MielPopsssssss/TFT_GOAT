# Roadmap

This is where the project is going and **where contributors can plug in**. Items marked
**🙋 help wanted** are good places to start. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup.

Status legend: ✅ done · 🔧 in progress · ⏳ planned · ⏸️ optional/out-of-scope

---

## ✅ Done

- **Data & Knowledge Layer** — CommunityDragon Set 17 content (champions, traits, items, augments),
  shop odds, augment tier odds, Riot `match-v1` collector, datatft meta-stats scraper + verifier.
- **Macro Environment** — PettingZoo 8-player `ParallelEnv`: economy, interest, leveling/XP, shop
  RNG, buy/sell, items (component→item recipes), augments (real tier odds + reroll), rounds, HP.
- **RL Agent** — custom CleanRL-style PPO with action masking + self-play, plus a scripted opponent
  for credible evaluation.
- **Combat surrogate** — `CombatNet` trained on real challenger games *and* on the engine; plugged
  in via `NeuralResolver`. Hybrid surrogate reaches ~0.88 real-game val accuracy.
- **Real tick-by-tick engine (core)** — hex grid, real stats, auto-attacks, mana/cast, CC, shields,
  omnivamp/grievous/durability, ability crit, role-aware placement, 68/68 champion abilities.

---

## 🔧 In progress — the big open challenges

### 1. Train the agent to actually be good 🙋 help wanted · `RL`
**This is the headline problem.** The pipeline is complete and the agent crushes random, but it
**still loses to the scripted opponent** (top-4 ~40%). We need training at scale: large rollouts,
hyperparameter tuning, and possibly a curriculum against the scripted bot.
- Profile and scale the self-play loop.
- Reward shaping experiments (economy priors, placement).
- Better evaluation harness + tracking (win-rate curves vs. random *and* scripted).

### 2. Fill in the combat long-tail 🙋 help wanted · `game-knowledge` · `good first issue`
The engine uses real data for stats + abilities, but a long tail of effects still falls back to a
default. Each one is a small, self-contained, testable PR. Exact gaps are tracked in
[`docs/COMBAT_COVERAGE.md`](docs/COMBAT_COVERAGE.md):
- **Item procs** — ~22 special effects done; the rest currently apply stats only.
- **Augment combat logic** — 67–74 / 276 implemented; the others are correctly no-op (eco/loot) but
  some still need wiring.
- **Non-stat trait effects** — summons, conditional shields, execution thresholds.

### 3. Item identities in the env 🙋 help wanted · `env`
The env currently assigns a *random* completed item to an EQUIP action. Replace this with a real
component→item choice driven by the agent, so item *identity* (not just a counter) reaches combat.

---

## ⏳ Planned

- **Vectorized env / engine** 🙋 help wanted · `performance` — self-play needs millions of games;
  batch the environment and/or the engine for throughput.
- **Exact game flow** — finalize disputed XP/streak tables against official patch notes (some values
  are intentionally not flipped without an official source — see COMBAT_COVERAGE).
- **Player positioning granularity** — richer positioning in the observation/action space.
- **Realm of the Gods (full)** — the core vote → alignment → God Boon mechanic is now modeled
  (2 gods per lobby, Minor Blessing votes at 2-4/3-4/4-4, majority alignment, real God Boon at 4-7).
  What's left: couple each blessing to the god it belongs to, implement the actual Minor Blessing
  effects, and add the god-specific artifacts / loot.
- **Set-refresh tooling** — make "new set = one data refresh" a single, documented command.
- **MuZero / Gumbel-MuZero** 🙋 help wanted · `research` — stretch goal on top of the existing env.

---

## ⏸️ Optional / out of scope for the core

- **Perception (computer vision / OCR)** and **Actuation (playing the real client)**.
  ⚠️ In-game automation violates Riot's ToS. The RL core is deliberately **offline**; if ever built,
  actuation is test-account-only and at the user's own risk.

---

## How to claim a task

1. Comment on the related issue (or open one) saying you're taking it.
2. Read the relevant section of [`docs/COMBAT_COVERAGE.md`](docs/COMBAT_COVERAGE.md) or
   [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).
3. Open a draft PR early — it's the best way to get feedback.

Don't see your idea here? Open a [Discussion](../../discussions) — new directions are welcome.
