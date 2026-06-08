"""Entrainement du combat surrogate (CombatNet).

Deux sources de donnees :
  - bootstrap : distillation du combat heuristique ancre (pas de cle requise).
  - riot      : paires board->placement depuis des parties match-v1 collectees
                (voir scripts/collect_matches.py).

Usage :
  .venv/bin/python -m tft_goat.scripts.train_surrogate --source bootstrap --content synthetic
  .venv/bin/python -m tft_goat.scripts.train_surrogate --source riot --matches data/matches/matches_17.4.jsonl
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import torch
from torch import nn

from ..data.content import load_set
from ..data.datatft import load_meta_stats
from ..data.riot.match import parse_match
from ..data.sample import build_sample_content
from ..env.encoding import Encoder
from ..surrogate.dataset import (
    make_bootstrap_dataset,
    make_engine_dataset,
    pairs_from_matches,
)
from ..surrogate.featurize import batch_boards
from ..surrogate.net import CombatNet


def _to_tensors(boards, encoder, device):
    return batch_boards(boards, encoder, device)


def _featurize_all(boards_a, boards_b, encoder, device):
    return _to_tensors(boards_a, encoder, device), _to_tensors(boards_b, encoder, device)


def _index(feat, idx):
    return {k: v[idx] for k, v in feat.items()}


def train(args) -> None:
    rng = np.random.default_rng(args.seed)
    torch.manual_seed(args.seed)
    device = args.device

    # --- contenu + dataset ---
    def _load_matches():
        lines = Path(args.matches).read_text().splitlines()
        return [parse_match(json.loads(l)) for l in lines if l.strip()]

    if args.source == "bootstrap":
        if args.content == "synthetic":
            content, meta = build_sample_content(), None
        else:
            content, meta = load_set(), load_meta_stats()
        boards_a, boards_b, labels = make_bootstrap_dataset(content, meta, args.pairs, rng)
    elif args.source == "engine":
        content = load_set()
        boards_a, boards_b, labels = make_engine_dataset(
            content, args.pairs, rng, samples=args.engine_samples
        )
        print(f"moteur : {len(labels)} paires (verite terrain combat) ; "
              f"taux victoire A = {labels.mean():.2f}")
    elif args.source == "riot":
        content = load_set()
        matches = _load_matches()
        boards_a, boards_b, labels = pairs_from_matches(matches)
        print(f"{len(matches)} parties -> {len(labels)} paires")
    else:  # hybrid : vraies paires + bootstrap multi-stades (corrige le decalage de distribution)
        content, meta = load_set(), load_meta_stats()
        matches = _load_matches()
        ra, rb, ry = pairs_from_matches(matches)
        ba, bb, by = make_bootstrap_dataset(content, meta, args.pairs, rng)
        boards_a, boards_b = list(ra) + list(ba), list(rb) + list(bb)
        labels = np.concatenate([ry, by])
        print(f"hybride : {len(ry)} paires reelles + {len(by)} paires bootstrap = {len(labels)}")

    encoder = Encoder(content)
    fa, fb = _featurize_all(boards_a, boards_b, encoder, device)
    y = torch.as_tensor(labels, device=device)
    n = len(labels)

    # split train / held-out
    perm = rng.permutation(n)
    n_val = max(1, n // 10)
    val_idx = torch.as_tensor(perm[:n_val], device=device)
    train_idx = torch.as_tensor(perm[n_val:], device=device)

    net = CombatNet(encoder.n_champ, encoder.n_trait).to(device)
    optim = torch.optim.Adam(net.parameters(), lr=args.lr)
    loss_fn = nn.BCEWithLogitsLoss()

    for epoch in range(1, args.epochs + 1):
        net.train()
        order = train_idx[torch.randperm(len(train_idx))]
        total = 0.0
        for start in range(0, len(order), args.batch_size):
            mb = order[start : start + args.batch_size]
            logits = net.logit(_index(fa, mb), _index(fb, mb))
            loss = loss_fn(logits, y[mb])
            optim.zero_grad()
            loss.backward()
            optim.step()
            total += float(loss.item())
        acc = _accuracy(net, fa, fb, y, val_idx)
        print(f"epoch {epoch:2d} | loss {total/max(1,len(order)//args.batch_size):.4f} | val_acc {acc:.3f}")

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    ckpt = out / "combatnet.pt"
    torch.save(
        {"state_dict": net.state_dict(), "n_champ": encoder.n_champ,
         "n_trait": encoder.n_trait, "content": args.content if args.source == "bootstrap" else "real"},
        ckpt,
    )
    print(f"checkpoint -> {ckpt}")


@torch.no_grad()
def _accuracy(net, fa, fb, y, idx) -> float:
    net.eval()
    p = net.win_prob(_index(fa, idx), _index(fb, idx))
    pred = (p > 0.5).float()
    target = (y[idx] > 0.5).float()
    return float((pred == target).float().mean().item())


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--source", choices=["bootstrap", "riot", "hybrid", "engine"], default="bootstrap")
    p.add_argument("--engine-samples", type=int, default=1, help="runs moteur par paire (label doux si >1)")
    p.add_argument("--content", choices=["synthetic", "real"], default="synthetic")
    p.add_argument("--matches", default="data/matches/matches_17.4.jsonl")
    p.add_argument("--pairs", type=int, default=20000)
    p.add_argument("--epochs", type=int, default=5)
    p.add_argument("--batch-size", type=int, default=256)
    p.add_argument("--lr", type=float, default=1e-3)
    p.add_argument("--device", default="cpu")
    p.add_argument("--seed", type=int, default=0)
    p.add_argument("--out", default="runs/surrogate")
    train(p.parse_args())


if __name__ == "__main__":
    main()
