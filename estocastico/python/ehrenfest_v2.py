import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from math import comb
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(
    page_title="Modelo de Ehrenfest",
    page_icon="⚪",
    layout="wide"
)

# Título e descrição
st.title("🔄 Modelo de Ehrenfest - Simulação Interativa")
st.markdown("""
O **Modelo de Ehrenfest** simula a transferência de bolas entre duas urnas, representando um processo estocástico que 
demonstra como sistemas físicos evoluem para o equilíbrio estatístico.

**Como funciona:**
- Temos N bolas distribuídas entre duas urnas (A e B)
- A cada passo, escolhemos uma urna com probabilidade proporcional ao número de bolas nela
- Transferimos uma bola dessa urna para a outra
""")

# Sidebar para parâmetros
st.sidebar.header("⚙️ Parâmetros da Simulação")

N = st.sidebar.slider("Número total de bolas (N)", 10, 100, 50, help="Total de bolas no sistema")
T = st.sidebar.slider("Número de passos (T)", 1000, 50000, 10000, step=1000, help="Duração da simulação")
X0 = st.sidebar.slider("Estado inicial", 0, N, N, help="Número inicial de bolas na urna A")

# Botão para executar simulação
if st.sidebar.button("🎲 Executar Simulação", type="primary"):
    
    # Barra de progresso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Simulação
    status_text.text("Executando simulação...")
    X = np.zeros(T+1, dtype=int)
    X[0] = X0
    
    for t in range(T):
        k = X[t]
        # Com probabilidade k/N tiramos da urna A
        if np.random.rand() < k / N:
            X[t+1] = k - 1
        else:
            X[t+1] = k + 1
        
        # Atualizar barra de progresso a cada 1000 passos
        if t % 1000 == 0:
            progress_bar.progress(t / T)
    
    progress_bar.progress(1.0)
    status_text.text("Simulação concluída!")
    
    # Armazenar resultados no session_state
    st.session_state.X = X
    st.session_state.N = N
    st.session_state.T = T
    st.session_state.simulation_done = True

# Verificar se existe simulação nos resultados
if hasattr(st.session_state, 'simulation_done') and st.session_state.simulation_done:
    
    X = st.session_state.X
    N_sim = st.session_state.N
    T_sim = st.session_state.T
    
    # Layout em colunas
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📈 Trajetória no Tempo")
        
        # Controle para número de passos a mostrar
        max_steps = st.slider("Mostrar primeiros X passos", 100, min(T_sim, 5000), min(2000, T_sim))
        
        # Criar gráfico da trajetória
        fig_traj = go.Figure()
        fig_traj.add_trace(go.Scatter(
            x=list(range(max_steps)),
            y=X[:max_steps],
            mode='lines',
            name='Trajetória',
            line=dict(color='blue', width=1)
        ))
        fig_traj.add_hline(
            y=N_sim/2, 
            line_dash="dash", 
            line_color="red",
            annotation_text="Equilíbrio (N/2)"
        )
        fig_traj.update_layout(
            title=f"Trajetória do Modelo de Ehrenfest (primeiros {max_steps} passos)",
            xaxis_title="Tempo",
            yaxis_title="Número de bolas na urna A",
            height=400
        )
        st.plotly_chart(fig_traj, use_container_width=True)
    
    with col2:
        st.subheader("📊 Estatísticas")
        
        # Calcular estatísticas
        mean_val = np.mean(X)
        std_val = np.std(X)
        min_val = np.min(X)
        max_val = np.max(X)
        
        # Tempo de primeira chegada ao equilíbrio (se houver)
        equilibrium = N_sim // 2
        eq_times = np.where(X == equilibrium)[0]
        first_eq_time = eq_times[0] if len(eq_times) > 0 else "Não atingido"
        
        st.metric("Média", f"{mean_val:.2f}")
        st.metric("Desvio Padrão", f"{std_val:.2f}")
        st.metric("Mínimo", min_val)
        st.metric("Máximo", max_val)
        st.metric("1º Equilíbrio", first_eq_time)
        
        # Porcentagem de tempo próximo ao equilíbrio
        near_equilibrium = np.sum(np.abs(X - N_sim/2) <= 2) / len(X) * 100
        st.metric("% Próximo ao equilíbrio (±2)", f"{near_equilibrium:.1f}%")
    
    # Distribuição empírica vs teórica
    st.subheader("📊 Distribuição Empírica vs Teórica")
    
    # Calcular distribuições
    counts = Counter(X)
    empirical_probs = np.array([counts[k] / (T_sim+1) for k in range(N_sim+1)])
    theoretical_probs = np.array([comb(N_sim, k) * (0.5**N_sim) for k in range(N_sim+1)])
    
    # Criar DataFrame para o gráfico
    df_dist = pd.DataFrame({
        'k': list(range(N_sim+1)),
        'Empírica': empirical_probs,
        'Teórica (Binomial)': theoretical_probs
    })
    
    # Gráfico de barras comparativo
    fig_dist = go.Figure()
    fig_dist.add_trace(go.Bar(
        x=df_dist['k'],
        y=df_dist['Empírica'],
        name='Simulação',
        opacity=0.7,
        marker_color='lightblue'
    ))
    fig_dist.add_trace(go.Scatter(
        x=df_dist['k'],
        y=df_dist['Teórica (Binomial)'],
        mode='lines+markers',
        name='Distribuição Binomial(N, 1/2)',
        line=dict(color='red', width=2, dash='dash')
    ))
    fig_dist.update_layout(
        title=f"Distribuição empírica vs teórica (N={N_sim}, T={T_sim})",
        xaxis_title="Número de bolas na urna A",
        yaxis_title="Probabilidade",
        height=500
    )
    st.plotly_chart(fig_dist, use_container_width=True)
    
    # Análise adicional
    st.subheader("🔍 Análise Adicional")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.subheader("Histograma de Estados")
        # Histograma dos estados visitados
        fig_hist = px.histogram(
            x=X, 
            nbins=min(50, N_sim+1),
            title="Frequência dos Estados Visitados",
            labels={'x': 'Número de bolas na urna A', 'y': 'Frequência'}
        )
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col4:
        st.subheader("Função de Autocorrelação")
        # Calcular autocorrelação para os primeiros lags
        max_lag = min(100, len(X)//10)
        autocorr = [np.corrcoef(X[:-lag], X[lag:])[0,1] if lag > 0 else 1.0 for lag in range(max_lag)]
        
        fig_autocorr = go.Figure()
        fig_autocorr.add_trace(go.Scatter(
            x=list(range(max_lag)),
            y=autocorr,
            mode='lines+markers',
            name='Autocorrelação'
        ))
        fig_autocorr.update_layout(
            title="Função de Autocorrelação",
            xaxis_title="Lag",
            yaxis_title="Correlação"
        )
        st.plotly_chart(fig_autocorr, use_container_width=True)
    
    # Opção para download dos dados
    st.subheader("💾 Download dos Dados")
    
    # Criar DataFrame com os resultados
    results_df = pd.DataFrame({
        'Tempo': range(len(X)),
        'Bolas_Urna_A': X,
        'Bolas_Urna_B': N_sim - X
    })
    
    csv = results_df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"ehrenfest_simulation_N{N_sim}_T{T_sim}.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Configure os parâmetros na barra lateral e clique em 'Executar Simulação' para começar!")
    
    # Mostrar exemplo teórico
    st.subheader("📚 Teoria do Modelo de Ehrenfest")
    st.markdown("""
    **Propriedades teóricas:**
    
    - **Estado estacionário**: Distribuição Binomial(N, 1/2)
    - **Média de equilíbrio**: N/2
    - **Variância de equilíbrio**: N/4
    - **Tempo de relaxação**: Aproximadamente N passos
    
    **Interpretação física:**
    O modelo representa a difusão molecular entre dois compartimentos, demonstrando como 
    sistemas isolados evoluem naturalmente para estados de máxima entropia.
    """)

# Sidebar com informações adicionais
st.sidebar.markdown("---")
st.sidebar.subheader("ℹ️ Sobre o Modelo")
st.sidebar.markdown("""
**Modelo de Ehrenfest (1907)**

Desenvolvido pelos físicos Paul e Tatiana Ehrenfest para ilustrar conceitos da mecânica estatística, especialmente:

- Irreversibilidade macroscópica
- Equilíbrio estatístico  
- Teorema H de Boltzmann
- Paradoxo da reversibilidade

**Aplicações:**
- Física estatística
- Teoria de filas
- Dinâmica populacional
- Processos de difusão
""")
