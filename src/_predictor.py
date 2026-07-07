"""
Prediction Module
"""

import logging
import numpy as np
import joblib
from typing import Tuple, Optional
from ._preprocessor import TextPreprocessor
from ._feature_extractor import FeatureExtractor

logger = logging.getLogger(__name__)

class SpamPredictor:
    """Predict spam emails using trained model"""
    
    def __init__(self, model_path: Optional[str] = None, 
                 vectorizer_path: Optional[str] = None):
        """
        Initialize SpamPredictor
        
        Args:
            model_path: Path to trained model
            vectorizer_path: Path to fitted vectorizer
        """
        self.model = None
        self.vectorizer = None
        self.preprocessor = TextPreprocessor()
        self._is_loaded = False
        
        if model_path and vectorizer_path:
            self.load_model(model_path, vectorizer_path)
    
    def load_model(self, model_path: str, vectorizer_path: Optional[str] = None):
        """
        Load trained model and vectorizer
        
        Args:
            model_path: Path to model file
            vectorizer_path: Path to vectorizer file
        """
        try:
            self.model = joblib.load(model_path)
            logger.info(f"Model loaded from {model_path}")
            
            if vectorizer_path:
                self.vectorizer = joblib.load(vectorizer_path)
                logger.info(f"Vectorizer loaded from {vectorizer_path}")
            
            self._is_loaded = True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            raise
    
    def predict(self, text: str) -> Tuple[str, float]:
        """
        Predict if an email is spam or ham
        
        Args:
            text: Email text to classify
            
        Returns:
            Tuple of (prediction_label, confidence_score)
        """
        if not self._is_loaded:
            raise ValueError("Model not loaded. Call load_model() first.")
        
        # Vectorize using the same input style as during training
        if self.vectorizer:
            features = self.vectorizer.transform([text])
        else:
            raise ValueError("Vectorizer not loaded")
        
        # Predict
        prediction = self.model.predict(features)[0]
        
        # Get confidence
        if hasattr(self.model, 'predict_proba'):
            confidence = self.model.predict_proba(features)[0][prediction]
        else:
            # For models without predict_proba (e.g., SVM with linear kernel)
            confidence = 1.0
        
        label = 'Spam' if prediction == 1 else 'Ham'
        
        logger.info(f"Prediction: {label} (Confidence: {confidence:.4f})")
        return label, float(confidence)
    
    def predict_batch(self, texts: list) -> list:
        """
        Predict multiple emails in batch
        
        Args:
            texts: List of email texts
            
        Returns:
            List of predictions
        """
        results = []
        for text in texts:
            label, confidence = self.predict(text)
            results.append({
                'text': text[:100] + '...' if len(text) > 100 else text,
                'prediction': label,
                'confidence': confidence
            })
        return results
    
    def is_loaded(self) -> bool:
        """Check if model is loaded"""
        return self._is_loaded
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model"""
        if not self._is_loaded:
            return {'status': 'not loaded'}
        
        return {
            'status': 'loaded',
            'model_type': type(self.model).__name__,
            'has_probability': hasattr(self.model, 'predict_proba')
        }