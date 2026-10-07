import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.animation import FuncAnimation
import time
import random

# Configuração da página
st.set_page_config(
    page_title="Galton Board Simulator",
    page_icon="🎯",
    layout="wide"
)

# Título principal
st.title("Simulador do Galton Board")
# st.markdown("*Também conhecido como Bean Machine ou Quincunx*")

# Descrição
with st.expander("ℹ️ Sobre o Galton Board"):
    st.markdown("""
    O **Galton Board** foi inventado por Francis Galton para demonstrar o **Teorema Central do Limite**.
    
    **Como funciona:**
    - Bolinhas são soltas do topo
    - Em cada pino, a bolinha pode ir para esquerda ou direita (50% cada)
    - As bolinhas se acumulam em compartimentos na base
    - Com muitas bolinhas, forma-se uma **distribuição normal** (curva de sino)
    
    """)

# Sidebar com controles
st.sidebar.header("🎛️ Controles da Simulação")

# Parâmetros da simulação
n_levels = st.sidebar.slider("Número de níveis de pinos", 5, 15, 10)
n_balls = st.sidebar.slider("Número de bolinhas", 100, 5000, 1000)
speed = st.sidebar.selectbox("Velocidade da simulação", 
                            ["Muito Lenta", "Lenta", "Normal", "Rápida", "Muito Rápida"],
                            index=2)

# Mapear velocidade para valores
speed_map = {
    "Muito Lenta": 0.1,
    "Lenta": 0.05,
    "Normal": 0.02,
    "Rápida": 0.01,
    "Muito Rápida": 0.005
}
delay = speed_map[speed]

# Botões de controle
col1, col2, col3 = st.sidebar.columns(3)
with col1:
    run_simulation = st.button("▶️ Simular")
with col2:
    reset_button = st.button("🔄 Reset")
with col3:
    show_theory = st.button("📊 Teoria")

# Classe para simular o Galton Board
class GaltonBoard:
    def __init__(self, levels, n_balls):
        self.levels = levels
        self.n_balls = n_balls
        self.bins = levels + 1
        self.results = np.zeros(self.bins)
        self.paths = []
        
    def simulate_single_ball(self):
        """Simula o caminho de uma única bolinha"""
        position = 0
        path = [0]
        
        for level in range(self.levels):
            # 50% chance para esquerda ou direita
            if random.random() < 0.5:
                position -= 0.5
            else:
                position += 0.5
            path.append(position)
        
        # Converter para índice do compartimento (0 a bins-1)
        final_bin = int(position + self.levels / 2)
        final_bin = max(0, min(self.bins - 1, final_bin))
        
        return final_bin, path
    
    def run_simulation(self):
        """Executa a simulação completa"""
        self.results = np.zeros(self.bins)
        self.paths = []
        
        for i in range(self.n_balls):
            bin_index, path = self.simulate_single_ball()
            self.results[bin_index] += 1
            # Armazenar mais caminhos para visualização
            if i < 100:  # Armazenar os primeiros 100 caminhos
                self.paths.append(path)
    
    def get_theoretical_distribution(self):
        """Calcula a distribuição teórica (binomial normalizada)"""
        from scipy.stats import binom
        n = self.levels
        p = 0.5
        x = np.arange(self.bins)
        theoretical = binom.pmf(x, n, p) * self.n_balls
        return theoretical

# Inicializar estado da sessão
if 'galton_board' not in st.session_state:
    st.session_state.galton_board = None
if 'simulation_done' not in st.session_state:
    st.session_state.simulation_done = False

# Reset
if reset_button:
    st.session_state.galton_board = None
    st.session_state.simulation_done = False
    st.rerun()

        # Criar layout principal
main_col, stats_col = st.columns([2, 1])

with main_col:
    st.subheader("🎲 Simulação")
    
    if run_simulation:
        # Criar nova instância do Galton Board
        st.session_state.galton_board = GaltonBoard(n_levels, n_balls)
        
        # Placeholder para mostrar progresso
        progress_bar = st.progress(0)
        status_text = st.empty()
        chart_placeholder = st.empty()
        
        # Executar simulação com visualização em tempo real
        st.session_state.galton_board.results = np.zeros(st.session_state.galton_board.bins)
        
        for i in range(n_balls):
            # Simular uma bolinha
            bin_index, _ = st.session_state.galton_board.simulate_single_ball()
            st.session_state.galton_board.results[bin_index] += 1
            
            # Atualizar visualização a cada 100 bolinhas ou na última
            if i % max(1, n_balls // 50) == 0 or i == n_balls - 1:
                progress = (i + 1) / n_balls
                progress_bar.progress(progress)
                status_text.text(f'Bolinhas simuladas: {i + 1}/{n_balls}')
                
                # Criar gráfico combinado com tabuleiro e histograma
                fig, (ax_board, ax_hist) = plt.subplots(2, 1, figsize=(12, 10), 
                                                       gridspec_kw={'height_ratios': [1.2, 1]})
                
                # ===== TABULEIRO SUPERIOR =====
                # Calcular dimensões proporcionais ao número de compartimentos
                board_width = len(st.session_state.galton_board.results)
                compartment_width = 0.8  # Largura de cada compartimento
                pin_spacing = compartment_width  # Espaçamento entre pinos igual à largura dos compartimentos
                
                # Desenhar funil de entrada
                funnel_top = n_levels + 1
                ax_board.plot([-0.2, 0, 0.2], [funnel_top, funnel_top-0.2, funnel_top], 
                             'k-', linewidth=3)
                ax_board.plot([0], [funnel_top+0.1], 'ro', markersize=8, label='Entrada de bolinhas')
                
                # Desenhar os pinos em formato triangular - PROPORCIONAL AO GRÁFICO
                for level in range(n_levels):
                    y = n_levels - level - 0.5
                    n_pins = level + 1
                    # Centralizar os pinos com base no número de compartimentos
                    start_pos = -(level * pin_spacing) / 2
                    for pin in range(n_pins):
                        x = start_pos + (pin * pin_spacing)
                        ax_board.plot(x, y, 'ko', markersize=10, markerfacecolor='gray', 
                                     markeredgecolor='black', markeredgewidth=2)
                
                # Desenhar paredes laterais proporcionais
                wall_height = n_levels + 0.5
                wall_left = -(board_width * compartment_width) / 2 - 0.2
                wall_right = (board_width * compartment_width) / 2 + 0.2
                # ax_board.plot([wall_left, wall_left], [-0.3, wall_height], 'k-', linewidth=3)
                # ax_board.plot([wall_right, wall_right], [-0.3, wall_height], 'k-', linewidth=3)
                
                # Desenhar separadores dos compartimentos - ALINHADOS COM AS BARRAS
                for comp in range(st.session_state.galton_board.bins + 2):
                    x = (comp - st.session_state.galton_board.bins/2) * compartment_width - compartment_width/2
                    ax_board.plot([x, x], [-0.3, 0.1], 'k-', linewidth=2)
                
                # Configurar eixos do tabuleiro - MESMA ESCALA DO GRÁFICO
                ax_board.set_xlim(wall_left-0.3, wall_right+0.3)
                ax_board.set_ylim(-0.5, n_levels + 1.5)
                ax_board.set_title('🎯 Galton Board - Tabuleiro com Pinos', fontsize=14, fontweight='bold')
                ax_board.set_xticks([])
                ax_board.set_yticks([])
                ax_board.spines['top'].set_visible(False)
                ax_board.spines['right'].set_visible(False)
                ax_board.spines['bottom'].set_visible(False)
                ax_board.spines['left'].set_visible(False)
                
                # # Adicionar seta indicando direção
                # ax_board.annotate('', xy=(0, 0.3), xytext=(0, 1.5),
                #                 arrowprops=dict(arrowstyle='->', lw=3, color='red'))
                # ax_board.text(0.8, 1, 'Bolinhas caem\naqui!', fontsize=9, 
                #              bbox=dict(boxstyle="round,pad=0.3", facecolor='yellow', alpha=0.7))
                
                # ===== HISTOGRAMA INFERIOR =====
                bins = np.arange(len(st.session_state.galton_board.results))
                bars = ax_hist.bar(bins, st.session_state.galton_board.results, 
                                  width=0.8, alpha=0.8, color='lightblue', edgecolor='navy', linewidth=1)
                
                # Adicionar valores no topo das barras se não for muito pequeno
                max_val = max(st.session_state.galton_board.results) if max(st.session_state.galton_board.results) > 0 else 1
                for j, bar in enumerate(bars):
                    height = bar.get_height()
                    if height > max_val * 0.05:  # Só mostrar se a barra for alta o suficiente
                        ax_hist.text(bar.get_x() + bar.get_width()/2., height + max_val*0.01,
                                   f'{int(height)}', ha='center', va='bottom', fontsize=8)
                
                ax_hist.set_title(f'📊 Distribuição das Bolinhas - {i + 1} bolinhas simuladas', 
                                 fontsize=14, fontweight='bold')
                ax_hist.set_xlabel('Compartimento', fontsize=12)
                ax_hist.set_ylabel('Número de Bolinhas', fontsize=12)
                ax_hist.grid(True, alpha=0.3)
                
                # Alinhar os eixos x - MESMA ESCALA
                ax_hist.set_xlim(-0.5, len(bins)-0.5)
                
                plt.tight_layout()
                chart_placeholder.pyplot(fig)
                plt.close()
                
                if i < n_balls - 1:
                    time.sleep(delay)
        
        progress_bar.progress(1.0)
        status_text.text('✅ Simulação concluída!')
        st.session_state.simulation_done = True
    
    # Mostrar resultado final se a simulação foi executada
    if st.session_state.galton_board is not None and st.session_state.simulation_done:
        st.subheader("📈 Análise Final")
        
        # Gráfico principal: Tabuleiro + Histograma Final
        fig, (ax_board, ax_hist) = plt.subplots(2, 1, figsize=(14, 12), 
                                               gridspec_kw={'height_ratios': [1.2, 1]})
        
        # ===== TABULEIRO SUPERIOR COM CAMINHOS =====
        # Calcular dimensões proporcionais
        board_width = len(st.session_state.galton_board.results)
        compartment_width = 0.8
        pin_spacing = compartment_width
        
        # Desenhar funil de entrada
        funnel_top = n_levels + 1
        ax_board.plot([-0.2, 0, 0.2], [funnel_top, funnel_top-0.2, funnel_top], 
                     'k-', linewidth=3)
        ax_board.plot([0], [funnel_top+0.1], 'ro', markersize=10, label='Entrada')
        
        # Desenhar os pinos - PROPORCIONAL AOS COMPARTIMENTOS
        for level in range(n_levels):
            y = n_levels - level - 0.5
            n_pins = level + 1
            start_pos = -(level * pin_spacing) / 2
            for pin in range(n_pins):
                x = start_pos + (pin * pin_spacing)
                ax_board.plot(x, y, 'ko', markersize=12, markerfacecolor='darkgray', 
                             markeredgecolor='black', markeredgewidth=2)
        
        # Desenhar paredes laterais proporcionais
        wall_height = n_levels + 0.5
        wall_left = -(board_width * compartment_width) / 2 - 0.3
        wall_right = (board_width * compartment_width) / 2 + 0.3
        # ax_board.plot([wall_left, wall_left], [-0.3, wall_height], 'k-', linewidth=4)
        # ax_board.plot([wall_right, wall_right], [-0.3, wall_height], 'k-', linewidth=4)
        
        # Desenhar separadores dos compartimentos - ALINHADOS COM BARRAS
        for comp in range(st.session_state.galton_board.bins + 2):
            x = (comp - st.session_state.galton_board.bins/2) * compartment_width - compartment_width/2
            ax_board.plot([x, x], [-0.3, 0.2], 'k-', linewidth=2)
        
        # Desenhar alguns caminhos das bolinhas - AJUSTADOS À NOVA ESCALA
        if hasattr(st.session_state.galton_board, 'paths') and st.session_state.galton_board.paths:
            colors = plt.cm.rainbow(np.linspace(0, 1, min(15, len(st.session_state.galton_board.paths))))
            for i, path in enumerate(st.session_state.galton_board.paths[:15]):
                y_coords = [n_levels + 0.5] + [n_levels - j - 0.5 for j in range(len(path)-1)]
                # Ajustar escala dos caminhos para coincidir com os pinos
                path_scaled = []
                for j, p in enumerate(path):
                    if j == 0:
                        path_scaled.append(0)  # Começa no centro
                    else:
                        # Escalar proporcionalmente ao espaçamento dos pinos
                        path_scaled.append(p * pin_spacing)
                ax_board.plot(path_scaled, y_coords, '-', alpha=0.7, linewidth=2, 
                             color=colors[i], label=f'Bolinha {i+1}' if i < 3 else "")
        
        # Adicionar bolinhas nos compartimentos (representação visual)
        for comp in range(len(st.session_state.galton_board.results)):
            if st.session_state.galton_board.results[comp] > 0:
                x_comp = (comp - st.session_state.galton_board.bins/2) * compartment_width + compartment_width/2
                # Mostrar algumas bolinhas empilhadas
                n_balls_show = min(int(st.session_state.galton_board.results[comp] / 
                                      max(st.session_state.galton_board.results) * 6), 8)
                for ball_level in range(n_balls_show):
                    y_ball = -0.2 + ball_level * 0.12
                    ax_board.plot(x_comp, y_ball, 'o', color='red', markersize=5, alpha=0.8)
        
        ax_board.set_xlim(wall_left-0.5, wall_right+0.5)
        ax_board.set_ylim(-0.8, n_levels + 1.5)
        ax_board.set_title('🎯 Galton Board Completo - Tabuleiro e Caminhos das Bolinhas', 
                          fontsize=16, fontweight='bold', pad=20)
        ax_board.set_xticks([])
        ax_board.set_yticks([])
        for spine in ax_board.spines.values():
            spine.set_visible(False)
        
        if hasattr(st.session_state.galton_board, 'paths') and st.session_state.galton_board.paths:
            ax_board.legend(loc='upper right', fontsize=8)
        
        # ===== HISTOGRAMA INFERIOR =====
        bins = np.arange(len(st.session_state.galton_board.results))
        bars = ax_hist.bar(bins, st.session_state.galton_board.results, 
                          alpha=0.8, color='lightblue', edgecolor='navy', linewidth=2)
        
        # Comparação com distribuição teórica
        try:
            from scipy.stats import binom
            theoretical = st.session_state.galton_board.get_theoretical_distribution()
            ax_hist.plot(bins, theoretical, 'ro-', linewidth=3, 
                        markersize=6, label='Distribuição Teórica (Binomial)', alpha=0.8)
            ax_hist.legend()
        except ImportError:
            pass
        
        # Adicionar valores nas barras mais altas
        max_val = max(st.session_state.galton_board.results)
        for j, bar in enumerate(bars):
            height = bar.get_height()
            if height > max_val * 0.1:  # Só nas barras mais altas
                ax_hist.text(bar.get_x() + bar.get_width()/2., height + max_val*0.01,
                           f'{int(height)}', ha='center', va='bottom', fontsize=10, fontweight='bold')
        
        ax_hist.set_title('📊 Distribuição Final das Bolinhas', fontsize=16, fontweight='bold')
        ax_hist.set_xlabel('Compartimento', fontsize=12)
        ax_hist.set_ylabel('Número de Bolinhas', fontsize=12)
        ax_hist.grid(True, alpha=0.3)
        ax_hist.set_xlim(-0.6, len(bins)-0.4)
        
        plt.tight_layout()
        st.pyplot(fig)
        
        # Gráfico adicional: Comparação teórica detalhada
        if st.checkbox("🔬 Mostrar Análise Estatística Detalhada"):
            fig2, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
            
            # Gráfico 1: Distribuição normalizada
            normalized_results = st.session_state.galton_board.results / np.sum(st.session_state.galton_board.results)
            ax1.bar(bins, normalized_results, alpha=0.7, color='lightgreen', 
                   edgecolor='darkgreen', linewidth=1, label='Simulação (Normalizada)')
            
            try:
                theoretical_norm = theoretical / np.sum(theoretical)
                ax1.plot(bins, theoretical_norm, 'ro-', linewidth=2, 
                        markersize=5, label='Teórico (Normalizado)')
                ax1.legend()
            except:
                pass
            
            ax1.set_title('Distribuições Normalizadas')
            ax1.set_xlabel('Compartimento')
            ax1.set_ylabel('Probabilidade')
            ax1.grid(True, alpha=0.3)
            
            # Gráfico 2: Erro relativo
            try:
                error = np.abs(st.session_state.galton_board.results - theoretical) / theoretical * 100
                ax2.bar(bins, error, alpha=0.7, color='orange', edgecolor='red', linewidth=1)
                ax2.set_title('Erro Relativo (%)')
                ax2.set_xlabel('Compartimento')
                ax2.set_ylabel('Erro (%)')
                ax2.grid(True, alpha=0.3)
            except:
                ax2.text(0.5, 0.5, 'Análise de erro\nnão disponível', 
                        ha='center', va='center', transform=ax2.transAxes, fontsize=14)
                ax2.set_title('Análise de Erro')
            
            plt.tight_layout()
            st.pyplot(fig2)

with stats_col:
    st.subheader("📊 Estatísticas")
    
    if st.session_state.galton_board is not None and st.session_state.simulation_done:
        results = st.session_state.galton_board.results
        
        # Calcular estatísticas
        total_balls = np.sum(results)
        mean_bin = np.average(range(len(results)), weights=results)
        variance = np.average((np.array(range(len(results))) - mean_bin)**2, weights=results)
        std_dev = np.sqrt(variance)
        
        # Mostrar métricas
        st.metric("Total de Bolinhas", int(total_balls))
        st.metric("Compartimento Médio", f"{mean_bin:.2f}")
        st.metric("Desvio Padrão", f"{std_dev:.2f}")
        
        # Mostrar distribuição por compartimento
        st.subheader("📋 Distribuição por Compartimento")
        
        df_results = pd.DataFrame({
            'Compartimento': range(len(results)),
            'Bolinhas': results.astype(int),
            'Percentual': (results / total_balls * 100).round(1)
        })
        
        st.dataframe(df_results, hide_index=True)
        
        # Compartimento mais popular
        max_bin = np.argmax(results)
        st.success(f"🏆 Compartimento mais popular: {max_bin} ({int(results[max_bin])} bolinhas)")
        
    else:
        st.info("👆 Execute uma simulação para ver as estatísticas")

# Mostrar teoria se solicitado
if show_theory:
    st.subheader("📚 Fundamentos Teóricos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **🎲 Probabilidade Básica**
        - Cada pino: 50% esquerda, 50% direita
        - Decisões independentes
        - Distribuição binomial resultante
        
        **📊 Parâmetros**
        - n = número de níveis
        - p = 0.5 (probabilidade de ir para direita)
        - Média: n × p = n/2
        - Variância: n × p × (1-p) = n/4
        """)
    
    with col2:
        st.markdown("""
        **🔔 Distribuição Normal**
        - Com n grande: Binomial → Normal
        - Teorema Central do Limite
        - Curva de sino característica
        
        **🎯 Aplicações**
        - Controle de qualidade
        - Fenômenos naturais
        - Erros de medição
        - Características humanas
        """)

# Footer
st.markdown("---")
st.markdown("*Desenvolvido para demonstrar conceitos de probabilidade e estatística*")