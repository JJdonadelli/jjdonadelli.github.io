import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="Algoritmo PageRank", page_icon="🔍", layout="wide")

# Título
st.title("🔍 Algoritmo PageRank")


# Função para calcular PageRank
def calculate_pagerank(edges, num_nodes, alpha):
    N = num_nodes
    
    if len(edges) == 0:
        v = np.ones(N) / N
        return v ,  [v.copy()]
    
    # Criar matriz de adjacência
    A = np.zeros((N, N))
    for from_node, to_node in edges:
        A[from_node - 1][to_node - 1] = 1
    
    # Criar matriz de probabilidade de transição (P)
    P = np.zeros((N, N))
    for i in range(N):
        row_sum = np.sum(A[i, :])
        for j in range(N):
            if row_sum > 0:
                P[i, j] = A[i, j] / row_sum
            else:
                P[i, j] = 1 / N
    
    # Criar matriz Google (G)
    G = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            G[i, j] = alpha * P[i, j] + (1 - alpha) / N
    
    # Método das potências
    v = np.ones(N) / N
    history = [v.copy()]
    for _ in range(100):
        v = G.T @ v
        v = v / np.sum(v)
        history.append(v.copy())
        
    
    return v , history

# Função para desenhar o grafo
def draw_graph(edges, num_nodes, pagerank_values):
    G = nx.DiGraph()
    G.add_nodes_from(range(1, num_nodes + 1))
    G.add_edges_from(edges)
    
    # Layout circular
    pos = nx.circular_layout(G)
    
    # Tamanhos dos nós baseados no PageRank
    node_sizes = [pr * 10000 for pr in pagerank_values]
    
    # Criar figura com fundo branco
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
    ax.set_facecolor('white')
    
    # Desenhar arestas com setas MUITO visíveis
    # IMPORTANTE: As setas vão de i -> j (origem para destino)
    nx.draw_networkx_edges(G, pos, 
                          edge_color='#34495e',        # Cor mais escura
                          arrows=True,                 # Ativar setas
                          arrowsize=30,                # Seta bem grande
                          arrowstyle='->',             # Seta simples e clara
                          width=3,                     # Linha bem grossa
                          node_size=node_sizes,        # Respeita tamanho dos nós
                          connectionstyle='arc3,rad=0.15',  # Curvatura para ver melhor
                          min_source_margin=20,        # Espaço da origem
                          min_target_margin=20,        # Espaço do destino
                          alpha=0.8,
                          ax=ax)
    
    # Desenhar nós POR CIMA das arestas
    nx.draw_networkx_nodes(G, pos, 
                          node_size=node_sizes, 
                          node_color='#3498db',        # Azul
                          alpha=0.95, 
                          edgecolors='#2c3e50',        # Borda escura
                          linewidths=4,                # Borda bem grossa
                          ax=ax)
    
    # Desenhar labels POR CIMA de tudo
    nx.draw_networkx_labels(G, pos, 
                           font_size=16,               # Fonte maior
                           font_color='white', 
                           font_weight='bold',
                           font_family='sans-serif',
                           ax=ax)
    
    # Título e informação
    title = f"Visualização do Grafo Direcionado\n"
    title += f"(Tamanho dos nós ∝ PageRank | Setas: origem → destino)"
    ax.set_title(title, fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    plt.tight_layout()
    
    return fig

# Sidebar - Configurações
st.sidebar.header("⚙️ Configurações")

# Seleção do grafo
graph_type = st.sidebar.selectbox(
    "Selecione o Grafo:",
    ["Exemplo da aula", "Exemplo 1 - Notebook", "Exemplo 2 - Assimétrico", "Exemplo Simples", "Personalizado"]
)

# Parâmetro alpha
alpha = st.sidebar.slider(
    "Parâmetro α (damping factor):",
    min_value=0.01,
    max_value=0.99,
    value=0.85,
    step=0.01,
    help="Probabilidade de seguir um link vs. saltar para página aleatória"
)

# Definir grafos de exemplo
if graph_type == "Exemplo da aula":
    num_nodes = 6
    edges = [(1,2), (1,3), (2,1), (2,3), (3,1), (3,2), (4,1), (4,5), (4,6), (5,3), (5,4), (5,6)]

elif graph_type == "Exemplo 1 - Notebook":
    num_nodes = 6
    edges = [(1,2), (1,3), (3,1), (3,2), (3,5), (5,4), (5,6), (4,5), (4,6), (6,4)]
    
elif graph_type == "Exemplo 2 - Assimétrico":
    num_nodes = 10
    edges = [(1,2), (3,2), (4,2), (5,2), (2,10), (10,9), (9,8), (8,7), 
             (7,6), (6,9), (9,7), (9,6), (8,6)]
    
elif graph_type == "Exemplo Simples":
    num_nodes = 4
    edges = [(1,2), (2,3), (3,4), (4,1), (1,3)]
    
else:  # Personalizado
    st.sidebar.markdown("---")
    st.sidebar.subheader("✏️ Editor de Grafo")
    
    num_nodes = st.sidebar.slider("Número de Vértices:", 2, 15, 6)
    
    st.sidebar.markdown("**Adicionar Arestas:**")
    col1, col2 = st.sidebar.columns(2)
    from_node = col1.number_input("De:", 1, num_nodes, 1)
    to_node = col2.number_input("Para:", 1, num_nodes, 2)
    
    # Inicializar edges no session_state
    if 'custom_edges' not in st.session_state:
        st.session_state.custom_edges = []
    
    col_add, col_clear = st.sidebar.columns(2)
    if col_add.button("➕ Adicionar"):
        if (from_node, to_node) not in st.session_state.custom_edges:
            st.session_state.custom_edges.append((from_node, to_node))
    
    if col_clear.button("🗑️ Limpar"):
        st.session_state.custom_edges = []
    
    # Área de texto para edição direta
    edges_text = st.sidebar.text_area(
        "Editar arestas (formato: de,para por linha):",
        value="\n".join([f"{e[0]},{e[1]}" for e in st.session_state.custom_edges]),
        height=150
    )
    
    # Atualizar edges do texto
    try:
        edges = []
        for line in edges_text.strip().split('\n'):
            if line.strip():
                parts = line.split(',')
                if len(parts) == 2:
                    f, t = int(parts[0].strip()), int(parts[1].strip())
                    if 1 <= f <= num_nodes and 1 <= t <= num_nodes:
                        edges.append((f, t))
        st.session_state.custom_edges = edges
    except:
        edges = st.session_state.custom_edges

# Calcular PageRank
pagerank_values , history = calculate_pagerank(edges, num_nodes, alpha)

# Layout principal
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 Informações do Grafo")
    info_col1, info_col2 = st.columns(2)
    info_col1.metric("Vértices", num_nodes)
    info_col2.metric("Arestas", len(edges))
    
    st.markdown("---")
    
    # Tabela de resultados
    st.subheader("🎯 Ranking dos Vértices")
    results_df = pd.DataFrame({
        'Vértice': range(1, num_nodes + 1),
        'PageRank': pagerank_values,
        'Percentual (%)': pagerank_values * 100
    })
    results_df = results_df.sort_values('PageRank', ascending=False).reset_index(drop=True)
    results_df.index = results_df.index + 1
    results_df.index.name = 'Posição'
    
    st.dataframe(
        results_df.style.format({
            'PageRank': '{:.6f}',
            'Percentual (%)': '{:.2f}'
        }).background_gradient(subset=['PageRank'], cmap='Blues'),
        use_container_width=True
    )
    
    # Gráfico de barras
    st.subheader("📈 PageRank dos Vértices")
    chart_data = pd.DataFrame({
        'Vértice': [f"V{i}" for i in range(1, num_nodes + 1)],
        'PageRank': pagerank_values
    })
    st.bar_chart(chart_data.set_index('Vértice'))
    # Gráfico de convergência
    st.subheader("🔄 Convergência do PageRank")
    history_array = np.array(history)
    fig_convergence, ax_convergence = plt.subplots(figsize=(8, 5))
    for i in range(num_nodes):
        ax_convergence.plot(history_array[:, i], label=f"Página {i+1}", linewidth=2)
    ax_convergence.set_xlabel("Iteração", fontsize=12)
    ax_convergence.set_ylabel("Probabilidade", fontsize=12)
    ax_convergence.set_title(f"Convergência do PageRank (α={alpha})", fontsize=14, fontweight='bold')
    ax_convergence.legend(loc='best', fontsize=9)
    ax_convergence.grid(True, alpha=0.3)
    plt.tight_layout()
    st.pyplot(fig_convergence)

with col2:
    st.subheader("🕸️ Visualização do Grafo")
    if len(edges) > 0:
        fig = draw_graph(edges, num_nodes, pagerank_values)
        st.pyplot(fig)
    else:
        st.warning("⚠️ Adicione arestas ao grafo para visualizar")

# Informações adicionais
st.markdown("---")
st.info("""
💡 **Sobre o PageRank:**

O [PageRank](http://ilpubs.stanford.edu:8090/422/1/1999-66.pdf) é um algoritmo usado pelo Google para classificar páginas da web. 
Ele funciona modelando o comportamento de um navegador aleatório que clica em links 
com probabilidade α ou salta para uma página aleatória com probabilidade (1-α).

""")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #7f8c8d;'>
        <p>Introdução aos Processos Estocásticos --- UFABC</p>
    </div>
    """,
    unsafe_allow_html=True
)