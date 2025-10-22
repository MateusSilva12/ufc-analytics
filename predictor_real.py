# predictor_real.py
import pandas as pd
import numpy as np
import joblib

def create_real_features(fighter1, fighter2, df_fighters):
    """Cria features reais para o modelo baseado nos stats dos lutadores"""
    
    # Buscar dados dos lutadores
    f1_data = df_fighters[df_fighters['Name'] == fighter1].iloc[0]
    f2_data = df_fighters[df_fighters['Name'] == fighter2].iloc[0]
    
    # Calcular features similares às usadas no treino
    features = {
        '00_2_f1_made': f1_data.get('Wins', 0) / 10,  # Normalizado
        '00_2_f1_attempt': f1_data.get('Total_Fights', 10) / 10,
        '00_2_f2_made': f2_data.get('Wins', 0) / 10,
        '00_2_f2_attempt': f2_data.get('Total_Fights', 10) / 10,
        '10_2_f1_made': f1_data.get('Win_Rate', 50) / 100,
        '10_2_f1_attempt': 1.0,  # Placeholder
        '10_2_f2_made': f2_data.get('Win_Rate', 50) / 100,
        '10_2_f2_attempt': 1.0   # Placeholder
    }
    
    return pd.DataFrame([features])

def load_model_safe():
    """Carrega modelo com tratamento de erro"""
    try:
        return joblib.load("models/xgb_ufc_real.joblib")
    except Exception as e:
        print(f"Erro ao carregar modelo: {e}")
        return None