import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

# Parâmetros do processo
lambda_rate = 1.0
T = 10.0
np.random.seed(42)

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

# Simulação de uma trajetória
t, arrivals = simulate_poisson(lambda_rate, T)

# Configuração do gráfico
fig, ax = plt.subplots(figsize=(8,5))
ax.set_xlim(0, T)
ax.set_ylim(0, max(arrivals)+1)
ax.set_xlabel("tempo t")
ax.set_ylabel("X(t)")
ax.set_title("Processo de Poisson (animação)")

(line,) = ax.step([], [], where="post", lw=2, color="blue")

def init():
    line.set_data([], [])
    return (line,)

def update(frame):
    line.set_data(t[:frame+1], arrivals[:frame+1])
    return (line,)

ani = FuncAnimation(fig, update, frames=len(t),
                    init_func=init, blit=True,
                    interval=800, repeat=False)

# Salvar como GIF
writer = PillowWriter(fps=2)
ani.save("poisson_trajetoria.gif", writer=writer)

plt.close()
print("GIF salvo como poisson_trajetoria.gif")
