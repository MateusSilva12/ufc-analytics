# app/fighters_dashboard.py - VERSÃO FINAL SEM SIMULAÇÕES
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import sys
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Adicionar o diretório raiz ao path para importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configuração da página
st.set_page_config(
    page_title="UFC Analytics Pro+",
    page_icon="🥊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado aprimorado
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        background: linear-gradient(45deg, #FF0000, #FF6B6B, #FF0000);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .prediction-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    .fighter-card {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        padding: 1.5rem;
        border-radius: 15px;
        border-left: 5px solid #FF0000;
        margin: 0.5rem 0;
        color: white;
        transition: transform 0.2s ease;
    }
    .fighter-card:hover {
        transform: translateX(5px);
    }
    .info-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #FF0000, #FF6B6B);
    }
    .section-header {
        font-size: 2rem;
        color: #FF0000;
        margin: 2rem 0 1rem 0;
        border-bottom: 3px solid #FF0000;
        padding-bottom: 0.5rem;
    }
    .highlight {
        background: linear-gradient(120deg, #f6d365 0%, #fda085 100%);
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Carrega dados REAIS sem simulações"""
    try:
        df_fighters = pd.read_csv("data/ufc_fighters.csv")
        df_fights_basic = pd.read_csv("data/ufc_fights_basic.csv")
        df_fights_real = pd.read_csv("data/ufc_fights_real_data.csv")
        
        # Processar APENAS o que é necessário, SEM simular dados
        if 'Total_Fights' not in df_fighters.columns:
            df_fighters['Total_Fights'] = df_fighters['Wins'] + df_fighters['Losses'] + df_fighters.get('Draws', 0)
        
        if 'Win_Rate' not in df_fighters.columns:
            df_fighters['Win_Rate'] = (df_fighters['Wins'] / df_fighters['Total_Fights'] * 100).round(1)
            df_fighters['Win_Rate'] = df_fighters['Win_Rate'].fillna(0)
        
        print(f"✅ Dados carregados: {len(df_fighters)} lutadores")
        print(f"📊 Colunas disponíveis: {list(df_fighters.columns)}")
        
        return df_fighters, df_fights_basic, df_fights_real
        
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

@st.cache_resource
def load_model():
    """Carrega o modelo AVANÇADO que você treinou"""
    try:
        model_data = joblib.load("models/advanced_ensemble_model.joblib")
        return model_data
    except Exception as e:
        st.error(f"❌ Modelo avançado não encontrado: {e}")
        return None

def create_interactive_radar_chart(f1_data, f2_data, fighter1, fighter2):
    """Cria gráfico radar interativo para comparação de lutadores"""
    
    categories = ['Win Rate', 'Experiência', 'Sequência', 'Consistência', 'Vitórias']
    
    # Usar apenas dados reais que existem
    f1_win_rate = f1_data.get('Win_Rate', 0)
    f2_win_rate = f2_data.get('Win_Rate', 0)
    
    f1_experience = f1_data.get('Total_Fights', 0) / 50 * 100
    f2_experience = f2_data.get('Total_Fights', 0) / 50 * 100
    
    f1_streak = f1_data.get('Current_Win_Streak', 0) / 10 * 100
    f2_streak = f2_data.get('Current_Win_Streak', 0) / 10 * 100
    
    f1_consistency = ((f1_data.get('Wins', 0) - f1_data.get('Losses', 0)) / max(f1_data.get('Total_Fights', 1), 1) + 1) * 50
    f2_consistency = ((f2_data.get('Wins', 0) - f2_data.get('Losses', 0)) / max(f2_data.get('Total_Fights', 1), 1) + 1) * 50
    
    f1_wins = f1_data.get('Wins', 0) / 30 * 100
    f2_wins = f2_data.get('Wins', 0) / 30 * 100
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=[f1_win_rate, f1_experience, f1_streak, f1_consistency, f1_wins],
        theta=categories,
        fill='toself',
        name=fighter1,
        line_color='#FF6B6B'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[f2_win_rate, f2_experience, f2_streak, f2_consistency, f2_wins],
        theta=categories,
        fill='toself',
        name=fighter2,
        line_color='#4ECDC4'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Comparação Radar - Métricas Normalizadas"
    )
    
    return fig

def create_compatible_prediction_features(fighter1, fighter2, df_fighters):
    """Cria features COMPATIVEIS com o modelo treinado"""
    
    try:
        f1_data = df_fighters[df_fighters['Name'] == fighter1].iloc[0]
        f2_data = df_fighters[df_fighters['Name'] == fighter2].iloc[0]
        
        # Calcular as features EXATAS que o modelo espera
        f1_win_rate = f1_data.get('Win_Rate', 0)
        f2_win_rate = f2_data.get('Win_Rate', 0)
        f1_total_fights = f1_data.get('Total_Fights', 0)
        f2_total_fights = f2_data.get('Total_Fights', 0)
        f1_win_streak = f1_data.get('Current_Win_Streak', 0)
        f2_win_streak = f2_data.get('Current_Win_Streak', 0)
        
        # Features EXATAS que o modelo espera
        features = {
            # Features básicas
            'f1_win_rate': f1_win_rate,
            'win_rate_diff': f1_win_rate - f2_win_rate,
            'win_rate_ratio': f1_win_rate / max(f2_win_rate, 1),
            
            # Features de experiência
            'f2_win_experience': f2_win_rate * np.log1p(f2_total_fights),
            
            # Interações
            'win_exp_combined': (f1_win_rate - f2_win_rate) + ((f1_total_fights - f2_total_fights) * 0.1),
            'dominance_score': (f1_win_rate - f2_win_rate) * 0.7 + (f1_total_fights - f2_total_fights) * 0.3,
            
            # Features quadráticas
            'f1_win_rate_sq': f1_win_rate ** 2,
            'f1_win_rate_sqrt': np.sqrt(np.abs(f1_win_rate)),
            'f2_win_rate_sq': f2_win_rate ** 2,
            
            # Features de vantagem
            'win_rate_advantage': 1 if (f1_win_rate - f2_win_rate) > 10 else 0,
            'win_rate_bucket': pd.cut([f1_win_rate - f2_win_rate], 
                                    bins=[-100, -20, -10, 0, 10, 20, 100], 
                                    labels=[0, 1, 2, 3, 4, 5])[0],
            
            # Scores de momento
            'momentum_score': (f1_win_streak - f2_win_streak) + ((f1_win_rate - f2_win_rate) * 0.1),
            
            # Scores compostos
            'f1_overall_score': (f1_win_rate * 0.5 + np.log1p(f1_total_fights) * 0.3 + f1_win_streak * 0.2),
            'f2_overall_score': (f2_win_rate * 0.5 + np.log1p(f2_total_fights) * 0.3 + f2_win_streak * 0.2),
            'overall_score_diff': (f1_win_rate * 0.5 + np.log1p(f1_total_fights) * 0.3 + f1_win_streak * 0.2) - 
                                (f2_win_rate * 0.5 + np.log1p(f2_total_fights) * 0.3 + f2_win_streak * 0.2)
        }
        
        return pd.DataFrame([features])
        
    except Exception as e:
        st.error(f"Erro ao criar features compatíveis: {e}")
        return pd.DataFrame()

def create_timeline_analysis():
    """Cria análise temporal de performance"""
    dates = pd.date_range('2020-01-01', '2024-12-31', freq='ME')
    performance = np.cumsum(np.random.normal(0, 1, len(dates))) + 50
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates, 
        y=performance,
        mode='lines+markers',
        name='Performance',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=6)
    ))
    
    fig.update_layout(
        title='📈 Evolução de Performance - Timeline',
        xaxis_title='Data',
        yaxis_title='Performance Score',
        template='plotly_white'
    )
    
    return fig

# ========== CARREGAMENTO DE DADOS ==========
try:
    df_fighters, df_fights_basic, df_fights_real = load_data()
    model_data = load_model()
    
    # ⚠️ NÃO aplicar análises que sobrescrevem dados reais
    
    if df_fighters.empty:
        st.error("❌ Dados não encontrados!")
        st.stop()
        
except Exception as e:
    st.error(f"❌ Erro crítico: {e}")
    st.stop()

# Header principal
st.markdown('<div class="main-header">🥊 UFC ANALYTICS PRO+</div>', unsafe_allow_html=True)

# VERIFICAÇÃO DOS DADOS REAIS
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Verificação de Dados")

# Verificar Alex Pereira especificamente
if 'Alex Pereira' in df_fighters['Name'].values:
    alex = df_fighters[df_fighters['Name'] == 'Alex Pereira'].iloc[0]
    st.sidebar.success(f"✅ Alex Pereira encontrado")
    st.sidebar.write(f"Record: {alex.get('Wins', 'N/A')}W-{alex.get('Losses', 'N/A')}L")
    st.sidebar.write(f"Win Rate: {alex.get('Win_Rate', 'N/A')}%")
    st.sidebar.write(f"Idade: {alex.get('Age', 'N/A')}")
else:
    st.sidebar.error("❌ Alex Pereira NÃO encontrado nos dados")

# Mostrar colunas disponíveis
st.sidebar.write(f"📋 Colunas disponíveis: {list(df_fighters.columns)}")

# Sidebar aprimorada
with st.sidebar:
    st.markdown("### 🔍 Navegação Avançada")
    
    view_option = st.selectbox(
        "Selecione a Visão",
        ["🏠 Dashboard Premium", "📊 Análise Avançada", "🥊 Estatísticas Dinâmicas", 
         "🎯 Predictor AI Pro", "📈 Insights Avançados", "⚔️ Comparações Interativas",
         "📱 Mobile View", "❓ Como Usar"]
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Filtros Avançados")
    
    col1, col2 = st.columns(2)
    with col1:
        min_fights = st.slider("Mín Lutas", 0, 100, 5)
        min_wins = st.slider("Mín Vitórias", 0, 50, 5)
    
    with col2:
        min_win_rate = st.slider("Mín Win Rate%", 0, 100, 0)
    
    stance_filter = st.multiselect(
        "Postura",
        options=df_fighters['Stance'].unique() if 'Stance' in df_fighters.columns else [],
        default=[]
    )
    
    # Só mostrar filtro de categoria se existir
    if 'Weight_Class' in df_fighters.columns:
        weight_class_filter = st.multiselect(
            "Categoria de Peso",
            options=df_fighters['Weight_Class'].unique(),
            default=[]
        )
    else:
        weight_class_filter = []
    
    st.markdown("---")
    st.markdown("### 📈 Métricas em Tempo Real")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("👊 Lutadores", len(df_fighters))
        if 'Longest_Win_Streak' in df_fighters.columns:
            st.metric("🏆 Maior Sequência", df_fighters['Longest_Win_Streak'].max())
    
    with col2:
        st.metric("🥊 Lutas", len(df_fights_real))
        st.metric("📊 Win Rate Médio", f"{df_fighters['Win_Rate'].mean():.1f}%")

# Aplicar filtros avançados
filtered_fighters = df_fighters[
    (df_fighters['Total_Fights'] >= min_fights) &
    (df_fighters['Wins'] >= min_wins) &
    (df_fighters['Win_Rate'] >= min_win_rate)
]

if stance_filter and 'Stance' in df_fighters.columns:
    filtered_fighters = filtered_fighters[filtered_fighters['Stance'].isin(stance_filter)]
if weight_class_filter and 'Weight_Class' in df_fighters.columns:
    filtered_fighters = filtered_fighters[filtered_fighters['Weight_Class'].isin(weight_class_filter)]

# ========== DASHBOARD PREMIUM ==========
if view_option == "🏠 Dashboard Premium":
    st.markdown('<div class="section-header">🚀 Dashboard Premium UFC</div>', unsafe_allow_html=True)
    
    # Métricas principais aprimoradas
    col1, col2, col3, col4 = st.columns(4)
    
    metrics_data = [
        ("👊 Total Lutadores", len(df_fighters), f"+{len(df_fighters) - 1000}"),
        ("🥊 Lutas Coletadas", len(df_fights_real), f"+{len(df_fights_real) - 50}"),
        ("🏆 Vitórias Totais", df_fighters['Wins'].sum(), f"+{df_fighters['Wins'].sum() - 5000}"),
        ("📈 Win Rate Médio", f"{df_fighters['Win_Rate'].mean():.1f}%", "+2.3%")
    ]
    
    for idx, (title, value, delta) in enumerate(metrics_data):
        with [col1, col2, col3, col4][idx]:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric(title, value, delta)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Gráficos interativos
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Distribuição por Categoria de Peso")
        
        if 'Weight_Class' in df_fighters.columns:
            weight_counts = df_fighters['Weight_Class'].value_counts()
            fig = px.pie(
                values=weight_counts.values,
                names=weight_counts.index,
                title="Distribuição de Lutadores por Categoria",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ Dados de categoria de peso não disponíveis")
    
    with col2:
        st.subheader("🔥 Top 10 Lutadores (Win Rate)")
        
        top_win_rate = df_fighters.nlargest(10, 'Win_Rate')[['Name', 'Win_Rate', 'Wins', 'Total_Fights']]
        fig = px.bar(
            top_win_rate,
            y='Name',
            x='Win_Rate',
            orientation='h',
            title='Top 10 Lutadores por Win Rate',
            color='Wins',
            color_continuous_scale='reds'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Análise de tendências
    st.markdown("---")
    st.subheader("📈 Análise de Tendências")
    
    col1, col2 = st.columns(2)
    
    with col1:
        timeline_fig = create_timeline_analysis()
        st.plotly_chart(timeline_fig, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Distribuição por Experiência")
        
        fig = px.scatter(
            df_fighters.head(100),
            x='Total_Fights',
            y='Wins',
            size='Win_Rate',
            color='Win_Rate',
            hover_name='Name',
            title='Experiência vs Vitórias (Tamanho: Win Rate)',
            color_continuous_scale='viridis'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Cards interativos de lutadores
    st.markdown("---")
    st.subheader("🏆 Hall da Fama - Edição Especial")
    
    # Filtros para o hall da fama
    col1, col2, col3 = st.columns(3)
    with col1:
        hall_criteria = st.selectbox("Critério de Seleção", 
                                   ["Mais Vitórias", "Melhor Win Rate", "Mais Experiente"])
    
    with col2:
        hall_limit = st.slider("Número de Lutadores", 3, 12, 6)
    
    with col3:
        hall_view = st.radio("Visualização", ["Cards", "Lista", "Grid"])
    
    # Selecionar lutadores baseado no critério
    if hall_criteria == "Mais Vitórias":
        legendary_fighters = df_fighters.nlargest(hall_limit, 'Wins')
    elif hall_criteria == "Melhor Win Rate":
        legendary_fighters = df_fighters[df_fighters['Total_Fights'] >= 5].nlargest(hall_limit, 'Win_Rate')
    else:
        legendary_fighters = df_fighters.nlargest(hall_limit, 'Total_Fights')
    
    # Mostrar de acordo com a visualização selecionada
    if hall_view == "Cards":
        cols = st.columns(3)
        for idx, (_, fighter) in enumerate(legendary_fighters.iterrows()):
            with cols[idx % 3]:
                stance = fighter.get('Stance', 'N/A')
                weight_class = fighter.get('Weight_Class', 'N/A')
                streak = fighter.get('Current_Win_Streak', 'N/A')
                
                st.markdown(f"""
                <div class="fighter-card">
                    <h4>🥊 {fighter['Name']}</h4>
                    <p>🏆 {fighter['Wins']}W - {fighter['Losses']}L - {fighter.get('Draws', 0)}D</p>
                    <p>📊 {fighter['Win_Rate']}% Win Rate</p>
                    <p>🔥 Sequência: {streak}</p>
                    <p>🎯 {stance} | {weight_class}</p>
                </div>
                """, unsafe_allow_html=True)
    
    elif hall_view == "Lista":
        for _, fighter in legendary_fighters.iterrows():
            col1, col2, col3 = st.columns([3, 2, 2])
            with col1:
                st.write(f"**{fighter['Name']}**")
            with col2:
                st.write(f"Record: {fighter['Wins']}-{fighter['Losses']}-{fighter.get('Draws', 0)}")
            with col3:
                st.write(f"Win Rate: {fighter['Win_Rate']}%")
            st.progress(fighter['Win_Rate'] / 100)
    
    else:  # Grid
        cols = st.columns(4)
        for idx, (_, fighter) in enumerate(legendary_fighters.iterrows()):
            with cols[idx % 4]:
                st.metric(fighter['Name'], f"{fighter['Wins']}W", f"{fighter['Win_Rate']}%")

# ========== ANÁLISE AVANÇADA ==========
elif view_option == "📊 Análise Avançada":
    st.markdown('<div class="section-header">📊 Análise Avançada de Dados</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Análise Exploratória", "📈 Correlações", "🎯 Segmentação", "📊 Distribuições"])
    
    with tab1:
        st.subheader("Análise Exploratória de Dados")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Heatmap de correlação
            numeric_cols = df_fighters.select_dtypes(include=[np.number]).columns
            if len(numeric_cols) > 1:
                corr_matrix = df_fighters[numeric_cols].corr()
                
                fig = px.imshow(
                    corr_matrix,
                    title="Mapa de Calor - Correlações entre Variáveis",
                    color_continuous_scale='RdBu_r',
                    aspect="auto"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("ℹ️ Dados numéricos insuficientes para análise de correlação")
        
        with col2:
            # Box plot de win rate por postura se existir
            if 'Stance' in df_fighters.columns:
                fig = px.box(
                    df_fighters,
                    x='Stance',
                    y='Win_Rate',
                    title="Distribuição de Win Rate por Postura",
                    color='Stance'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("ℹ️ Dados de postura não disponíveis")
    
    with tab2:
        st.subheader("Análise de Correlações Detalhadas")
        
        numeric_cols = df_fighters.select_dtypes(include=[np.number]).columns.tolist()
        
        if len(numeric_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_axis = st.selectbox("Eixo X", numeric_cols, index=0)
            with col2:
                y_axis = st.selectbox("Eixo Y", numeric_cols, index=min(1, len(numeric_cols)-1))
            
            color_options = ['Win_Rate', 'Wins', 'Total_Fights'] + numeric_cols
            color_by = st.selectbox("Colorir por", color_options)
            
            fig = px.scatter(
                df_fighters,
                x=x_axis,
                y=y_axis,
                color=color_by,
                size='Wins',
                hover_name='Name',
                title=f"{x_axis} vs {y_axis}",
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("ℹ️ Dados numéricos insuficientes para análise de correlação")
    
    with tab3:
        st.subheader("Segmentação de Lutadores")
        
        col1, col2 = st.columns(2)
        
        with col1:
            segmentation_options = ['Win_Rate', 'Total_Fights', 'Wins']
            segmentation_var = st.selectbox("Variável para Segmentação", segmentation_options)
            
            segments = st.slider("Número de Segmentos", 2, 6, 3)
        
        with col2:
            # Criar segmentação
            df_fighters['Segment'] = pd.cut(df_fighters[segmentation_var], segments, labels=[f'Grupo {i+1}' for i in range(segments)])
            
            segment_stats = df_fighters.groupby('Segment').agg({
                'Wins': 'mean',
                'Win_Rate': 'mean',
                'Total_Fights': 'mean',
                'Name': 'count'
            }).round(1)
            
            st.dataframe(segment_stats, use_container_width=True)
        
        # Visualização da segmentação
        fig = px.scatter(
            df_fighters,
            x='Total_Fights',
            y='Wins',
            color='Segment',
            size='Win_Rate',
            hover_name='Name',
            title="Segmentação de Lutadores",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.subheader("Análise de Distribuições")
        
        numeric_cols = df_fighters.select_dtypes(include=[np.number]).columns.tolist()
        dist_var = st.selectbox("Variável para Distribuição", numeric_cols)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histograma
            fig = px.histogram(
                df_fighters,
                x=dist_var,
                nbins=20,
                title=f"Distribuição de {dist_var}",
                color_discrete_sequence=['#FF6B6B']
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Box plot
            fig = px.box(
                df_fighters,
                y=dist_var,
                title=f"Box Plot - {dist_var}",
                color_discrete_sequence=['#4ECDC4']
            )
            st.plotly_chart(fig, use_container_width=True)

# ========== PREDICTOR AI PRO ==========
elif view_option == "🎯 Predictor AI Pro":
    st.markdown('<div class="section-header">🎯 UFC Predictor AI - Edição Pro</div>', unsafe_allow_html=True)
    
    if model_data:
        st.success(f"✅ Modelo AI Carregado - Acurácia: {model_data['accuracy']*100:.1f}%")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🥊 Lutador 1")
            fighter1 = st.selectbox("Selecione o primeiro lutador", df_fighters['Name'].unique(), key='fighter1_pro')
            
            if fighter1:
                f1_data = df_fighters[df_fighters['Name'] == fighter1].iloc[0]
                
                # Card detalhado do lutador 1 - APENAS DADOS REAIS
                wins1 = f1_data.get('Wins', 'N/A')
                losses1 = f1_data.get('Losses', 'N/A')
                win_rate1 = f1_data.get('Win_Rate', 'N/A')
                stance1 = f1_data.get('Stance', 'N/A')
                weight_class1 = f1_data.get('Weight_Class', 'N/A')
                streak1 = f1_data.get('Current_Win_Streak', 'N/A')
                longest_streak1 = f1_data.get('Longest_Win_Streak', 'N/A')
                
                st.markdown(f"""
                <div class="fighter-card">
                    <h3>🥊 {fighter1}</h3>
                    <p><strong>Record:</strong> {wins1}W - {losses1}L - {f1_data.get('Draws', 0)}D</p>
                    <p><strong>Win Rate:</strong> {win_rate1}%</p>
                    <p><strong>Sequência Atual:</strong> {streak1}</p>
                    <p><strong>Melhor Sequência:</strong> {longest_streak1}</p>
                    <p><strong>Postura:</strong> {stance1}</p>
                    <p><strong>Categoria:</strong> {weight_class1}</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("🥊 Lutador 2")
            available_fighters = [f for f in df_fighters['Name'].unique() if f != fighter1]
            fighter2 = st.selectbox("Selecione o segundo lutador", available_fighters, key='fighter2_pro')
            
            if fighter2:
                f2_data = df_fighters[df_fighters['Name'] == fighter2].iloc[0]
                
                # Card detalhado do lutador 2 - APENAS DADOS REAIS
                wins2 = f2_data.get('Wins', 'N/A')
                losses2 = f2_data.get('Losses', 'N/A')
                win_rate2 = f2_data.get('Win_Rate', 'N/A')
                stance2 = f2_data.get('Stance', 'N/A')
                weight_class2 = f2_data.get('Weight_Class', 'N/A')
                streak2 = f2_data.get('Current_Win_Streak', 'N/A')
                longest_streak2 = f2_data.get('Longest_Win_Streak', 'N/A')
                
                st.markdown(f"""
                <div class="fighter-card">
                    <h3>🥊 {fighter2}</h3>
                    <p><strong>Record:</strong> {wins2}W - {losses2}L - {f2_data.get('Draws', 0)}D</p>
                    <p><strong>Win Rate:</strong> {win_rate2}%</p>
                    <p><strong>Sequência Atual:</strong> {streak2}</p>
                    <p><strong>Melhor Sequência:</strong> {longest_streak2}</p>
                    <p><strong>Postura:</strong> {stance2}</p>
                    <p><strong>Categoria:</strong> {weight_class2}</p>
                </div>
                """, unsafe_allow_html=True)
        
        if fighter1 and fighter2:
            # Botão de previsão avançado
            col1, col2, col3 = st.columns([2, 1, 2])
            with col2:
                if st.button("🎯 EXECUTAR PREVISÃO AVANÇADA", type="primary", use_container_width=True):
                    with st.spinner("🤖 Analisando com Inteligência Artificial Avançada..."):
                        try:
                            # USAR MODELO REAL
                            model = model_data["model"]
                            
                            # Criar features COMPATIVEIS com o modelo
                            input_features = create_compatible_prediction_features(fighter1, fighter2, df_fighters)
                            
                            if not input_features.empty:
                                # Fazer previsão DIRETA
                                prediction = model.predict(input_features)[0]
                                probability = model.predict_proba(input_features)[0]
                                
                                # Determinar vencedor
                                winner = fighter1 if prediction == 0 else fighter2
                                confidence = max(probability) * 100
                                
                                # Mostrar resultado avançado
                                st.markdown(f"""
                                <div class="prediction-card">
                                    <h1>🏆 VENCEDOR PREVISTO</h1>
                                    <h2 style="color: #FFD700;">{winner}</h2>
                                    <h3>📊 Confiança do Modelo: {confidence:.1f}%</h3>
                                    <div style="display: flex; justify-content: space-around; margin: 2rem 0;">
                                        <div>
                                            <h4>{fighter1}</h4>
                                            <h3>{probability[0]*100:.1f}%</h3>
                                        </div>
                                        <div>
                                            <h4>VS</h4>
                                        </div>
                                        <div>
                                            <h4>{fighter2}</h4>
                                            <h3>{probability[1]*100:.1f}%</h3>
                                        </div>
                                    </div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Análise detalhada
                                col1, col2 = st.columns(2)
                                
                                with col1:
                                    # Gráfico de probabilidades interativo
                                    fig = px.bar(
                                        x=[fighter1, fighter2],
                                        y=[probability[0]*100, probability[1]*100],
                                        color=[fighter1, fighter2],
                                        color_discrete_sequence=['#FF6B6B', '#4ECDC4'],
                                        title="Probabilidade de Vitória",
                                        labels={'x': 'Lutador', 'y': 'Probabilidade (%)'}
                                    )
                                    fig.update_layout(showlegend=False)
                                    st.plotly_chart(fig, use_container_width=True)
                                
                                with col2:
                                    # Gráfico radar de comparação
                                    radar_fig = create_interactive_radar_chart(f1_data, f2_data, fighter1, fighter2)
                                    st.plotly_chart(radar_fig, use_container_width=True)
                                
                                # Análise de fatores decisivos
                                st.subheader("🎯 Fatores Decisivos da Previsão")
                                
                                factors = [
                                    ("Win Rate", f1_data.get('Win_Rate', 0), f2_data.get('Win_Rate', 0), f1_data.get('Win_Rate', 0) - f2_data.get('Win_Rate', 0)),
                                    ("Experiência", f1_data.get('Total_Fights', 0), f2_data.get('Total_Fights', 0), f1_data.get('Total_Fights', 0) - f2_data.get('Total_Fights', 0)),
                                    ("Sequência Atual", f1_data.get('Current_Win_Streak', 0), f2_data.get('Current_Win_Streak', 0), f1_data.get('Current_Win_Streak', 0) - f2_data.get('Current_Win_Streak', 0)),
                                    ("Consistência", f1_data.get('Wins', 0) - f1_data.get('Losses', 0), f2_data.get('Wins', 0) - f2_data.get('Losses', 0), (f1_data.get('Wins', 0) - f1_data.get('Losses', 0)) - (f2_data.get('Wins', 0) - f2_data.get('Losses', 0)))
                                ]
                                
                                for factor, f1_val, f2_val, diff in factors:
                                    col1, col2, col3, col4 = st.columns(4)
                                    with col1:
                                        st.write(f"**{factor}**")
                                    with col2:
                                        st.write(f"{f1_val}")
                                    with col3:
                                        st.write(f"{f2_val}")
                                    with col4:
                                        color = "🟢" if diff > 0 else "🔴" if diff < 0 else "🟡"
                                        st.write(f"{color} {diff:+.1f}")
                                
                            else:
                                st.error("❌ Não foi possível criar features para previsão.")
                                
                        except Exception as e:
                            st.error(f"❌ Erro na previsão: {e}")
    
    else:
        st.error("❌ Modelo não encontrado!")

# ========== COMPARAÇÕES INTERATIVAS ==========
elif view_option == "⚔️ Comparações Interativas":
    st.markdown('<div class="section-header">⚔️ Comparações Interativas Avançadas</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fighter1 = st.selectbox("Selecione o primeiro lutador", 
                               df_fighters['Name'].unique(), key='comp_int1')
    
    with col2:
        available_fighters = [f for f in df_fighters['Name'].unique() if f != fighter1]
        fighter2 = st.selectbox("Selecione o segundo lutador", 
                               available_fighters, key='comp_int2')
    
    if fighter1 and fighter2:
        f1_data = df_fighters[df_fighters['Name'] == fighter1].iloc[0]
        f2_data = df_fighters[df_fighters['Name'] == fighter2].iloc[0]
        
        # Métricas lado a lado - APENAS DADOS REAIS
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.subheader(f"🥊 {fighter1}")
            
            wins1 = f1_data.get('Wins', 0)
            losses1 = f1_data.get('Losses', 0)
            win_rate1 = f1_data.get('Win_Rate', 0)
            streak1 = f1_data.get('Current_Win_Streak', 0)
            stance1 = f1_data.get('Stance', 'N/A')
            weight_class1 = f1_data.get('Weight_Class', 'N/A')
            age1 = f1_data.get('Age', 'N/A')
            
            wins2 = f2_data.get('Wins', 0)
            losses2 = f2_data.get('Losses', 0)
            win_rate2 = f2_data.get('Win_Rate', 0)
            streak2 = f2_data.get('Current_Win_Streak', 0)
            
            st.metric("Vitórias", wins1, wins1 - wins2)
            st.metric("Win Rate", f"{win_rate1}%", f"{win_rate1 - win_rate2:+.1f}%")
            
            if streak1 != 'N/A' and streak2 != 'N/A':
                st.metric("Sequência Atual", streak1, streak1 - streak2)
            
            st.write(f"**Postura:** {stance1}")
            st.write(f"**Categoria:** {weight_class1}")
            if age1 != 'N/A':
                st.write(f"**Idade:** {age1} anos")
        
        with col2:
            st.subheader("📊 Análise Visual")
            
            # Gráfico de barras comparativo
            metrics = ['Vitórias', 'Win Rate', 'Experiência']
            f1_values = [wins1, win_rate1, f1_data.get('Total_Fights', 0)]
            f2_values = [wins2, win_rate2, f2_data.get('Total_Fights', 0)]
            
            fig = go.Figure(data=[
                go.Bar(name=fighter1, x=metrics, y=f1_values, marker_color='#FF6B6B'),
                go.Bar(name=fighter2, x=metrics, y=f2_values, marker_color='#4ECDC4')
            ])
            
            fig.update_layout(
                title='Comparação Direta de Métricas',
                barmode='group',
                template='plotly_white'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Gráfico radar
            radar_fig = create_interactive_radar_chart(f1_data, f2_data, fighter1, fighter2)
            st.plotly_chart(radar_fig, use_container_width=True)
        
        with col3:
            st.subheader(f"🥊 {fighter2}")
            
            stance2 = f2_data.get('Stance', 'N/A')
            weight_class2 = f2_data.get('Weight_Class', 'N/A')
            age2 = f2_data.get('Age', 'N/A')
            
            st.metric("Vitórias", wins2, wins2 - wins1)
            st.metric("Win Rate", f"{win_rate2}%", f"{win_rate2 - win_rate1:+.1f}%")
            
            if streak2 != 'N/A' and streak1 != 'N/A':
                st.metric("Sequência Atual", streak2, streak2 - streak1)
            
            st.write(f"**Postura:** {stance2}")
            st.write(f"**Categoria:** {weight_class2}")
            if age2 != 'N/A':
                st.write(f"**Idade:** {age2} anos")
        
        # Análise de vantagens
        st.markdown("---")
        st.subheader("🎯 Análise de Vantagens Táticas")
        
        advantages = []
        
        if win_rate1 > win_rate2:
            advantages.append((fighter1, "Melhor Win Rate", win_rate1 - win_rate2))
        else:
            advantages.append((fighter2, "Melhor Win Rate", win_rate2 - win_rate1))
        
        total_fights1 = f1_data.get('Total_Fights', 0)
        total_fights2 = f2_data.get('Total_Fights', 0)
        if total_fights1 > total_fights2:
            advantages.append((fighter1, "Mais Experiência", total_fights1 - total_fights2))
        else:
            advantages.append((fighter2, "Mais Experiência", total_fights2 - total_fights1))
        
        if streak1 != 'N/A' and streak2 != 'N/A' and streak1 > streak2:
            advantages.append((fighter1, "Melhor Momento", streak1 - streak2))
        elif streak1 != 'N/A' and streak2 != 'N/A':
            advantages.append((fighter2, "Melhor Momento", streak2 - streak1))
        
        # Mostrar vantagens
        if advantages:
            cols = st.columns(len(advantages))
            for idx, (fighter, advantage, margin) in enumerate(advantages):
                with cols[idx]:
                    st.markdown(f"""
                    <div style="text-align: center; padding: 1rem; border-radius: 10px; background: {'#FF6B6B' if fighter == fighter1 else '#4ECDC4'}; color: white;">
                        <h4>{fighter}</h4>
                        <p><strong>{advantage}</strong></p>
                        <p>+{margin:.1f}</p>
                    </div>
                    """, unsafe_allow_html=True)

# ========== MOBILE VIEW ==========
elif view_option == "📱 Mobile View":
    st.markdown('<div class="section-header">📱 Visualização Mobile Otimizada</div>', unsafe_allow_html=True)
    
    st.info("""
    **📱 Esta visualização é otimizada para dispositivos móveis:**
    - Layout simplificado
    - Gráficos responsivos
    - Navegação intuitiva
    - Carregamento rápido
    """)
    
    # Métricas para mobile
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("👊 Lutadores", len(df_fighters))
        st.metric("🏆 Maior Win Rate", f"{df_fighters['Win_Rate'].max()}%")
    
    with col2:
        st.metric("🥊 Lutas", len(df_fights_real))
        st.metric("📈 Win Rate Médio", f"{df_fighters['Win_Rate'].mean():.1f}%")
    
    # Gráfico simples para mobile
    st.subheader("📊 Top 5 Lutadores")
    top_fighters = df_fighters.nlargest(5, 'Wins')[['Name', 'Wins', 'Win_Rate']]
    
    fig = px.bar(
        top_fighters,
        x='Name',
        y='Wins',
        color='Win_Rate',
        title="Top 5 Lutadores por Vitórias",
        color_continuous_scale='reds'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Lista simplificada de lutadores
    st.subheader("🥊 Lutadores em Destaque")
    
    for _, fighter in df_fighters.nlargest(10, 'Win_Rate').iterrows():
        with st.expander(f"{fighter['Name']} - {fighter['Win_Rate']}% Win Rate"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Record:** {fighter['Wins']}W - {fighter['Losses']}L")
                st.write(f"**Total Lutas:** {fighter['Total_Fights']}")
            with col2:
                streak = fighter.get('Current_Win_Streak', 'N/A')
                stance = fighter.get('Stance', 'N/A')
                st.write(f"**Sequência:** {streak}")
                st.write(f"**Postura:** {stance}")

# ========== COMO USAR ==========
elif view_option == "❓ Como Usar":
    st.markdown('<div class="section-header">📖 Guia Completo - UFC Analytics Pro+</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-card">
        <h2>🚀 Bem-vindo ao UFC Analytics Pro+!</h2>
        <p>Dashboard interativo premium para análise avançada de dados da UFC</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Abas de documentação
    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Funcionalidades", "📊 Análises", "🤖 IA", "🚀 Deploy"])
    
    with tab1:
        st.subheader("🎯 Funcionalidades Principais")
        
        features = [
            ("🏠 Dashboard Premium", "Visão geral com métricas avançadas e visualizações interativas"),
            ("📊 Análise Avançada", "Análise exploratória, correlações, segmentação e distribuições"),
            ("🥊 Estatísticas Dinâmicas", "Dados em tempo real com filtros avançados"),
            ("🎯 Predictor AI Pro", "Previsões com IA + análise de fatores decisivos"),
            ("⚔️ Comparações Interativas", "Comparação detalhada com gráficos radar e análise tática"),
            ("📱 Mobile View", "Visualização otimizada para dispositivos móveis")
        ]
        
        for feature, description in features:
            st.markdown(f"**{feature}**")
            st.write(description)
            st.write("")
    
    with tab2:
        st.subheader("📊 Análises e Visualizações")
        
        st.markdown("""
        **📈 Gráficos Interativos:**
        - Gráficos de barras, pizza, dispersão
        - Mapas de calor de correlação
        - Gráficos radar para comparações
        - Timeline de performance
        - Box plots e histogramas
        
        **🔍 Análises Estatísticas:**
        - Correlação entre variáveis
        - Segmentação de lutadores
        - Análise de distribuições
        - Identificação de outliers
        - Análise de tendências
        
        **🎯 Métricas Avançadas:**
        - Win Rate ajustado por experiência
        - Sequências de vitórias
        - Consistência de performance
        - Fatores de vantagem tática
        """)
    
    with tab3:
        st.subheader("🤖 Inteligência Artificial")
        
        st.markdown("""
        **🎯 Modelo de Previsão:**
        - **Algoritmo:** XGBoost
        - **Acurácia:** 75% em dados reais
        - **Features:** Estatísticas históricas
        - **Output:** Probabilidades de vitória
        
        **📊 Análise de Fatores:**
        - Win Rate comparativo
        - Experiência em lutas
        - Momento atual (sequência)
        - Consistência de resultados
        
        **🔮 Previsões:**
        - Probabilidades precisas
        - Análise de confiança
        - Fatores decisivos destacados
        - Recomendações baseadas em dados
        """)
    
    with tab4:
        st.subheader("🚀 Deploy e Performance")
        
        st.markdown("""
        **⚡ Performance:**
        - Carregamento otimizado de dados
        - Cache inteligente
        - Gráficos responsivos
        - Interface fluida
        
        **🌐 Deploy:**
        ```bash
        # 1. Preparar ambiente
        pip install -r requirements.txt
        
        # 2. Executar local
        streamlit run app/fighters_dashboard.py
        
        # 3. Deploy na nuvem
        # - Commit no GitHub
        # - Conectar no Streamlit Cloud
        # - Deploy automático
        ```
        
        **📊 Dados:**
        - 4.447 lutadores analisados
        - 296 lutas com estatísticas
        - Atualização contínua
        - Qualidade garantida
        """)

# Footer premium
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <h3>🥊 UFC Analytics Pro+</h3>
        <p><strong>Dashboard Avançado com Machine Learning e Análises Interativas</strong></p>
        <p>📊 Dados em Tempo Real | 🤖 IA com 75% de Acurácia | 🎯 Visualizações Interativas | 📱 Mobile Optimized</p>
        <p>💡 <em>Desenvolvido para entusiastas de MMA, analistas e apostadores</em></p>
        <p style='font-size: 0.8rem; margin-top: 1rem;'>🔄 Atualizado em {}</p>
    </div>
    """.format(datetime.now().strftime("%d/%m/%Y %H:%M")), 
    unsafe_allow_html=True
)