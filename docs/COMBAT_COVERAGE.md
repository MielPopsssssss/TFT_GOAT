# Couverture du moteur de combat (Set 17)

État honnête de ce qui est **réellement** simulé vs ce qui utilise un effet **par défaut**.
Mis à jour à la main au fil du remplissage (PARTIE B du plan étape 6).

## Mécaniques du moteur — ✅ complètes
- Grille hexagonale (distance, déplacement, ciblage du plus proche).
- Auto-attaques, cadence = attack speed (**cap 5.0**), mitigation armure/RM, crit.
- Mana (gain par attaque + on-hit) → **cast dès mana plein, même monté en subissant des dégâts**.
- Boucliers (absorbent avant les PV), stuns (saute l'action), soins.
- **Ordre d'action randomisé chaque tick** → matchup miroir équitable (~50/50, vérifié 300 parties).
- **Placement rôle-aware** : tanks/bruisers centre-avant, carrys/casters/supports en rangées
  arrière, **carrys dans les COINS** (bords) de la backline (score rôle + tankiness + portée).
- **Ciblage / focus** : par défaut chaque unité vise l'ennemi le **plus proche** → les tanks devant
  encaissent, les carrys derrière survivent et DPS. Cible **persistante** (gardée jusqu'à la mort).
- **Dash d'assassin (Reaper)** : au début du combat, téléportation adjacent au **carry** ennemi
  (plus bas `frontline_score`, indépendant de la position → symétrique) + verrouillage de la cible.
  Miroir ~54% (résidu de parité odd-r ~3% vs baseline 51%, vs bug à 84% avant correction).
- Morts, fin de combat, départage par survivants puis PV restants.

### Bugs TFT trouvés & corrigés (audit)
- Cast ne se déclenchait que sur auto-attaque (les tanks ne castaient jamais). → corrigé.
- Pas de cap d'attack speed. → cap 5.0.
- Biais « équipe 0 agit en premier » → miroir gagné à 100% par l'équipe 0. → ordre randomisé.

## Données réelles appliquées AUTOMATIQUEMENT — ✅
- **Stats de base** des 83 champions (HP/AD/AS/armure/RM/portée/mana/crit) — data.
  - **✅ Intégrité mana vérifiée (2026-06-08)** : 63/65 jouables ont un mana de cast réel (1..300) ;
    les 2 à mana=0 (**Caitlyn**, Mini Black Hole) sont des casters **passifs légitimes** (Caitlyn =
    headshot 15% sur auto-attaque, vérifié patch — pas un bug, le moteur ne la mana-caste jamais).
    🟡 *Limite* : le passif de Caitlyn (headshot) n'est pas modélisé (elle ne fait qu'auto-attaquer).
    Pins : `tests/test_champion_data.py`.
  - **✅ Ranges d'attaque vérifiés (2026-06-08)** : buckets réels 1=mêlée(33)/2(3)/4(19)/6=longue
    portée(9, ex Jhin/Ezreal) ; range 0 = Mini Black Hole (fake). Pin : `test_attack_ranges_are_real_and_sane`.
- **Star scaling** HP/AD ×1.8 par étoile.
- **Effets de stats des items** (`item.effects` numériques) — data, quand l'identité de l'objet
  est connue. ⚠️ L'env ne traque pour l'instant qu'un *compteur* d'objets → bonus générique
  (identités d'objets dans l'env = à faire, PARTIE C).
- **Bonus de stats des traits** actifs (armure/PV/RM/AS) — data, sous-ensemble « stat ».

## Long tail hand-codé — 🔧 en cours (PARTIE B)
| Catégorie | Implémenté | Total | Défaut utilisé pour le reste |
|---|---|---|---|
| **Sorts de champions** | **68 / 68** (cost 1-5) ✅ | 68 | — (les ~15 unités PvE/minions sont no-op) |
| **Procs d'items** (effets spéciaux) | **~22** (CS 6, on-attack 16, on-cast 1) ✅ | 55 complétés | les autres = stats seules / emblèmes (pas de proc) |
| **Augments (logique de combat)** | **67 / 276** ✅ | 276 | les ~209 autres = éco/utilité/loot (no-op correct) |
| Effets de traits non-stat (invoc./exécution/bouclier conditionnel) | 0 | plusieurs | ignorés |

### Câblage — ✅ branché dans l'env
- **Sorts + traits-stat** : actifs dans tout combat moteur.
- **Procs d'items** : l'env assigne une **identité d'objet réelle** à l'EQUIP (`BoardUnit.item_apis`)
  → les procs s'activent en combat moteur. (Choix d'objet = aléatoire parmi les complétés réels —
  approximation du choix joueur ; à raffiner via un vrai système composants→objet.)
- **Augments de combat** : l'env stocke `PlayerState.chosen_augments` (vrais apiNames) et les passe
  au resolver (`augments_a/b`) → effets appliqués en combat moteur. Vérifié en partie réelle.
  - **🐛 BUG CORRIGÉ — mitigation des dégâts joueur (2026-06-08)** : `_apply_damage` réduisait les
    dégâts JOUEUR via `augment_power` (~25% moy, jusqu'à 45%). **Faux** : un augment renforce le board
    (proba de victoire, via le resolver), il ne réduit pas les dégâts subis à la défaite. Ça gonflait
    les parties : **stage final moyen 7.8 → 6.9, médiane 8-2 → 7-2** (réaliste). `augment_power` reste
    dans l'observation de l'agent (non mécanique pour l'instant). NB : le HeuristicResolver v0 ignore
    les augments ; leur vrai effet combat passe par le moteur. Pin : `tests/test_game_length.py`.

### Fact-check effectué ✅ (data CommunityDragon = vérité primaire + wiki en secondaire)
Passe de vérification par 8 agents (un par lot, accès web). Résultats :
- **Augments : 67 → 74** (faux négatifs ajoutés : Crash Test Dummies stun, Cursed Crown, Electrocharge I,
  Healing Orbs, Little Buddies, Side Effects, Climb The Ladder I).
- **Procs d'items : 23 → 26** (ajouts : Ionic Spark shred, emblèmes Brawler/Voyager combat-start).
- **Bug récurrent corrigé** : AP en `%` appliqué comme **flat** (Kayle, Stand United, Climb The Ladder II,
  Tour of the Galaxy, Hold the Line) → corrigé en multiplicateur.
- **2 imports interdits** (`..simulate`) corrigés.
- **⚠️ Renommages d'items Set 17 confirmés** (les apiNames réutilisent des noms classiques mais sont
  d'AUTRES items ce set) — le code était bien aligné sur l'effet Set 17 réel :
  `RunaansHurricane`=**Kraken's Fury**, `RedBuff`/`RapidFireCannon`=**Sunfire/Red Buff**,
  `Leviathan`=**Nashor's**, `PowerGauntlet`=**Striker's Flail**, `SpectralGauntlet`=**Evenshroud**,
  `GuardianAngel`=**Edge of Night**, `FrozenHeart`=**Protector's Vow**, `StatikkShiv`=**Void Staff**,
  `MadredsBloodrazor`=**Giant Slayer**, `Redemption`=**Spirit Visage**, `HextechGunblade`=heal allié.

### Hooks moteur ✅ (avec vraies valeurs, apiNames vérifiés présents dans la data)
- **on-being-hit** (`ITEM_ON_DAMAGED`) → **Bramble Vest** (reflet 100 magie).
- **on-tick ~1/s** (`ITEM_ON_TICK`) → **Dragon's Claw** (1.25%/s PV max), **Spirit Visage** (2%/s PV manquants).
- **seuil de PV** (`ITEM_HP_THRESHOLD`, 4) → **Sterak's Gage** (60% → bouclier 40%), **Edge of Night**
  (60% → soin 20% manquants + bouclier), **Protector's Vow** (40% → bouclier 20%), **Zhonya's Paradox**
  (40% → invuln approx). *Edge of Night & Protector's Vow déplacés de combat-start → seuil (vrai comportement).*
- **durability** (`CombatUnit.incoming_reduction`) → **Steadfast Heart** (−15% dégâts subis).
- **damage amp** (`CombatUnit.damage_amp`) sur tous les dégâts sortants.
- **crit des sorts** : IE / Jeweled Gauntlet → `can_ability_crit` (autos crittent toujours à 25%).
- **revive** (`ITEM_REVIVE`) : mécanisme moteur en place et testé. **Aucun item standard Set 17 ne
  ressuscite** (GA est devenu Edge of Night = intargetable+soin ; le revive n'existe que sur des items
  hors-Set-17 / artefacts). Registre vide pour Set 17, prêt si un tel item apparaît.
- **Vrai système composants→objet** (`env/items.py`) : 10 composants, 55 recettes réelles ; l'EQUIP
  combine 2 composants → l'objet complet exact. **✅ VÉRIFIÉ (2026-06-08)** : 10 composants,
  C(10,2)+10 = **55 recettes**, chaque sortie = vrai objet distinct existant, combos canoniques
  exacts (BF+BF=Deathblade, Rod+Rod=Rabadon's, Tear+Tear=Blue Buff, Belt+Belt=Warmog's). Pins :
  `tests/test_item_recipes.py`.

### Probabilités d'événements — audit expert TFT (✅ tiers d'augments corrigés)
Un agent expert TFT indépendant a vérifié les **proba de chaque événement** sur une partie rejouée.
- **🔴 → ✅ Tiers d'augments (CRITIQUE, corrigé)** : avant, `_sample_augments` tirait **uniformément**
  parmi les 276 augments, **sans aucune logique de tier** (silver/gold/prismatic identiques aux 3
  rounds). Désormais :
  - Tier lu depuis l'**icône CDragon** (`data/augment_tiers.py`, romain `_I/_II/_III` ou chiffre
    `1/2/3` avant le `.tex` = la bordure que Riot affiche) → champ `Augment.tier`. **276/276 résolus**.
  - **Vraies odds par round** (`AUGMENT_TIER_ODDS`, source metatft/tftodds), un tier tiré par slot :
    | Choix | Round | Silver | Gold | Prismatic |
    |---|---|---|---|---|
    | 1er | 2-1 | 28% | 62% | 10% |
    | 2e  | 3-2 | 35% | 45% | 20% |
    | 3e  | 4-2 | 6%  | 74% | 20% |
  - Distribution vérifiée empiriquement (20k tirages) : écart < 0.5% vs odds réelles.
  - **17 God Augments** (`*GodAugment*`, boons Realm of the Gods) **exclus** du pool régulier →
    pool de 259 (silver 67 / gold 124 / prismatic 68). Pas de doublon dans une offre ni entre rounds.
- **✅ Offre par joueur + reroll** : chaque joueur reçoit une offre **aléatoire et différente**
  (3 augments tirés indépendamment), **doit en choisir 1**, et peut **reroll** l'offre pour **2 gold**
  (`REROLL_AUGMENT`, action 42 ; re-tire toute la ligne selon les odds du round, légal si gold≥2).
  Scripted : reroll si l'offre est tout-silver et gold suffisant. NUM_ACTIONS 42→43.
- **✅ Timing d'augments** : rounds 2-1 / 3-2 / 4-2 — confirmé correct.
- **✅ Interest (VÉRIFIÉ vs patch 17.4, 2026-06-08)** : +1/10 gold, cap +5 à 50 gold — unanime
  (wiki LoL + op.gg + lolchess). Pin : `tests/test_economy.py::test_interest_boundaries_verified_patch_17_4`.
- **🟡 Streak gold (DISPUTÉ à streak=3)** : code 2→+1, 3→+2, 4→+2, 5+→+3 ; deux sources suggèrent
  3→+1 (et le wiki une table encore différente). Extractions web non fiables (SPA, colonnes
  historiques) → conservé tel quel, **ne pas flipper sans patch notes officiels**. Réalisme éco seul.
- **🟡→✅ partiel Table XP (AUDIT 2026-06-08)** : confirmés vs patch 17.4 → niveau max **10**,
  2 XP/round, achat 4 XP/4 gold, increments L1→L6 = **2,2,6,10,20,36** (code = tft.ninja = wiki).
  **Top-3 non résolu** : code 56/80/100 (L7→8,8→9,9→10) vs tft.ninja 48/72/84 (anciens sets) ;
  sources officielles inaccessibles → conservé tel quel, **ne pas flipper sans patch notes officiels**.
  Impact realisme seul. Pins : `tests/test_economy.py::test_xp_*`.
- **✅ Shop odds (VÉRIFIÉ vs patch 17.4, 2026-06-08)** : désaccord L7/8/9 tranché. **op.gg ET
  esportstales concordent exactement** avec la table (L7=19/30/40/10/1, L8=17/24/32/24/3,
  L9=15/18/25/30/12). tftactics divergeait mais sa ligne L7 sommait à **95** (stale/invalide). Pool
  sizes 30/25/18/10/9 confirmés (la « divergence » d'un résumé web confondait copies-par-champion
  et nombre-de-champions-distincts). Pin : `tests/test_odds.py::test_disputed_levels_match_verified_patch_17_4`.
- **🟡 Realm of the Gods** : modélisé « 1 champion parmi 3 » (directive utilisateur). Le vrai mécanisme
  = **Minor Blessing** + vote d'alignement → boon 4-7.
  - **✅ Timing corrigé (2026-06-08, vs patch 17.4)** : `is_god_round` ne se déclenche plus qu'aux
    **2-4, 3-4, 4-4** (3 votes), au lieu de **chaque** x-4 (bug : 5-4/6-4/7-4 déclenchaient à tort).
    Confirmé eloboost24 + mobalytics + bunnymuffins. Pin : `tests/test_rounds_schedule.py`.
  - **✅ Modèle vote→alignement→boon (2026-06-08)** : `data/gods.py` expose les **9 dieux réels** +
    leurs **17 God Boons** (augments tier="god" CDragon, double-confirmé skill+data). Au départ,
    **2 dieux tirés pour le lobby** (`choose_lobby_gods`, `GameState.lobby_gods`). Chaque offrande
    (2-4/3-4/4-4) est associée à un dieu → la prendre **vote** (`god_offer_gods`, `god_votes`). Au
    4-4, la **majorité fixe le dieu aligné** et tire son **God Boon réel** (`aligned_god`, `god_boon`).
    Pins : `tests/test_gods.py`.
  - **✅ Octroi du God Boon au 4-7 (2026-06-08)** : `is_god_boon_round` (4-7 uniquement, vérifié
    eloboost24/mobalytics) ; au 4-7 le boon réel du dieu aligné est **délivré dans le pipeline
    d'augments** (`chosen_augments` → resolver), idempotent. Pins : `tests/test_gods.py`.
  - **✅ Robustesse du flux de vote (2026-06-10, review adversariale)** : (1) une action illégale
    pendant une offre forcée est coercée vers la **première action légale** (plus jamais vers un
    PASS aveugle qui sautait le vote) ; (2) une offre de dieu non consommée est **purgée à chaque
    round** (plus de votes fantômes par fuite) ; (3) l'alignement se déclenche au **3e vote** (compte,
    pas numéro de round) avec **filet au 4-7** si un vote a été manqué ; (4) l'offre des dieux est
    tirée du **roster jouable du pool** (plus d'unité PvE offerte puis refusée silencieusement).
    Pins : `tests/test_gods.py` (4 tests de régression).
  - **Restant (sous-étapes)** : (1) **effets de combat des god augments** — même long-tail que les
    augments réguliers : **6/17 God Boons seulement** sont dans le registre `augments_set17` (les
    11 autres = no-op silencieux, comme les ~202 augments non implémentés — tracé `TODOS.md` P2).
    Effets ambigus (clés hashées, quêtes/loot) → non devinés. (2) effets des Minor Blessings,
    (3) artefacts de dieu.

### Vérification datatft ↔ contenu (✅ rosters cohérents)
datatft = **couche META uniquement** (place moyenne, top4%, win%, count, best items par champ/trait/
objet, perf par étoile). **Aucune donnée statique** (HP/AD/sorts/recettes/tiers) ; le champ augments
(`hex`/`hexs`) est **vide côté API**. La donnée statique reste CommunityDragon. Scraper étendu
(`data/datatft.py` : hero+trait+**equip**), vérif `scripts/verify_datatft.py`. Résultat patch 17.4 :
- **Champions** : 64/64 suivis existent chez nous ✅ (on en a 19 de plus, non-meta : PvE/loot).
  - **✅ BUG CORRIGÉ — pool de boutique pollué (2026-06-08)** : 3 unités PvE/evergreen
    (`TFT_BlueGolem`, `TFT9_SLIME_Crab`, `TFT_TrainingDummy`) ont cost=1 dans setData et étaient
    **dans le pool achetable** → 1-cost à **18 au lieu de 15** + un « Training Dummy » pouvait
    apparaître en boutique. Fix : `Pool` ne garde que le préfixe `TFT<set>_`. Roster du pool
    désormais **exactement** le roster vérifié (15/13/13/14/10 = 65). Pin :
    `tests/test_shop_pool.py::test_real_pool_roster_matches_verified_set17`.
- **Traits** : 41/41 ✅.
  - **✅ Breakpoints vérifiés (2026-06-08)** : pour les 23 traits standard, la data CDragon
    concorde **exactement** avec la table du skill tft-knowledge (double source indépendante).
    Pin : `tests/test_traits.py::test_set17_trait_breakpoints_match_real_data`.
  - **🟡 Stargazer = cas spécial** : breakpoints **variables par constellation** (ex: Boar 3/4/5/6) ;
    le moteur utilise les breakpoints du trait de base (3,5,7,8,9,10) — approximation documentée
    (la constellation active n'est pas modélisée). Pin : `test_stargazer_is_constellation_variable`.
  - **✅ Cohérence champion↔trait (2026-06-08)** : tout trait s'active depuis le roster (1er palier
    ≤ nb de membres) ; les hauts paliers (Dark Star 9, Space Groove 10…) via emblèmes = design
    correct ; 12 traits uniques/god (1 champ, palier 1). Pin :
    `tests/test_traits.py::test_every_trait_first_breakpoint_reachable_from_roster`.
- **Objets** : 150/151 ✅. Seul absent : `TFT17_Item_Artifact_EkkoArtifact` (+ KayleArtifact) —
  **artefacts de dieu** présents dans CDragon mais **hors `setData.items`** (octroyés par Realm of
  the Gods, pas dans le pool normal). Notre filtre `setData` est correct ; edge case documenté.

### Garde-fou : test d'existence
`tests/test_engine.py::test_all_registry_apis_exist_in_content` — échoue si un item/augment référencé
dans un registre n'existe pas dans la vraie data (anti-typo permanent).

### Audit moteur (4 agents) — bugs CORRIGÉS
- **C1 off-by-one d'étoile** (le pire) : `ability_value` lisait `vals[star-1]` mais le format CDragon
  est `[placeholder, 1★, 2★, 3★, 4★]` → 1★ lisait l'index 0 (souvent 0). Corrigé → index par `star`.
  (Jinx 1★ ADDamage 3→**29**.)
- **Sorts AD mal scalés** (batch_2, batch_4) : `ad×valeur` au lieu de `ad×valeur/100` (100× trop). Corrigé.
- **Biais géométrique odd-r** : team0 (rangée 3 impaire) vs team1 (rangée 4 paire) → géométrie
  asymétrique amplifiée par les sorts (miroir tombait à 14%). Corrigé : team1 = **rotation 180°** de
  team0 → miroir **~49%**.
- **Mouvement** : cible **persistante** (gardée jusqu'à sa mort, fini le jitter de retarget), tie-break
  **aléatoire**, **sidestep** (ne reste plus bloqué derrière les alliés), `MOVE_INTERVAL` 0.25→0.5
  (multiple exact du tick, ~2 hex/s réaliste).
- **HP_THRESHOLD** : garde `max_mana` boguée retirée. **Double-wipe** : tie-break aléatoire (anti-biais).

### Backlog audit — ✅ TRAITÉ (ancré data, cumuls corrects)
1. **Système de traits réécrit** (`trait_effects`) : mapping explicite des vraies clés (BonusArmor/MR,
   ADAP, AS, DR, DamageAmp, Resists→armure+RM…), **team-wide** vs porteurs, **cumul** (durability
   multiplicatif). Vérifié : Bastion → +armure/+RM (dont team-wide). Clés non-stat/{hex} ignorées.
2. **Mana-lock 1s post-cast** + **mana-sur-dégâts** = 1% pré-mit + 7% post-mit, plafonné (42.5).
   - **✅ Constantes combat auditées (2026-06-08)** : crit **25% / ×1.4**, **AS cap 5.0**, star ×1.8,
     mana-lock 1s — confirmés (wiki Critical strike + skill). Pins : `tests/test_combat_constants.py`.
   - **🟡 Modèle mana** : code = 10/attaque (tous) + 1%/7% (tous), cap 42.5 (= réf skill, modèle
     moderne). La page wiki décrit un modèle **par rôle** (10/7/5) + tanks-only 1%/3% = **historique** ;
     non flippé sans confirmation officielle Set 17 (réalisme de cadence de cast).
3. **Items** : **omnivamp** (champ, soigne sur dégâts infligés, additif), **Grievous Wounds**
   (`apply_grievous`, max actif), **ManaRegen** (champ, /s), **durability multiplicative**
   (`add_durability`), **boucliers à durée** (expirent + s'empilent), **sunder/shred** (`ctx`, max actif).
4. **Dégâts au joueur = vraie formule TFT** : `base_stage + 1 × (nb survivants ennemis)`, base réelle
   Set 17 {2-1:2, 3:5, 4:8, 5:10, 6:12, 7+:17}, **plat 1/unité** (PAS pondéré étoile). **✅ RE-VÉRIFIÉ
   vs patch 17.4 (op.gg, 2026-06-08)** : table et per-unité confirmés exactement. Pin :
   `tests/test_rounds_schedule.py::test_player_damage_base_table_verified_patch_17_4`.
   Corrige les parties trop longues (finissaient toutes à 7-2 → maintenant ~6-5).
5. **Mécaniques ajoutées** : windup d'attaque, **silence** (no-cast), **disarm** (no-attack),
   **untargetable** (exclu du ciblage), shred/sunder réels.

### Limites restantes (documenté)
- **Summons** non modélisés (pas de nouvelles unités en cours de combat).
- Trait effects « EnhancedTeamwide » conditionnels appliqués sans condition (léger sur-bonus).
- Heuristique %/flat des stats de traits (valeur > 1 = pourcentage) ; ICD du reflet Bramble ignoré ;
  invuln/untargetable approximés ; pas de sudden-death (départage par survivants puis PV).

### Sorts : implémentés mais APPROXIMÉS (honnêteté)
Les 68 sorts utilisent les **vraies variables data** (dégâts/boucliers/stuns/heals scalés par
étoile) et l'effet **dominant** de la description. Les mécaniques non exprimables par l'API moteur
sont approximées (commentaire `# approx:` dans le code) :
- dashes / sauts / unités intargetables → traités comme dégâts à la cible
- skillshots en ligne / cônes → AoE autour de la cible (`enemies_in_radius`)
- invocations → dégâts/buff équivalents
- % PV max / exécutions → `deal_true(target.max_hp × frac)`
- multi-hits / multicasts → un nuke unique plus gros
Test anti-régression : `tests/test_engine.py::test_all_set17_abilities_execute` (les 68 tournent).

### Réalisme du déroulé de partie — ✅ audité (2026-06-08)
- **Longueur** : après fix de la mitigation augment, stage final moyen **6.9**, médiane **7-2** (réaliste).
  Pin : `tests/test_game_length.py::test_average_game_length_is_realistic`.
- **Progression de niveau** : courbe niveau-par-stage **fidèle** au vrai TFT (S2≈3.8, S3≈5.7, S4≈6.7,
  S6≈7.9, S7≈8.3 — bandes réelles respectées) même en jeu aléatoire → éco/XP correcte. Pin :
  `test_level_progression_matches_real_tft`.
- **Streaks** : séries victoire/défaite se forment (max moy ±4, jusqu'à ±12) et le **bonus d'or de
  streak est actif ~48%** des observations joueur → mécanisme exercé et réaliste. (Tiers déjà pinés :
  `test_streak_bonus_tiers`.)
- **Distribution des survivants** (→ dégâts joueur) : moy ~1.7, médiane 1, étalée 1→7 (combats
  serrés majoritaires, blowouts occasionnels). `survivors = round(board × marge)` — déterministe
  par matchup, varie selon l'adversaire. Réaliste. Pin :
  `test_combat.py::test_survivors_bounded_by_winning_board_with_variance`.
- **Cohérence macro placement↔progression** : meilleur placement ⇒ niveau plus haut (place 1 ≈ 8.4,
  place 8 ≈ 7.7, gradient monotone) — la boucle combat→survie→progression est cohérente. Pin :
  `test_better_placement_correlates_with_higher_level`. (NB : corrélation force-board(S5)↔placement
  = +0.15, faible mais positive ; atténuée par le churn d'achat/vente du jeu aléatoire, pas un bug.)
- **🟡 Or thésaurisé + 1ère mort tardive (stage 5.2 vs ~3-4)** : artefacts du **jeu aléatoire** qui
  ne dépense pas (or moy 115 / max 250 à S7 vs ~10-50 réel). L'éco est **correcte** : interest plafonné
  à 5, revenu/round borné à 13 (base 5 + interest 5 + streak 3) — pas de runaway. Pins :
  `test_interest_boundaries_verified_patch_17_4`, `test_round_income_is_bounded_no_runaway`.
- **🟡 Boards sous-remplis (2-4 unités vs cap = niveau)** : artefact du **jeu aléatoire**, PAS un bug.
  Preuve (audit) : l'action FIELD est **légale et fonctionnelle** (prise 21% quand dispo ; mécaniques
  `test_field_unit_to_board` + `test_buy_from_shop` vertes), board_cap = niveau (place pour ~8). Le vrai
  limiteur : les survivants n'ont que ~3.7 unités TOTALES (board 2 + bench 1.7) à niveau 8 → le random
  **sous-achète** (achats/ventes aléatoires). Un agent entraîné field plein. Documenté, non corrigé.

### Cohérence en jeu JOUÉ (agent PPO entraîné) — ✅ 2 itérations × 500 parties (2026-06-09)
Boucle « 500 parties → vérif cohérence → correction » avec l'agent PPO long (`runs/ppo_long`).
- **Itération 1 (6 invariants structurels)** : TOUT COHÉRENT à 500 parties. Longueur (stage 7.0),
  placements = permutation 1..8, **équité sièges 4.30–4.68** (le FAIL à 30 parties était du bruit),
  gradient board top>bottom, agent fielde (board top4 7.1), board≤cap. Lock : `tests/test_coherence.py`.
- **Itération 2 (3 invariants de comp)** : TOUT COHÉRENT. Boards gagnants = **3.19 traits actifs**
  (vraies synergies), **coût moyen 1.74** (pas que du 1-cost). Le check « méta-alignement » a été
  **re-diagnostiqué** : comparer top/bottom en self-play est mal posé (comps homogènes) et viser la
  haute méta n'est pas requis (board_strength récompense coût×étoile×traits) → c'est de la **qualité
  d'agent** (agent 0.965 vs roster 0.998), PAS une incohérence sim. Remplacé par un vrai test de
  cohérence : l'ancrage datatft influence bien la force de board (`test_combat.py::
  test_datatft_meta_coherently_affects_board_strength`).
- **Itération 3 (éco/étoiles/items en jeu joué)** : ✅ items équipés (top4 1.2 → mécanisme d'items
  fonctionne en jeu). **Éco + étoiles re-diagnostiquées qualité d'agent** : le PPO (300 it) thésaurise
  (or ~270) et sous-star (max-star 1.42). **Preuve rigoureuse que ce N'est PAS un bug sim** : l'agent
  **scripté** (heuristique) atteint or ~**52** et max-star ~**1.90** sur le même sim → la dépense
  (buy/reroll) et la combinaison (2-star) fonctionnent ; le PPO est juste sous-entraîné. Lock de la
  *capacité* du sim : `tests/test_coherence.py::test_sim_supports_realistic_economy_and_starring_via_scripted_agent`.
- **Conclusion** : 3 itérations × 500 parties, **0 bug simulateur**. Tous les écarts (méta-alignement,
  thésaurisation, sous-starring) sont de la **qualité d'agent PPO** (sous-entraîné), prouvés non-sim
  via l'agent scripté. Le simulateur est **cohérent de bout en bout**. Harnais : `scripts/check_coherence.py`
  (PASS/FAIL = cohérence sim ; INFO = qualité d'agent). Prochain levier réel = **plus d'entraînement**.

### Réalisme vs datatft — ✅ diagnostic (2026-06-08)
Validation que l'**EngineResolver** est directionnellement réaliste, mesurée contre la meta datatft.
- **Méthode** (`scripts/realism_vs_datatft.py`) : core de 6 unités partagé + 1 carry varié (impact
  marginal → win rates étalés), contre un board baseline fixe ; corrélation de rang (Spearman)
  entre win rate moteur et `-avg_place` datatft, par coût. ⚠️ Diagnostic, pas preuve : l'avg_place
  datatft est confondu par playrate/coût/utilité.
- **Résultat (5-cost)** : **Spearman ≈ +0.57** — le moteur s'aligne globalement (Jhin/Sona, top
  datatft, dominent ; pires datatft perdent).
- **Écarts = limites déjà documentées** : les unités d'**utilité/CC/summon** (Bard datatft 4.01 mais
  win 0.36 ; Blitzcrank hook) sont **sous-évaluées** par le moteur car leur valeur réelle vient de
  l'utilité (summons/buffs/hook) approximée en dégâts bruts. Cohérent avec « Summons non modélisés »
  et « sorts approximés » — **pas un bug caché**.
- **Garde-fou** : `tests/test_realism.py` (corrélation > 0.2 + carry datatft-top domine) — détecte une
  régression qui inverserait/casserait la fidélité.

## Conséquence
Stats + sorts = désormais **réels** (avec approximations documentées). Restent à remplir :
**procs d'items** et **logique des 276 augments**. Le contenu **doit être revérifié à chaque patch**.
