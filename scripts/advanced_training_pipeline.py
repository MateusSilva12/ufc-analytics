# advanced_training_pipeline.py - VERSÃO COMPLETA CORRIGIDA
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import sys
import os

# Adicionar o diretório atual ao path para importar módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from features_engineering import create_advanced_features, create_feature_interactions
from advanced_model_training import train_advanced_ensemble
from feature_selection import select_best_features, analyze_feature_importance

def advanced_training_pipeline(df_fights, df_fighters):
    """Pipeline completo de treinamento avançado - VERSÃO CORRIGIDA"""
    
    print("=" * 60)
    print("🚀 INICIANDO PIPELINE AVANÇADO DE TREINAMENTO")
    print("=" * 60)
    
    # 1. Engenharia de Features
    print("🔧 1. Criando features avançadas...")
    features_df = create_advanced_features(df_fights, df_fighters)
    print(f"   ✅ Features criadas: {len(features_df)} linhas")
    
    if len(features_df) == 0:
        print("❌ ERRO CRÍTICO: Nenhuma feature foi criada!")
        print("   Verifique se os nomes dos lutadores nas lutas batem com o arquivo de lutadores")
        return None
    
    # 2. Limpeza de dados
    print("🔧 2. Limpando dados...")
    initial_count = len(features_df)
    features_df = features_df.dropna()
    final_count = len(features_df)
    print(f"   ✅ Dados limpos: {final_count} linhas (removidas {initial_count - final_count})")
    
    if len(features_df) == 0:
        print("❌ ERRO: Nenhum dado após limpeza!")
        return None
    
    # 3. Criar interações
    print("🔧 3. Criando interações entre features...")
    features_df = create_feature_interactions(features_df)
    print(f"   ✅ Features com interações: {len(features_df.columns)} colunas")
    
    # 4. Separar features e target
    print("🔧 4. Preparando dados para treinamento...")
    X = features_df.drop('winner', axis=1)
    y = features_df['winner']
    print(f"   ✅ X shape: {X.shape}, y shape: {y.shape}")
    print(f"   ✅ Distribuição do target: {dict(y.value_counts())}")
    
    # 5. Seleção de features
    print("🔧 5. Selecionando melhores features...")
    k_features = min(15, X.shape[1])  # Não selecionar mais features que as disponíveis
    X_selected, selected_features = select_best_features(X, y, k=k_features)
    print(f"   ✅ Features selecionadas: {len(selected_features)}")
    print(f"   ✅ Features: {list(selected_features)}")
    
    # 6. Normalização
    print("🔧 6. Normalizando dados...")
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_selected)
    print(f"   ✅ Dados normalizados: {X_scaled.shape}")
    
    # 7. Split dos dados
    print("🔧 7. Dividindo dados em treino e teste...")
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   ✅ Treino: {X_train.shape}, Teste: {X_test.shape}")
    
    # 8. Treinar ensemble
    print("🔧 8. Treinando ensemble avançado...")
    ensemble, models, cv_score = train_advanced_ensemble(X_train, y_train)
    print(f"   🎯 Acurácia CV: {cv_score:.3f}")
    
    # 9. Avaliação no teste
    print("🔧 9. Avaliando no conjunto de teste...")
    y_pred = ensemble.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    print(f"   🎯 Acurácia no Teste: {test_accuracy:.3f}")
    
    # 10. Salvar modelo
    print("🔧 10. Salvando modelo...")
    model_data = {
        'model': ensemble,
        'scaler': scaler,
        'features': selected_features,
        'accuracy': test_accuracy,
        'cv_accuracy': cv_score,
        'feature_names': list(selected_features),
        'feature_importance': analyze_feature_importance(X, y) if len(X) > 0 else None
    }
    
    # Garantir que a pasta models existe
    os.makedirs('models', exist_ok=True)
    
    joblib.dump(model_data, 'models/advanced_ensemble_model.joblib')
    print("   💾 Modelo salvo: models/advanced_ensemble_model.joblib")
    
    # 11. Análise de performance
    print("🔧 11. Gerando relatório de performance...")
    analyze_model_performance(ensemble, X_test, y_test, selected_features, test_accuracy)
    
    print("=" * 60)
    print("✅ PIPELINE CONCLUÍDO COM SUCESSO!")
    print("=" * 60)
    
    return model_data

def analyze_model_performance(model, X_test, y_test, feature_names, accuracy):
    """Análise detalhada da performance do modelo"""
    
    from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    print(f"🎯 ACURÁCIA FINAL: {accuracy:.3f}")
    
    # Classification Report
    print("\n📈 RELATÓRIO DE CLASSIFICAÇÃO:")
    print(classification_report(y_test, y_pred))
    
    # AUC Score (se disponível)
    if y_proba is not None:
        auc_score = roc_auc_score(y_test, y_proba)
        print(f"📊 AUC Score: {auc_score:.3f}")
    
    # Matriz de Confusão
    cm = confusion_matrix(y_test, y_pred)
    print("\n🎯 MATRIZ DE CONFUSÃO:")
    print(cm)
    
    # Feature Importance (se disponível)
    if hasattr(model, 'feature_importances_'):
        print("\n🔍 TOP 10 FEATURES MAIS IMPORTANTES:")
        feature_imp = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print(feature_imp.head(10).to_string(index=False))

def simple_training_fallback():
    """Fallback simplificado se o pipeline avançado falhar"""
    print("🔄 Iniciando treinamento simplificado...")
    
    try:
        # CORREÇÃO DOS CAMINHOS
        df_fights = pd.read_csv('data/ufc_fights_real_data.csv')
        df_fighters = pd.read_csv('data/ufc_fighters.csv')
        
        print(f"   📊 Dados carregados: {len(df_fights)} lutas, {len(df_fighters)} lutadores")
        
        # Features simples que sempre funcionam
        features_list = []
        success_count = 0
        
        for idx, fight in df_fights.iterrows():
            try:
                f1_data = df_fighters[df_fighters['Name'] == fight['fighter_1']].iloc[0]
                f2_data = df_fighters[df_fighters['Name'] == fight['fighter_2']].iloc[0]
                
                # Determinar winner de forma robusta
                if fight['winner'] == 'fighter_1':
                    winner = 0
                elif fight['winner'] == 'fighter_2':
                    winner = 1
                else:
                    continue
                    
                features = {
                    'f1_win_rate': f1_data['Win_Rate'],
                    'f2_win_rate': f2_data['Win_Rate'],
                    'f1_total_fights': f1_data['Total_Fights'],
                    'f2_total_fights': f2_data['Total_Fights'],
                    'win_rate_diff': f1_data['Win_Rate'] - f2_data['Win_Rate'],
                    'experience_diff': f1_data['Total_Fights'] - f2_data['Total_Fights'],
                    'winner': winner
                }
                features_list.append(features)
                success_count += 1
                
            except Exception as e:
                continue
        
        features_df = pd.DataFrame(features_list)
        print(f"   ✅ Features criadas: {success_count}/{len(df_fights)} lutas processadas")
        
        if len(features_df) > 0:
            from sklearn.ensemble import RandomForestClassifier
            
            X = features_df.drop('winner', axis=1)
            y = features_df['winner']
            
            print(f"   📊 Dados finais: X={X.shape}, y={y.shape}")
            print(f"   📈 Distribuição: {dict(y.value_counts())}")
            
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
            
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            accuracy = model.score(X_test, y_test)
            print(f"🎯 Acurácia (Simplificado): {accuracy:.3f}")
            
            # Salvar modelo
            model_data = {
                'model': model,
                'features': list(X.columns),
                'accuracy': accuracy
            }
            
            os.makedirs('models', exist_ok=True)
            joblib.dump(model_data, 'models/simple_model.joblib')
            print("💾 Modelo simples salvo: models/simple_model.joblib")
            
            return model_data
        else:
            print("❌ Nenhuma feature pôde ser criada no modo simples")
            return None
    
    except Exception as e:
        print(f"❌ Erro no treinamento simplificado: {e}")
        import traceback
        traceback.print_exc()
    
    return None

if __name__ == "__main__":
    try:
        # CORREÇÃO DOS CAMINHOS - USANDO CAMINHOS RELATIVOS CORRETOS
        print("📊 Carregando dados...")
        df_fights = pd.read_csv('data/ufc_fights_real_data.csv')
        df_fighters = pd.read_csv('data/ufc_fighters.csv')
        
        print(f"   ✅ Dados carregados: {len(df_fights)} lutas, {len(df_fighters)} lutadores")
        
        # Verificar primeiras lutas para debug
        print("\n🔍 Primeiras 3 lutas para verificação:")
        for i in range(min(3, len(df_fights))):
            fight = df_fights.iloc[i]
            print(f"   Luta {i+1}: {fight['fighter_1']} vs {fight['fighter_2']} -> Winner: {fight['winner']}")
        
        # Executar pipeline avançado
        model_data = advanced_training_pipeline(df_fights, df_fighters)
        
        if model_data is None:
            print("🔄 Pipeline avançado falhou, tentando versão simplificada...")
            model_data = simple_training_fallback()
            
    except Exception as e:
        print(f"❌ ERRO NO PIPELINE PRINCIPAL: {e}")
        import traceback
        traceback.print_exc()
        print("🔄 Tentando treinamento simplificado...")
        model_data = simple_training_fallback()