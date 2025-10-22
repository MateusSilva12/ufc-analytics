# fix_dados_reais.py
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import re

def processar_dados_reais():
    print("🎯 PROCESSANDO DADOS REAIS CORRETAMENTE...")
    
    df = pd.read_csv("data/ufc_fights_real_data.csv")
    print(f"📊 Dados carregados: {df.shape}")
    
    # 1. IDENTIFICAR E PROCESSAR COLUNAS COM ESTATÍSTICAS
    print("\n🔍 Processando colunas de estatísticas...")
    
    # Colunas base
    df_clean = df[['fighter_1', 'fighter_2', 'winner', 'method']].copy()
    
    # Procurar colunas que contêm padrões de estatísticas
    stat_cols = []
    for col in df.columns:
        if any(x in str(col) for x in [' of ', '%', '00_', '_2']):
            stat_cols.append(col)
    
    print(f"📈 Colunas de estatísticas identificadas: {len(stat_cols)}")
    
    # 2. EXTRAIR NÚMEROS DAS ESTATÍSTICAS
    feature_cols = []
    
    for col in stat_cols:
        # Cada coluna parece conter dados para AMBOS os lutadores
        # Exemplo: "3 of 42 of 2" -> Lutador1: 3 of 4, Lutador2: 2 of 2
        # Exemplo: "75%100%" -> Lutador1: 75%, Lutador2: 100%
        
        values = df[col].dropna()
        if len(values) == 0:
            continue
            
        # Analisar o padrão dos dados
        sample = str(values.iloc[0])
        
        # Padrão 1: "X of YZ of W" (dois conjuntos de números)
        match1 = re.search(r'(\d+)\s*of\s*(\d+)\s*(\d+)\s*of\s*(\d+)', sample)
        if match1:
            # Criar features para cada lutador
            df_clean[f'{col}_f1_made'] = df[col].str.extract(r'^(\d+)\s*of', expand=False)
            df_clean[f'{col}_f1_attempt'] = df[col].str.extract(r'^(\d+)\s*of\s*(\d+)', expand=False)[1]
            df_clean[f'{col}_f2_made'] = df[col].str.extract(r'(\d+)\s*of\s*(\d+)$', expand=False)[0]
            df_clean[f'{col}_f2_attempt'] = df[col].str.extract(r'(\d+)\s*of\s*(\d+)$', expand=False)[1]
            
            feature_cols.extend([f'{col}_f1_made', f'{col}_f1_attempt', f'{col}_f2_made', f'{col}_f2_attempt'])
            print(f"   ✅ {col} -> 4 features (made/attempt para cada lutador)")
            continue
        
        # Padrão 2: "XX%YY%" (duas porcentagens)
        match2 = re.search(r'(\d+)%(\d+)%', sample)
        if match2:
            df_clean[f'{col}_f1_pct'] = df[col].str.extract(r'^(\d+)%', expand=False)
            df_clean[f'{col}_f2_pct'] = df[col].str.extract(r'(\d+)%$', expand=False)
            feature_cols.extend([f'{col}_f1_pct', f'{col}_f2_pct'])
            print(f"   ✅ {col} -> 2 features (porcentagem para cada lutador)")
            continue
        
        # Padrão 3: Números simples
        if any(char.isdigit() for char in sample):
            # Tentar extrair todos os números
            numbers = re.findall(r'\d+', sample)
            if len(numbers) >= 2:
                for i, num in enumerate(numbers[:2]):  # Pegar até 2 números
                    df_clean[f'{col}_num_{i}'] = df[col].str.extract(f'^(?:.*?)(\\d+)', expand=False)
                    feature_cols.append(f'{col}_num_{i}')
                print(f"   ✅ {col} -> {len(numbers[:2])} features numéricas")
    
    print(f"📊 Total de features criadas: {len(feature_cols)}")
    
    # 3. CONVERTER PARA NUMÉRICO E CRIAR FEATURES DE DIFERENÇA
    print("\n🔢 Convertendo para numérico...")
    
    numeric_features = []
    for col in feature_cols:
        df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        if df_clean[col].notna().sum() > 50:  # Pelo menos 50 valores válidos
            numeric_features.append(col)
    
    # Criar features de diferença entre lutadores
    diff_features = []
    for i in range(0, len(numeric_features)-1, 2):
        if i+1 < len(numeric_features):
            col1, col2 = numeric_features[i], numeric_features[i+1]
            if 'f1' in col1 and 'f2' in col2:
                diff_col = col1.replace('f1', 'diff')
                df_clean[diff_col] = df_clean[col1] - df_clean[col2]
                diff_features.append(diff_col)
                print(f"   📈 {diff_col} = {col1} - {col2}")
    
    # 4. CRIAR TARGET E DATASET FINAL
    le = LabelEncoder()
    df_clean['winner_encoded'] = le.fit_transform(df_clean['winner'])
    
    # Features finais (diferenças + algumas features individuais)
    final_features = diff_features + numeric_features[:10]  # Limitar para não ficar muito grande
    
    if final_features:
        # Preencher NaN
        X = df_clean[final_features].fillna(0)
        y = df_clean['winner_encoded']
        
        df_final = pd.concat([X, y], axis=1)
        df_final = df_final.dropna()
        
        print(f"\n✅ DATASET FINAL CRIADO!")
        print(f"📦 Shape: {df_final.shape}")
        print(f"🎯 Distribuição: {df_final['winner_encoded'].value_counts().to_dict()}")
        print(f"🔢 Features finais: {len(final_features)}")
        
        # Salvar
        df_final.to_csv("data/ufc_model_ready_real.csv", index=False)
        print("💾 Salvo: data/ufc_model_ready_real.csv")
        
        return df_final
    else:
        print("❌ Não foi possível criar features suficientes")
        return pd.DataFrame()

if __name__ == "__main__":
    df_final = processar_dados_reais()
    if not df_final.empty:
        print(f"\n🎉 SUCESSO! Dataset real pronto para ML!")
        print(f"📊 Amostra das features:")
        print(df_final.head(3))
    else:
        print(f"\n❌ Falha no processamento")