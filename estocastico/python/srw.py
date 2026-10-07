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

def plotar_passeio_aleatorio(n_passos=1000, n_simulacoes=1):
    """
    Plota um ou múltiplos passeios aleatórios simples.
    """
    plt.figure(figsize=(12, 8))
    
    for i in range(n_simulacoes):
        posicoes = passeio_aleatorio_simples(n_passos)
        tempo = np.arange(len(posicoes))
        
        if n_simulacoes == 1:
            plt.plot(tempo, posicoes, 'b-', linewidth=1.5, alpha=0.8)
        else:
            plt.plot(tempo, posicoes, linewidth=1, alpha=0.6)
    
    plt.title(f'Passeio Aleatório Simples - {n_passos} passos', fontsize=16)
    plt.xlabel('Tempo (número de passos)', fontsize=12)
    plt.ylabel('Posição', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='r', linestyle='--', alpha=0.5, label='Posição inicial')
    
    if n_simulacoes > 1:
        plt.legend([f'{n_simulacoes} simulações', 'Posição inicial'])
    else:
        plt.legend(['Trajetória', 'Posição inicial'])
    
    plt.tight_layout()
    plt.show()

def analisar_passeio_aleatorio(n_passos=1000, n_simulacoes=100):
    """
    Analisa propriedades estatísticas de múltiplos passeios aleatórios.
    """
    posicoes_finais = []
    distancias_maximas = []
    
    for _ in range(n_simulacoes):
        posicoes = passeio_aleatorio_simples(n_passos)
        posicoes_finais.append(posicoes[-1])
        distancias_maximas.append(np.max(np.abs(posicoes)))
    
    # Cria subplots para análise
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 10))
    
    # 1. Exemplo de um único passeio
    exemplo_posicoes = passeio_aleatorio_simples(n_passos)
    ax1.plot(exemplo_posicoes, 'b-', linewidth=1.5)
    ax1.set_title('Exemplo de um Passeio Aleatório')
    ax1.set_xlabel('Passos')
    ax1.set_ylabel('Posição')
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    
    # 2. Distribuição das posições finais
    ax2.hist(posicoes_finais, bins=30, alpha=0.7, color='green', edgecolor='black')
    ax2.set_title(f'Distribuição das Posições Finais\n({n_simulacoes} simulações)')
    ax2.set_xlabel('Posição Final')
    ax2.set_ylabel('Frequência')
    ax2.axvline(x=0, color='r', linestyle='--', alpha=0.5)
    ax2.grid(True, alpha=0.3)
    
    # 3. Distribuição das distâncias máximas
    ax3.hist(distancias_maximas, bins=30, alpha=0.7, color='orange', edgecolor='black')
    ax3.set_title('Distribuição das Distâncias Máximas')
    ax3.set_xlabel('Distância Máxima da Origem')
    ax3.set_ylabel('Frequência')
    ax3.grid(True, alpha=0.3)
    
    # 4. Múltiplos passeios sobrepostos
    for i in range(min(20, n_simulacoes)):
        posicoes = passeio_aleatorio_simples(n_passos)
        ax4.plot(posicoes, alpha=0.4, linewidth=0.8)
    
    ax4.set_title(f'Sobreposição de {min(20, n_simulacoes)} Passeios Aleatórios')
    ax4.set_xlabel('Passos')
    ax4.set_ylabel('Posição')
    ax4.grid(True, alpha=0.3)
    ax4.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.show()
    
    # Estatísticas
    print(f"\n=== ESTATÍSTICAS DO PASSEIO ALEATÓRIO ===")
    print(f"Número de passos: {n_passos}")
    print(f"Número de simulações: {n_simulacoes}")
    print(f"\nPosições finais:")
    print(f"  Média: {np.mean(posicoes_finais):.2f}")
    print(f"  Desvio padrão: {np.std(posicoes_finais):.2f}")
    print(f"  Valor esperado teórico do desvio padrão: {np.sqrt(n_passos):.2f}")
    print(f"\nDistâncias máximas:")
    print(f"  Média: {np.mean(distancias_maximas):.2f}")
    print(f"  Máximo absoluto: {np.max(distancias_maximas)}")

# Exemplos de uso:

# 1. Gráfico simples de um passeio aleatório
print("1. Plotando um único passeio aleatório com 1000 passos...")
plotar_passeio_aleatorio(n_passos=1000, n_simulacoes=1)

# 2. Múltiplos passeios aleatórios
print("\n2. Plotando 5 passeios aleatórios sobrepostos...")
plotar_passeio_aleatorio(n_passos=1000, n_simulacoes=5)

# 3. Análise completa
print("\n3. Análise estatística completa...")
analisar_passeio_aleatorio(n_passos=1000, n_simulacoes=100)
