"""
Utility Functions
"""

import os
import sys
import logging
import json
import yaml
from datetime import datetime
from typing import Any, Dict, Optional
import joblib
import pickle

def setup_logging(log_file: Optional[str] = None, 
                 log_level: str = 'INFO') -> None:
    """
    Setup logging configuration
    
    Args:
        log_file: Path to log file (optional)
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_level = getattr(logging, log_level.upper())
    
    handlers = [logging.StreamHandler(sys.stdout)]
    
    if log_file:
        # Create log directory if it doesn't exist
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=handlers
    )
    
    # Set specific log levels for third-party libraries
    logging.getLogger('matplotlib').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

def save_model(model: Any, filepath: str, method: str = 'joblib') -> None:
    """
    Save model to disk
    
    Args:
        model: Model object to save
        filepath: Path to save model
        method: 'joblib' or 'pickle'
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    if method == 'joblib':
        joblib.dump(model, filepath)
    elif method == 'pickle':
        with open(filepath, 'wb') as f:
            pickle.dump(model, f)
    else:
        raise ValueError(f"Unsupported save method: {method}")
    
    logging.info(f"Model saved to {filepath}")

def load_model(filepath: str, method: str = 'joblib') -> Any:
    """
    Load model from disk
    
    Args:
        filepath: Path to model file
        method: 'joblib' or 'pickle'
        
    Returns:
        Loaded model
    """
    if method == 'joblib':
        return joblib.load(filepath)
    elif method == 'pickle':
        with open(filepath, 'rb') as f:
            return pickle.load(f)
    else:
        raise ValueError(f"Unsupported load method: {method}")

def save_config(config: Dict, filepath: str) -> None:
    """
    Save configuration to YAML file
    
    Args:
        config: Configuration dictionary
        filepath: Path to save config
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        yaml.dump(config, f, default_flow_style=False)
    logging.info(f"Configuration saved to {filepath}")

def load_config(filepath: str) -> Dict:
    """
    Load configuration from YAML file
    
    Args:
        filepath: Path to config file
        
    Returns:
        Configuration dictionary
    """
    with open(filepath, 'r') as f:
        config = yaml.safe_load(f)
    logging.info(f"Configuration loaded from {filepath}")
    return config

def get_timestamp() -> str:
    """Get current timestamp string"""
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

def create_metrics_report(metrics: Dict) -> str:
    """
    Create a formatted metrics report
    
    Args:
        metrics: Dictionary of metrics
        
    Returns:
        Formatted report string
    """
    report = "=" * 50 + "\n"
    report += "MODEL PERFORMANCE REPORT\n"
    report += "=" * 50 + "\n"
    report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for key, value in metrics.items():
        if isinstance(value, float):
            report += f"{key:20s}: {value:.4f}\n"
        else:
            report += f"{key:20s}: {value}\n"
    
    report += "=" * 50 + "\n"
    return report

def save_metrics_report(metrics: Dict, filepath: str) -> None:
    """
    Save metrics report to file
    
    Args:
        metrics: Dictionary of metrics
        filepath: Path to save report
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    report = create_metrics_report(metrics)
    with open(filepath, 'w') as f:
        f.write(report)
    logging.info(f"Metrics report saved to {filepath}")

def validate_text(text: str, max_length: int = 5000) -> bool:
    """
    Validate email text
    
    Args:
        text: Text to validate
        max_length: Maximum allowed length
        
    Returns:
        True if valid, False otherwise
    """
    if not text or not isinstance(text, str):
        return False
    if len(text) > max_length:
        return False
    return True