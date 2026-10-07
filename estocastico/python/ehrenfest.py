import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from math import comb

# parâmetros
N = 50         # número total de bolas
T = 100000     # número de passos da simulação
X0 = N         # estado inicial (todas as bolas na urna A)

# simulação
X = np.zeros(T+1, dtype=int)
X[0] = X0
for t in range(T):
    k = X[t]
    # com probabilidade k/N tiramos da urna A
    if np.random.rand() < k / N:
        X[t+1] = k - 1
    else:
        X[t+1] = k + 1

# distribuição empírica
counts = Counter(X)
empirical_probs = np.array([counts[k] / (T+1) for k in range(N+1)])

# distribuição teórica (Binomial)
theoretical_probs = np.array([comb(N, k) * (0.5**N) for k in range(N+1)])

# --- gráficos ---
fig, axs = plt.subplots(2, 1, figsize=(12, 8))

# 1) Trajetória no tempo
axs[0].plot(range(2000), X[:2000], lw=1.2, color="C0")
axs[0].axhline(N/2, color="r", linestyle="--", label="Equilíbrio (N/2)")
axs[0].set_title("Trajetória do modelo de Ehrenfest (primeiros 2000 passos)")
axs[0].set_xlabel("Tempo")
axs[0].set_ylabel("Número de bolas na urna A")
axs[0].legend()

# 2) Distribuição empírica vs teórica
axs[1].bar(range(N+1), empirical_probs, alpha=0.6, label="Simulação", color="C0")
axs[1].plot(range(N+1), theoretical_probs, "r--", lw=2, label="Distribuição Binomial(N, 1/2)")
axs[1].set_xlabel("Número de bolas na urna A")
axs[1].set_ylabel("Probabilidade")
axs[1].set_title(f"Distribuição empírica vs teórica (N={N}, T={T})")
axs[1].legend()

plt.tight_layout()
plt.show()
