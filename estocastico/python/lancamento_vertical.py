import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do movimento
v0 = 10  # velocidade inicial em m/s
g = 10   # aceleração da gravidade em m/s²

# Tempo total de voo (quando h = 0 novamente)
tempo_total = (2 * v0) / g  # 2 segundos

# Criar array de tempo
t = np.linspace(0, tempo_total, 100)

# Calcular altura usando a equação: h(t) = v₀t - ½gt²
altura = v0 * t - 0.5 * g * t**2

# Calcular pontos importantes
tempo_altura_maxima = v0 / g  # tempo para atingir altura máxima
altura_maxima = (v0**2) / (2 * g)  # altura máxima

# Criar o gráfico
plt.figure(figsize=(10, 8))
plt.plot(t, altura, 'b-', linewidth=3, label=r'Altura $S(t)$')
plt.plot(tempo_altura_maxima, altura_maxima, 'ro', markersize=10, 
         label=f'Altura máxima ({tempo_altura_maxima:.1f}s, {altura_maxima:.1f}m)')

# Configurar o gráfico
plt.xlabel(r'Tempo ($s$)', fontsize=12)
plt.ylabel(r'Altura ($m$)', fontsize=12)
plt.title('Movimento Vertical de Projétil - $S(t) = v_0t - \\frac{1}{2}gt^2$', fontsize=14)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=11)

## Adicionar anotações
#plt.annotate(f'Altura máxima\n{altura_maxima} m', 
#             xy=(tempo_altura_maxima, altura_maxima), 
#             xytext=(tempo_altura_maxima + 0.3, altura_maxima - 0.5),
#             arrowprops=dict(arrowstyle='->', color='red'),
#             fontsize=10, ha='left')
#
# Configurar limites dos eixos
plt.xlim(0, tempo_total * 1.05)
plt.ylim(0, altura_maxima * 1.1)

# Adicionar informações do problema
textstr = fr'''Parâmetros:
• $v_0=${v0} m/s
• $g=${g} m/s²
• posição: $S(t)=${v0}$t - ${g/2:.1f}$t^2$
'''

props = dict(boxstyle='round', facecolor='lightblue', alpha=0.8)
plt.text(0.02, 0.98, textstr, transform=plt.gca().transAxes, fontsize=10,
         verticalalignment='top', bbox=props)

plt.tight_layout()
plt.show()

# Imprimir alguns valores importantes
print("ANÁLISE DO MOVIMENTO VERTICAL")
print("=" * 40)
print(f"Velocidade inicial (v₀): {v0} m/s")
print(f"Aceleração da gravidade (g): {g} m/s²")
print(f"Altura máxima: {altura_maxima} m")
print(f"Tempo para altura máxima: {tempo_altura_maxima} s")
print(f"Tempo total de voo: {tempo_total} s")
print(fr"Equação do movimento: $S(t) = v_0t - \frac g2 t^2")

print("\nALGUNS PONTOS DA TRAJETÓRIA:")
print("=" * 40)
tempos_exemplo = [0, 0.5, 1.0, 1.5, 2.0]
for t_ex in tempos_exemplo:
    if t_ex <= tempo_total:
        h_ex = v0 * t_ex - 0.5 * g * t_ex**2
        v_ex = v0 - g * t_ex  # velocidade no tempo t
        print(f"t = {t_ex:3.1f}s | h = {h_ex:5.2f}m | v = {v_ex:5.1f}m/s")
