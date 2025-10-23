# feature_selection.py
import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_feature_importance(X, y):
    """Analisa importância das features"""
    
    # Random Forest Feature Importance
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    # Criar DataFrame com importâncias
    feature_importance = pd.DataFrame({
        'feature': X.columns,
        'importance': rf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    # Plot
    plt.figure(figsize=(10, 8))
    sns.barplot(data=feature_importance.head(15), x='importance', y='feature')
    plt.title('Top 15 Features Mais Importantes')
    plt.tight_layout()
    plt.show()
    
    return feature_importance

def select_best_features(X, y, k=15):
    """Seleciona as melhores features"""
    
    # ANOVA F-value
    selector = SelectKBest(score_func=f_classif, k=k)
    X_selected = selector.fit_transform(X, y)
    
    selected_features = X.columns[selector.get_support()]
    print(f"🎯 Features selecionadas: {list(selected_features)}")
    
    return X_selected, selected_features

def create_feature_interactions(X):
    """Cria interações entre features importantes"""
    
    # Adicionar interações
    X['win_rate_experience_interaction'] = X['win_rate_diff'] * X['experience_diff']
    X['streak_win_rate_interaction'] = X['streak_diff'] * X['win_rate_diff']
    X['momentum_ratio'] = (X['f1_form_momentum'] + 1) / (X['f2_form_momentum'] + 1)
    
    # Polynomial features para features mais importantes
    X['win_rate_diff_squared'] = X['win_rate_diff'] ** 2
    X['experience_ratio_squared'] = X['f1_experience_ratio'] ** 2
    
    return X