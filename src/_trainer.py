"""
Model Training Module
"""

import logging
import numpy as np
import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import GridSearchCV, cross_val_score
import joblib
from typing import Dict, Any, Tuple, Optional

logger = logging.getLogger(__name__)

class ModelTrainer:
    """Train and evaluate spam detection models"""
    
    def __init__(self, model_type: str = 'logistic_regression', random_state: int = 42):
        """
        Initialize ModelTrainer
        
        Args:
            model_type: Type of model to use
            random_state: Random seed for reproducibility
        """
        self.model_type = model_type
        self.random_state = random_state
        self.model = None
        self.best_params = None
        
        # Available models
        self.models = {
            'naive_bayes': MultinomialNB(),
            'logistic_regression': LogisticRegression(max_iter=1000, random_state=random_state),
            'svm': SVC(kernel='linear', random_state=random_state, probability=True),
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=random_state),
            'gradient_boosting': GradientBoostingClassifier(n_estimators=100, random_state=random_state)
        }
        
        # Hyperparameter grids for tuning
        self.param_grids = {
            'logistic_regression': {
                'C': [0.1, 1.0, 10.0],
                'solver': ['liblinear', 'saga'],
                'penalty': ['l1', 'l2']
            },
            'svm': {
                'C': [0.1, 1.0, 10.0],
                'gamma': ['scale', 'auto'],
                'kernel': ['linear', 'rbf']
            },
            'random_forest': {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 10, 20],
                'min_samples_split': [2, 5, 10]
            },
            'naive_bayes': {
                'alpha': [0.1, 0.5, 1.0, 2.0]
            },
            'gradient_boosting': {
                'n_estimators': [50, 100, 200],
                'learning_rate': [0.01, 0.1, 0.3],
                'max_depth': [3, 5, 7]
            }
        }
    
    def get_model(self) -> Any:
        """Get the selected model"""
        if self.model_type not in self.models:
            raise ValueError(f"Model type '{self.model_type}' not found. Available: {list(self.models.keys())}")
        return self.models[self.model_type]
    
    def train(self, X_train, y_train) -> Any:
        """
        Train the model
        
        Args:
            X_train: Training features
            y_train: Training labels
            
        Returns:
            Trained model
        """
        self.model = self.get_model()
        logger.info(f"Training {self.model_type} model...")
        self.model.fit(X_train, y_train)
        logger.info("Training complete!")
        return self.model
    
    def tune_hyperparameters(self, X_train, y_train, cv: int = 5) -> Dict:
        """
        Tune hyperparameters using GridSearchCV
        
        Args:
            X_train: Training features
            y_train: Training labels
            cv: Number of cross-validation folds
            
        Returns:
            Best parameters
        """
        if self.model_type not in self.param_grids:
            logger.warning(f"No parameter grid defined for {self.model_type}")
            return {}
        
        param_grid = self.param_grids[self.model_type]
        logger.info(f"Tuning hyperparameters for {self.model_type}...")
        
        grid_search = GridSearchCV(
            self.get_model(),
            param_grid,
            cv=cv,
            scoring='f1',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        self.best_params = grid_search.best_params_
        self.model = grid_search.best_estimator_
        
        logger.info(f"Best parameters: {self.best_params}")
        logger.info(f"Best cross-validation F1 score: {grid_search.best_score_:.4f}")
        
        return self.best_params
    
    def evaluate(self, X_test, y_test) -> Dict[str, float]:
        """
        Evaluate the model on test data
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary of evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model not trained. Call train() first.")
        
        y_pred = self.model.predict(X_test)
        
        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, average='binary'),
            'recall': recall_score(y_test, y_pred, average='binary'),
            'f1_score': f1_score(y_test, y_pred, average='binary')
        }
        
        logger.info(f"Evaluation metrics: {metrics}")
        return metrics
    
    def cross_validate(self, X, y, cv: int = 5) -> Dict[str, float]:
        """
        Perform cross-validation
        
        Args:
            X: Features
            y: Labels
            cv: Number of folds
            
        Returns:
            Dictionary of cross-validation scores
        """
        model = self.get_model()
        
        scores = {
            'accuracy': cross_val_score(model, X, y, cv=cv, scoring='accuracy'),
            'precision': cross_val_score(model, X, y, cv=cv, scoring='precision'),
            'recall': cross_val_score(model, X, y, cv=cv, scoring='recall'),
            'f1': cross_val_score(model, X, y, cv=cv, scoring='f1')
        }
        
        results = {
            'accuracy_mean': scores['accuracy'].mean(),
            'accuracy_std': scores['accuracy'].std(),
            'precision_mean': scores['precision'].mean(),
            'precision_std': scores['precision'].std(),
            'recall_mean': scores['recall'].mean(),
            'recall_std': scores['recall'].std(),
            'f1_mean': scores['f1'].mean(),
            'f1_std': scores['f1'].std()
        }
        
        logger.info(f"Cross-validation results: {results}")
        return results
    
    def save_model(self, filepath: str):
        """Save trained model to disk"""
        if self.model is None:
            raise ValueError("No model to save. Train first.")
        joblib.dump(self.model, filepath)
        logger.info(f"Model saved to {filepath}")
    
    def load_model(self, filepath: str):
        """Load trained model from disk"""
        self.model = joblib.load(filepath)
        logger.info(f"Model loaded from {filepath}")
    
    def get_feature_importance(self, feature_names: Optional[list] = None) -> pd.DataFrame:
        """
        Get feature importance (for tree-based models)
        
        Args:
            feature_names: List of feature names
            
        Returns:
            DataFrame with feature importance
        """
        import pandas as pd
        
        if hasattr(self.model, 'feature_importances_'):
            importance = self.model.feature_importances_
        elif hasattr(self.model, 'coef_'):
            importance = np.abs(self.model.coef_).flatten()
        else:
            raise ValueError("Model doesn't support feature importance")
        
        if feature_names is None:
            feature_names = [f'feature_{i}' for i in range(len(importance))]
        
        df_importance = pd.DataFrame({
            'feature': feature_names,
            'importance': importance
        }).sort_values('importance', ascending=False)
        
        return df_importance