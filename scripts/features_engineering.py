# features_engineering.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

def create_advanced_features(df_fights, df_fighters):
    """Cria features avançadas para melhorar acurácia"""
    
    features_list = []
    
    for _, fight in df_fights.iterrows():
        try:
            # Buscar dados dos lutadores
            f1_data = df_fighters[df_fighters['Name'] == fight['fighter_1']].iloc[0]
            f2_data = df_fighters[df_fighters['Name'] == fight['fighter_2']].iloc[0]
            
            # FEATURES BÁSICAS
            features = {
                # Win Rate e Experiência
                'f1_win_rate': f1_data['Win_Rate'],
                'f2_win_rate': f2_data['Win_Rate'],
                'f1_total_fights': f1_data['Total_Fights'],
                'f2_total_fights': f2_data['Total_Fights'],
                'f1_experience_ratio': f1_data['Total_Fights'] / max(f2_data['Total_Fights'], 1),
                
                # Sequências e Momentum
                'f1_win_streak': f1_data.get('Current_Win_Streak', 0),
                'f2_win_streak': f2_data.get('Current_Win_Streak', 0),
                'f1_loss_streak': f1_data.get('Current_Loss_Streak', 0),
                'f2_loss_streak': f2_data.get('Current_Loss_Streak', 0),
                
                # Eficiência e Consistência
                'f1_win_consistency': (f1_data['Wins'] - f1_data['Losses']) / max(f1_data['Total_Fights'], 1),
                'f2_win_consistency': (f2_data['Wins'] - f2_data['Losses']) / max(f2_data['Total_Fights'], 1),
                'f1_ko_ratio': f1_data.get('KO_Wins', 0) / max(f1_data['Wins'], 1),
                'f2_ko_ratio': f2_data.get('KO_Wins', 0) / max(f2_data['Wins'], 1),
                
                # Features Comparativas
                'win_rate_diff': f1_data['Win_Rate'] - f2_data['Win_Rate'],
                'experience_diff': f1_data['Total_Fights'] - f2_data['Total_Fights'],
                'streak_diff': f1_data.get('Current_Win_Streak', 0) - f2_data.get('Current_Win_Streak', 0),
                
                # Features de Interação
                'win_rate_product': f1_data['Win_Rate'] * f2_data['Win_Rate'],
                'experience_product': f1_data['Total_Fights'] * f2_data['Total_Fights'],
                
                # Target
                'winner': 0 if fight['winner'] == fight['fighter_1'] else 1
            }
            
            features_list.append(features)
            
        except Exception as e:
            continue
    
    return pd.DataFrame(features_list)

def add_rolling_features(df, window=5):
    """Adiciona features de tendência temporal"""
    df = df.sort_values('date')  # Supondo que temos data
    
    # Rolling stats
    df['f1_rolling_win_rate'] = df['f1_win_rate'].rolling(window=window).mean()
    df['f2_rolling_win_rate'] = df['f2_win_rate'].rolling(window=window).mean()
    df['f1_form_momentum'] = df['f1_win_streak'] - df['f1_loss_streak']
    df['f2_form_momentum'] = df['f2_win_streak'] - df['f2_loss_streak']
    
    return df.fillna(method='bfill')