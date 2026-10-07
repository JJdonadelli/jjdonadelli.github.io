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

def plotar_passeio_aleatorio(n_passos=1000, n_simulacoes=1, discreto=True):
    """
    Plota um ou múltiplos passeios aleatórios simples.
    Se discreto=True, mostra cada passo como pontos individuais.
    """
    plt.figure(figsize=(12, 8))
    
    for i in range(n_simulacoes):
        posicoes = passeio_aleatorio_simples(n_passos)
        tempo = np.arange(len(posicoes))
        
        if discreto:
            if n_simulacoes == 1:
                # Para um único passeio, mostra pontos conectados e destacados
#                plt.plot(tempo, posicoes, 'b-', linewidth=1, alpha=0.7, label='Trajetória')
                plt.scatter(tempo, posicoes, c='blue', s=20, alpha=0.8, zorder=5)
                plt.xticks(range(min(tempo), max(tempo)+1))
            else:
                # Para múltiplos passeios, só pontos menores para não poluir
                cores = plt.cm.tab10(i / min(n_simulacoes, 10))
                plt.scatter(tempo, posicoes, s=8, alpha=0.6, c=[cores])
        else:
            # Modo contínuo (linha apenas)
            if n_simulacoes == 1:
                plt.plot(tempo, posicoes, 'b-', linewidth=1.5, alpha=0.8)
            else:
                plt.plot(tempo, posicoes, linewidth=1, alpha=0.6)
    
    modo = "Discreto" if discreto else "Contínuo"
    plt.title(f'Passeio Aleatório Simples ({modo}) - {n_passos} passos', fontsize=16)
    plt.xlabel('Tempo (número de passos)', fontsize=12)
    plt.ylabel('Posição', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.axhline(y=0, color='r', linestyle='--', alpha=0.5, label='Posição inicial')
    
    if n_simulacoes == 1 and discreto:
        plt.legend()
    elif n_simulacoes > 1:
        plt.legend([f'{n_simulacoes} simulações', 'Posição inicial'])
    else:
        plt.legend(['Trajetória', 'Posição inicial'])
    
    plt.tight_layout()
    plt.show()

def plotar_comparacao_discreto_continuo(n_passos=50):
    """
    Compara visualização discreta vs contínua do mesmo passeio aleatório.
    """
    # Gera um único passeio para comparar
    np.random.seed(42)  # Para reprodutibilidade
    posicoes = passeio_aleatorio_simples(n_passos)
    tempo = np.arange(len(posicoes))
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Gráfico discreto
    ax1.scatter(tempo, posicoes, c='blue', s=40, alpha=0.8, zorder=5, label='Posições')
    ax1.plot(tempo, posicoes, 'b-', linewidth=1, alpha=0.5)
    ax1.set_title(f'Passeio Aleatório DISCRETO\n({n_passos} passos)', fontsize=14)
    ax1.set_xlabel('Tempo (passos discretos)', fontsize=12)
    ax1.set_ylabel('Posição', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    ax1.legend()
    
    # Destacar alguns pontos específicos
    for i in range(0, len(tempo), max(1, len(tempo)//10)):
        ax1.annotate(f't={i}', 
                    xy=(tempo[i], posicoes[i]), 
                    xytext=(5, 5), 
                    textcoords='offset points',
                    fontsize=8, alpha=0.7)
    
    # Gráfico contínuo (para comparação)
    ax2.plot(tempo, posicoes, 'b-', linewidth=2, alpha=0.8, label='Trajetória')
    ax2.set_title(f'Mesma Trajetória CONTÍNUA\n(para comparação)', fontsize=14)
    ax2.set_xlabel('Tempo', fontsize=12)
    ax2.set_ylabel('Posição', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    ax2.legend()
    
    plt.tight_layout()
    plt.show()

def analisar_passeio_aleatorio(n_passos=1000, n_simulacoes=100, discreto=True):
    """
    Analisa propriedades estatísticas de múltiplos passeios aleatórios.
    Se discreto=True, usa visualização discreta quando apropriado.
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
    exemplo_tempo = np.arange(len(exemplo_posicoes))
    
    if discreto and n_passos <= 200:  # Só mostra pontos se não for muitos passos
        ax1.scatter(exemplo_tempo, exemplo_posicoes, c='blue', s=15, alpha=0.8, zorder=5)
        ax1.plot(exemplo_tempo, exemplo_posicoes, 'b-', linewidth=1, alpha=0.6)
    else:
        ax1.plot(exemplo_tempo, exemplo_posicoes, 'b-', linewidth=1.5)
    
    modo = "Discreto" if discreto else "Contínuo"
    ax1.set_title(f'Exemplo de Passeio Aleatório ({modo})')
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

# 1. Gráfico discreto de um passeio aleatório (poucos passos para ver claramente)
print("1. Passeio aleatório DISCRETO com 50 passos...")
plotar_passeio_aleatorio(n_passos=50, n_simulacoes=1, discreto=True)

# 2. DOIS passeios aleatórios DISCRETOS no mesmo gráfico (com cores diferentes)
print("\n2. DOIS passeios aleatórios discretos com cores diferentes...")
plotar_passeio_aleatorio(n_passos=50, n_simulacoes=2, discreto=True)

# 3. Comparação visual: discreto vs contínuo
print("\n3. Comparação: mesmo passeio em formato discreto e contínuo...")
plotar_comparacao_discreto_continuo(n_passos=30)

# 4. Múltiplos passeios discretos (3 passeios com cores diferentes)
print("\n4. Três passeios aleatórios discretos...")
plotar_passeio_aleatorio(n_passos=100, n_simulacoes=3, discreto=True)

# 5. Cinco passeios discretos sobrepostos
print("\n5. Cinco passeios aleatórios discretos...")
plotar_passeio_aleatorio(n_passos=100, n_simulacoes=5, discreto=True)

# 6. Passeio mais longo (discreto, mas sem destacar cada ponto individual)
print("\n6. Passeio discreto mais longo (1000 passos)...")
plotar_passeio_aleatorio(n_passos=1000, n_simulacoes=1, discreto=False)

# 7. Análise completa no modo discreto
print("\n7. Análise estatística completa (modo discreto)...")
analisar_passeio_aleatorio(n_passos=200, n_simulacoes=100, discreto=True)
