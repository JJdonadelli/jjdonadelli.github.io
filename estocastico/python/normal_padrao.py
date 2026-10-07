import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib.patches as patches

# Configurar o matplotlib para usar fonte que suporta caracteres especiais
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.figsize'] = (12, 8)

# Gerar dados para a distribuição normal padrão
x = np.linspace(-4, 4, 1000)
y = stats.norm.pdf(x, 0, 1)  # média=0, desvio-padrão=1

# Criar o gráfico
fig, ax = plt.subplots(figsize=(12, 8))

# Plotar a curva da distribuição normal
ax.plot(x, y, 'k-', linewidth=2, label='N(0,1)')

# Definir cores para cada região
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
alphas = [0.3, 0.25, 0.2]

# Preencher as áreas para 1, 2 e 3 desvios-padrão
for i, sigma in enumerate([1, 2, 3]):
    # Área entre -sigma e +sigma
    x_fill = x[(x >= -sigma) & (x <= sigma)]
    y_fill = stats.norm.pdf(x_fill, 0, 1)
    
    ax.fill_between(x_fill, y_fill, alpha=alphas[i], color=colors[i], 
                    label=f'±{sigma}σ ({stats.norm.cdf(sigma) - stats.norm.cdf(-sigma):.1%})')

# Adicionar linhas verticais nos desvios-padrão
for sigma in range(-3, 4):
    if sigma != 0:
        ax.axvline(x=sigma, color='gray', linestyle='--', alpha=0.5)
        ax.text(sigma, -0.02, f'{sigma}σ', ha='center', va='top', fontsize=10)

# Linha vertical no centro (média)
ax.axvline(x=0, color='black', linestyle='-', alpha=0.7)
ax.text(0, -0.02, '0', ha='center', va='top', fontsize=10, fontweight='bold')

# Configurações do gráfico
ax.set_xlim(-4, 4)
ax.set_ylim(-0.05, 0.45)
ax.set_xlabel('Valores Padronizados (Z)', fontsize=12)
ax.set_ylabel('Densidade de Probabilidade', fontsize=12)
ax.set_title('Distribuição Normal Padrão N(0,1)', 
             fontsize=14, fontweight='bold', pad=20)

# Adicionar grade
ax.grid(True, alpha=0.3)

# Legenda
ax.legend(loc='upper right', fontsize=10)

# Adicionar caixa de texto com o Teorema Central do Limite
textstr = 'Teorema Central do Limite:\n\n'
textstr += r'$\mathbf{{S_n} {{n}^{-1/2}} \rightarrow N(0,1)}$' + '\n\n'
textstr += 'onde:'
textstr += r'$S_n = \sum_{i=1}^{n} X_i$' #+ '\n'
textstr += 'e $X_i$ são v.a. i.i.d. com\n'
textstr += 'média finita e variância finita'

# Criar caixa de texto
props = dict(boxstyle='round,pad=0.5', facecolor='lightblue', alpha=0.8)
ax.text(-3.5, 0.35, textstr, fontsize=11, verticalalignment='top',
        bbox=props, family='monospace')

# Adicionar informações estatísticas
info_text = 'Regra Empírica (68-95-99.7):\n'
info_text += '• ±1σ: ≈68.27% dos dados\n'
info_text += '• ±2σ: ≈95.45% dos dados\n'
info_text += '• ±3σ: ≈99.73% dos dados'

props2 = dict(boxstyle='round,pad=0.5', facecolor='lightyellow', alpha=0.8)
ax.text(1.8, 0.35, info_text, fontsize=16, verticalalignment='top',
        bbox=props2)

# Ajustar layout
plt.tight_layout()

# Exibir o gráfico
plt.show()

# Imprimir informações adicionais
print("Distribuição Normal Padrão N(0,1)")
print("=" * 40)
print("\nPorcentagens exatas:")
for sigma in [1, 2, 3]:
    prob = stats.norm.cdf(sigma) - stats.norm.cdf(-sigma)
    print(f"P(-{sigma}σ ≤ Z ≤ +{sigma}σ) = {prob:.4f} = {prob:.2%}")

print("\nValores da função densidade:")
for z in [-3, -2, -1, 0, 1, 2, 3]:
    density = stats.norm.pdf(z, 0, 1)
    print(f"f({z}) = {density:.4f}")
