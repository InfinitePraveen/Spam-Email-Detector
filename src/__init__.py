"""
Spam Email Detector - Source Code Package
"""

from ._data_loader import DataLoader
from .preprocessor import TextPreprocessor
from ._feature_extractor import FeatureExtractor
from ._trainer import ModelTrainer
from ._predictor import SpamPredictor
from ._utils import setup_logging, save_model, load_model

__version__ = "1.0.0"
__all__ = [
    'DataLoader',
    'TextPreprocessor',
    'FeatureExtractor',
    'ModelTrainer',
    'SpamPredictor',
    'setup_logging',
    'save_model',
    'load_model'
]