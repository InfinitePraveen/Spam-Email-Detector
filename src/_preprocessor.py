"""
Text Preprocessing Module
"""

import re
import string
import logging
from typing import List, Optional
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

logger = logging.getLogger(__name__)

class TextPreprocessor:
    """
    Preprocess text data for spam detection
    
    This class handles all text preprocessing operations including:
    - Lowercasing
    - Punctuation removal
    - Number removal
    - Stopword removal
    - Stemming/Lemmatization
    - Tokenization
    """
    
    def __init__(self, use_stemming: bool = True, remove_stopwords: bool = True,
                 remove_punctuation: bool = True, remove_numbers: bool = True,
                 lowercase: bool = True):
        """
        Initialize TextPreprocessor
        
        Args:
            use_stemming: If True, use stemming; else use lemmatization
            remove_stopwords: If True, remove stopwords
            remove_punctuation: If True, remove punctuation
            remove_numbers: If True, remove numbers
            lowercase: If True, convert to lowercase
        """
        self.use_stemming = use_stemming
        self.remove_stopwords = remove_stopwords
        self.remove_punctuation = remove_punctuation
        self.remove_numbers = remove_numbers
        self.lowercase = lowercase
        
        # Initialize stemmer and lemmatizer
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        
        # Load stopwords
        self.stop_words = set(stopwords.words('english'))
        
        # Add custom stopwords for spam detection
        self.custom_stopwords = {
            'subject', 'hello', 'hi', 'dear', 'sincerely', 'regards',
            'thanks', 'thank', 'please', 'kindly', 'best', 'regard'
        }
        self.stop_words.update(self.custom_stopwords)
        
        logger.info(f"TextPreprocessor initialized with: "
                   f"use_stemming={use_stemming}, "
                   f"remove_stopwords={remove_stopwords}, "
                   f"remove_punctuation={remove_punctuation}, "
                   f"remove_numbers={remove_numbers}")
    
    def clean_text(self, text: str) -> str:
        """
        Clean and preprocess text
        
        Args:
            text: Raw text to clean
            
        Returns:
            Cleaned text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Convert to lowercase
        if self.lowercase:
            text = text.lower()
        
        # Remove punctuation
        if self.remove_punctuation:
            text = ''.join([char for char in text if char not in string.punctuation])
        
        # Remove numbers
        if self.remove_numbers:
            text = re.sub(r'\d+', '', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove special characters
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Text to tokenize
            
        Returns:
            List of tokens
        """
        if not text:
            return []
        
        try:
            tokens = word_tokenize(text)
        except:
            # Fallback to simple split
            tokens = text.split()
        
        return tokens
    
    def remove_stopwords_from_tokens(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords from token list
        
        Args:
            tokens: List of tokens
            
        Returns:
            List of tokens without stopwords
        """
        if not self.remove_stopwords:
            return tokens
        
        return [token for token in tokens if token not in self.stop_words]
    
    def stem_tokens(self, tokens: List[str]) -> List[str]:
        """
        Apply stemming to tokens
        
        Args:
            tokens: List of tokens
            
        Returns:
            List of stemmed tokens
        """
        if self.use_stemming:
            return [self.stemmer.stem(token) for token in tokens]
        else:
            return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def tokenize_and_stem(self, text: str) -> str:
        """
        Complete preprocessing pipeline: clean, tokenize, remove stopwords, stem
        
        Args:
            text: Raw text
            
        Returns:
            Processed text as string
        """
        if not text:
            return ""
        
        # Clean text
        cleaned = self.clean_text(text)
        
        # Tokenize
        tokens = self.tokenize(cleaned)
        
        # Remove stopwords
        tokens = self.remove_stopwords_from_tokens(tokens)
        
        # Stem/Lemmatize
        tokens = self.stem_tokens(tokens)
        
        # Join back to string
        return ' '.join(tokens)
    
    def process_batch(self, texts: List[str]) -> List[str]:
        """
        Process a batch of texts
        
        Args:
            texts: List of text strings
            
        Returns:
            List of processed texts
        """
        return [self.tokenize_and_stem(text) for text in texts]
    
    def get_text_stats(self, text: str) -> dict:
        """
        Get statistics about the text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary with text statistics
        """
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        
        stats = {
            'original_length': len(text),
            'cleaned_length': len(cleaned),
            'word_count': len(tokens),
            'unique_words': len(set(tokens)),
            'avg_word_length': sum(len(t) for t in tokens) / len(tokens) if tokens else 0,
            'has_numbers': bool(re.search(r'\d', text)),
            'has_punctuation': bool(re.search(r'[{}]'.format(string.punctuation), text)),
            'has_uppercase': any(c.isupper() for c in text),
            'special_char_count': len(re.findall(r'[^a-zA-Z0-9\s]', text))
        }
        
        return stats
    
    def extract_features_from_text(self, text: str) -> dict:
        """
        Extract additional features from text
        
        Args:
            text: Input text
            
        Returns:
            Dictionary of additional features
        """
        stats = self.get_text_stats(text)
        
        features = {
            'word_count': stats['word_count'],
            'unique_word_ratio': stats['unique_words'] / stats['word_count'] if stats['word_count'] > 0 else 0,
            'avg_word_length': stats['avg_word_length'],
            'special_char_ratio': stats['special_char_count'] / stats['original_length'] if stats['original_length'] > 0 else 0,
            'has_links': 1 if re.search(r'https?://|www\.|\.com|\.org|\.net', text) else 0,
            'has_money': 1 if re.search(r'\$|€|£|[0-9]+\.?[0-9]*\s*(dollars|usd|eur|gbp)', text) else 0,
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'uppercase_ratio': sum(1 for c in text if c.isupper()) / len(text) if len(text) > 0 else 0
        }
        
        return features
    
    def set_custom_stopwords(self, stopwords_list: List[str]):
        """
        Add custom stopwords
        
        Args:
            stopwords_list: List of words to add to stopwords
        """
        self.stop_words.update(stopwords_list)
        logger.info(f"Added {len(stopwords_list)} custom stopwords")
    
    def get_stopwords(self) -> set:
        """Get current stopwords set"""
        return self.stop_words
    
    def add_stopword(self, word: str):
        """Add a single stopword"""
        self.stop_words.add(word.lower())
    
    def remove_stopword(self, word: str):
        """Remove a stopword"""
        if word.lower() in self.stop_words:
            self.stop_words.remove(word.lower())


def preprocess_dataframe(df, text_column: str, target_column: Optional[str] = None,
                         clean_column_name: str = 'cleaned_text',
                         processed_column_name: str = 'processed_text'):
    """
    Convenience function to preprocess entire dataframe
    
    Args:
        df: Pandas DataFrame
        text_column: Name of column containing text
        target_column: Optional target column name to keep
        clean_column_name: Name for cleaned text column
        processed_column_name: Name for processed text column
        
    Returns:
        Preprocessed DataFrame
    """
    preprocessor = TextPreprocessor()
    
    # Make a copy to avoid modifying original
    df_processed = df.copy()
    
    # Clean text
    df_processed[clean_column_name] = df_processed[text_column].apply(
        preprocessor.clean_text
    )
    
    # Process text (tokenize + stem)
    df_processed[processed_column_name] = df_processed[clean_column_name].apply(
        preprocessor.tokenize_and_stem
    )
    
    # Extract features
    feature_columns = []
    for idx, row in df_processed.iterrows():
        features = preprocessor.extract_features_from_text(row[text_column])
        for key, value in features.items():
            col_name = f'feature_{key}'
            df_processed.loc[idx, col_name] = value
            if col_name not in feature_columns:
                feature_columns.append(col_name)
    
    logger.info(f"Preprocessed {len(df_processed)} rows")
    logger.info(f"Added {len(feature_columns)} feature columns")
    
    # Keep only relevant columns if target specified
    if target_column:
        columns_to_keep = [target_column, clean_column_name, processed_column_name] + feature_columns
        df_processed = df_processed[columns_to_keep]
    
    return df_processed