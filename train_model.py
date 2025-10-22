# train_model_real.py - VERSÃO CORRIGIDA
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os

def train_real_model(model_csv="data/ufc_model_ready_real.csv", out_model="models/xgb_ufc_real.joblib"):
    print("🎯 TREINANDO MODELO COM DADOS REAIS...")
    
    try:
        df = pd.read_csv(model_csv)
        print(f"📊 Dataset carregado: {df.shape}")
        print(f"📋 Colunas: {df.columns.tolist()}")
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")
        return None, None
    
    # Verificar target
    if 'winner_encoded' not in df.columns:
        print("❌ Coluna 'winner_encoded' não encontrada")
        return None, None
    
    # Separar features e target
    X = df.drop(columns=['winner_encoded'])
    y = df['winner_encoded']
    
    print(f"🎯 Distribuição do target: {y.value_counts().to_dict()}")
    print(f"🔢 Número de features: {X.shape[1]}")
    
    # Preencher valores NaN
    X = X.fillna(0)
    
    # Split dos dados
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"📚 Treino: {X_train.shape}, Teste: {X_test.shape}")
    
    # Treinar modelo
    print("🤖 Treinando XGBoost...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=4,
        learning_rate=0.1,
        random_state=42,
        eval_metric='logloss'
    )
    
    model.fit(X_train, y_train)
    
    # Avaliar
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"🎯 Acurácia no teste: {accuracy:.3f}")
    print("\n📊 Relatório de classificação:")
    print(classification_report(y_test, y_pred))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\n📈 Top 10 Features Mais Importantes:")
    print(feature_importance.head(10))
    
    # Salvar modelo
    os.makedirs("models", exist_ok=True)
    
    model_data = {
        "model": model,
        "features": X.columns.tolist(),
        "accuracy": accuracy,
        "feature_importance": feature_importance.to_dict()
    }
    
    joblib.dump(model_data, out_model)
    print(f"💾 Modelo salvo: {out_model}")
    
    return model, model_data  # CORREÇÃO: Retornar model_data também

if __name__ == "__main__":
    model, model_data = train_real_model()  # CORREÇÃO: Receber model_data
    if model is not None:
        print(f"\n🎉 MODELO REAL TREINADO COM SUCESSO!")
        print(f"📊 Acurácia com dados reais: {model_data['accuracy']:.3f}")  # CORREÇÃO: Usar model_data
        print("🚀 Agora você tem um modelo treinado com dados REAIS!")
    else:
        print("\n❌ Falha no treinamento")