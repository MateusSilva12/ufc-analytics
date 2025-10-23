# features_engineering.py - VERSÃO COMPLETA E CORRIGIDA
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

def create_advanced_features(df_fights, df_fighters):
    """Cria features avançadas - VERSÃO COMPLETA"""
    
    features_list = []
    success_count = 0
    error_count = 0
    
    print(f"🔧 Processando {len(df_fights)} lutas...")
    
    # Calcular Win Rate se não existir
    if 'Win_Rate' not in df_fighters.columns:
        df_fighters['Total_Fights'] = df_fighters['Wins'] + df_fighters['Losses'] + df_fighters.get('Draws', 0)
        df_fighters['Win_Rate'] = (df_fighters['Wins'] / df_fighters['Total_Fights'] * 100).round(1)
        df_fighters['Win_Rate'] = df_fighters['Win_Rate'].fillna(0)
    
    for idx, fight in df_fights.iterrows():
        try:
            # Buscar dados dos lutadores
            f1_match = df_fighters[df_fighters['Name'] == fight['fighter_1']]
            f2_match = df_fighters[df_fighters['Name'] == fight['fighter_2']]
            
            if len(f1_match) == 0 or len(f2_match) == 0:
                error_count += 1
                continue
                
            f1_data = f1_match.iloc[0]
            f2_data = f2_match.iloc[0]
            
            # Lógica robusta para determinar winner
            if fight['winner'] == 'fighter_1':
                winner = 0
            elif fight['winner'] == 'fighter_2':
                winner = 1
            else:
                error_count += 1
                continue

            # Calcular Total_Fights se não existir
            f1_total_fights = f1_data.get('Total_Fights', f1_data['Wins'] + f1_data['Losses'] + f1_data.get('Draws', 0))
            f2_total_fights = f2_data.get('Total_Fights', f2_data['Wins'] + f2_data['Losses'] + f2_data.get('Draws', 0))
            
            # Calcular Win_Rate se não existir
            f1_win_rate = f1_data.get('Win_Rate', (f1_data['Wins'] / max(f1_total_fights, 1) * 100).round(1))
            f2_win_rate = f2_data.get('Win_Rate', (f2_data['Wins'] / max(f2_total_fights, 1) * 100).round(1))

            # Criar features COMPLETAS
            features = {
                # Win Rate e Experiência
                'f1_win_rate': f1_win_rate,
                'f2_win_rate': f2_win_rate,
                'f1_total_fights': f1_total_fights,
                'f2_total_fights': f2_total_fights,
                'f1_experience_ratio': f1_total_fights / max(f2_total_fights, 1),
                
                # Features Comparativas
                'win_rate_diff': f1_win_rate - f2_win_rate,
                'experience_diff': f1_total_fights - f2_total_fights,
                'win_rate_ratio': f1_win_rate / max(f2_win_rate, 1),
                
                # Features de Performance
                'f1_win_streak': f1_data.get('Win_Streak', 0),
                'f2_win_streak': f2_data.get('Win_Streak', 0),
                'win_streak_diff': f1_data.get('Win_Streak', 0) - f2_data.get('Win_Streak', 0),
                
                # Features de Estatísticas (se disponíveis)
                'f1_avg_fight_time': f1_data.get('Avg_Fight_Time_Seconds', 0),
                'f2_avg_fight_time': f2_data.get('Avg_Fight_Time_Seconds', 0),
                'fight_time_diff': f1_data.get('Avg_Fight_Time_Seconds', 0) - f2_data.get('Avg_Fight_Time_Seconds', 0),
                
                # Target
                'winner': winner
            }
            
            # Adicionar features de striking se disponíveis
            if 'SLpM' in f1_data and 'SLpM' in f2_data:
                features.update({
                    'f1_strikes_landed_per_min': f1_data['SLpM'],
                    'f2_strikes_landed_per_min': f2_data['SLpM'],
                    'striking_diff': f1_data['SLpM'] - f2_data['SLpM']
                })
            
            # Adicionar features de grappling se disponíveis
            if 'TD_Avg' in f1_data and 'TD_Avg' in f2_data:
                features.update({
                    'f1_takedown_avg': f1_data['TD_Avg'],
                    'f2_takedown_avg': f2_data['TD_Avg'],
                    'takedown_diff': f1_data['TD_Avg'] - f2_data['TD_Avg']
                })
            
            features_list.append(features)
            success_count += 1
            
        except Exception as e:
            error_count += 1
            continue
    
    print(f"✅ Features criadas: {success_count} sucessos, {error_count} erros")
    
    if success_count > 0:
        print(f"📊 Exemplo de features: {list(features_list[0].keys())}")
    
    return pd.DataFrame(features_list)

def create_feature_interactions(df):
    """
    Cria features de interação entre variáveis importantes - VERSÃO COMPLETA
    """
    df = df.copy()
    
    print("🔧 Criando interações entre features...")
    
    # Interações entre Win Rate e Experiência
    if 'f1_win_rate' in df.columns and 'f1_total_fights' in df.columns:
        df['f1_win_experience'] = df['f1_win_rate'] * np.log1p(df['f1_total_fights'])
        df['f1_win_consistency'] = df['f1_win_rate'] / np.log1p(df['f1_total_fights'] + 1)
    
    if 'f2_win_rate' in df.columns and 'f2_total_fights' in df.columns:
        df['f2_win_experience'] = df['f2_win_rate'] * np.log1p(df['f2_total_fights'])
        df['f2_win_consistency'] = df['f2_win_rate'] / np.log1p(df['f2_total_fights'] + 1)
    
    # Interações entre diferenças
    if 'win_rate_diff' in df.columns and 'experience_diff' in df.columns:
        df['win_exp_interaction'] = df['win_rate_diff'] * df['experience_diff']
        df['win_exp_combined'] = df['win_rate_diff'] + (df['experience_diff'] * 0.1)
        df['dominance_score'] = (df['win_rate_diff'] * 0.7) + (df['experience_diff'] * 0.3)
    
    # Features quadráticas e polinomiais
    if 'f1_win_rate' in df.columns:
        df['f1_win_rate_sq'] = df['f1_win_rate'] ** 2
        df['f1_win_rate_sqrt'] = np.sqrt(np.abs(df['f1_win_rate']))
    
    if 'f2_win_rate' in df.columns:
        df['f2_win_rate_sq'] = df['f2_win_rate'] ** 2
        df['f2_win_rate_sqrt'] = np.sqrt(np.abs(df['f2_win_rate']))
    
    # Razões importantes
    if 'f1_total_fights' in df.columns and 'f2_total_fights' in df.columns:
        df['experience_ratio'] = df['f1_total_fights'] / (df['f2_total_fights'] + 1)
        df['log_experience_ratio'] = np.log1p(df['experience_ratio'])
    
    # Features de dominância e vantagem
    if 'win_rate_diff' in df.columns:
        df['win_rate_advantage'] = np.where(df['win_rate_diff'] > 10, 1, 0)
        df['significant_advantage'] = np.where(df['win_rate_diff'] > 20, 1, 0)
        df['win_rate_bucket'] = pd.cut(df['win_rate_diff'], bins=[-100, -20, -10, 0, 10, 20, 100], labels=False)
    
    # Interações com streaks
    if 'win_streak_diff' in df.columns and 'win_rate_diff' in df.columns:
        df['momentum_score'] = df['win_streak_diff'] + (df['win_rate_diff'] * 0.1)
        df['hot_streak'] = np.where((df['f1_win_streak'] > 3) & (df['f2_win_streak'] < 2), 1, 0)
    
    # Features de estilo de luta (se disponíveis)
    if 'striking_diff' in df.columns and 'takedown_diff' in df.columns:
        df['striker_vs_grappler'] = np.where(
            (df['striking_diff'] > 1) & (df['takedown_diff'] < -1), 1, 0
        )
        df['balanced_fighter'] = np.where(
            (np.abs(df['striking_diff']) < 0.5) & (np.abs(df['takedown_diff']) < 0.5), 1, 0
        )
    
    # Features de tempo (se disponíveis)
    if 'fight_time_diff' in df.columns:
        df['endurance_advantage'] = np.where(df['fight_time_diff'] > 60, 1, 0)
    
    # Features de combinação
    if all(col in df.columns for col in ['f1_win_rate', 'f1_total_fights', 'f1_win_streak']):
        df['f1_overall_score'] = (
            df['f1_win_rate'] * 0.5 + 
            np.log1p(df['f1_total_fights']) * 0.3 + 
            df['f1_win_streak'] * 0.2
        )
    
    if all(col in df.columns for col in ['f2_win_rate', 'f2_total_fights', 'f2_win_streak']):
        df['f2_overall_score'] = (
            df['f2_win_rate'] * 0.5 + 
            np.log1p(df['f2_total_fights']) * 0.3 + 
            df['f2_win_streak'] * 0.2
        )
    
    # Score final comparativo
    if 'f1_overall_score' in df.columns and 'f2_overall_score' in df.columns:
        df['overall_score_diff'] = df['f1_overall_score'] - df['f2_overall_score']
    
    print(f"✅ Interações criadas: {len(df.columns)} features totais")
    print(f"📊 Colunas disponíveis: {list(df.columns)}")
    
    return df

def create_rolling_features(df, window=5):
    """
    Cria features rolling para séries temporais
    """
    df = df.copy()
    
    # Ordenar por data se existir coluna de data
    if 'date' in df.columns:
        df = df.sort_values('date')
    
    # Features rolling para win rate
    for col in ['f1_win_rate', 'f2_win_rate', 'win_rate_diff']:
        if col in df.columns:
            df[f'{col}_rolling_mean'] = df[col].rolling(window=window, min_periods=1).mean()
            df[f'{col}_rolling_std'] = df[col].rolling(window=window, min_periods=1).std()
            df[f'{col}_rolling_trend'] = df[col].diff().rolling(window=3, min_periods=1).mean()
    
    return df

def create_statistical_features(df):
    """
    Cria features estatísticas avançadas
    """
    df = df.copy()
    
    # Features de volatilidade
    if 'f1_win_rate' in df.columns:
        df['f1_win_rate_volatility'] = df['f1_win_rate'].rolling(window=5, min_periods=1).std()
    
    if 'f2_win_rate' in df.columns:
        df['f2_win_rate_volatility'] = df['f2_win_rate'].rolling(window=5, min_periods=1).std()
    
    # Z-scores para normalização
    for col in ['win_rate_diff', 'experience_diff']:
        if col in df.columns:
            mean_val = df[col].mean()
            std_val = df[col].std()
            if std_val > 0:
                df[f'{col}_zscore'] = (df[col] - mean_val) / std_val
    
    return df

def engineer_all_features(df_fights, df_fighters, include_interactions=True, include_rolling=True):
    """
    Função principal que cria todas as features
    """
    print("🚀 INICIANDO ENGENHARIA COMPLETA DE FEATURES")
    print("=" * 50)
    
    # 1. Features básicas
    df_features = create_advanced_features(df_fights, df_fighters)
    
    if len(df_features) == 0:
        print("❌ Nenhuma feature foi criada!")
        return pd.DataFrame()
    
    # 2. Interações
    if include_interactions:
        df_features = create_feature_interactions(df_features)
    
    # 3. Features rolling (se houver dados temporais)
    if include_rolling and 'date' in df_fights.columns:
        df_features = create_rolling_features(df_features)
    
    # 4. Features estatísticas
    df_features = create_statistical_features(df_features)
    
    # Remover colunas com muitos valores missing
    threshold = len(df_features) * 0.7  # Manter colunas com pelo menos 70% de dados
    df_features = df_features.dropna(axis=1, thresh=threshold)
    
    # Preencher valores missing restantes
    for col in df_features.columns:
        if df_features[col].isna().any():
            if df_features[col].dtype in ['float64', 'int64']:
                df_features[col] = df_features[col].fillna(df_features[col].median())
            else:
                df_features[col] = df_features[col].fillna(df_features[col].mode()[0] if len(df_features[col].mode()) > 0 else 0)
    
    print(f"✅ ENGENHARIA CONCLUÍDA: {len(df_features)} linhas, {len(df_features.columns)} features")
    print(f"📊 Colunas finais: {list(df_features.columns)}")
    print("=" * 50)
    
    return df_features

def get_feature_categories():
    """
    Retorna categorias de features para análise
    """
    return {
        'win_rate_features': [
            'f1_win_rate', 'f2_win_rate', 'win_rate_diff', 'win_rate_ratio',
            'f1_win_rate_sq', 'f2_win_rate_sq', 'win_rate_advantage'
        ],
        'experience_features': [
            'f1_total_fights', 'f2_total_fights', 'experience_diff', 
            'experience_ratio', 'f1_experience_ratio'
        ],
        'interaction_features': [
            'win_exp_interaction', 'win_exp_combined', 'dominance_score',
            'f1_win_experience', 'f2_win_experience'
        ],
        'streak_features': [
            'f1_win_streak', 'f2_win_streak', 'win_streak_diff', 'momentum_score'
        ],
        'statistical_features': [
            'f1_win_rate_volatility', 'f2_win_rate_volatility',
            'win_rate_diff_zscore', 'experience_diff_zscore'
        ]
    }

if __name__ == "__main__":
    # Teste da função
    try:
        df_fights = pd.read_csv('../data/ufc_fights_real_data.csv')
        df_fighters = pd.read_csv('../data/ufc_fighters.csv')
        
        print("🧪 Testando criação completa de features...")
        features = engineer_all_features(df_fights.head(20), df_fighters)
        
        if len(features) > 0:
            print(f"✅ Teste bem-sucedido: {len(features)} linhas, {len(features.columns)} colunas")
            print(f"📊 Primeiras features:\n{features.head(3)}")
        else:
            print("❌ Teste falhou - nenhuma feature criada")
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()