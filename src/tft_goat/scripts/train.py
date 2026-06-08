"""Entrainement PPO self-play sur TftEnv.

Usage :
  .venv/bin/python -m tft_goat.scripts.train --content synthetic --iterations 30
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import torch

from ..agent.config import PPOConfig
from ..agent.evaluate import eval_vs_opponents, eval_vs_random
from ..agent.network import ActorCritic
from ..agent.ppo import ppo_update
from ..agent.rollout import collect_games
from ..data.content import load_set
from ..data.datatft import load_meta_stats
from ..data.sample import build_sample_content
from ..env.combat import HeuristicResolver
from ..env.tft_env import TftEnv
from ..surrogate.net import CombatNet
from ..surrogate.resolver import NeuralResolver


def make_env(args) -> TftEnv:
    content = build_sample_content() if args.content == "synthetic" else load_set()
    env = TftEnv(set_content=content)
    if args.resolver == "neural":
        assert args.content == "real", "le surrogate neural exige --content real"
        ck = torch.load(args.surrogate, weights_only=False)
        net = CombatNet(ck["n_champ"], ck["n_trait"])
        net.load_state_dict(ck["state_dict"])
        env.resolver = NeuralResolver(net, env.encoder, args.device)
        print(f"combat = NeuralResolver ({args.surrogate})")
    elif args.resolver == "heuristic" and args.content == "real":
        env.resolver = HeuristicResolver(load_meta_stats())
        print("combat = HeuristicResolver ancre datatft")
    return env


def train(args) -> None:
    cfg = PPOConfig(
        rollout_steps=args.rollout_steps,
        device=args.device,
        seed=args.seed,
    )
    torch.manual_seed(cfg.seed)
    np.random.seed(cfg.seed)

    env = make_env(args)
    policy = ActorCritic(
        n_champ=env.encoder.n_champ,
        n_trait=env.encoder.n_trait,
        embed_dim=cfg.embed_dim,
        hidden_dim=cfg.hidden_dim,
    ).to(cfg.device)
    optimizer = torch.optim.Adam(policy.parameters(), lr=cfg.lr)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    base = eval_vs_random(policy, env, n_games=args.eval_games, device=cfg.device)
    print(f"baseline (agent NON entraine) : placement moyen {base['mean_placement']:.2f} "
          f"(random ~4.5)")
    for it in range(1, args.iterations + 1):
        batch = collect_games(
            env, policy, cfg.rollout_steps, cfg.gamma, cfg.gae_lambda, cfg.device
        )
        metrics = ppo_update(policy, optimizer, batch, cfg)
        print(
            f"it {it:3d} | transitions {len(batch):5d} | parties {batch.n_games:3d} "
            f"| reward/partie {batch.mean_game_reward:+.3f} | len {batch.mean_game_len:6.1f} "
            f"| pi {metrics['policy_loss']:+.3f} v {metrics['value_loss']:.3f} "
            f"H {metrics['entropy']:.3f}"
        )
        if it % args.eval_every == 0 or it == args.iterations:
            ev = eval_vs_random(policy, env, n_games=args.eval_games, device=cfg.device)
            sc = eval_vs_opponents(policy, env, "scripted", n_games=args.eval_games, device=cfg.device)
            print(
                f"     EVAL vs random {ev['mean_placement']:.2f} (top4 {ev['top4_rate']:.2f}) "
                f"| vs scripté {sc['mean_placement']:.2f} (top4 {sc['top4_rate']:.2f})"
            )
            torch.save(policy.state_dict(), out / f"policy_it{it}.pt")
    torch.save(policy.state_dict(), out / "policy_final.pt")
    print(f"checkpoints dans {out}/")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--content", choices=["synthetic", "real"], default="synthetic")
    p.add_argument("--resolver", choices=["default", "heuristic", "neural"], default="default")
    p.add_argument("--surrogate", default="runs/surrogate/combatnet.pt")
    p.add_argument("--iterations", type=int, default=30)
    p.add_argument("--rollout-steps", type=int, default=4096)
    p.add_argument("--eval-games", type=int, default=30)
    p.add_argument("--eval-every", type=int, default=10)
    p.add_argument("--device", default="cpu")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--out", default="runs/ppo")
    train(p.parse_args())


if __name__ == "__main__":
    main()
