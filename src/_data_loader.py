"""
Data Loading Module
"""

import os
import pandas as pd
import logging
from typing import Tuple, Optional
from pathlib import Path

logger = logging.getLogger(__name__)

class DataLoader:
    """Load and validate dataset for spam detection"""
    
    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize DataLoader
        
        Args:
            data_path: Path to the dataset file (CSV)
        """
        self.data_path = data_path
        self.df = None
        
    def load_from_csv(self, file_path: str, encoding: str = 'latin-1') -> pd.DataFrame:
        """
        Load dataset from CSV file
        
        Args:
            file_path: Path to CSV file
            encoding: File encoding (default: 'latin-1')
            
        Returns:
            DataFrame with loaded data
        """
        try:
            logger.info(f"Loading dataset from {file_path}")
            self.df = pd.read_csv(file_path, encoding=encoding)
            logger.info(f"Loaded {len(self.df)} records")
            return self.df
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            raise
    
    def load_from_kaggle(self, dataset_name: str) -> pd.DataFrame:
        """
        Load dataset directly from Kaggle (requires kaggle CLI)
        
        Args:
            dataset_name: Kaggle dataset name (e.g., 'uciml/sms-spam-collection-dataset')
            
        Returns:
            DataFrame with loaded data
        """
        try:
            import subprocess
            import zipfile
            
            # Download dataset
            logger.info(f"Downloading dataset from Kaggle: {dataset_name}")
            subprocess.run(['kaggle', 'datasets', 'download', '-d', dataset_name], check=True)
            
            # Unzip and load
            zip_name = dataset_name.split('/')[-1] + '.zip'
            with zipfile.ZipFile(zip_name, 'r') as zip_ref:
                zip_ref.extractall('data/raw/')
            
            # Find CSV file
            csv_files = [f for f in os.listdir('data/raw/') if f.endswith('.csv')]
            if not csv_files:
                raise FileNotFoundError("No CSV file found in downloaded data")
            
            self.df = pd.read_csv(os.path.join('data/raw/', csv_files[0]), encoding='latin-1')
            logger.info(f"Loaded {len(self.df)} records from Kaggle")
            return self.df
            
        except Exception as e:
            logger.error(f"Error loading from Kaggle: {e}")
            raise
    
    def clean_data(self) -> pd.DataFrame:
        """
        Clean and prepare the dataset
        
        Returns:
            Cleaned DataFrame
        """
        if self.df is None:
            raise ValueError("No data loaded. Call load_from_csv() or load_from_kaggle() first.")
        
        # Make a copy
        df = self.df.copy()
        
        # Detect columns (for SMS Spam Collection)
        if 'v1' in df.columns and 'v2' in df.columns:
            df = df[['v1', 'v2']]
            df.columns = ['label', 'message']
        elif 'label' in df.columns and 'text' in df.columns:
            df = df[['label', 'text']]
            df.columns = ['label', 'message']
        elif 'Category' in df.columns and 'Message' in df.columns:
            df = df[['Category', 'Message']]
            df.columns = ['label', 'message']
        
        # Clean labels
        df['label'] = df['label'].astype(str).str.strip().str.lower()
        df['label'] = df['label'].map({'ham': 0, 'spam': 1, 'spam': 1})
        
        # Remove empty messages
        df = df.dropna(subset=['message'])
        df = df[df['message'].str.strip() != '']
        
        # Remove duplicates
        df = df.drop_duplicates('message')
        
        logger.info(f"Cleaned data: {len(df)} records remaining")
        self.df = df
        return df
    
    def get_class_distribution(self) -> pd.Series:
        """Get class distribution of the dataset"""
        if self.df is None:
            raise ValueError("No data loaded")
        return self.df['label'].value_counts()
    
    def split_data(self, test_size: float = 0.2, random_state: int = 42):
        """
        Split data into train and test sets
        
        Args:
            test_size: Proportion of test data
            random_state: Random seed for reproducibility
            
        Returns:
            Tuple of (X_train, X_test, y_train, y_test)
        """
        from sklearn.model_selection import train_test_split
        
        if self.df is None:
            raise ValueError("No data loaded")
        
        X = self.df['message']
        y = self.df['label']
        
        return train_test_split(X, y, test_size=test_size, 
                              random_state=random_state, stratify=y)