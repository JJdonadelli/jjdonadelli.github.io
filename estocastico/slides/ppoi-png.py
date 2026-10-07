import numpy as np
import matplotlib.pyplot as plt
import os

# Criar pasta para os quadros
os.makedirs("frames", exist_ok=True)

# Parâmetros do processo
lambda_rate = 1.0
T = 10.0
np.random.seed(42)

# Simular trajetória de Poisson
def simulate_poisson(lambda_rate, T):
    t, arrivals = [0], [0]
    time = 0
    while time < T:
        interarrival = np.random.exponential(1/lambda_rate)
        time += interarrival
        if time <= T:
            t.append(time)
            arrivals.append(arrivals[-1] + 1)
    return np.array(t), np.array(arrivals)

t, arrivals = simulate_poisson(lambda_rate, T)

# Gerar um PNG para cada quadro (passo da escada)
for i in range(1, len(t)+1):
    plt.figure(figsize=(8,5))
    plt.step(t[:i], arrivals[:i], where='post', color='blue', lw=2)
    plt.xlim(0, T)
    plt.ylim(0, max(arrivals)+1)
    plt.xlabel("tempo t")
    plt.ylabel("X(t)")
    plt.title("Processo de Poisson: Trajetória Simulada")
    plt.grid(alpha=0.3)
#    plt.savefig(f"frames/frame_{i:03d}.png")
    plt.savefig(f"frames/frame_{i}.png")
    plt.close()
