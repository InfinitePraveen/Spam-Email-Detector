# web/app.py
"""
Spam Email Detector - Web Application
"""

import os
import sys
import logging
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src._predictor import SpamPredictor
from src._utils import setup_logging

# Load environment variables
load_dotenv()

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Enable CORS
CORS(app)

# Initialize predictor
predictor = SpamPredictor()

# Load model on startup
try:
    predictor.load_model()
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    logger.warning("Running in demo mode (model not loaded)")

# Form for email input
class EmailForm(FlaskForm):
    email = TextAreaField('Email Content', 
                         validators=[DataRequired(message="Email content is required"), 
                                    Length(min=1, max=5000)])
    submit = SubmitField('Classify Email')

@app.route('/', methods=['GET', 'POST'])
def index():
    """Main page with email classification form"""
    form = EmailForm()
    result = None
    confidence = None
    error = None
    
    if form.validate_on_submit():
        email_text = form.email.data
        try:
            # Get prediction
            prediction, confidence = predictor.predict(email_text)
            result = prediction
            
            # Log the prediction
            logger.info(f"Prediction: {prediction} (Confidence: {confidence:.2%})")
            
            # Store in session for history
            if 'history' not in session:
                session['history'] = []
            session['history'].append({
                'email': email_text[:100] + '...' if len(email_text) > 100 else email_text,
                'prediction': prediction,
                'confidence': confidence,
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
            session.modified = True
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            error = "Failed to classify email. Please try again."
    
    return render_template('index.html', 
                         form=form, 
                         result=result, 
                         confidence=confidence,
                         error=error,
                         history=session.get('history', [])[:10])  # Show last 10 predictions

@app.route('/predict', methods=['POST'])
def predict_api():
    """API endpoint for predictions"""
    try:
        data = request.get_json()
        
        if not data or 'email' not in data:
            return jsonify({'error': 'No email content provided'}), 400
        
        email_text = data['email']
        prediction, confidence = predictor.predict(email_text)
        
        response = {
            'prediction': prediction,
            'confidence': round(confidence, 4),
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/history')
def history():
    """View prediction history"""
    return render_template('history.html', history=session.get('history', []))

@app.route('/clear_history', methods=['POST'])
def clear_history():
    """Clear prediction history"""
    session['history'] = []
    session.modified = True
    return jsonify({'status': 'success'}), 200

@app.route('/health')
def health_check():
    """Health check endpoint"""
    status = {
        'status': 'healthy',
        'model_loaded': predictor.is_loaded(),
        'timestamp': datetime.now().isoformat()
    }
    return jsonify(status), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)
