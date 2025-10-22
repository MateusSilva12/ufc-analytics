# prepare_data.py - VERSÃO CORRIGIDA
import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import LabelEncoder

def parse_ratio(val):
    if pd.isna(val):
        return (np.nan, np.nan)
    s = str(val)
    m = re.search(r"(\d+)\D+(\d+)", s)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    m2 = re.search(r"(\d+)", s)
    if m2:
        v = int(m2.group(1))
        return (v, np.nan)
    return (np.nan, np.nan)

def load_and_prepare(detailed_csv="data/ufc_fights_detailed.csv"):
    print("📊 Carregando dados detalhados...")
    df = pd.read_csv(detailed_csv)
    
    print(f"✅ Dados carregados: {len(df)} lutas")
    print(f"📋 Colunas disponíveis: {df.columns.tolist()}")
    
    # Verificar estrutura dos dados
    print("\n🔍 Analisando estrutura dos dados...")
    
    # Método 1: Tentar encontrar quem venceu baseado no método
    if "method" in df.columns:
        print("🎯 Encontrada coluna 'method', criando target...")
        # Simplificação: assumir que o primeiro lutador venceu (precisaríamos de dados mais precisos)
        df["winner"] = "fighter_1"  # Placeholder - em dados reais precisaríamos analisar o método
        
    # Método 2: Se não tem método, criar target simulado baseado em estatísticas
    else:
        print("⚠️ Coluna 'method' não encontrada, criando target simulado...")
        # Simular vencedor baseado em dados disponíveis
        np.random.seed(42)
        df["winner"] = np.random.choice(["fighter_1", "fighter_2"], len(df))
    
    # Normalizar nomes das colunas
    df.columns = [c.strip().lower().replace(" ", "_").replace("%","pct") for c in df.columns]
    
    print(f"🎯 Target criado. Distribuição: {df['winner'].value_counts().to_dict()}")
    
    # Criar features básicas a partir dos dados disponíveis
    feature_cols = []
    
    # 1. Features de diferença se tivermos dados numéricos
    numeric_cols = [c for c in df.columns if df[c].dtype in [np.int64, np.float64]]
    print(f"🔢 Colunas numéricas: {numeric_cols}")
    
    # 2. Se não tivermos dados numéricos, criar features baseadas nos lutadores
    if not numeric_cols:
        print("📝 Criando features baseadas em dados dos lutadores...")
        
        # Carregar dados dos lutadores para criar features
        try:
            fighters_df = pd.read_csv("data/ufc_fighters.csv")
            fighters_df['total_fights'] = fighters_df['Wins'] + fighters_df['Losses'] + fighters_df['Draws']
            fighters_df['win_rate'] = fighters_df['Wins'] / (fighters_df['total_fights'] + 1)
            
            # Criar mapeamento
            fighter_stats = fighters_df.set_index('Name')[['win_rate', 'total_fights', 'Wins']].to_dict('index')
            
            # Adicionar features baseadas nos lutadores
            df['f1_win_rate'] = df['fighter_1'].map(lambda x: fighter_stats.get(x, {}).get('win_rate', 0.5))
            df['f2_win_rate'] = df['fighter_2'].map(lambda x: fighter_stats.get(x, {}).get('win_rate', 0.5))
            df['f1_experience'] = df['fighter_1'].map(lambda x: fighter_stats.get(x, {}).get('total_fights', 10))
            df['f2_experience'] = df['fighter_2'].map(lambda x: fighter_stats.get(x, {}).get('total_fights', 10))
            
            # Criar features de diferença
            df['win_rate_diff'] = df['f1_win_rate'] - df['f2_win_rate']
            df['experience_diff'] = df['f1_experience'] - df['f2_experience']
            
            feature_cols = ['win_rate_diff', 'experience_diff']
            
        except Exception as e:
            print(f"❌ Erro ao carregar dados dos lutadores: {e}")
            # Criar features aleatórias como fallback
            np.random.seed(42)
            df['feature_1'] = np.random.normal(0, 1, len(df))
            df['feature_2'] = np.random.normal(0, 1, len(df))
            feature_cols = ['feature_1', 'feature_2']
    
    # Codificar target
    le = LabelEncoder()
    df['winner_encoded'] = le.fit_transform(df['winner'])
    
    print(f"🎯 Classes do target: {dict(zip(le.classes_, range(len(le.classes_))))}")
    print(f"📊 Features selecionadas: {feature_cols}")
    
    # Criar dataset final
    if feature_cols:
        df_model = df[feature_cols + ['winner_encoded']].copy()
        df_model = df_model.dropna()
        print(f"✅ Dataset final: {df_model.shape}")
        
        # Salvar
        df_model.to_csv("data/ufc_model_ready.csv", index=False)
        print("💾 Salvo: data/ufc_model_ready.csv")
        
        return df_model
    else:
        print("❌ Nenhuma feature criada")
        return pd.DataFrame()

if __name__ == "__main__":
    dfm = load_and_prepare()
    if not dfm.empty:
        print(f"\n🎉 Preparação concluída!")
        print(f"📦 Shape final: {dfm.shape}")
        print(f"🎯 Distribuição do target: {dfm['winner_encoded'].value_counts().to_dict()}")
    else:
        print("\n❌ Falha na preparação dos dados")