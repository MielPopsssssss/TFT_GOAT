# Set 17 "Space Gods" — Realm of the Gods, roster, traits

## The Realm of the Gods (replaces the carousel)

Set 17's signature mechanic; it **fully replaces the carousel**.

1. **Two gods** are chosen at random from a pool of **9** at the start of each game (same two for the
   whole lobby).
2. At each **x-4 round** (2-4, 3-4, 4-4) you choose between offerings (**Minor Blessings**) presented
   by the two gods. Picking a god's offering casts a **vote** for that god, and grants an immediate
   blessing (buff / economy / loot).
3. After **4-4**, your majority vote determines your **aligned god**.
4. At **4-7**, your aligned god grants a powerful **God Boon** — substantially stronger than any single
   item, often defining the endgame.
5. Placement-based catch-up loot is delivered on the PvE rounds.

### The 9 gods

| God | Domain | Blessing flavor |
|---|---|---|
| Soraka | Stars | Team gains 2 HP per point of missing Tactician HP |
| Yasuo | Abyss | — |
| Ahri | Opulence | Gold, XP, and rerolls (notably at 4-7) |
| Thresh | Pacts | Each stage, a random boon from any other god / mystery loot |
| Kayle | Order | Upgrades a random completed item into a **Radiant** item |
| Varus | Love | — |
| Evelynn | Temptation | — |
| Ekko | Time | — |
| Aurelion Sol | Wonders | Quests each stage in exchange for rewards |

- **God augments** (`*GodAugment*` in CDragon) and **god artifacts** (e.g. `TFT17_Item_Artifact_
  EkkoArtifact` = Ekko's Patience, `KayleArtifact`) belong to this mechanic. They exist in CDragon's
  global item list but are **NOT in `setData(TFTSet17).items`** (granted by the god mechanic, not the
  normal pool) — which is why TFT_GOAT's strict setData filter legitimately excludes them.

> TFT_GOAT currently **abstracts** Realm of the Gods as "pick 1 champion of 3" (`env/rounds.py::
> is_god_round`, `_sample_gods`). That is a simplification — the real mechanic is the
> blessing/vote/boon system above. Revisit if higher fidelity is needed.

## Champion roster by cost (73 playable, `TFT17_` prefix)

- **1-cost (15)**: Aatrox, Briar, Caitlyn, Cho'Gath, Ezreal, Leona, Lissandra, Mini Black Hole, Nasus,
  Poppy, Rek'Sai, Talon, Teemo, Twisted Fate, Veigar
- **2-cost (13)**: Akali, Bel'Veth, Gnar, Gragas, Gwen, Jax, Jinx, Meepsie, Milio, Mordekaiser,
  Pantheon, Pyke, Zoe
- **3-cost (13)**: Aurora, Diana, Fizz, Illaoi, Kai'Sa, Lulu, Maokai, Miss Fortune, Ornn, Rhaast,
  Samira, Urgot, Viktor
- **4-cost (14)**: Aurelion Sol, Corki, Karma, Kindred, LeBlanc, Master Yi, Morgana, Nami,
  Nunu & Willump, Rammus, Riven, Tahm Kench, The Mighty Mech, Xayah
- **5-cost (10)**: Apex Primordian, Bard, Blitzcrank, Fiora, Graves, Jhin, Shen, Sona, Vex, Zed

(Plus ~10 non-playable PvE units / loot objects: BlueGolem, SLIME_Crab, TrainingDummy, ArmoryKey*.)

## Traits with activation breakpoints

| Trait | Breakpoints |
|---|---|
| Anima | 3 / 6 |
| Arbiter | 2 / 3 |
| Bastion | 2 / 4 / 6 |
| Brawler | 2 / 4 / 6 |
| Challenger | 2 / 3 / 4 / 5 |
| Conduit | 2 / 3 / 4 / 5 |
| Dark Star | 2 / 4 / 6 / 9 |
| Fateweaver | 2 / 4 |
| Marauder | 2 / 4 / 6 |
| Mecha | 3 / 4 / 6 |
| Meeple | 3 / 5 / 7 / 10 |
| N.O.V.A. | 2 / 5 |
| Primordian | 2 / 3 |
| Psionic | 2 / 4 |
| Replicator | 2 / 4 |
| Rogue | 2 / 3 / 4 / 5 |
| Shepherd | 3 / 5 / 7 |
| Sniper | 2 / 3 / 4 |
| Space Groove | 1 / 3 / 5 / 7 / 10 |
| Stargazer | 3 / 4 / 5 / 6 |
| Timebreaker | 2 / 3 / 4 |
| Vanguard | 2 / 4 / 6 |
| Voyager | 2 / 3 / 4 / 5 / 6 |

Plus several **god / unique traits** at 1 unit (Bulwark, Commander, Dark Lady, Divine Duelist, Doomer,
Eradicator, Factory New, Galaxy Hunter, Gun Goddess, Oracle, Party Animal, Redeemer) — typically tied
to a single signature champion or the god mechanic.

> Roster/traits/breakpoints above are generated from the live Set 17 `setData` in TFT_GOAT
> (`load_set()`), so they regenerate automatically each patch — re-run to refresh.

Sources: official Set 17 overview, mobalytics/eloboost24 Realm of the Gods guides, TFT_GOAT content.
