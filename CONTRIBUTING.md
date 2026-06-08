# Contributing to TFT_GOAT

Thanks for your interest! 🐐 This project welcomes contributions of all sizes — from fixing a single
augment's combat logic to scaling up the RL training loop. This guide gets you productive fast.

## TL;DR

```bash
git clone https://github.com/<owner>/TFT_GOAT.git
cd TFT_GOAT
python3.11 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest -q          # 113 tests should pass
```

Then pick a task from the [ROADMAP](ROADMAP.md) or an issue tagged `good first issue`, open a draft
PR early, and ask questions in the issue/PR thread.

## Project layout

```
src/tft_goat/
  data/        # CommunityDragon + datatft + Riot API content layer (immutable, versioned per patch)
  env/         # PettingZoo macro environment (economy, shop, items, augments, rounds)
  agent/       # PPO self-play, scripted opponent, evaluation
  surrogate/   # CombatNet neural resolver (P(win | A, B))
  engine/      # Real tick-by-tick combat engine (hex grid, abilities, item procs, traits)
  scripts/     # Entry points: train, train_surrogate, collect_matches, scrape_datatft, ...
tests/         # pytest suite — every subsystem is covered
docs/          # ARCHITECTURE.md, COMBAT_COVERAGE.md
```

## How to pick a first task

We sort contributions by the skill they exercise:

- **Game knowledge + Python (great first PR):** implement a missing **item proc** or **augment
  combat effect** in the engine. [`docs/COMBAT_COVERAGE.md`](docs/COMBAT_COVERAGE.md) has the exact
  list of what's done vs. using a default effect. These tasks are self-contained and verifiable.
- **Data / APIs:** improve the `datatft` and Riot `match-v1` collectors, or the set-refresh tooling.
- **Performance:** vectorize the env/engine to raise self-play throughput.
- **RL / research:** the headline challenge — train PPO at scale so the agent beats the **scripted**
  opponent (it currently doesn't), or prototype MuZero on top of the env.

If unsure, open an issue describing what you'd like to work on and we'll point you at the right spot.

## Ground rules (from the codebase conventions)

1. **Real data is the source of truth.** Champion/item/trait/augment values come from
   CommunityDragon, *not* hand-typed numbers. If you add content, wire it to the data layer.
2. **Be honest about fidelity.** If an effect is approximated, mark it with a `# approx:` comment and
   update `docs/COMBAT_COVERAGE.md`. We document what we *don't* faithfully simulate.
3. **Immutable data structures.** Build new objects; don't mutate shared state in place.
4. **Small, focused modules.** Prefer many small files (one domain each) over large ones.
5. **Tests are required.** There's an anti-typo guard (`test_all_registry_apis_exist_in_content`) and
   per-subsystem tests. New combat logic must come with a test that executes it.
6. **Pin verified numbers.** When you verify a value against the live patch, add/extend a pinned test
   (see the `*_verified_patch_*` tests) and cite your source in the test or PR.

## Workflow

1. **Fork** and create a branch: `git checkout -b feat/short-description`.
2. **Write a test first** when adding behavior (RED → GREEN → refactor). The suite must stay green:
   `python -m pytest -q`.
3. **Commit** using [Conventional Commits](https://www.conventionalcommits.org/):
   `feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`, `perf:`.
4. **Open a PR** (draft is fine) with: what you changed, why, how you verified it, and any source
   links for game-data claims.
5. A maintainer reviews; address feedback; we merge. 🎉

## Verifying combat / engine work

```bash
python -m pytest tests/test_engine.py -q                 # engine + ability registry
python -m tft_goat.scripts.random_rollout                # full game smoke test
python -m tft_goat.scripts.train_surrogate --source engine --pairs 2000   # surrogate vs engine
```

## Code of conduct

Be kind, be constructive, assume good faith. We're here to learn and build something fun together.
Harassment or hostility isn't welcome.

## Questions?

Open a [Discussion](../../discussions) or an issue. No question is too small — if the setup docs
didn't work for you, that's a bug in *our* docs and we want to hear about it.
