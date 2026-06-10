# Promotion kit — where & how to post

Ready-to-paste posts to recruit contributors. The repo link is already filled in
(<https://github.com/MielPopsssssss/TFT_GOAT>). Read each community's rules first — most allow
open-source/self-projects but some require a specific flair, a weekly thread, or a minimum-karma account.

---

## Where to post (ranked)

| Forum | Audience | Notes / etiquette |
|---|---|---|
| **r/MachineLearning** | ML researchers/engineers | Use the **`[P]` (Project)** flair. High bar — lead with the *technical* angle (RL surrogate, self-play). |
| **r/reinforcementlearning** | RL practitioners | Best fit for the "agent loses to scripted, help me scale it" framing. Very welcoming to real envs. |
| **r/CompetitiveTFT** | Hardcore TFT players | Check the **self-promotion / content rules** and pinned mod posts first; may need a flair or a mod OK. Lead with the TFT angle. |
| **r/learnmachinelearning** | ML beginners/students | Great for recruiting first-time contributors (the "good first issue" tasks). |
| **r/Python** | Python devs | Post on the weekly **"Showcase Saturday/Sunday"** thread to respect rules. |
| **Hacker News** (`Show HN:`) | Generalist devs | Not Reddit, but high signal. Title: `Show HN: TFT_GOAT – an RL agent that learns Teamfight Tactics`. Post, then add a first comment with context. |
| **r/TeamfightTactics** | General TFT | Bigger but more casual; check self-promo rules. |
| **Discords** | Direct reach | TFT competitive servers, RL/ML servers (e.g. EleutherAI-style), and "open source" project channels. Drop it in #projects/#showcase channels. |
| **r/leagueoflegends** | ⚠️ usually **no** | Strict self-promo rules; likely removed. Skip unless you know the rules. |

**General etiquette:** post to one or two communities at a time (not all at once), reply to every
comment, don't repost the same text within a short window, and be upfront that it's your project and
you're looking for contributors.

---

## Variant A — ML / RL subreddits (r/MachineLearning `[P]`, r/reinforcementlearning)

**Title:** `[P] TFT_GOAT — an open-source RL agent that learns Teamfight Tactics via self-play (and currently loses to a scripted bot — help wanted)`

> I've been building **TFT_GOAT**, an open-source attempt to train a Teamfight Tactics agent with
> reinforcement learning + self-play — roughly the approach **Riot described at GDC 2024**: learn the
> macro game with RL, and resolve combat with a **learned neural surrogate** instead of a brittle
> hand-written simulator.
>
> **The setup:**
> - A from-scratch **PettingZoo 8-player environment** (economy, leveling, shop RNG, items, augments,
>   rounds) — imperfect information, multi-agent.
> - **Three swappable combat resolvers** behind one interface: a heuristic, a neural surrogate
>   `P(win | board A, board B)`, and a **real tick-by-tick engine** (hex grid, real champ/item/trait
>   stats, abilities, CC) used as ground truth.
> - The surrogate (`CombatNet`) hits ~0.85–0.88 val accuracy predicting which board wins, trained
>   either on real challenger games (Riot match-v1) or on the engine itself.
> - Custom CleanRL-style **PPO with action masking + self-play**, evaluated vs. random *and* a
>   scripted opponent.
>
> **The honest part / where I need help:** the pipeline is complete and the agent crushes random,
> but it **still loses to the scripted opponent** (top-4 ~40%). The headline open problem is
> *training at scale* — bigger rollouts, tuning, maybe a curriculum. There's also a long tail of
> game logic to fill in, env vectorization for throughput, and a MuZero stretch goal.
>
> Everything is data-driven (CommunityDragon), MIT-licensed, 147 tests, with a documented roadmap
> and `good first issue`s. Combat fidelity is tracked openly — I document exactly what's faithfully
> simulated vs. approximated.
>
> Repo + roadmap: **https://github.com/MielPopsssssss/TFT_GOAT**
>
> Would love feedback on the surrogate-vs-engine approach and the self-play setup — and
> contributors of any level are very welcome.

---

## Variant B — TFT subreddits (r/CompetitiveTFT, r/TeamfightTactics)

**Title:** `Building an open-source AI that learns to play TFT (Set 17) — looking for contributors who know the game`

> Hey all — I'm building **TFT_GOAT**, an open-source AI that learns to play TFT through
> self-play / reinforcement learning (the same high-level approach Riot talked about at GDC 2024).
>
> It already simulates a full **8-player Set 17 game** — economy, interest, leveling, shop odds,
> items, augments (with real tier odds + reroll), rounds and player damage — and has a **real
> tick-by-tick combat engine** with the actual champion/item/trait stats and abilities from
> CommunityDragon. I've been obsessive about getting the *numbers* right and documenting honestly
> what's faithfully simulated vs. approximated.
>
> **Where TFT knowledge would massively help:**
> - Implementing the remaining **item procs** and **augment combat effects** (each one is a small,
>   self-contained task with a clear list of what's left).
> - Sanity-checking mechanics against the live patch (XP/streak tables, trait breakpoints, Realm of
>   the Gods).
>
> You don't need to be an ML person — a lot of the most valuable work is "you know exactly what this
> augment/item does in combat, help me encode it." It's MIT-licensed with a roadmap and beginner
> tasks tagged.
>
> Repo: **https://github.com/MielPopsssssss/TFT_GOAT**
>
> Happy to answer anything about how it models the game.

---

## Variant C — short (Discord / r/Python showcase / HN comment)

> **TFT_GOAT** — open-source RL agent that learns Teamfight Tactics via self-play. From-scratch
> PettingZoo 8-player env, a neural combat surrogate `P(win | A, B)` trained on real games *and* on a
> tick-by-tick engine, custom PPO. Pipeline's complete but the agent still loses to a scripted
> bot — training it at scale is the open challenge. Python 3.11, PyTorch, MIT, 147 tests, roadmap +
> `good first issue`s. Contributors welcome: **https://github.com/MielPopsssssss/TFT_GOAT**

---

## After you post

- Pin the repo link and the **ROADMAP** in your first reply.
- Add a few `good first issue` GitHub issues *before* posting so newcomers have somewhere to land.
- Respond to comments quickly in the first hours — that's what drives stars and contributors.
