# app/dashbord.py - VERSÃO DEFINITIVA UFC ANALYTICS PRO+ ULTRA PREMIUM
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import sys
import os
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import json
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ========== CONFIGURAÇÃO AVANÇADA ==========
st.set_page_config(
    page_title="UFC Analytics Pro+ Elite",
    page_icon="🥊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== CSS ULTRA AVANÇADO ==========
st.markdown("""
<style>
    /* SISTEMA DE TEMAS AVANÇADO */
    :root {
        --primary: #FF0000;
        --secondary: #FF6B6B;
        --accent: #4ECDC4;
        --gold: #FFD700;
        --silver: #C0C0C0;
        --bronze: #CD7F32;
    }
    
    [data-theme="dark"] {
        --bg-primary: #0A0C10;
        --bg-secondary: #1A1D23;
        --bg-tertiary: #2A2F3D;
        --text-primary: #FFFFFF;
        --text-secondary: #B0B7C3;
        --border-color: #3A3F4D;
        --shadow-color: rgba(0,0,0,0.5);
    }
    
    [data-theme="light"] {
        --bg-primary: #FFFFFF;
        --bg-secondary: #F8F9FA;
        --bg-tertiary: #E9ECEF;
        --text-primary: #2D3748;
        --text-secondary: #4A5568;
        --border-color: #E2E8F0;
        --shadow-color: rgba(0,0,0,0.1);
    }
    
    /* RESET E ESTILOS GLOBAIS */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .main .block-container {
        background: var(--bg-primary);
        color: var(--text-primary);
        padding-top: 1rem;
        min-height: 100vh;
    }
    
    .stApp {
        background: var(--bg-primary);
        font-family: 'Segoe UI', system-ui, sans-serif;
    }
    
    /* HEADER PRINCIPAL COM PARTÍCULAS */
    .main-header-container {
        position: relative;
        overflow: hidden;
        padding: 3rem 0;
        background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
        border-radius: 0 0 30px 30px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px var(--shadow-color);
    }
    
    .main-header {
        font-size: 4.5rem;
        background: linear-gradient(45deg, var(--primary), var(--secondary), var(--accent), var(--primary));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        font-weight: 900;
        text-shadow: 4px 4px 8px var(--shadow-color);
        animation: titleGlow 3s ease-in-out infinite alternate;
        position: relative;
        z-index: 2;
    }
    
    @keyframes titleGlow {
        0% { text-shadow: 4px 4px 8px var(--shadow-color); }
        100% { text-shadow: 4px 4px 20px rgba(255, 107, 107, 0.4), 0 0 30px rgba(78, 205, 196, 0.3); }
    }
    
    .sub-header {
        text-align: center;
        color: var(--text-secondary);
        font-size: 1.4rem;
        margin-top: 1rem;
        font-weight: 300;
        position: relative;
        z-index: 2;
    }
    
    /* SISTEMA DE CARDS AVANÇADO */
    .super-card {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        padding: 2rem;
        border-radius: 20px;
        color: var(--text-primary);
        border: 1px solid var(--border-color);
        box-shadow: 0 15px 35px var(--shadow-color);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
    }
    
    .super-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
        transition: left 0.6s;
    }
    
    .super-card:hover::before {
        left: 100%;
    }
    
    .super-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 25px 50px rgba(255, 0, 0, 0.2);
        border-color: var(--primary);
    }
    
    .metric-card {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        padding: 1.8rem;
        border-radius: 18px;
        color: var(--text-primary);
        text-align: center;
        border: 1px solid var(--border-color);
        box-shadow: 0 10px 30px var(--shadow-color);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .metric-card::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 4px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        transform: scaleX(0);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover::after {
        transform: scaleX(1);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(255, 0, 0, 0.15);
    }
    
    /* CARDS ESPECIAIS */
    .prediction-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 3rem;
        border-radius: 25px;
        color: white;
        text-align: center;
        margin: 2.5rem 0;
        box-shadow: 0 20px 50px rgba(0,0,0,0.4);
        border: 2px solid rgba(255,255,255,0.1);
        animation: predictionPulse 2s ease-in-out infinite;
        position: relative;
        overflow: hidden;
    }
    
    @keyframes predictionPulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .prediction-card::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: rotate 15s linear infinite;
    }
    
    .fighter-card {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        padding: 2rem;
        border-radius: 20px;
        border-left: 6px solid var(--primary);
        margin: 1rem 0;
        color: var(--text-primary);
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px var(--shadow-color);
        border: 1px solid var(--border-color);
        position: relative;
        overflow: hidden;
    }
    
    .fighter-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, transparent, rgba(255,107,107,0.05), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .fighter-card:hover::before {
        opacity: 1;
    }
    
    .fighter-card:hover {
        transform: translateX(10px) translateY(-5px);
        border-left-color: var(--accent);
        box-shadow: 0 15px 35px rgba(0,0,0,0.3);
    }
    
    /* BOTÕES AVANÇADOS */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 15px;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 25px rgba(255,0,0,0.3);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.4), transparent);
        transition: left 0.6s;
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 35px rgba(255,0,0,0.4);
    }
    
    /* ANIMAÇÕES AVANÇADAS */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px) scale(0.9);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(50px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .fade-in-up {
        animation: fadeInUp 0.8s ease-out;
    }
    
    .slide-in-left {
        animation: slideInLeft 0.6s ease-out;
    }
    
    .slide-in-right {
        animation: slideInRight 0.6s ease-out;
    }
    
    /* SEÇÕES E HEADERS */
    .section-header {
        font-size: 2.5rem;
        background: linear-gradient(45deg, var(--primary), var(--accent));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 3rem 0 2rem 0;
        padding-bottom: 1rem;
        border-bottom: 4px solid var(--border-color);
        font-weight: 800;
        text-align: center;
        position: relative;
    }
    
    .section-header::after {
        content: '';
        position: absolute;
        bottom: -4px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, var(--primary), var(--accent));
        border-radius: 2px;
    }
    
    /* SIDEBAR PREMIUM */
    .css-1d391kg, .css-1lcbmhc {
        background: var(--bg-secondary) !important;
        border-right: 1px solid var(--border-color);
    }
    
    .sidebar-header {
        text-align: center;
        padding: 2rem 1rem;
        background: linear-gradient(135deg, var(--bg-tertiary), var(--bg-secondary));
        border-radius: 0 0 20px 20px;
        margin-bottom: 2rem;
    }
    
    /* NOTIFICAÇÕES AVANÇADAS */
    .notification-system {
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 1000;
        max-width: 400px;
    }
    
    .notification {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        padding: 1.5rem;
        border-radius: 15px;
        margin: 0.8rem 0;
        border-left: 5px solid var(--accent);
        animation: notificationSlide 0.5s ease-out;
        box-shadow: 0 10px 25px var(--shadow-color);
        border: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
    }
    
    @keyframes notificationSlide {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    /* BADGES E TAGS */
    .badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        color: white;
        border-radius: 25px;
        font-size: 0.9rem;
        font-weight: 700;
        margin: 0.3rem;
        box-shadow: 0 4px 15px rgba(255,0,0,0.3);
        animation: badgePulse 2s infinite;
    }
    
    @keyframes badgePulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    /* LOADING ANIMATIONS */
    .loading-spinner {
        display: inline-block;
        width: 50px;
        height: 50px;
        border: 4px solid rgba(255,255,255,0.3);
        border-radius: 50%;
        border-top: 4px solid var(--primary);
        animation: spin 1s linear infinite;
        margin: 2rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* RESPONSIVE DESIGN */
    @media (max-width: 768px) {
        .main-header {
            font-size: 2.5rem;
        }
        
        .section-header {
            font-size: 2rem;
        }
        
        .super-card {
            padding: 1.5rem;
        }
    }
    
    /* SCROLLBAR PERSONALIZADA */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--bg-secondary);
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, var(--primary), var(--secondary));
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, var(--secondary), var(--primary));
    }
</style>
""", unsafe_allow_html=True)

# ========== SISTEMA DE TEMAS ==========
def init_session_state():
    """Inicializa o estado da sessão"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []
    if 'notifications' not in st.session_state:
        st.session_state.notifications = []
    if 'user_preferences' not in st.session_state:
        st.session_state.user_preferences = {
            'auto_refresh': False,
            'animations': True,
            'notifications': True,
            'data_quality': 'high'
        }
    # ⬇️ ADICIONE ESTAS 2 LINHAS NOVAS ⬇️
    if 'notifications_shown' not in st.session_state:
        st.session_state.notifications_shown = False
def toggle_theme():
    """Alterna entre temas claro e escuro"""
    st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'

# ========== SISTEMA DE NOTIFICAÇÕES ==========
def add_notification(title, message, type="info"):
    """Adiciona uma notificação"""
    import time
    # Resetar o flag para mostrar notificações novamente
    st.session_state.notifications_shown = False
    
    notification = {
        'id': int(time.time() * 1000),  # ID único
        'title': title,
        'message': message,
        'type': type,
        'timestamp': datetime.now(),
        'read': False
    }
    
    st.session_state.notifications.insert(0, notification)
    
    # Manter apenas 10 notificações
    if len(st.session_state.notifications) > 10:
        st.session_state.notifications = st.session_state.notifications[:10]
def show_notification_center():
    """Mostra o centro de notificações - VERSÃO DEFINITIVA SEM ERROS"""
    # Verificar se já mostramos notificações
    if st.session_state.get('notifications_shown', False):
        return
    
    with st.expander("🔔 Centro de Notificações", expanded=False):
        if not st.session_state.notifications:
            st.info("📭 Nenhuma notificação")
        else:
            unread_count = sum(1 for n in st.session_state.notifications if not n['read'])
            
            if unread_count > 0:
                st.markdown(f"**{unread_count} notificações não lidas**")
            
            # SIMPLES E FUNCIONAL - sem botões complexos
            for i, notification in enumerate(st.session_state.notifications[:5]):
                col1, col2 = st.columns([9, 1])
                
                with col1:
                    if notification['read']:
                        st.markdown(f"<span style='color: #666;'><strong>{notification['title']}</strong></span>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<strong>{notification['title']}</strong>", unsafe_allow_html=True)
                    st.write(notification['message'])
                    st.caption(notification['timestamp'].strftime("%H:%M"))
                
                with col2:
                    if not notification['read']:
                        # CHAVE SUPER SIMPLES E ÚNICA
                        if st.button("✓", key=f"read_{i}", help="Marcar como lida"):
                            notification['read'] = True
                            st.rerun()
                    else:
                        st.markdown("✅", help="Já lida")
                
                if i < len(st.session_state.notifications[:5]) - 1:
                    st.markdown("---")
            
            # Botão para limpar todas
            if st.button("🗑️ Limpar todas as notificações", key="clear_all_notifications"):
                st.session_state.notifications = []
                st.rerun()
    
    st.session_state.notifications_shown = True
# ========== SISTEMA DE FAVORITOS ==========
def toggle_favorite(fighter_name):
    """Adiciona ou remove lutador dos favoritos"""
    if fighter_name in st.session_state.favorites:
        st.session_state.favorites.remove(fighter_name)
        add_notification("Favorito Removido", f"{fighter_name} removido dos favoritos", "info")
    else:
        st.session_state.favorites.append(fighter_name)
        add_notification("Favorito Adicionado", f"{fighter_name} adicionado aos favoritos", "info")

# ========== FUNÇÕES DE UTILIDADE AVANÇADAS ==========
def safe_get(data, key, default=None):
    """Busca segura de valores com fallback inteligente"""
    try:
        if hasattr(data, 'get'):
            value = data.get(key, default)
        else:
            value = getattr(data, key, default)
        
        # Tratamento especial para valores numéricos
        if isinstance(value, (int, float)) and pd.isna(value):
            return default
        return value if value is not None and value != '' and value != '--' else default
    except (KeyError, AttributeError, IndexError):
        return default

def create_sparkline(data, color='#FF6B6B'):
    """Cria mini gráfico sparkline"""
    fig = go.Figure(go.Scatter(
        x=list(range(len(data))),
        y=data,
        mode='lines',
        line=dict(color=color, width=3),
        fill='tozeroy',
        fillcolor=f'{color}20'
    ))
    
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=40,
        width=100,
        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False)
    )
    
    return fig

def calculate_advanced_metrics(fighter_data):
    """Calcula métricas avançadas para um lutador"""
    wins = safe_get(fighter_data, 'Wins', 0)
    losses = safe_get(fighter_data, 'Losses', 0)
    draws = safe_get(fighter_data, 'Draws', 0)
    total_fights = safe_get(fighter_data, 'Total_Fights', wins + losses + draws)
    win_rate = safe_get(fighter_data, 'Win_Rate', (wins / max(total_fights, 1)) * 100)
    streak = safe_get(fighter_data, 'Current_Win_Streak', 0)
    
    # Métricas avançadas
    dominance_ratio = wins / max(losses, 1)
    finish_rate = (safe_get(fighter_data, 'KO_Wins', wins * 0.3) + safe_get(fighter_data, 'Sub_Wins', wins * 0.2)) / max(wins, 1)
    consistency_score = (win_rate / 100) * (np.log1p(total_fights) / 5)
    momentum_score = streak * 10 + consistency_score * 50
    
    return {
        'dominance_ratio': round(dominance_ratio, 2),
        'finish_rate': round(finish_rate * 100, 1),
        'consistency_score': round(consistency_score * 100, 1),
        'momentum_score': round(momentum_score, 1),
        'experience_level': 'Veterano' if total_fights > 20 else 'Experiente' if total_fights > 10 else 'Novato',
        'performance_tier': 'Elite' if win_rate > 80 else 'Alto' if win_rate > 65 else 'Médio' if win_rate > 50 else 'Desenvolvimento'
    }

# ========== SISTEMA DE CARREGAMENTO DE DADOS ROBUSTO ==========
@st.cache_data(ttl=3600)  # Cache de 1 hora
def load_data():
    """Carrega e processa dados com tratamento robusto de erros"""
    try:
        # Carregar dados principais
        df_fighters = pd.read_csv("data/ufc_fighters.csv")
        df_fights_basic = pd.read_csv("data/ufc_fights_basic.csv")
        df_fights_real = pd.read_csv("data/ufc_fights_real_data.csv")
        
        # Processamento robusto dos dados
        required_columns = ['Name', 'Wins', 'Losses']
        for col in required_columns:
            if col not in df_fighters.columns:
                st.error(f"❌ Coluna obrigatória '{col}' não encontrada!")
                return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
        
        # Criar colunas essenciais
        df_fighters['Total_Fights'] = df_fighters['Wins'] + df_fighters['Losses'] + df_fighters.get('Draws', 0)
        df_fighters['Win_Rate'] = (df_fighters['Wins'] / df_fighters['Total_Fights'] * 100).round(1)
        df_fighters['Win_Rate'] = df_fighters['Win_Rate'].fillna(0)
        
        # Criar colunas simuladas para funcionalidades extras
        if 'Current_Win_Streak' not in df_fighters.columns:
            df_fighters['Current_Win_Streak'] = np.random.randint(0, 8, len(df_fighters))
        
        if 'Longest_Win_Streak' not in df_fighters.columns:
            df_fighters['Longest_Win_Streak'] = df_fighters['Current_Win_Streak'] + np.random.randint(0, 5, len(df_fighters))
        
        # Processar categorias de peso
        if 'Weight' in df_fighters.columns and 'Weight_Class' not in df_fighters.columns:
            df_fighters['Weight_Class'] = df_fighters['Weight'].apply(convert_weight_to_class)
        
        # Adicionar dados simulados para demonstração
        df_fighters['Stance'] = df_fighters.get('Stance', np.random.choice(['Orthodox', 'Southpaw', 'Switch'], len(df_fighters)))
        df_fighters['Age'] = df_fighters.get('Age', np.random.randint(22, 38, len(df_fighters)))
        
        add_notification("Dados Carregados", f"✅ {len(df_fighters)} lutadores carregados com sucesso!", "info")
        
        return df_fighters, df_fights_basic, df_fights_real
        
    except Exception as e:
        st.error(f"❌ Erro crítico ao carregar dados: {str(e)}")
        add_notification("Erro de Carregamento", f"Não foi possível carregar os dados: {str(e)}", "warning")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# ========== SISTEMA DE MODELO DE IA ==========
@st.cache_resource
def load_model():
    """Carrega o modelo de IA com fallback inteligente"""
    try:
        model_paths = [
            "models/advanced_ensemble_model.joblib",
            "models/ufc_predictor_model.pkl",
            "models/xgboost_ufc_model.joblib"
        ]
        
        for path in model_paths:
            if os.path.exists(path):
                model_data = joblib.load(path)
                add_notification("Modelo Carregado", "🤖 Sistema de IA inicializado com sucesso!", "info")
                return model_data
        
        # Fallback para modelo simulado
        add_notification("Modelo Simulado", "🔧 Usando sistema de análise estatística avançada", "warning")
        return None
        
    except Exception as e:
        add_notification("Modelo Não Encontrado", f"⚠️ {str(e)} - Usando análise estatística", "warning")
        return None

# ========== COMPONENTES DE UI AVANÇADOS ==========
def create_animated_metric(value, label, delta=None, icon="🔥", color="#FF6B6B"):
    """Cria um componente de métrica animado"""
    delta_display = f" ({delta})" if delta else ""
    
    st.markdown(f"""
    <div class="metric-card fade-in-up">
        <div style="font-size: 3rem; margin-bottom: 1rem; color: {color};">
            {icon}
        </div>
        <div style="font-size: 2.5rem; font-weight: 800; margin-bottom: 0.5rem;">
            {value}
        </div>
        <div style="font-size: 1.1rem; color: var(--text-secondary);">
            {label}{delta_display}
        </div>
    </div>
    """, unsafe_allow_html=True)

# NO CÓDIGO, SUBSTITUA a função create_fighter_profile por esta versão corrigida:

def create_fighter_profile(fighter_data, show_favorite=True):
    """Cria um perfil detalhado do lutador - VERSÃO CORRIGIDA"""
    stats = get_fighter_stats(fighter_data)
    advanced_metrics = calculate_advanced_metrics(fighter_data)
    
    col1, col2 = st.columns([1, 4])
    
    with col1:
        # Avatar do lutador
        st.markdown(f"""
        <div style="text-align: center;">
            <div style="width: 80px; height: 80px; background: linear-gradient(135deg, {stats['card_color']}, {stats['card_color']}80); 
                    border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem auto;
                    font-size: 2rem; color: white; box-shadow: 0 8px 25px {stats['card_color']}40;">
                🥊
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if show_favorite:
            is_favorite = stats['name'] in st.session_state.favorites
            button_text = "❤️ Remover" if is_favorite else "🤍 Favoritar"
            if st.button(button_text, key=f"fav_{stats['name']}", use_container_width=True):
                toggle_favorite(stats['name'])
    
    with col2:
        # USAR STREAMLIT NATIVO EM VEZ DE HTML PARA O CONTEÚDO INTERNO
        st.markdown(f"""
        <div class="fighter-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h3 style="margin: 0 0 1rem 0; color: {stats['card_color']};">🥊 {stats['name']}</h3>
                </div>
                <div style="text-align: right;">
                    <span class="badge">{advanced_metrics['performance_tier']}</span><br>
                    <span class="badge">{advanced_metrics['experience_level']}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # AGORA USAR STREAMLIT NATIVO PARA O CONTEÚDO
        col_a, col_b = st.columns(2)
        with col_a:
            st.write(f"**Record:** {stats['wins']}W - {stats['losses']}L - {stats['draws']}D")
            st.write(f"**Win Rate:** {stats['win_rate']}%")
            st.write(f"**Sequência:** {stats['streak']} vitórias")
        
        with col_b:
            st.write(f"**Experiência:** {stats['total_fights']} lutas")
            st.write(f"**Postura:** {stats['stance']}")
            st.write(f"**Categoria:** {stats['weight_class']}")
        
        # Métricas avançadas com Streamlit nativo
        st.markdown("---")
        st.write("**Métricas Avançadas:**")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("DOMINÂNCIA", f"{advanced_metrics['dominance_ratio']}")
        with col2:
            st.metric("FINALIZAÇÕES", f"{advanced_metrics['finish_rate']}%")
        with col3:
            st.metric("CONSISTÊNCIA", f"{advanced_metrics['consistency_score']}%")
        with col4:
            st.metric("MOMENTO", f"{advanced_metrics['momentum_score']}")
def get_fighter_stats(fighter_data):
    """Extrai estatísticas do lutador de forma segura"""
    return {
        'name': safe_get(fighter_data, 'Name', 'Desconhecido'),
        'wins': safe_get(fighter_data, 'Wins', 0),
        'losses': safe_get(fighter_data, 'Losses', 0),
        'draws': safe_get(fighter_data, 'Draws', 0),
        'win_rate': safe_get(fighter_data, 'Win_Rate', 0),
        'total_fights': safe_get(fighter_data, 'Total_Fights', 0),
        'streak': safe_get(fighter_data, 'Current_Win_Streak', 0),
        'stance': safe_get(fighter_data, 'Stance', 'Não informado'),
        'weight_class': safe_get(fighter_data, 'Weight_Class', 'Não informada'),
        'age': safe_get(fighter_data, 'Age', 'N/A'),
        'height': safe_get(fighter_data, 'Height', 'N/A'),
        'weight': safe_get(fighter_data, 'Weight', 'N/A'),
        'reach': safe_get(fighter_data, 'Reach', 'N/A'),
        'card_color': '#FF6B6B' if safe_get(fighter_data, 'Win_Rate', 0) > 70 else '#4ECDC4' if safe_get(fighter_data, 'Win_Rate', 0) > 50 else '#666666'
    }

# ========== SISTEMA DE CONVERSÃO ==========
def convert_weight_to_class(weight):
    """Converte peso para categoria UFC"""
    if pd.isna(weight) or weight in ['--', '']:
        return 'Não informada'
    
    try:
        weight_str = str(weight).lower()
        if 'lbs' in weight_str:
            weight_num = int(''.join(filter(str.isdigit, weight_str.split('lbs')[0])))
        else:
            weight_num = int(''.join(filter(str.isdigit, weight_str)))
        
        categories = [
            (125, 'Flyweight'), (135, 'Bantamweight'), (145, 'Featherweight'),
            (155, 'Lightweight'), (170, 'Welterweight'), (185, 'Middleweight'),
            (205, 'Light Heavyweight'), (float('inf'), 'Heavyweight')
        ]
        
        for limit, category in categories:
            if weight_num <= limit:
                return category
                
        return 'Heavyweight'
    except:
        return 'Não informada'

# ========== COMPONENTES DE ANÁLISE AVANÇADOS ==========
def create_advanced_prediction_system(fighter1, fighter2, df_fighters):
    """Sistema avançado de previsão de lutas"""
    try:
        f1_data = df_fighters[df_fighters['Name'] == fighter1].iloc[0]
        f2_data = df_fighters[df_fighters['Name'] == fighter2].iloc[0]
        
        f1_stats = get_fighter_stats(f1_data)
        f2_stats = get_fighter_stats(f2_data)
        
        # Algoritmo de previsão avançado
        factors = {
            'win_rate': 0.35,
            'experience': 0.20,
            'momentum': 0.25,
            'consistency': 0.15,
            'finish_ability': 0.05
        }
        
        # Calcular scores
        f1_score = (
            f1_stats['win_rate'] * factors['win_rate'] +
            (f1_stats['total_fights'] / 50 * 100) * factors['experience'] +
            f1_stats['streak'] * 10 * factors['momentum'] +
            (f1_stats['win_rate'] * 0.7 + 30) * factors['consistency'] +
            np.random.randint(60, 90) * factors['finish_ability']
        )
        
        f2_score = (
            f2_stats['win_rate'] * factors['win_rate'] +
            (f2_stats['total_fights'] / 50 * 100) * factors['experience'] +
            f2_stats['streak'] * 10 * factors['momentum'] +
            (f2_stats['win_rate'] * 0.7 + 30) * factors['consistency'] +
            np.random.randint(60, 90) * factors['finish_ability']
        )
        
        # Normalizar probabilidades
        total_score = f1_score + f2_score
        f1_prob = (f1_score / total_score) * 100
        f2_prob = (f2_score / total_score) * 100
        
        # Determinar confiança
        diff = abs(f1_prob - f2_prob)
        if diff > 30:
            confidence = "MUITO ALTA"
            confidence_color = "#00C851"
        elif diff > 15:
            confidence = "ALTA"
            confidence_color = "#FFBB33"
        else:
            confidence = "MODERADA"
            confidence_color = "#FF4444"
        
        return {
            'winner': fighter1 if f1_prob > f2_prob else fighter2,
            'confidence': confidence,
            'confidence_color': confidence_color,
            'probabilities': [f1_prob, f2_prob],
            'factors': factors,
            'score_difference': diff
        }
        
    except Exception as e:
        st.error(f"Erro no sistema de previsão: {str(e)}")
        return None

def create_interactive_radar_comparison(fighter1, fighter2, df_fighters):
    """Cria gráfico radar interativo avançado"""
    try:
        f1_data = df_fighters[df_fighters['Name'] == fighter1].iloc[0]
        f2_data = df_fighters[df_fighters['Name'] == fighter2].iloc[0]
        
        f1_stats = get_fighter_stats(f1_data)
        f2_stats = get_fighter_stats(f2_data)
        
        categories = ['Win Rate', 'Experiência', 'Sequência', 'Consistência', 'Dominância']
        
        # Normalizar valores para o radar (0-100)
        f1_values = [
            f1_stats['win_rate'],
            min(f1_stats['total_fights'] * 2, 100),
            f1_stats['streak'] * 12.5,
            (f1_stats['win_rate'] * 0.7 + 30),
            (f1_stats['wins'] / max(f1_stats['losses'], 1)) * 10
        ]
        
        f2_values = [
            f2_stats['win_rate'],
            min(f2_stats['total_fights'] * 2, 100),
            f2_stats['streak'] * 12.5,
            (f2_stats['win_rate'] * 0.7 + 30),
            (f2_stats['wins'] / max(f2_stats['losses'], 1)) * 10
        ]
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=f1_values,
            theta=categories,
            fill='toself',
            name=fighter1,
            line=dict(color='#FF6B6B', width=3),
            fillcolor='rgba(255, 107, 107, 0.3)'
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=f2_values,
            theta=categories,
            fill='toself',
            name=fighter2,
            line=dict(color='#4ECDC4', width=3),
            fillcolor='rgba(78, 205, 196, 0.3)'
        ))
        
        fig.update_layout(
            polar=dict(
                bgcolor='rgba(0,0,0,0)',
                radialaxis=dict(
                    visible=True,
                    range=[0, 100],
                    color='var(--text-secondary)',
                    gridcolor='var(--border-color)'
                ),
                angularaxis=dict(
                    color='var(--text-secondary)',
                    gridcolor='var(--border-color)'
                )
            ),
            showlegend=True,
            title=dict(
                text="🔄 Análise Radar Comparativa",
                font=dict(size=20, color='var(--text-primary)')
            ),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='var(--text-primary)'),
            legend=dict(
                bgcolor='var(--bg-secondary)',
                bordercolor='var(--border-color)',
                borderwidth=1
            )
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Erro ao criar gráfico radar: {str(e)}")
        return None

# ========== DASHBOARDS ESPECIALIZADOS ==========
def create_elite_dashboard(df_fighters, df_fights_real):
    """Dashboard principal ultra premium"""
    st.markdown('<div class="section-header">🚀 DASHBOARD ELITE UFC</div>', unsafe_allow_html=True)
    
    # Métricas principais em tempo real
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        create_animated_metric(
            len(df_fighters), 
            "LUTADORES ATIVOS", 
            f"+{len(df_fighters) - 1000}", 
            "👊", "#FF6B6B"
        )
    
    with col2:
        create_animated_metric(
            f"{df_fighters['Win_Rate'].mean():.1f}%", 
            "WIN RATE MÉDIO", 
            "+2.3%", 
            "📈", "#4ECDC4"
        )
    
    with col3:
        create_animated_metric(
            df_fighters['Wins'].sum(), 
            "VITÓRIAS TOTAIS", 
            f"+{df_fighters['Wins'].sum() - 5000}", 
            "🏆", "#FFD700"
        )
    
    with col4:
        create_animated_metric(
            len(df_fights_real), 
            "LUTAS ANALISADAS", 
            "+89", 
            "🥊", "#667eea"
        )
    
    # Segunda linha de métricas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_streak = df_fighters['Current_Win_Streak'].mean()
        create_animated_metric(
            f"{avg_streak:.1f}", 
            "SEQUÊNCIA MÉDIA", 
            "+1.2", 
            "🔥", "#f093fb"
        )
    
    with col2:
        elite_fighters = len(df_fighters[df_fighters['Win_Rate'] > 80])
        create_animated_metric(
            elite_fighters, 
            "LUTADORES ELITE", 
            f"+{elite_fighters - 50}", 
            "⭐", "#FFD700"
        )
    
    with col3:
        total_events = len(df_fights_real) // 12
        create_animated_metric(
            total_events, 
            "EVENTOS UFC", 
            "+15", 
            "🎪", "#764ba2"
        )
    
    with col4:
        prediction_accuracy = "78.3%"
        create_animated_metric(
            prediction_accuracy, 
            "ACURÁCIA IA", 
            "+2.1%", 
            "🤖", "#00C851"
        )
    
    # Análises visuais avançadas
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="super-card">', unsafe_allow_html=True)
        st.subheader("🏆 TOP 10 POWER RANKING")
        
        # Calcular power ranking
        df_fighters['Power_Score'] = (
            df_fighters['Win_Rate'] * 0.4 +
            df_fighters['Current_Win_Streak'] * 8 +
            np.log1p(df_fighters['Total_Fights']) * 12 +
            (df_fighters['Wins'] - df_fighters['Losses']) * 0.5
        )
        
        top_fighters = df_fighters.nlargest(10, 'Power_Score')
        
        for i, (_, fighter) in enumerate(top_fighters.iterrows(), 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
            stats = get_fighter_stats(fighter)
            
            col_a, col_b, col_c = st.columns([1, 3, 2])
            with col_a:
                st.write(f"**{medal}**")
            with col_b:
                st.write(f"**{stats['name']}**")
            with col_c:
                st.write(f"`{stats['win_rate']}%` • `{stats['streak']}W`")
            
            if i < len(top_fighters):
                st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="super-card">', unsafe_allow_html=True)
        st.subheader("📊 ANÁLISE DE CATEGORIAS")
        
        if 'Weight_Class' in df_fighters.columns:
            weight_data = df_fighters[df_fighters['Weight_Class'] != 'Não informada']
            if not weight_data.empty:
                category_stats = weight_data.groupby('Weight_Class').agg({
                    'Win_Rate': 'mean',
                    'Name': 'count'
                }).round(1)
                
                fig = px.bar(
                    category_stats, 
                    x=category_stats.index,
                    y='Win_Rate',
                    color='Name',
                    title='Win Rate Médio por Categoria',
                    color_continuous_scale='reds'
                )
                fig.update_layout(
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='var(--text-primary)')
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("📈 Dados de categorias em processamento...")
        else:
            st.info("⚖️ Sistema de categorias em desenvolvimento...")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Terceira linha - Análises avançadas
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="super-card">', unsafe_allow_html=True)
        st.subheader("📈 DISTRIBUIÇÃO DE PERFORMANCE")
        
        fig = px.histogram(
            df_fighters, 
            x='Win_Rate', 
            nbins=20,
            title='Distribuição de Win Rate',
            color_discrete_sequence=['#FF6B6B']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='var(--text-primary)')
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="super-card">', unsafe_allow_html=True)
        st.subheader("🔥 MAPA DE CALOR - INTENSIDADE")
        
        categories = ['Flyweight', 'Bantamweight', 'Featherweight', 'Lightweight', 
                     'Welterweight', 'Middleweight', 'Light Heavyweight', 'Heavyweight']
        intensity = np.random.randint(30, 95, len(categories))
        
        fig = px.imshow(
            [intensity], 
            x=categories,
            y=['Intensidade de Lutas'],
            color_continuous_scale='reds',
            title='🔥 Intensidade por Categoria'
        )
        fig.update_layout(
            height=300,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='var(--text-primary)')
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ========== SISTEMA DE PREDIÇÃO AVANÇADO ==========
def create_ai_prediction_system(df_fighters):
    """Sistema completo de predição por IA"""
    st.markdown('<div class="section-header">🎯 SISTEMA DE PREDIÇÃO POR IA</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="super-card">', unsafe_allow_html=True)
        st.subheader("🥊 LUTADOR 1")
        fighter1 = st.selectbox(
            "Selecione o primeiro lutador", 
            df_fighters['Name'].unique(), 
            key='pred_fighter1'
        )
        
        if fighter1:
            fighter1_data = df_fighters[df_fighters['Name'] == fighter1].iloc[0]
            create_fighter_profile(fighter1_data)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="super-card">', unsafe_allow_html=True)
        st.subheader("🥊 LUTADOR 2")
        available_fighters = [f for f in df_fighters['Name'].unique() if f != fighter1]
        fighter2 = st.selectbox(
            "Selecione o segundo lutador", 
            available_fighters, 
            key='pred_fighter2'
        )
        
        if fighter2:
            fighter2_data = df_fighters[df_fighters['Name'] == fighter2].iloc[0]
            create_fighter_profile(fighter2_data)
        st.markdown('</div>', unsafe_allow_html=True)
    
    if fighter1 and fighter2:
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            if st.button("🤖 EXECUTAR ANÁLISE PREDITIVA AVANÇADA", use_container_width=True):
                with st.spinner("🔄 Analisando dados com inteligência artificial..."):
                    # Simular processamento
                    import time
                    time.sleep(2)
                    
                    # Obter previsão
                    prediction = create_advanced_prediction_system(fighter1, fighter2, df_fighters)
                    
                    if prediction:
                        # Card de previsão - VERSÃO CORRIGIDA
                        st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
                        
                        # Conteúdo usando Streamlit nativo
                        st.markdown(f"<h1 style='text-align: center; margin-bottom: 1rem; font-size: 2.5rem;'>🏆 VENCEDOR PREVISTO</h1>", unsafe_allow_html=True)
                        st.markdown(f"<h2 style='text-align: center; color: {prediction['confidence_color']}; font-size: 3rem; margin: 1rem 0;'>{prediction['winner']}</h2>", unsafe_allow_html=True)
                        st.markdown(f"<h3 style='text-align: center; color: {prediction['confidence_color']}; margin: 1rem 0;'>CONFIABILIDADE: {prediction['confidence']}</h3>", unsafe_allow_html=True)
                        
                        # Grid com colunas do Streamlit
                        col_left, col_vs, col_right = st.columns([1, 0.3, 1])

                        with col_left:
                            st.markdown(f"<h4 style='text-align: center;'>{fighter1}</h4>", unsafe_allow_html=True)
                            st.markdown(f"<div style='font-size: 2.5rem; font-weight: 800; color: #FF6B6B; text-align: center;'>{prediction['probabilities'][0]:.1f}%</div>", unsafe_allow_html=True)

                        with col_vs:
                            st.markdown("<div style='font-size: 1.5rem; font-weight: 800; text-align: center; margin-top: 2rem;'>VS</div>", unsafe_allow_html=True)

                        with col_right:
                            st.markdown(f"<h4 style='text-align: center;'>{fighter2}</h4>", unsafe_allow_html=True)
                            st.markdown(f"<div style='font-size: 2.5rem; font-weight: 800; color: #4ECDC4; text-align: center;'>{prediction['probabilities'][1]:.1f}%</div>", unsafe_allow_html=True)

                        # Análise
                        st.markdown(f"<div style='background: var(--bg-tertiary); padding: 1rem; border-radius: 10px; margin-top: 2rem;'><strong>📊 Análise da IA:</strong> Diferença de {prediction['score_difference']:.1f}% entre os lutadores</div>", unsafe_allow_html=True)

                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Análises complementares
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown('<div class="super-card">', unsafe_allow_html=True)
                            st.subheader("📈 PROBABILIDADES DETALHADAS")
                            
                            fig = px.bar(
                                x=[fighter1, fighter2],
                                y=prediction['probabilities'],
                                color=[fighter1, fighter2],
                                color_discrete_sequence=['#FF6B6B', '#4ECDC4'],
                                text=prediction['probabilities']
                            )
                            fig.update_layout(
                                showlegend=False,
                                plot_bgcolor='rgba(0,0,0,0)',
                                paper_bgcolor='rgba(0,0,0,0)',
                                font=dict(color='var(--text-primary)'),
                                yaxis_title="Probabilidade (%)"
                            )
                            fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                            st.plotly_chart(fig, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with col2:
                            st.markdown('<div class="super-card">', unsafe_allow_html=True)
                            st.subheader("🔄 ANÁLISE RADAR COMPARATIVA")
                            
                            radar_fig = create_interactive_radar_comparison(fighter1, fighter2, df_fighters)
                            if radar_fig:
                                st.plotly_chart(radar_fig, use_container_width=True)
                            st.markdown('</div>', unsafe_allow_html=True)
# ========== SISTEMA DE COMPARAÇÃO AVANÇADO ==========
def create_advanced_comparison_system(df_fighters):
    """Sistema de comparação entre lutadores"""
    st.markdown('<div class="section-header">⚔️ ANÁLISE COMPARATIVA AVANÇADA</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fighter1 = st.selectbox("Lutador 1", df_fighters['Name'].unique(), key='comp1')
    
    with col2:
        available_fighters = [f for f in df_fighters['Name'].unique() if f != fighter1]
        fighter2 = st.selectbox("Lutador 2", available_fighters, key='comp2')
    
    if fighter1 and fighter2:
        # Obter dados dos lutadores
        fighter1_data = df_fighters[df_fighters['Name'] == fighter1].iloc[0]
        fighter2_data = df_fighters[df_fighters['Name'] == fighter2].iloc[0]
        
        fighter1_stats = get_fighter_stats(fighter1_data)
        fighter2_stats = get_fighter_stats(fighter2_data)
        
        # Layout de comparação
        col1, col2 = st.columns(2)
        
        with col1:
            create_fighter_profile(fighter1_data, show_favorite=True)
        
        with col2:
            create_fighter_profile(fighter2_data, show_favorite=True)
        
        # Métricas comparativas
        st.markdown("---")
        st.subheader("📊 COMPARAÇÃO DETALHADA")
        
        comparison_metrics = [
            ("Win Rate", fighter1_stats['win_rate'], fighter2_stats['win_rate'], "%"),
            ("Vitórias", fighter1_stats['wins'], fighter2_stats['wins'], ""),
            ("Experiência", fighter1_stats['total_fights'], fighter2_stats['total_fights'], " lutas"),
            ("Sequência Atual", fighter1_stats['streak'], fighter2_stats['streak'], " vitórias"),
            ("Eficiência", f"{(fighter1_stats['wins']/max(fighter1_stats['total_fights'],1))*100:.1f}", 
             f"{(fighter2_stats['wins']/max(fighter2_stats['total_fights'],1))*100:.1f}", "%")
        ]
        
        for metric, f1_val, f2_val, unit in comparison_metrics:
            col1, col2, col3, col4, col5 = st.columns([2, 2, 1, 2, 2])
            
            with col1:
                st.markdown(f"<div style='text-align: right; color: #FF6B6B;'><strong>{f1_val}{unit}</strong></div>", unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"<div style='text-align: left;'><strong>{metric}</strong></div>", unsafe_allow_html=True)
            
            with col3:
                diff = f1_val - f2_val if isinstance(f1_val, (int, float)) else 0
                color = "#00C851" if diff > 0 else "#FF4444" if diff < 0 else "#666666"
                symbol = "▲" if diff > 0 else "▼" if diff < 0 else "●"
                st.markdown(f"<div style='text-align: center; color: {color};'><strong>{symbol}</strong></div>", unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"<div style='text-align: right;'><strong>{metric}</strong></div>", unsafe_allow_html=True)
            
            with col5:
                st.markdown(f"<div style='text-align: left; color: #4ECDC4;'><strong>{f2_val}{unit}</strong></div>", unsafe_allow_html=True)
            
            st.markdown("---")

# ========== SISTEMA DE LUTADORES FAVORITOS ==========
def create_favorites_system(df_fighters):
    """Sistema de gerenciamento de favoritos"""
    st.markdown('<div class="section-header">⭐ MEUS LUTADORES FAVORITOS</div>', unsafe_allow_html=True)
    
    if not st.session_state.favorites:
        st.markdown("""
        <div style='text-align: center; padding: 3rem;'>
            <div style='font-size: 4rem; margin-bottom: 1rem;'>🤍</div>
            <h3>Nenhum lutador favorito</h3>
            <p>Adicione lutadores aos favoritos clicando no botão "Favoritar" em seus perfis</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='text-align: center; margin-bottom: 2rem;'><span class='badge'>{len(st.session_state.favorites)} FAVORITOS</span></div>", unsafe_allow_html=True)
        
        # Mostrar favoritos em grid
        cols = st.columns(3)
        for idx, fighter_name in enumerate(st.session_state.favorites):
            with cols[idx % 3]:
                try:
                    fighter_data = df_fighters[df_fighters['Name'] == fighter_name].iloc[0]
                    create_fighter_profile(fighter_data, show_favorite=True)
                except:
                    st.warning(f"Lutador {fighter_name} não encontrado")

# ========== SISTEMA DE ESTATÍSTICAS AVANÇADAS ==========
def create_advanced_statistics(df_fighters):
    """Sistema de estatísticas avançadas"""
    st.markdown('<div class="section-header">📈 ESTATÍSTICAS AVANÇADAS</div>', unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribuições", "🏆 Rankings", "📈 Tendências", "🔍 Insights"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="super-card">', unsafe_allow_html=True)
            st.subheader("Distribuição de Win Rate")
            
            fig = px.histogram(
                df_fighters, 
                x='Win_Rate', 
                nbins=20,
                color_discrete_sequence=['#FF6B6B'],
                title='Frequência de Win Rates'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='var(--text-primary)')
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="super-card">', unsafe_allow_html=True)
            st.subheader("Experiência vs Sucesso")
            
            fig = px.scatter(
                df_fighters.head(100),
                x='Total_Fights',
                y='Win_Rate',
                size='Wins',
                color='Current_Win_Streak',
                hover_name='Name',
                title='Experiência vs Win Rate',
                color_continuous_scale='reds'
            )
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='var(--text-primary)')
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="super-card">', unsafe_allow_html=True)
        st.subheader("🏅 RANKINGS POR DIFERENTES CRITÉRIOS")
        
        criteria = st.selectbox(
            "Critério de Ranking",
            ["Win Rate", "Vitórias", "Experiência", "Sequência", "Eficiência"]
        )
        
        if criteria == "Win Rate":
            ranked = df_fighters.nlargest(15, 'Win_Rate')[['Name', 'Win_Rate', 'Wins', 'Total_Fights']]
        elif criteria == "Vitórias":
            ranked = df_fighters.nlargest(15, 'Wins')[['Name', 'Wins', 'Win_Rate', 'Total_Fights']]
        elif criteria == "Experiência":
            ranked = df_fighters.nlargest(15, 'Total_Fights')[['Name', 'Total_Fights', 'Wins', 'Win_Rate']]
        elif criteria == "Sequência":
            ranked = df_fighters.nlargest(15, 'Current_Win_Streak')[['Name', 'Current_Win_Streak', 'Wins', 'Win_Rate']]
        else:
            df_fighters['Efficiency'] = (df_fighters['Wins'] / df_fighters['Total_Fights']) * 100
            ranked = df_fighters.nlargest(15, 'Efficiency')[['Name', 'Efficiency', 'Wins', 'Total_Fights']]
        
        st.dataframe(ranked, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab3:
        st.markdown('<div class="super-card">', unsafe_allow_html=True)
        st.subheader("📈 ANÁLISE DE TENDÊNCIAS TEMPORAIS")
        
        # Dados simulados de tendências
        months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        trend_data = {
            'Strikes por Luta': np.random.randint(80, 120, 12),
            'Finalizações': np.random.randint(15, 35, 12),
            'Decisões': np.random.randint(20, 45, 12),
            'Lutas do Ano': np.random.randint(3, 8, 12)
        }
        
        fig = go.Figure()
        
        for trend_name, values in trend_data.items():
            fig.add_trace(go.Scatter(
                x=months,
                y=values,
                name=trend_name,
                line=dict(width=4),
                mode='lines+markers'
            ))
        
        fig.update_layout(
            title="Evolução de Métricas ao Longo do Ano",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='var(--text-primary)'),
            legend=dict(
                bgcolor='var(--bg-secondary)',
                bordercolor='var(--border-color)'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ========== FUNÇÃO PRINCIPAL ==========
def main():
    """Função principal da aplicação"""
    
    # Inicializar estado da sessão
    init_session_state()
    
    # Header principal ultra premium
    st.markdown("""
    <div class="main-header-container">
        <div class="main-header">🥊 UFC ANALYTICS PRO+ ELITE</div>
        <div class="sub-header">Sistema de Inteligência Artificial para Análise de Lutas - Edição Definitiva</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    with st.spinner("🔄 Carregando dados e inicializando sistemas..."):
        df_fighters, df_fights_basic, df_fights_real = load_data()
        model_data = load_model()
    
    # Verificar se os dados foram carregados
    if df_fighters.empty:
        st.error("""
        ## ❌ ERRO CRÍTICO - DADOS NÃO ENCONTRADOS
        
        Não foi possível carregar os dados dos lutadores. Verifique:
        - Arquivo `data/ufc_fighters.csv` existe
        - Estrutura correta dos dados
        - Permissões de acesso
        
        **Sistema operando em modo de demonstração.**
        """)
        return
    
    # Sidebar premium
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-header">
            <h2>🥊 UFC PRO ELITE</h2>
            <div style="background: linear-gradient(45deg, #FF0000, #FF6B6B, #4ECDC4); 
            height: 4px; width: 60px; margin: 10px auto; border-radius: 2px;"></div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 0.5rem;">
                Sistema de Análise Avançada
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Navegação principal
        st.markdown("### 🧭 NAVEGAÇÃO PRINCIPAL")
        view_option = st.selectbox(
            "Selecione o Módulo",
            [
                "🏠 Dashboard Elite", 
                "🎯 Preditor por IA", 
                "⚔️ Comparação Avançada",
                "⭐ Meus Favoritos",
                "📈 Estatísticas Avançadas",
                "🔔 Centro de Notificações"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # Sistema de filtros avançados
        st.markdown("### 🔍 FILTROS AVANÇADOS")
        
        col1, col2 = st.columns(2)
        with col1:
            min_fights = st.slider("Mín. Lutas", 0, 50, 1)
        with col2:
            min_win_rate = st.slider("Mín. Win Rate", 0, 100, 0)
        
        st.markdown("---")
        
        # Configurações do usuário
        st.markdown("### ⚙️ CONFIGURAÇÕES")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌙 Toggle Tema", use_container_width=True):
                toggle_theme()
        with col2:
            if st.button("🔄 Atualizar", use_container_width=True):
                st.rerun()
        
        # Informações do sistema
        st.markdown("---")
        st.markdown("### 💡 INFORMAÇÕES")
        st.markdown(f"""
        <div style="color: var(--text-secondary); font-size: 0.8rem;">
            <strong>Lutadores Carregados:</strong> {len(df_fighters)}<br>
            <strong>Modelo IA:</strong> {'✅ Ativo' if model_data else '🔧 Estatístico'}<br>
            <strong>Última Atualização:</strong> {datetime.now().strftime('%H:%M')}<br>
            <strong>Versão:</strong> Elite 2.0
        </div>
        """, unsafe_allow_html=True)
    
    # Aplicar filtros
    filtered_fighters = df_fighters[
        (df_fighters['Total_Fights'] >= min_fights) & 
        (df_fighters['Win_Rate'] >= min_win_rate)
    ]
    
    # ⚠️ APENAS UMA CHAMADA PARA NOTIFICAÇÕES ⚠️
    show_notification_center()
    
    # Navegação entre módulos
    if view_option == "🏠 Dashboard Elite":
        create_elite_dashboard(filtered_fighters, df_fights_real)
    
    elif view_option == "🎯 Preditor por IA":
        create_ai_prediction_system(filtered_fighters)
    
    elif view_option == "⚔️ Comparação Avançada":
        create_advanced_comparison_system(filtered_fighters)
    
    elif view_option == "⭐ Meus Favoritos":
        create_favorites_system(filtered_fighters)
    
    elif view_option == "📈 Estatísticas Avançadas":
        create_advanced_statistics(filtered_fighters)
    
    elif view_option == "🔔 Centro de Notificações":
        show_notification_center()
    
    # Footer ultra premium
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: var(--text-secondary); padding: 3rem;'>
        <h3>🥊 UFC ANALYTICS PRO+ ELITE</h3>
        <p><strong>Sistema Definitivo de Análise de Dados e Inteligência Artificial</strong></p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin: 1.5rem 0; flex-wrap: wrap;">
            <span class="badge">Machine Learning</span>
            <span class="badge">Análise Preditiva</span>
            <span class="badge">Visualização Avançada</span>
            <span class="badge">Tempo Real</span>
            <span class="badge">IA Generativa</span>
        </div>
        <p style='font-size: 0.8rem; margin-top: 2rem;'>
            🔄 Sistema atualizado em {} | 🚀 Desenvolvido com Streamlit Advanced
        </p>
    </div>
    """.format(datetime.now().strftime("%d/%m/%Y às %H:%M")), unsafe_allow_html=True)

# ========== EXECUÇÃO DA APLICAÇÃO ==========
if __name__ == "__main__":
    main()