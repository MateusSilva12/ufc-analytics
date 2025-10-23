# advanced_training_pipeline.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_predict
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.preprocessing import StandardScaler
import joblib

def advanced_training_pipeline(df_fights, df_fighters):
    """Pipeline completo de treinamento avançado"""
    
    # 1. Engenharia de Features
    print("🔧 Criando features avançadas...")
    features_df = create_advanced_features(df_fights, df_fighters)
    
    # 2. Limpeza de dados
    features_df = features_df.dropna()
    
    # 3. Criar interações
    features_df = create_feature_interactions(features_df)
    
    # 4. Separar features e target
    X = features_df.drop('winner', axis=1)
    y = features_df['winner']
    
    # 5. Seleção de features
    print("🎯 Selecionando melhores features...")
    X_selected, selected_features = select_best_features(X, y, k=15)
    
    # 6. Normalização
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_selected)
    
    # 7. Split dos dados
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 8. Treinar ensemble
    print("🤖 Treinando ensemble avançado...")
    ensemble, models, cv_score = train_advanced_ensemble(X_train, y_train)
    
    # 9. Avaliação
    y_pred = ensemble.predict(X_test)
    test_accuracy = accuracy_score(y_test, y_pred)
    
    print(f"🎯 Acurácia no Teste: {test_accuracy:.3f}")
    print(f"🎯 Acurácia CV: {cv_score:.3f}")
    
    # 10. Salvar modelo
    model_data = {
        'model': ensemble,
        'scaler': scaler,
        'features': selected_features,
        'accuracy': test_accuracy,
        'cv_accuracy': cv_score,
        'feature_names': list(selected_features)
    }
    
    joblib.dump(model_data, 'models/advanced_ensemble_model.joblib')
    
    # 11. Análise de performance
    analyze_model_performance(ensemble, X_test, y_test, selected_features)
    
    return model_data

def analyze_model_performance(model, X_test, y_test, feature_names):
    """Análise detalhada da performance do modelo"""
    
    from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
    import matplotlib.pyplot as plt
    import seaborn as sns
    
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]
    
    print("\n" + "="*50)
    print("📊 RELATÓRIO DE PERFORMANCE DETALHADO")
    print("="*50)
    
    # Classification Report
    print("\n📈 Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # AUC Score
    auc_score = roc_auc_score(y_test, y_proba)
    print(f"🎯 AUC Score: {auc_score:.3f}")
    
    # Matriz de Confusão
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
    plt.title('Matriz de Confusão')
    plt.ylabel('Verdadeiro')
    plt.xlabel('Predito')
    plt.show()
    
    # Feature Importance (se disponível)
    if hasattr(model, 'feature_importances_'):
        feature_imp = pd.DataFrame({
            'feature': feature_names,
            'importance': model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        plt.figure(figsize=(10, 8))
        sns.barplot(data=feature_imp.head(10), x='importance', y='feature')
        plt.title('Top 10 Features - Importância do Modelo')
        plt.tight_layout()
        plt.show()