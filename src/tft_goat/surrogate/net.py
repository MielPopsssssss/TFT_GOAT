"""CombatNet : encodeur de board partage -> P(board A bat board B)."""

from __future__ import annotations

import torch
from torch import nn


class BoardEncoder(nn.Module):
    """Encode un board (champions + etoiles + items poolés + traits) -> vecteur."""

    def __init__(self, n_champ: int, n_trait: int, embed_dim: int = 16, out_dim: int = 64):
        super().__init__()
        self.embed = nn.Embedding(n_champ + 1, embed_dim)  # 0 = vide
        self.n_champ = n_champ
        # embedding + star + items concatenes, puis traits
        self.mlp = nn.Sequential(
            nn.Linear(embed_dim + 2 + n_trait, out_dim), nn.ReLU(),
            nn.Linear(out_dim, out_dim), nn.ReLU(),
        )

    def forward(self, feat: dict[str, torch.Tensor]) -> torch.Tensor:
        idx = feat["champ_idx"].long().clamp(0, self.n_champ)
        emb = self.embed(idx)  # (B, U, emb)
        star = feat["star"].unsqueeze(-1)
        items = feat["items"].unsqueeze(-1)
        pooled = torch.cat([emb, star, items], dim=-1).mean(dim=1)  # (B, emb+2)
        return self.mlp(torch.cat([pooled, feat["trait_vec"]], dim=-1))


class CombatNet(nn.Module):
    """P(board A bat board B). Anti-symetrie encouragee via la composante difference."""

    def __init__(self, n_champ: int, n_trait: int, embed_dim: int = 16, board_dim: int = 64,
                 hidden_dim: int = 128):
        super().__init__()
        self.board_encoder = BoardEncoder(n_champ, n_trait, embed_dim, board_dim)
        self.head = nn.Sequential(
            nn.Linear(board_dim * 3, hidden_dim), nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def logit(self, a: dict[str, torch.Tensor], b: dict[str, torch.Tensor]) -> torch.Tensor:
        ea = self.board_encoder(a)
        eb = self.board_encoder(b)
        combined = torch.cat([ea, eb, ea - eb], dim=-1)
        return self.head(combined).squeeze(-1)

    def win_prob(self, a, b) -> torch.Tensor:
        return torch.sigmoid(self.logit(a, b))
