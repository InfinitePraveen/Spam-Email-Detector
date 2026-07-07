#!/usr/bin/env python3
"""
Training Script for Spam Email Detector
"""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src._data_loader import DataLoader
from src._preprocessor import TextPreprocessor
from src._feature_extractor import FeatureExtractor
from src._trainer import ModelTrainer
from src._utils import setup_logging, save_config, load_config, save_metrics_report

logger = logging.getLogger(__name__)

def train_model(config_path: str = 'config/config.yml'):
    """
    Train the spam detection model
    
    Args:
        config_path: Path to configuration file
    """
    # Load configuration
    config = load_config(config_path)
    setup_logging(log_file=config['logging']['file'], 
                 log_level=config['logging']['level'])
    
    logger.info("=" * 50)
    logger.info("SPAM DETECTOR MODEL TRAINING")
    logger.info("=" * 50)
    
    # 1. Load data
    logger.info("1. Loading data...")
    data_loader = DataLoader()
    
    if config['data']['source'] == 'kaggle':
        df = data_loader.load_from_kaggle(config['data']['kaggle_dataset'])
    else:
        df = data_loader.load_from_csv(config['data']['local_path'])
    
    # Clean data
    df = data_loader.clean_data()
    logger.info(f"Data loaded: {len(df)} samples")
    logger.info(f"Class distribution:\n{data_loader.get_class_distribution()}")
    
    # 2. Preprocess text
    logger.info("2. Preprocessing text...")
    preprocessor = TextPreprocessor()
    df['processed_text'] = df['message'].apply(preprocessor.clean_text)
    df['processed_text'] = df['processed_text'].apply(preprocessor.tokenize_and_stem)
    
    # 3. Split data
    logger.info("3. Splitting data...")
    X_train, X_test, y_train, y_test = data_loader.split_data(
        test_size=config['data']['test_size'],
        random_state=config['data']['random_state']
    )
    logger.info(f"Training: {len(X_train)} samples")
    logger.info(f"Testing: {len(X_test)} samples")
    
    # 4. Extract features
    logger.info("4. Extracting features...")
    feature_extractor = FeatureExtractor(
        max_features=config['features']['max_features'],
        ngram_range=tuple(config['features']['ngram_range']),
        use_tfidf=config['features']['vectorizer'] == 'tfidf'
    )
    
    X_train_features = feature_extractor.fit_transform(X_train)
    X_test_features = feature_extractor.transform(X_test)
    logger.info(f"Features shape: {X_train_features.shape}")
    
    # 5. Train model
    logger.info("5. Training model...")
    trainer = ModelTrainer(
        model_type=config['model']['type'],
        random_state=config['model']['random_state']
    )
    
    # Hyperparameter tuning
    if config['model']['hyperparameter_tuning']:
        logger.info("   Performing hyperparameter tuning...")
        trainer.tune_hyperparameters(
            X_train_features, 
            y_train,
            cv=config['model']['cv_folds']
        )
    else:
        trainer.train(X_train_features, y_train)
    
    # 6. Evaluate model
    logger.info("6. Evaluating model...")
    metrics = trainer.evaluate(X_test_features, y_test)
    logger.info(f"   Metrics: {metrics}")
    
    # Cross-validation
    logger.info("7. Cross-validation...")
    cv_results = trainer.cross_validate(
        X_train_features, 
        y_train,
        cv=config['model']['cv_folds']
    )
    logger.info(f"   CV Results: {cv_results}")
    
    # 7. Save model
    if config['training']['save_model']:
        logger.info("8. Saving model...")
        os.makedirs(os.path.dirname(config['training']['model_path']), exist_ok=True)
        trainer.save_model(config['training']['model_path'])
        feature_extractor.save_vectorizer(config['training']['vectorizer_path'])
        
        logger.info(f"   Model saved to: {config['training']['model_path']}")
        logger.info(f"   Vectorizer saved to: {config['training']['vectorizer_path']}")
    
    # 8. Save metrics
    if config['training']['save_metrics']:
        logger.info("9. Saving metrics...")
        all_metrics = {
            'model_type': config['model']['type'],
            'test_metrics': metrics,
            'cv_metrics': cv_results
        }
        
        os.makedirs(os.path.dirname(config['training']['metrics_path']), exist_ok=True)
        import json
        with open(config['training']['metrics_path'], 'w') as f:
            json.dump(all_metrics, f, indent=2)
        
        # Save report
        save_metrics_report(metrics, config['training']['report_path'])
        logger.info(f"   Metrics saved to: {config['training']['metrics_path']}")
    
    # 9. Summary
    logger.info("=" * 50)
    logger.info("TRAINING COMPLETE!")
    logger.info(f"Best Model: {config['model']['type']}")
    logger.info(f"Test Accuracy: {metrics['accuracy']:.4f}")
    logger.info(f"Test F1-Score: {metrics['f1_score']:.4f}")
    logger.info("=" * 50)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Train Spam Detection Model')
    parser.add_argument('--config', default='config/config.yml', 
                       help='Path to configuration file')
    args = parser.parse_args()
    
    train_model(args.config)

if __name__ == '__main__':
    main()