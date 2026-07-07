#!/usr/bin/env python3
"""
Evaluation Script for Spam Email Detector
"""

import os
import sys
import json
import argparse
import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src._predictor import SpamPredictor
from src._data_loader import DataLoader
from src._utils import setup_logging, load_config
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, auc

logger = logging.getLogger(__name__)

def evaluate_model(config_path: str = 'config/config.yml', output_dir: str = 'evaluation'):
    """
    Evaluate the trained spam detection model
    
    Args:
        config_path: Path to configuration file
        output_dir: Directory to save evaluation outputs
    """
    # Setup
    config = load_config(config_path)
    setup_logging()
    
    os.makedirs(output_dir, exist_ok=True)
    
    logger.info("=" * 50)
    logger.info("MODEL EVALUATION")
    logger.info("=" * 50)
    
    # 1. Load model
    logger.info("1. Loading model...")
    predictor = SpamPredictor(
        model_path=config['training']['model_path'],
        vectorizer_path=config['training']['vectorizer_path']
    )
    
    if not predictor.is_loaded():
        raise ValueError("Model not loaded. Train first or check paths.")
    
    logger.info(f"Model loaded: {predictor.get_model_info()}")
    
    # 2. Load test data
    logger.info("2. Loading test data...")
    data_loader = DataLoader()
    df = data_loader.load_from_csv(config['data']['local_path'])
    df = data_loader.clean_data()
    
    # Preprocess
    from src.preprocessor import TextPreprocessor
    preprocessor = TextPreprocessor()
    df['processed_text'] = df['message'].apply(preprocessor.clean_text)
    df['processed_text'] = df['processed_text'].apply(preprocessor.tokenize_and_stem)
    
    # Split
    X_train, X_test, y_train, y_test = data_loader.split_data(
        test_size=config['data']['test_size'],
        random_state=config['data']['random_state']
    )
    
    # 3. Make predictions
    logger.info("3. Making predictions...")
    predictions = []
    confidences = []
    
    for text in X_test:
        label, confidence = predictor.predict(text)
        predictions.append(1 if label == 'Spam' else 0)
        confidences.append(confidence)
    
    # 4. Calculate metrics
    logger.info("4. Calculating metrics...")
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
    
    metrics = {
        'accuracy': accuracy_score(y_test, predictions),
        'precision': precision_score(y_test, predictions, average='binary'),
        'recall': recall_score(y_test, predictions, average='binary'),
        'f1_score': f1_score(y_test, predictions, average='binary')
    }
    
    logger.info(f"Metrics: {metrics}")
    
    # 5. Confusion matrix
    logger.info("5. Generating confusion matrix...")
    cm = confusion_matrix(y_test, predictions)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Ham', 'Spam'],
                yticklabels=['Ham', 'Spam'])
    plt.title('Confusion Matrix')
    plt.xlabel('Predicted')
    plt.ylabel('Actual')
    plt.savefig(os.path.join(output_dir, 'confusion_matrix.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 6. Classification report
    logger.info("6. Generating classification report...")
    report = classification_report(y_test, predictions, 
                                   target_names=['Ham', 'Spam'],
                                   output_dict=True)
    
    with open(os.path.join(output_dir, 'classification_report.json'), 'w') as f:
        json.dump(report, f, indent=2)
    
    # 7. ROC Curve
    logger.info("7. Generating ROC curve...")
    fpr, tpr, _ = roc_curve(y_test, confidences)
    roc_auc = auc(fpr, tpr)
    
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2,
             label=f'ROC curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve')
    plt.legend(loc="lower right")
    plt.savefig(os.path.join(output_dir, 'roc_curve.png'), dpi=300, bbox_inches='tight')
    plt.close()
    
    # 8. Save metrics
    logger.info("8. Saving evaluation results...")
    all_results = {
        'model_info': predictor.get_model_info(),
        'test_size': len(X_test),
        'metrics': metrics,
        'confusion_matrix': cm.tolist(),
        'classification_report': report,
        'roc_auc': roc_auc
    }
    
    with open(os.path.join(output_dir, 'evaluation_results.json'), 'w') as f:
        json.dump(all_results, f, indent=2)
    
    # 9. Generate summary report
    logger.info("9. Generating summary report...")
    summary = f"""
    ========================================
    SPAM DETECTOR EVALUATION SUMMARY
    ========================================
    
    Model: {predictor.get_model_info()['model_type']}
    Test Samples: {len(X_test)}
    
    Performance Metrics:
    - Accuracy:  {metrics['accuracy']:.4f}
    - Precision: {metrics['precision']:.4f}
    - Recall:    {metrics['recall']:.4f}
    - F1-Score:  {metrics['f1_score']:.4f}
    
    ROC AUC:     {roc_auc:.4f}
    
    Confusion Matrix:
    [[{cm[0][0]:4d} {cm[0][1]:4d}]
     [{cm[1][0]:4d} {cm[1][1]:4d}]]
    
    ========================================
    """
    
    with open(os.path.join(output_dir, 'evaluation_summary.txt'), 'w') as f:
        f.write(summary)
    
    print(summary)
    logger.info(f"Evaluation complete! Results saved to: {output_dir}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Evaluate Spam Detection Model')
    parser.add_argument('--config', default='config/config.yml',
                       help='Path to configuration file')
    parser.add_argument('--output', default='evaluation',
                       help='Output directory for evaluation results')
    args = parser.parse_args()
    
    evaluate_model(args.config, args.output)

if __name__ == '__main__':
    main()