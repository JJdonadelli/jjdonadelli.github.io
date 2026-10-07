import numpy as np
import matplotlib.pyplot as plt
import random

def passeio_aleatorio_simples(n_passos):
    """
    Gera um passeio aleatório simples com n_passos.
    Em cada passo, move +1 ou -1 com probabilidade igual.
    """
    # Gera os passos aleatórios (+1 ou -1)
    passos = np.random.choice([-1, 1], size=n_passos)
    
    # Calcula a posição acumulada (começando em 0)
    posicao = np.cumsum(np.concatenate(([0], passos)))
    
    return posicao

def plotar_passeio_aleatorio(n_passos=50, n_simulacoes=2):
    """
    Plota dois passeios aleatórios simples discretos com cores diferentes,
    junto com as funções √x e -√x para comparação.
    """
    plt.figure(figsize=(12, 8))
    
    # Cores para os dois passeios
    cores = ['blue', 'red' , 'orange']
    
    for i in range(n_simulacoes):
        posicoes = passeio_aleatorio_simples(n_passos)
        tempo = np.arange(len(posicoes))
        cor = cores[i]
        
        # Linha conectora
        plt.plot(tempo, posicoes, '-', color=cor, linewidth=1.5, alpha=0.7, 
                label=f'Passeio {i+1}')
        # Pontos destacados
        plt.scatter(tempo, posicoes, c=cor, s=25, alpha=0.9, zorder=5, 
                   edgecolors='white', linewidth=0.5)
    
    # Adicionar as funções √x e -√x
    x = np.arange(0, n_passos + 1)
    y_pos = np.sqrt(x)
    y_neg = -np.sqrt(x)

    y_pos2 = np.sqrt(x) *2
    y_neg2 = -np.sqrt(x) *2

    y_pos3 = np.sqrt(x) *3
    y_neg3 = -np.sqrt(x) *3
    
    plt.plot(x, y_pos, 'lightgray', linewidth=1.5, alpha=0.8, label='√n', linestyle='-')
    plt.plot(x, y_neg, 'lightgray', linewidth=1.5, alpha=0.8, linestyle='-')

    plt.plot(x, y_pos2, 'darkgray', linewidth=1.5, alpha=0.8, label='2√n', linestyle='-')
    plt.plot(x, y_neg2, 'darkgray', linewidth=1.5, alpha=0.8, linestyle='-')

    plt.plot(x, y_pos3, 'black', linewidth=2, alpha=0.8, label='3√n', linestyle='-')
    plt.plot(x, y_neg3, 'black', linewidth=2, alpha=0.8,  linestyle='-')

    
    plt.title(fr'{ n_simulacoes} Passeios Aleatório $\times$ desvios-padrão ({n_passos} passos)', fontsize=16)
    plt.xlabel('Tempo (número de passos)', fontsize=12)
    plt.ylabel('Posição', fontsize=12)
    plt.grid(True, alpha=0.3)
#    plt.axhline(y=0, color='black', linestyle='--', alpha=0.5, label='Posição inicial')
    
    # Legenda
    plt.legend(loc='best', framealpha=0.9)
    
    plt.tight_layout()
    plt.show()

# Executar o gráfico
# print("Dois passeios aleatórios DISCRETOS com 50 passos...")
for _ in range (1,10): plotar_passeio_aleatorio(n_passos=3000, n_simulacoes=3)
