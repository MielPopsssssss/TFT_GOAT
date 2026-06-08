# TFT_GOAT — Spec d'architecture global

> Document de référence figé après brainstorming + recherche de prior art.
> Statut : **approuvé**. Chaque sous-système (étapes 1→6) aura son propre spec + plan
> avant implémentation. Ce document ne se code pas directement.

## Contexte & objectif

Un programme d'IA capable de jouer à Teamfight Tactics (TFT) à très haut niveau, à terme de
façon **autonome** (perception → décision → action in-game). Le « cerveau » est entraîné par
**reinforcement learning / self-play**.

Un bot autonome n'est pas un projet unique mais **4 sous-systèmes distincts** (+2 ultérieurs).
On fige ici l'architecture et les interfaces pour que chacun soit développé indépendamment.

## Décisions structurantes (issues du brainstorming + recherche)

- **But** : bot autonome complet (à terme). Cerveau via **RL / self-play**.
- **Combat NON simulé** : pas de simulation des sorts tick-par-tick. On utilise un **modèle
  d'issue de combat appris** (surrogate neuronal `P(win | board A, board B)`) — l'approche de
  Riot elle-même (GDC 2024). Seule voie qui survit au *set-churn*.
- **Pas de réutilisation d'un sim complet** : aucun simulateur TFT open-source n'est à jour
  (`silverlight6/TFTMuZeroAgent` est le seul vivant mais bloqué Set 4). Utilisé comme
  **référence d'architecture** uniquement.
- **Données** : API Riot `tft-match-v1` (post-game) pour entraîner le surrogate ;
  Data Dragon / CommunityDragon pour le contenu statique ; tables metatft (shop odds, augments)
  comme *priors*. Pas d'état live complet via l'API officielle (sans impact en self-play).

## ⚠️ Contraintes

- **ToS Riot** : l'automatisation in-game viole les CGU → ban. L'actuation (étape 6) est à
  exécuter **sur un compte de test/smurf uniquement**, aux risques de l'utilisateur. Le cœur
  RL/self-play est **offline** et ne touche pas au client → aucun risque ToS.
- **Principe anti-obsolescence** : *un nouveau set = un refresh de données (Data Dragon +
  ré-entraînement du surrogate), jamais une réécriture.* Tout le contenu est data-driven.

## Vue d'ensemble — sous-systèmes

```
┌──────────────────────────────────────────────────────────────┐
│ (4) Agent RL  — PPO self-play (puis MuZero en stretch)        │
│      policy partagée, 8 instances en lobby                    │
└───────────────▲──────────────────────────┬───────────────────┘
        observation │                action │
┌───────────────┴──────────────────────────▼───────────────────┐
│ (2) Macro Environment  (PettingZoo, à coder from scratch)     │
│   économie · level · roll · shop RNG · achat/vente · items ·  │
│   augments · positionnement grossier · rounds · PV · 8 joueurs│
│        appelle ▼  (interface CombatResolver enfichable)       │
│   ┌───────────────────────────────────────────────────┐      │
│   │ (3) Combat Resolver                                │      │
│   │   v0  heuristique force-de-board (placeholder)     │      │
│   │   v1  surrogate neuronal  P(win | boardA, boardB)  │      │
│   └───────────────────────────────────────────────────┘      │
└───────────────▲───────────────────────────────────────────────┘
   contenu/priors│
┌───────────────┴───────────────────────────────────────────────┐
│ (1) Data & Knowledge Layer                                     │
│   Data Dragon (contenu statique) · tables metatft (priors) ·   │
│   collecteur Riot match-v1 (dataset d'entraînement combat)     │
└────────────────────────────────────────────────────────────────┘

   [ ULTÉRIEUR / optionnel, hors RL — pour jouer sur le vrai client ]
   (5) Perception (computer vision/OCR)  →  (6) Actuation (clics) ⚠️ToS
```

## Sous-systèmes & interfaces

### (1) Data & Knowledge Layer
Source unique de vérité, versionnée par set/patch.
- **Content provider** : parse Data Dragon / CommunityDragon → champions (coût, traits, stats),
  traits (breakpoints), items (recettes), augments. Structures immuables, une version par patch.
- **Priors** : shop odds par niveau, taille des pools, distributions d'augments, encounter odds
  (scraping tables metatft, pas d'API).
- **Match collector** : client Riot `tft-match-v1` (rate-limiting + cache) → dataset boards
  finaux + placements pour entraîner (3.v1).

```
SetContent = { champions, traits, items, augments }   # immuable, versionné
ShopOdds.roll_odds(level) -> {cost: probability}
PoolSize(cost) -> int
load_set(patch: str) -> SetContent
```

### (2) Macro Environment (PettingZoo `ParallelEnv`)
Simule la *macro* d'une partie 8 joueurs — tout sauf la résolution des sorts. Délègue les
affrontements au `CombatResolver` (injecté → swap v0↔v1 sans toucher l'env). Récompense =
placement final ; reward shaping optionnel via priors.

```
reset() -> {agent_id: Observation}
step({agent_id: Action}) -> (obs, rewards, dones, infos)
# Observation : or, niveau, board, banc, shop, augments, + scouting adversaires
# Action (hybride) : roll, buy(slot), sell(unit), level_up,
#                    place(unit,pos), equip(item,unit), pick_augment(i), pass
```

### (3) Combat Resolver
Interface **stable** ; seules les implémentations changent.
```
resolve(board_a: Board, board_b: Board) -> CombatResult   # { winner, dmg, ... }
```
- **v0 (placeholder)** : heuristique « force de board » (coût × niveau d'étoile × breakpoints de
  traits). Permet de lancer la boucle RL immédiatement.
- **v1 (surrogate)** : réseau entraîné sur match-v1 → `P(win | A, B)`. Remplace v0 quand prêt.

### (4) Agent RL
Self-play. **PPO** d'abord (robuste à l'info imparfaite + multi-agent, policy partagée),
**MuZero/Gumbel-MuZero** en stretch (réf. TFTMuZeroAgent). 100 % offline.

## Stack technique
- Python 3.11+.
- PyTorch ; PettingZoo ; runner PPO (CleanRL-style maison ou RLlib).
- `httpx` + cache pour Riot API ; parsing Data Dragon (JSON) ; BeautifulSoup pour tables metatft.
- Structures immuables, petits modules par domaine, tests unitaires (éco/shop RNG/resolver),
  golden tests (content provider).

## Roadmap (chaque étape = son propre spec + plan)
1. **(1) Data & Knowledge Layer** — fondation, zéro dépendance.
2. **(2)+(3.v0) Macro Env + combat placeholder** — premier livrable « vivant ».
3. **(4) Agent RL (PPO self-play)** — prouve le pipeline.
4. **(3.v1) Combat surrogate** — dataset match-v1 → réseau, swap v0→v1.
5. **(4') Montée en puissance** — MuZero / reward shaping / éval.
6. *(ultérieur, optionnel)* **(5) Perception + (6) Actuation** ⚠️ ToS.

## Risques majeurs
- **Set-churn** (#1) : tout data-driven + ré-entraînable. Mitigé par surrogate + Data Dragon versionné.
- **Fidélité du combat** : surrogate biaisé par son dataset → v0 d'abord + calibration sur v1.
- **Explosion espace action/état** : action space factorisé + masquage actions illégales + obs compactes.
- **Compute self-play** : millions de parties → env vectorisé/rapide (le combat abstrait rend le throughput viable).
- **ToS/ban** : étapes 5-6 seulement, compte de test only.

## Validation de l'architecture (premiers jalons exécutables)
- **(1)** : charger le set courant, imprimer champions/traits/odds ; golden test vs metatft.
- **(2)+(3.v0)** : partie 8 joueurs scriptée (actions aléatoires) jusqu'à élimination ;
  invariants (or ≥ 0, pool respecté, 1 gagnant).
- **(3↔)** : substitution v0/v1 sans modifier l'env.
- **(4)** : courbe de reward PPO qui monte vs baseline aléatoire ; l'agent apprend l'éco.

## Décisions ouvertes (au spec de chaque étape)
- Set ciblé en premier (set live courant, à confirmer à l'implémentation).
- PPO maison (CleanRL) vs RLlib.
- Granularité du positionnement (slots discrets vs zones) dans l'Observation.
