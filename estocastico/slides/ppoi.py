import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Parâmetros do processo
lambda_rate = 1.0   # taxa de chegadas por unidade de tempo
T = 10.0            # horizonte temporal
n_traj = 5          # número de trajetórias para simulação

# Função para simular uma trajetória de Poisson
def simulate_poisson(lambda_rate, T):
    t, arrivals = [0], [0]
    time = 0
    while time < T:
        # tempo até a próxima chegada ~ Exp(lambda)
        interarrival = np.random.exponential(1/lambda_rate)
        time += interarrival
        if time <= T:
            t.append(time)
            arrivals.append(arrivals[-1] + 1)
    return np.array(t), np.array(arrivals)

# ------------------------------
# 1) FIGURA ESTÁTICA
# ------------------------------
plt.figure(figsize=(8,5))
for i in range(n_traj):
    t, arrivals = simulate_poisson(lambda_rate, T)
    plt.step(t, arrivals, where="post", label=f"Trajetória {i+1}", alpha=0.7)
plt.xlabel("tempo t")
plt.ylabel("X(t)")
plt.title(f"Processo de Poisson com taxa λ={lambda_rate}")
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# ------------------------------
# 2) ANIMAÇÃO (uma única trajetória)
# ------------------------------
t, arrivals = simulate_poisson(lambda_rate, T)

fig, ax = plt.subplots(figsize=(8,5))
ax.set_xlim(0, T)
ax.set_ylim(0, max(arrivals)+1)
ax.set_xlabel("tempo t")
ax.set_ylabel("X(t)")
ax.set_title("Animação: Processo de Poisson")

(line,) = ax.step([], [], where="post", lw=2)

def init():
    line.set_data([], [])
    return (line,)

def update(frame):
    line.set_data(t[:frame+1], arrivals[:frame+1])
    return (line,)

ani = FuncAnimation(fig, update, frames=len(t), init_func=init,
                    blit=True, interval=800, repeat=False)

plt.show()
