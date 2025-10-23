# Crie este arquivo como scripts/debug_features.py
import pandas as pd
import numpy as np

def debug_features():
    print("🔍 DEBUG DETALHADO DA CRIAÇÃO DE FEATURES")
    print("=" * 50)
    
    # Carregar dados
    df_fights = pd.read_csv('data/ufc_fights_real_data.csv')
    df_fighters = pd.read_csv('data/ufc_fighters.csv')
    
    print(f"📊 Dados carregados: {len(df_fights)} lutas, {len(df_fighters)} lutadores")
    
    # Testar as primeiras 5 lutas
    for i in range(min(5, len(df_fights))):
        fight = df_fights.iloc[i]
        print(f"\n--- Luta {i+1} ---")
        print(f"Lutador 1: '{fight['fighter_1']}'")
        print(f"Lutador 2: '{fight['fighter_2']}'")
        print(f"Winner: '{fight['winner']}'")
        
        try:
            # Tentar encontrar lutador 1
            f1_match = df_fighters[df_fighters['Name'] == fight['fighter_1']]
            print(f"Lutador 1 encontrado: {len(f1_match)} registros")
            if len(f1_match) > 0:
                f1_data = f1_match.iloc[0]
                print(f"  Dados: {f1_data['Wins']}W-{f1_data['Losses']}L, Win Rate: {f1_data['Win_Rate']}%")
            
            # Tentar encontrar lutador 2
            f2_match = df_fighters[df_fighters['Name'] == fight['fighter_2']]
            print(f"Lutador 2 encontrado: {len(f2_match)} registros")
            if len(f2_match) > 0:
                f2_data = f2_match.iloc[0]
                print(f"  Dados: {f2_data['Wins']}W-{f2_data['Losses']}L, Win Rate: {f2_data['Win_Rate']}%")
            
            # Testar a lógica do winner
            if fight['winner'] == 'fighter_1':
                winner = 0
                print("✅ Winner determinado: fighter_1 -> 0")
            elif fight['winner'] == 'fighter_2':
                winner = 1
                print("✅ Winner determinado: fighter_2 -> 1")
            else:
                print(f"❌ Winner não reconhecido: '{fight['winner']}'")
                
        except Exception as e:
            print(f"❌ Erro: {e}")

if __name__ == "__main__":
    debug_features()