"""
Tests for SpamPredictor
"""

import pytest
import numpy as np
from src._predictor import SpamPredictor
from src._trainer import ModelTrainer
from src._feature_extractor import FeatureExtractor

class TestSpamPredictor:
    """Test cases for SpamPredictor"""
    
    @pytest.fixture
    def sample_texts(self):
        return [
            "Congratulations! You won a free iPhone! Click here to claim.",
            "Hey, are we still meeting for lunch tomorrow?",
            "URGENT: Your bank account has been compromised. Verify now!",
            "The project report is attached. Please review before the meeting."
        ]
    
    @pytest.fixture
    def trained_predictor(self, tmp_path):
        """Create a predictor with trained model"""
        # Create sample data
        texts = [
            "win free money click here",
            "urgent verify account now",
            "hello how are you today",
            "meeting at 3pm tomorrow",
        ]
        labels = [1, 1, 0, 0]  # spam, spam, ham, ham
        
        # Train model
        trainer = ModelTrainer(model_type='logistic_regression')
        
        # Vectorize
        vectorizer = FeatureExtractor(max_features=10)
        X = vectorizer.fit_transform(texts)
        
        # Train
        trainer.train(X, labels)
        
        # Save model and vectorizer
        model_path = str(tmp_path / "model.pkl")
        vectorizer_path = str(tmp_path / "vectorizer.pkl")
        trainer.save_model(model_path)
        vectorizer.save_vectorizer(vectorizer_path)
        
        # Create predictor
        predictor = SpamPredictor(model_path, vectorizer_path)
        return predictor
    
    def test_predictor_initialization(self, trained_predictor):
        """Test predictor initialization"""
        assert trained_predictor.is_loaded() is True
        assert trained_predictor.model is not None
        assert trained_predictor.vectorizer is not None
    
    def test_predict_spam(self, trained_predictor):
        """Test spam prediction"""
        label, confidence = trained_predictor.predict("win free money click here")
        assert label == "Spam"
        assert confidence >= 0.5
    
    def test_predict_ham(self, trained_predictor):
        """Test ham prediction"""
        label, confidence = trained_predictor.predict("hello how are you today")
        assert label == "Ham"
        assert confidence >= 0.5
    
    def test_predict_batch(self, trained_predictor, sample_texts):
        """Test batch prediction"""
        results = trained_predictor.predict_batch(sample_texts)
        assert len(results) == len(sample_texts)
        assert all('text' in r for r in results)
        assert all('prediction' in r for r in results)
        assert all('confidence' in r for r in results)
    
    def test_confidence_score(self, trained_predictor):
        """Test confidence score is reasonable"""
        _, confidence = trained_predictor.predict("clear spam message here")
        assert 0.0 <= confidence <= 1.0
    
    def test_model_info(self, trained_predictor):
        """Test model info"""
        info = trained_predictor.get_model_info()
        assert info['status'] == 'loaded'
        assert 'model_type' in info
        assert 'has_probability' in info
    
    def test_unloaded_predictor(self, tmp_path):
        """Test predictor without loading model"""
        predictor = SpamPredictor()
        assert predictor.is_loaded() is False
        
        with pytest.raises(ValueError, match="Model not loaded"):
            predictor.predict("test message")