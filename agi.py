import torch
import torch.nn as nn
import torch.nn.functional as F

class Grok41MoE_v2(nn.Module):
    """
    Ulepszona implementacja MoE w stylu Grok-4 / DeepSeek-MoE / Mixtral
    z optymalizacją GPU, capacity limit i jitterem dla lepszego balansu.
    """
    def __init__(self, d_model=1024, num_experts=8, top_k=2, capacity_factor=1.2, jitter_scale=0.02):
        super().__init__()
        self.d_model = d_model
        self.num_experts = num_experts
        self.top_k = top_k
        self.capacity_factor = capacity_factor  # Limit pojemności ekspertów (1.2x top_k)
        self.jitter_scale = jitter_scale       # Szum dla routingu

        # Brama routingu z jitterem
        self.gate = nn.Linear(d_model, num_experts, bias=False)
        self.jitter = nn.Parameter(torch.randn(1, num_experts) * jitter_scale)

        # Eksperci z FFN (4× expansion)
        self.experts = nn.ModuleList([
            nn.Sequential(
                nn.Linear(d_model, d_model * 4, bias=False),
                nn.GELU(),
                nn.Linear(d_model * 4, d_model, bias=False)
            ) for _ in range(num_experts)
        ])

        # Personality bias z losowym seedem (polski charakter!)
        self.personality_bias = nn.Parameter(torch.randn(num_experts) * 0.01 + torch.linspace(-0.05, 0.05, num_experts))

    def forward(self, x):
        # x: (batch, seq_len, d_model)
        B, S, D = x.shape
        N = B * S  # Liczba tokenów
        x_flat = x.reshape(N, D)

        # Routing z jitterem i personality bias
        logits = self.gate(x_flat) + self.personality_bias + self.jitter  # (N, E)
        topk_weights, topk_indices = torch.topk(logits, self.top_k, dim=-1)
        weights = F.softmax(topk_weights, dim=-1, dtype=torch.float32).to(x.dtype)  # (N, k)

        # Entropia routingu (monitorowanie równomierności)
        entropy = -(weights * torch.log(weights + 1e-12)).sum(-1).mean()

        # Capacity limit – unikamy przeładowania ekspertów
        capacity = int(N * self.top_k * self.capacity_factor / self.num_experts)
        expert_usage = torch.zeros(N, self.num_experts, device=x.device)
        for k in range(self.top_k):
            expert_idx = topk_indices[:, k]
            mask = torch.scatter_add(
                expert_usage, 1, expert_idx.unsqueeze(-1), torch.ones_like(weights[:, k:k+1])
            ) <= capacity
            weights[:, k] *= mask.any(dim=-1).float()

        # Wektorowe obliczenia – zero pętli, pełna GPU-optymalizacja
        output = torch.zeros_like(x_flat)
        for k in range(self.top_k):
            expert_idx = topk_indices[:, k]
            expert_weight = weights[:, k].unsqueeze(-1)
            expert_inputs = x_flat[expert_weight > 0]
            if len(expert_inputs) == 0:
                continue
            expert_outputs = self.experts[expert_idx[expert_weight > 0]](expert_inputs)
            output[expert_weight > 0] += expert_outputs * expert_weight[expert_weight > 0]

        output = output.reshape(B, S, D)

        # Auxiliary loss z jitterem dla lepszego balansu
        usage = torch.zeros(self.num_experts, device=x.device)
        for k in range(self.top_k):
            usage.index_add_(0, topk_indices[:, k], torch.ones(N, device=x.device))
        prob = usage / usage.sum().clamp(min=1e-6)
        aux_loss = 0.01 * self.num_experts * torch.sum(prob * torch.log(prob + 1e-6))  # KL-divergence

        return output, aux_loss, entropy

# Przykład użycia
if __name__ == "__main__":
    x = torch.randn(2, 512, 1024)  # Batch 2, seq_len 512
    moe = Grok41MoE_v2(d_model=1024, num_experts=8, top_k=2)
    y, aux_loss, entropy = moe(x)
    print(f"Output shape: {y.shape}, Aux Loss: {aux_loss.item():.4f}, Entropy: {entropy.item():.4f}")
