"""Reseau acteur-critique avec embedding de champions et tete policy masquee."""

from __future__ import annotations

import torch
from torch import nn
from torch.distributions import Categorical

from ..env.actions import NUM_ACTIONS

NEG_INF = -1e9


class ActorCritic(nn.Module):
    def __init__(self, n_champ: int, n_trait: int, embed_dim: int = 16, hidden_dim: int = 256):
        super().__init__()
        self.embed = nn.Embedding(n_champ + 1, embed_dim)  # index 0 = vide
        self.n_champ = n_champ

        # scalaires [gold,level,xp,hp,streak,round,maxlvl,components,augment_power,augment_avail]
        self.register_buffer(
            "scalar_scale",
            torch.tensor([50.0, 10.0, 100.0, 100.0, 10.0, 50.0, 10.0, 10.0, 1.0, 1.0]),
        )
        self.register_buffer("opp_scale", torch.tensor([100.0, 10.0, 10.0]))

        n_scalars = 10
        unit_extra = 2  # star + items concatenes a l'embedding
        in_dim = (
            n_scalars + embed_dim + (embed_dim + unit_extra) * 2 + n_trait + 7 * 3
        )
        self.trunk = nn.Sequential(
            nn.Linear(in_dim, hidden_dim), nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim), nn.ReLU(),
        )
        self.policy_head = nn.Linear(hidden_dim, NUM_ACTIONS)
        self.value_head = nn.Linear(hidden_dim, 1)

    def _idx(self, t: torch.Tensor) -> torch.Tensor:
        return t.long().clamp(0, self.n_champ)

    def _features(self, obs: dict[str, torch.Tensor]) -> torch.Tensor:
        scalars = obs["scalars"] / self.scalar_scale
        shop = self.embed(self._idx(obs["shop"])).mean(dim=1)  # (B, emb)

        def units(key: str) -> torch.Tensor:
            emb = self.embed(self._idx(obs[key][..., 0]))  # (B, n, emb)
            star_items = obs[key][..., 1:3]  # (B, n, 2) = star + items
            return torch.cat([emb, star_items], dim=-1).mean(dim=1)  # (B, emb+2)

        bench = units("bench")
        board = units("board")
        opp = (obs["opponents"] / self.opp_scale).flatten(start_dim=1)  # (B, 21)
        return torch.cat([scalars, shop, bench, board, obs["traits"], opp], dim=-1)

    def forward(self, obs, mask) -> tuple[torch.Tensor, torch.Tensor]:
        h = self.trunk(self._features(obs))
        logits = self.policy_head(h).masked_fill(~mask, NEG_INF)
        value = self.value_head(h).squeeze(-1)
        return logits, value

    def act(self, obs, mask):
        logits, value = self.forward(obs, mask)
        dist = Categorical(logits=logits)
        action = dist.sample()
        return action, dist.log_prob(action), value

    @torch.no_grad()
    def act_greedy(self, obs, mask) -> torch.Tensor:
        logits, _ = self.forward(obs, mask)
        return logits.argmax(dim=-1)

    def evaluate_actions(self, obs, mask, actions):
        logits, value = self.forward(obs, mask)
        dist = Categorical(logits=logits)
        return dist.log_prob(actions), dist.entropy(), value
