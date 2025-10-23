# advanced_model_training.py
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
import joblib

def train_advanced_ensemble(X, y):
    """Treina ensemble avançado de modelos"""
    
    # Definir modelos
    models = {
        'xgb': XGBClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        ),
        'lgbm': LGBMClassifier(
            n_estimators=200,
            max_depth=6,
            learning_rate=0.1,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42
        ),
        'rf': RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            random_state=42
        ),
        'gbm': GradientBoostingClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42
        )
    }
    
    # Ensemble Voting
    ensemble = VotingClassifier(
        estimators=[(name, model) for name, model in models.items()],
        voting='soft',
        weights=[2, 2, 1, 1]  # Pesos baseados na performance
    )
    
    # Cross-validation
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    scores = cross_val_score(ensemble, X, y, cv=cv, scoring='accuracy')
    
    print(f"🎯 Acurácia CV: {scores.mean():.3f} (+/- {scores.std() * 2:.3f})")
    
    # Treinar modelo final
    ensemble.fit(X, y)
    
    return ensemble, models, scores.mean()

def hyperparameter_tuning(X, y):
    """Otimização de hiperparâmetros"""
    from sklearn.model_selection import RandomizedSearchCV
    
    param_dist = {
        'n_estimators': [100, 200, 300],
        'max_depth': [3, 6, 9],
        'learning_rate': [0.01, 0.1, 0.2],
        'subsample': [0.8, 0.9, 1.0],
        'colsample_bytree': [0.8, 0.9, 1.0]
    }
    
    xgb = XGBClassifier(random_state=42)
    random_search = RandomizedSearchCV(
        xgb, param_dist, n_iter=20, cv=3, scoring='accuracy', random_state=42
    )
    
    random_search.fit(X, y)
    
    print("🎯 Melhores parâmetros:", random_search.best_params_)
    print("🎯 Melhor score:", random_search.best_score_)
    
    return random_search.best_estimator_