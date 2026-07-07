"""
Feature Extraction Module
"""

import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import TruncatedSVD
from typing import Tuple, Optional
import joblib

logger = logging.getLogger(__name__)

class FeatureExtractor:
    """Extract features from text data"""
    
    def __init__(self, max_features: int = 5000, ngram_range: tuple = (1, 2),
                 use_tfidf: bool = True):
        """
        Initialize FeatureExtractor
        
        Args:
            max_features: Maximum number of features
            ngram_range: Range of n-grams to consider
            use_tfidf: If True, use TF-IDF; else use CountVectorizer
        """
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.use_tfidf = use_tfidf
        
        if use_tfidf:
            self.vectorizer = TfidfVectorizer(
                max_features=max_features,
                ngram_range=ngram_range,
                stop_words='english',
                lowercase=True,
                analyzer='word'
            )
        else:
            self.vectorizer = CountVectorizer(
                max_features=max_features,
                ngram_range=ngram_range,
                stop_words='english',
                lowercase=True,
                analyzer='word'
            )
        
        self.is_fitted = False
        
    def fit_transform(self, X_train) -> np.ndarray:
        """
        Fit vectorizer and transform training data
        
        Args:
            X_train: Training text data
            
        Returns:
            Transformed feature matrix
        """
        logger.info(f"Fitting vectorizer with max_features={self.max_features}")
        X_train_transformed = self.vectorizer.fit_transform(X_train)
        self.is_fitted = True
        logger.info(f"Features shape: {X_train_transformed.shape}")
        return X_train_transformed
    
    def transform(self, X_test) -> np.ndarray:
        """
        Transform test data using fitted vectorizer
        
        Args:
            X_test: Test text data
            
        Returns:
            Transformed feature matrix
        """
        if not self.is_fitted:
            raise ValueError("Vectorizer not fitted. Call fit_transform() first.")
        
        return self.vectorizer.transform(X_test)
    
    def get_feature_names(self) -> list:
        """Get feature names from vectorizer"""
        if not self.is_fitted:
            raise ValueError("Vectorizer not fitted")
        return self.vectorizer.get_feature_names_out()
    
    def reduce_dimensions(self, X, n_components: int = 100):
        """
        Reduce dimensions using SVD (for large datasets)
        
        Args:
            X: Feature matrix
            n_components: Number of components
            
        Returns:
            Reduced feature matrix
        """
        logger.info(f"Reducing dimensions to {n_components} components")
        svd = TruncatedSVD(n_components=n_components, random_state=42)
        X_reduced = svd.fit_transform(X)
        logger.info(f"Explained variance: {svd.explained_variance_ratio_.sum():.4f}")
        return X_reduced
    
    def save_vectorizer(self, filepath: str):
        """Save vectorizer to disk"""
        joblib.dump(self.vectorizer, filepath)
        logger.info(f"Vectorizer saved to {filepath}")
    
    def load_vectorizer(self, filepath: str):
        """Load vectorizer from disk"""
        self.vectorizer = joblib.load(filepath)
        self.is_fitted = True
        logger.info(f"Vectorizer loaded from {filepath}")