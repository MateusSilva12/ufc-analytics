# analise_simples.py - VERSÃO DEFINITIVA
import pandas as pd
import numpy as np

# Carregar CSV
df = pd.read_csv("data/ufc_fighters.csv")

print("=== ANÁLISE UFC FIGHTERS ===")
print(f"Total de lutadores: {len(df)}")

# VERIFICAR TIPOS DE DADOS
print("\n=== TIPOS DE DADOS ===")
for col in df.columns:
    print(f"{col}: {df[col].dtype}")

# CONVERTER COLUNAS NUMÉRICAS SE NECESSÁRIO
for col in ['Wins', 'Losses', 'Draws']:
    if df[col].dtype == 'object':
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)

# ANÁLISE 1: Estatísticas básicas
print("\n" + "="*50)
print("ESTATÍSTICAS BÁSICAS:")
print(f"Total de vitórias: {df['Wins'].sum()}")
print(f"Total de derrotas: {df['Losses'].sum()}")
print(f"Total de empates: {df['Draws'].sum()}")
print(f"Média de vitórias: {df['Wins'].mean():.1f}")
print(f"Média de derrotas: {df['Losses'].mean():.1f}")

# ANÁLISE 2: Top lutadores
print("\n" + "="*50)
print("TOP 10 MAIS VITORIOSOS:")
top_winners = df.nlargest(10, 'Wins')[['Name', 'Wins', 'Losses', 'Draws']]
for i, row in top_winners.iterrows():
    print(f"{row['Name']}: {row['Wins']}W {row['Losses']}L {row['Draws']}D")

# ANÁLISE 3: Posturas
print("\n" + "="*50)
print("DISTRIBUIÇÃO DE POSTURAS:")
stance_counts = df['Stance'].value_counts().head(10)
for stance, count in stance_counts.items():
    print(f"{stance}: {count} lutadores")

# ANÁLISE 4: Experiência
print("\n" + "="*50)
print("LUTADORES MAIS EXPERIENTES:")
df['Total_Fights'] = df['Wins'] + df['Losses'] + df['Draws']
most_experienced = df.nlargest(10, 'Total_Fights')[['Name', 'Total_Fights']]
for i, row in most_experienced.iterrows():
    print(f"{row['Name']}: {row['Total_Fights']} lutas")

# ANÁLISE 5: Eficiência
print("\n" + "="*50)
print("LUTADORES MAIS EFICIENTES (min. 10 lutas):")
experienced = df[df['Total_Fights'] >= 10]
if len(experienced) > 0:
    experienced['Win_Rate'] = (experienced['Wins'] / experienced['Total_Fights'] * 100).round(1)
    best_records = experienced.nlargest(10, 'Win_Rate')[['Name', 'Win_Rate', 'Wins', 'Total_Fights']]
    for i, row in best_records.iterrows():
        print(f"{row['Name']}: {row['Win_Rate']}% ({row['Wins']}/{row['Total_Fights']})")

print("\n" + "="*50)
print("ANÁLISE CONCLUÍDA! 🏆")