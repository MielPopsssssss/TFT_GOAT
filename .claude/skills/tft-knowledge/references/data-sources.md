# Data sources — what each provides, how TFT_GOAT uses them

Three real sources feed TFT_GOAT. Keep static vs meta vs match data separate.

## 1. CommunityDragon (CDragon) — STATIC game data (source of truth)

- Raw JSON snapshot: `raw.communitydragon.org/.../cdragon/tft/en_us.json` (pinned per patch).
- Provides: champions (stats, abilities + per-star variables, traits, role), items (recipes, effects,
  tags), augments (desc, effects, **icon → tier**), traits (effects + breakpoints).
- **Filtering**: there are ~38 `setData` entries; TFT_GOAT selects the **single `TFTSet17`** entry
  (mutator) and reads ONLY its `champions/traits/items/augments`. It ignores variants like
  `TFTSet17_PVEMODE` and `TFTSet17_PAIRS` (Double Up).
- **Non-`TFT17_` prefixes are legitimate**: evergreen augments reused across sets keep their original
  apiName (e.g. `TFT6_Augment_HyperRoll`); 10 "champions" are PvE units / loot objects.
- TFT_GOAT: `data/cdragon.py`, `data/content.py::load_set` → immutable `SetContent` (Pydantic v2).

## 2. datatft — META / performance stats (complementary)

- Unofficial API: `POST https://api.datatft.com/data/explore/list`, body
  `{version, tier:"all", filterTargetType}`. Nomenclature: **hero**=champion, **equip**=item,
  **trait**=trait, **hex**=augment.
- Provides **only meta stats**: avg placement, top4%, win%, play count, best items per champion,
  per-star performance, item builds, trait performance. **No static data** (no HP/AD/abilities/
  recipes/tiers). The augment (`hex`) data is **empty** via the public API.
- "Verify datatft matches our data" therefore means **roster consistency only** (every champion/item/
  trait datatft tracks must exist in our content). Patch 17.4: champions 64/64, traits 41/41, items
  150/151 (only `EkkoArtifact` differs — a god artifact outside `setData.items`).
- TFT_GOAT: `data/datatft.py` (snapshot hero+trait+equip), `scripts/verify_datatft.py` (cross-check),
  `data/stats_models.py` (`UnitStat`/`TraitStat`/`ItemStat`/`MetaStats`).

## 3. Riot TFT match-v1 — real match data

- Official API (needs `RIOT_API_KEY`, never committed; used via env var only).
- Provides real high-elo match timelines/results for calibration and (future) imitation signal.
- TFT_GOAT: `data/matches/` snapshots.

## Practical rules

- **Static fact** (a stat, recipe, ability value, augment tier) → CDragon / our `SetContent`.
- **"What's strong / best items / placement"** → datatft meta stats.
- **Real game behavior at scale** → Riot match-v1.
- Re-pin snapshots each patch; all hand-coded combat content (abilities/item procs/augment logic)
  must be re-verified per patch (see `docs/COMBAT_COVERAGE.md`).
