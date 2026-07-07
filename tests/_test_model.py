"""
Tests for ModelTrainer
"""

import pytest
import numpy as np
from sklearn.datasets import make_classification
from src._trainer import ModelTrainer

class TestModelTrainer:
    """Test cases for ModelTrainer"""
    
    @pytest.fixture
    def sample_data(self):
        """Create sample data for testing"""
        X, y = make_classification(
            n_samples=100,
            n_features=20,
            n_informative=10,
            n_redundant=5,
            random_state=42
        )
        return X, y
    
    @pytest.fixture
    def trainer(self):
        return ModelTrainer(model_type='logistic_regression')
    
    def test_model_initialization(self, trainer):
        """Test model initialization"""
        assert trainer.model_type == 'logistic_regression'
        assert trainer.random_state == 42
        assert trainer.model is None
    
    def test_get_model(self, trainer):
        """Test getting model"""
        model = trainer.get_model()
        assert model is not None
        assert hasattr(model, 'fit')
        assert hasattr(model, 'predict')
    
    def test_train_model(self, trainer, sample_data):
        """Test model training"""
        X, y = sample_data
        trainer.train(X, y)
        assert trainer.model is not None
        assert hasattr(trainer.model, 'predict')
    
    def test_evaluate_model(self, trainer, sample_data):
        """Test model evaluation"""
        X, y = sample_data
        X_train, X_test = X[:80], X[80:]
        y_train, y_test = y[:80], y[80:]
        
        trainer.train(X_train, y_train)
        metrics = trainer.evaluate(X_test, y_test)
        
        assert 'accuracy' in metrics
        assert 'precision' in metrics
        assert 'recall' in metrics
        assert 'f1_score' in metrics
        assert isinstance(metrics['accuracy'], float)
    
    def test_cross_validation(self, trainer, sample_data):
        """Test cross-validation"""
        X, y = sample_data
        results = trainer.cross_validate(X, y, cv=3)
        
        assert 'accuracy_mean' in results
        assert 'precision_mean' in results
        assert 'recall_mean' in results
        assert 'f1_mean' in results
    
    def test_hyperparameter_tuning(self, trainer, sample_data):
        """Test hyperparameter tuning"""
        X, y = sample_data
        params = trainer.tune_hyperparameters(X[:80], y[:80], cv=2)
        
        assert params is not None
        assert 'C' in params
    
    def test_save_load_model(self, trainer, sample_data, tmp_path):
        """Test saving and loading model"""
        X, y = sample_data
        trainer.train(X[:80], y[:80])
        
        model_path = tmp_path / "test_model.pkl"
        trainer.save_model(str(model_path))
        
        # Create new trainer and load model
        new_trainer = ModelTrainer()
        new_trainer.load_model(str(model_path))
        
        assert new_trainer.model is not None
        assert new_trainer.model.predict(X[80:]).shape[0] == X[80:].shape[0]