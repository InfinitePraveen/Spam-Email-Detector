"""
Tests for TextPreprocessor
"""

import pytest
from src._preprocessor import TextPreprocessor

class TestTextPreprocessor:
    """Test cases for TextPreprocessor"""
    
    @pytest.fixture
    def preprocessor(self):
        return TextPreprocessor()
    
    def test_clean_text_lowercase(self, preprocessor):
        """Test text is converted to lowercase"""
        text = "HELLO WORLD"
        cleaned = preprocessor.clean_text(text)
        assert cleaned == "hello world"
    
    def test_clean_text_punctuation(self, preprocessor):
        """Test punctuation is removed"""
        text = "Hello, world! How are you?"
        cleaned = preprocessor.clean_text(text)
        assert cleaned == "hello world how are you"
    
    def test_clean_text_numbers(self, preprocessor):
        """Test numbers are removed"""
        text = "Hello 123 world 456"
        cleaned = preprocessor.clean_text(text)
        assert cleaned == "hello world"
    
    def test_clean_text_extra_spaces(self, preprocessor):
        """Test extra spaces are removed"""
        text = "Hello    world     how are   you"
        cleaned = preprocessor.clean_text(text)
        assert cleaned == "hello world how are you"
    
    def test_tokenize_and_stem(self, preprocessor):
        """Test tokenization and stemming"""
        text = "running jumpers beautifully"
        processed = preprocessor.tokenize_and_stem(text)
        assert processed == "run jump beauti"
    
    def test_empty_text(self, preprocessor):
        """Test empty text handling"""
        text = ""
        cleaned = preprocessor.clean_text(text)
        assert cleaned == ""
        
    def test_special_characters(self, preprocessor):
        """Test special characters are handled"""
        text = "Hello! @world #spam $money"
        cleaned = preprocessor.clean_text(text)
        assert cleaned == "hello world spam money"
    
    def test_stopwords_removal(self, preprocessor):
        """Test stopwords are removed"""
        text = "the cat is running very fast"
        processed = preprocessor.tokenize_and_stem(text)
        assert "the" not in processed
        assert "is" not in processed
        assert "very" not in processed
    
    def test_unicode_text(self, preprocessor):
        """Test Unicode text handling"""
        text = "Hello 世界 😊"
        cleaned = preprocessor.clean_text(text)
        assert cleaned == "hello 世界"