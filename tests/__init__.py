"""
Test Suite for Spam Email Detector

This package contains all unit tests for the Spam Email Detector project.
Tests are organized to validate functionality across all modules including:
- Data preprocessing
- Feature extraction
- Model training and evaluation
- Prediction pipeline
- Web interface components
"""

# Import test modules for easier access
import importlib
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    importlib.import_module("tests._test_preprocessor")
    importlib.import_module("tests._test_model")
    importlib.import_module("tests._test_predictor")
else:
    from . import _test_preprocessor
    from . import _test_model
    from . import _test_predictor

__all__ = [
    '_test_preprocessor',
    '_test_model',
    '_test_predictor'
]

# Test configuration
TEST_DATA_PATH = 'data/test_samples.csv'
TEST_MODEL_PATH = 'models/test_model.pkl'
TEST_VECTORIZER_PATH = 'models/test_vectorizer.pkl'

# Test constants
SAMPLE_SPAM_TEXTS = [
    "Congratulations! You won a free iPhone! Click here to claim.",
    "URGENT: Your bank account has been compromised. Verify now!",
    "You have been selected as a winner of our lottery. Send money to claim."
]

SAMPLE_HAM_TEXTS = [
    "Hey, are we still meeting for lunch tomorrow?",
    "The project report is attached. Please review before the meeting.",
    "Thanks for your email. I'll get back to you shortly."
]

def get_test_texts():
    """
    Get sample texts for testing
    
    Returns:
        tuple: (spam_texts, ham_texts)
    """
    return SAMPLE_SPAM_TEXTS, SAMPLE_HAM_TEXTS