# TFT_GOAT 🐐

> An AI that learns to play **Teamfight Tactics** at a high level through **reinforcement learning / self-play**.

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![CI](https://github.com/MielPopsssssss/TFT_GOAT/actions/workflows/ci.yml/badge.svg)](https://github.com/MielPopsssssss/TFT_GOAT/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg)](CONTRIBUTING.md)
[![Set 17](https://img.shields.io/badge/TFT-Set%2017%20Space%20Gods-purple.svg)](#)

🇫🇷 *Une version française de ce README est disponible dans [README.fr.md](README.fr.md).*

---

## What is this?

TFT_GOAT is an open-source attempt to build a TFT agent the way **Riot themselves** described at
GDC 2024: learn the **macro game** (economy, rolling, leveling, comp building, items, augments,
positioning) with reinforcement learning, and resolve combat with a **learned neural surrogate**
instead of a brittle hand-written simulator.

Two combat backends live behind a single `CombatResolver` interface:

- a **real tick-by-tick engine** (hex grid, real champion/item/trait stats, abilities, CC,
  omnivamp / grievous / durability / shields, ability crit) — the **ground truth**, faithful but slow;
- a **neural surrogate** `P(win | board A, board B)` **trained on that engine** — a *fast*
  approximation that gives RL self-play the throughput it needs.

The whole content layer is **data-driven** (CommunityDragon + datatft), so a new TFT set is a
**data refresh**, not a rewrite.

> ⚠️ The RL/self-play core is **100% offline** and never touches the game client — no ToS risk.
> In-game actuation (a far-future, optional step) would violate Riot's ToS and is explicitly out of
> scope for the core project.

---

## Why it's interesting

- **A real, end-to-end RL environment** for an imperfect-information, 8-player auto-battler — not a toy.
- **Honest engineering.** We document exactly what is faithfully simulated vs. approximated
  (see [`docs/COMBAT_COVERAGE.md`](docs/COMBAT_COVERAGE.md)) — no hand-waving.
- **Three swappable combat resolvers** sharing one interface — a clean place to experiment.
- **A concrete open problem**: the pipeline is complete, but the agent still loses to a scripted
  opponent. Training it to actually be good is the headline challenge (see [Roadmap](#roadmap)).

---

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│ (4) RL Agent — PPO self-play (MuZero later)                   │
│      shared policy, 8 instances in one lobby                  │
└───────────────▲──────────────────────────┬───────────────────┘
     observation │                   action │
┌───────────────┴──────────────────────────▼───────────────────┐
│ (2) Macro Environment  (PettingZoo ParallelEnv)               │
│   economy · level · roll · shop RNG · buy/sell · items ·      │
│   augments · positioning · rounds · HP · 8 players            │
│        calls ▼  (pluggable CombatResolver interface)          │
│   ┌───────────────────────────────────────────────────┐      │
│   │ (3) Combat Resolver                                │      │
│   │   HeuristicResolver — board strength (fast)        │      │
│   │   NeuralResolver    — learned surrogate (fast)     │      │
│   │   EngineResolver    — real tick-by-tick (truth)    │      │
│   └───────────────────────────────────────────────────┘      │
└───────────────▲───────────────────────────────────────────────┘
   content/priors│
┌───────────────┴───────────────────────────────────────────────┐
│ (1) Data & Knowledge Layer                                     │
│   CommunityDragon (static content) · datatft (meta priors) ·  │
│   Riot match-v1 collector (combat training dataset)           │
└────────────────────────────────────────────────────────────────┘
```

Full design doc: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

---

## Run it

```bash
# 1. Setup
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# 2. Tests (215 passing)
python -m pytest -q

# 3. Play a full random 8-player game (Set 17)
python -m tft_goat.scripts.random_rollout

# 4. Train a PPO agent (eval vs random AND vs a scripted opponent)
python -m tft_goat.scripts.train --content real --resolver neural \
    --surrogate runs/surrogate/combatnet.pt --iterations 20
```

Train the combat surrogate against the **real engine** (faithful ground truth):

```bash
python -m tft_goat.scripts.train_surrogate --source engine --pairs 8000 --engine-samples 3
#   -> CombatNet ~83% agreement with the tick-by-tick engine; a fast stand-in for RL
```

Or against **real challenger games** via the Riot API:

```bash
RIOT_API_KEY=... python -m tft_goat.scripts.collect_matches --matches 150
python -m tft_goat.scripts.train_surrogate --source riot --matches data/matches/matches_17.4.jsonl
#   -> CombatNet ~85% accuracy at predicting which board places higher
```

---

## Project status

| Stage | Status | Notes |
|---|---|---|
| 1. Data & Knowledge Layer | ✅ | CommunityDragon Set 17 content, shop odds, Riot match-v1 collector |
| 2. Macro Environment + placeholder combat | ✅ | Playable end-to-end PettingZoo 8-player env |
| 3. RL Agent (PPO self-play) | ✅ pipeline / 🔧 strength | Beats random; **still loses to scripted** (top-4 ~40%) — needs training at scale |
| 4. Combat surrogate | ✅ | `CombatNet` on real games (val ~0.85) via `NeuralResolver` |
| 5. Items & augments in env + hybrid surrogate | ✅ | Robust hybrid surrogate (real val ~0.88), agent ~1.5–2 placement vs 4.5 random |
| 6. Real tick-by-tick engine | 🔧 | Core shipped; ability/item/augment long-tail being filled in |
| 7. Perception + Actuation | ⏸️ optional | ⚠️ ToS — out of scope for the core |

Combat fidelity is tracked honestly in [`docs/COMBAT_COVERAGE.md`](docs/COMBAT_COVERAGE.md), and
per-entity engine support (every champion / trait / item / augment, ✅ implemented vs 🟡 partial vs
⛔ shadowed) is audited in [`docs/fiches/INDEX.md`](docs/fiches/INDEX.md).

---

## 🙌 Want to help?

**Yes — contributors very welcome.** There's a wide range of work, from self-contained data-entry
tasks to deep RL research. Start here:

- 📋 **[ROADMAP.md](ROADMAP.md)** — what's planned and where help is most valuable
- 🛠️ **[CONTRIBUTING.md](CONTRIBUTING.md)** — setup, conventions, and how to pick a first task
- 🏷️ Look for [`good first issue`](../../labels/good%20first%20issue) on the issues tab

**Good entry points by skill:**

| You enjoy… | Try… |
|---|---|
| RL / training | Scaling PPO self-play so the agent beats the scripted baseline (the #1 challenge) |
| Game knowledge + Python | Implementing item procs / augment combat logic in the engine ([coverage gaps](docs/COMBAT_COVERAGE.md)) |
| Data / APIs | Improving the datatft & Riot match collectors; set-refresh tooling |
| Performance | Vectorizing the env / engine for higher self-play throughput |
| ML research | MuZero / Gumbel-MuZero on top of the existing env |

---

## Tech stack

Python 3.11+ · PyTorch · PettingZoo · `httpx` · pydantic · custom CleanRL-style PPO ·
data from CommunityDragon + datatft + Riot `tft-match-v1`.

---

## License

[MIT](LICENSE). TFT_GOAT is an independent, fan-made project and is **not affiliated with or
endorsed by Riot Games**. Teamfight Tactics and all related assets are trademarks of Riot Games, Inc.
