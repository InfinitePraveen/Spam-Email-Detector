Spam Email Detector - User Guide

## 📖 Introduction

Welcome to the **Spam Email Detector**! This application uses artificial intelligence and machine learning to automatically classify emails as either **spam** (unwanted, potentially malicious) or **ham** (legitimate, wanted emails).

Whether you're a regular user looking to filter out spam or a developer wanting to integrate spam detection into your application, this guide will help you get started.

## 🚀 Getting Started

### System Requirements

- **Python:** 3.8 or higher
- **Operating System:** Windows, macOS, or Linux
- **Memory:** Minimum 2GB RAM (4GB recommended)
- **Storage:** At least 500MB free space
- **Browser:** Any modern browser (Chrome, Firefox, Safari, Edge)

### Quick Installation

#### Option 1: Automated Install (Recommended)

```bash
# Clone or download the repository
git clone https://github.com/yourusername/spam-email-detector.git
cd spam-email-detector

# Make the deployment script executable
chmod +x scripts/deploy.sh

# Run the deployment script
./scripts/deploy.sh
```

#### Option 2: Manual Install

```bash
# 1. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# 4. Train the model
python scripts/train_model.py

# 5. Start the application
python web/app.py
```

#### Option 3: Docker Installation

```bash
# Build and run with Docker Compose
docker-compose -f docker/docker-compose.yml up --build

# Or use Docker directly
docker build -t spam-detector -f docker/Dockerfile .
docker run -p 5000:5000 spam-detector
```

---

## 🎯 Using the Web Interface

### Accessing the Application

1. **Open your web browser**
2. **Navigate to:** `http://localhost:5000`
3. **You'll see:** The main classification page with a clean, modern interface

![Home Page](static/images/screenshot_home.png) 

### How to Classify an Email

#### Step 1: Enter the Email Content

- **Type or paste** the email text into the text area
- **Maximum length:** 5,000 characters
- **Supported formats:** Plain text, HTML (will be stripped)

**Sample email (spam):**
```
Subject: Congratulations!
You have won a free iPhone 15 Pro Max!
Click here to claim your prize: http://fake-link.com
Hurry, this offer expires in 24 hours!
```

**Sample email (ham):**
```
Subject: Meeting tomorrow
Hi team,

Just a reminder about our meeting tomorrow at 3 PM.
We'll be discussing the Q4 project updates.

Best regards,
John
```

#### Step 2: Submit for Classification

- Click the **"Classify Email"** button
- You can also use **Ctrl+Enter** (or **Cmd+Enter** on Mac) as a keyboard shortcut
- The button will show a loading state while processing

#### Step 3: View the Results

The result will display:

| Element | Description |
|---------|-------------|
| **Prediction Icon** | ⚠️ for Spam, ✅ for Ham |
| **Prediction Label** | `Spam` or `Ham` in bold |
| **Confidence Score** | Percentage showing how certain the AI is |
| **Visual Bar** | Color-coded confidence bar |
| **Recommendation** | Actionable advice based on the result |

#### Step 4: Interpret the Results

| Result | Confidence | What It Means | Action |
|--------|------------|---------------|--------|
| **Spam** | > 90% | Very likely spam | Delete immediately, don't click links |
| **Spam** | 70-90% | Probably spam | Review carefully, be cautious |
| **Spam** | < 70% | Possibly spam | May need human verification |
| **Ham** | > 90% | Very likely legitimate | Safe to open |
| **Ham** | 70-90% | Probably legitimate | Probably safe, use caution |
| **Ham** | < 70% | Could be misclassified | Review manually if suspicious |

---

## 📊 Understanding the Results

### What Does "Spam" Mean?

Spam emails are unsolicited, often commercial or malicious messages that typically:
- Promise something too good to be true (money, prizes, etc.)
- Request personal information (passwords, bank details)
- Contain suspicious links or attachments
- Use urgent or threatening language
- Come from unknown senders

### What Does "Ham" Mean?

Ham emails are legitimate, wanted messages that:
- Come from known contacts
- Are relevant to your work or personal life
- Contain expected information
- Don't request suspicious information
- Are typically expected or solicited

### Understanding Confidence Scores

The confidence score represents how certain the AI is about its prediction:

- **95-100%:** Extremely confident
- **85-95%:** Very confident  
- **70-85%:** Moderately confident
- **50-70%:** Somewhat confident
- **Below 50%:** Not confident (rare)

---

## 💻 Using the API

For developers and automation, the API provides programmatic access to the spam detection functionality.

### Quick API Example

```python
import requests

# Single prediction
response = requests.post(
    'http://localhost:5000/predict',
    json={'email': 'Your email content here'}
)
result = response.json()
print(f"Prediction: {result['prediction']}")
print(f"Confidence: {result['confidence']:.2%}")
```

### API Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/predict` | POST | Classify a single email |
| `/predict/batch` | POST | Classify multiple emails |
| `/health` | GET | Check service status |
| `/history` | GET | View prediction history |
| `/clear_history` | POST | Clear history |

### Complete API Example

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:5000"

# 1. Health Check
response = requests.get(f"{BASE_URL}/health")
print("Health:", response.json())

# 2. Single Prediction
email_text = "Congratulations! You won a free iPhone!"
response = requests.post(
    f"{BASE_URL}/predict",
    json={"email": email_text}
)
result = response.json()
print(f"Prediction: {result['prediction']} ({result['confidence']:.2%})")

# 3. Batch Prediction
emails = [
    "Win money now! Click here!",
    "Hi, how are you doing today?",
    "Your account needs verification."
]
response = requests.post(
    f"{BASE_URL}/predict/batch",
    json={"emails": emails}
)
results = response.json()
for r in results['results']:
    print(f"{r['prediction']}: {r['confidence']:.2%} - {r['email_preview']}")
```

---

## 🛠️ Advanced Features

### 1. Batch Processing

Process multiple emails at once for efficiency:

```python
# Create a CSV file with emails
import pandas as pd

# Load emails from CSV
df = pd.read_csv('emails_to_check.csv')

# Send batch request
response = requests.post(
    'http://localhost:5000/predict/batch',
    json={'emails': df['email_content'].tolist()}
)

# Process results
results = response.json()
for i, result in enumerate(results['results']):
    df.loc[i, 'prediction'] = result['prediction']
    df.loc[i, 'confidence'] = result['confidence']

# Save results
df.to_csv('classified_emails.csv', index=False)
```

### 2. Custom Training

Train the model on your own dataset:

**Step 1:** Prepare your dataset
```python
# Your dataset should have 'label' and 'message' columns
import pandas as pd

# Example dataset
data = {
    'label': ['spam', 'ham', 'spam', 'ham'],
    'message': [
        'Win free money now!',
        'How are you doing today?',
        'Your account has been compromised!',
        'Meeting at 3 PM tomorrow'
    ]
}
df = pd.DataFrame(data)
df.to_csv('my_dataset.csv', index=False)
```

**Step 2:** Train the model
```bash
# Update config/config.yml with your dataset path
# Then run training
python scripts/train_model.py
```

### 3. Export Results

View and export prediction history:

```python
import pandas as pd
import requests

# Get history (requires session authentication if enabled)
session = requests.Session()
# If authentication is enabled, login here

# Get history
response = session.get('http://localhost:5000/history')
history = response.json()

# Convert to DataFrame
df = pd.DataFrame(history)
df.to_csv('prediction_history.csv', index=False)

# Generate summary report
summary = df.groupby('prediction').size()
print("Summary:")
print(summary)
```

### 4. Real-time Email Integration

Integrate with your email client:

```python
# Gmail Integration Example
import imaplib
import email
import requests

def check_gmail_spam():
    # Connect to Gmail
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('your_email@gmail.com', 'your_app_password')
    mail.select('inbox')
    
    # Get unread emails
    status, messages = mail.search(None, 'UNSEEN')
    
    for msg_id in messages[0].split():
        # Fetch email
        status, msg_data = mail.fetch(msg_id, '(RFC822)')
        email_body = email.message_from_bytes(msg_data[0][1])
        
        # Get email content
        content = ""
        if email_body.is_multipart():
            for part in email_body.walk():
                if part.get_content_type() == "text/plain":
                    content = part.get_payload(decode=True).decode()
                    break
        else:
            content = email_body.get_payload(decode=True).decode()
        
        # Check with spam detector
        response = requests.post(
            'http://localhost:5000/predict',
            json={'email': content}
        )
        result = response.json()
        
        if result['prediction'] == 'spam':
            print(f"⚠️ SPAM DETECTED: {email_body['subject']}")
            print(f"   Confidence: {result['confidence']:.2%}")
        else:
            print(f"✅ Safe: {email_body['subject']}")
    
    mail.close()
    mail.logout()

# Run the check
check_gmail_spam()
```

---

## 📊 Understanding the Model

### How It Works

The spam detection model follows these steps:

```
Email Input → Preprocessing → Feature Extraction → Classification → Result
```

#### 1. Text Preprocessing
- Converts to lowercase
- Removes punctuation and numbers
- Removes stopwords (common words like "the", "is")
- Applies stemming (reduces words to roots)

#### 2. Feature Extraction
- Converts text to numerical features
- Uses TF-IDF (Term Frequency-Inverse Document Frequency)
- Creates a vector representation of the text
- Identifies important words and patterns

#### 3. Classification
- Trained on 5,574 labeled emails
- Uses multiple models (Logistic Regression by default)
- Outputs prediction and confidence score

### Model Performance

Based on test data with 1,115 emails:

| Metric | Value | Explanation |
|--------|-------|-------------|
| **Accuracy** | 98.5% | Overall correct predictions |
| **Precision** | 98.3% | Of spam predictions, how many were actually spam |
| **Recall** | 98.6% | Of actual spam, how many were caught |
| **F1-Score** | 98.4% | Harmonic mean of precision and recall |

### What Makes an Email Spam?

Common spam indicators detected by the model:

**Keywords:**
- "free", "winner", "congratulations", "urgent"
- "verify", "confirm", "account", "security"
- "click here", "limited time", "offer"

**Patterns:**
- Excessive exclamation marks (!!!!)
- ALL CAPS text
- Suspicious URLs (shortened links, unusual domains)
- Requests for personal information
- Sense of urgency

**Metadata:**
- Unknown or spoofed sender
- Suspicious subject lines
- Unusual email structure

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### Issue 1: Application Won't Start

**Symptoms:** 
- Error: `ModuleNotFoundError`
- Error: `Could not find a version that satisfies the requirement`

**Solutions:**
```bash
# Upgrade pip
pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Check Python version
python --version  # Should be 3.8+

# Check if virtual environment is activated
which python  # Should show path to venv
```

#### Issue 2: Model Not Found

**Symptoms:**
- `FileNotFoundError: models/spam_detector_model.pkl`
- `Model not loaded` message

**Solutions:**
```bash
# Train the model
python scripts/train_model.py

# Check model path in config
cat config/config.yml | grep model_path

# Verify model exists
ls -la models/
```

#### Issue 3: Slow Predictions

**Symptoms:**
- Response takes > 1 second
- High CPU usage

**Solutions:**
```bash
# Reduce feature size
# Edit config/config.yml:
# features.max_features: 3000

# Use simpler model
# Edit config/config.yml:
# model.type: 'naive_bayes'

# Restart application
python web/app.py
```

#### Issue 4: NLTK Data Missing

**Symptoms:**
- `LookupError: Resource punkt not found`
- `LookupError: Resource stopwords not found`

**Solutions:**
```bash
# Download all NLTK data
python -c "import nltk; nltk.download('all')"

# Or download specific resources
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# Or use the convenience script
python scripts/download_nltk_data.py
```

#### Issue 5: Memory Issues

**Symptoms:**
- `MemoryError`
- Application crashes
- System becomes slow

**Solutions:**
```bash
# Reduce feature size
# config/config.yml:
# features.max_features: 2000

# Use smaller dataset
# Limit data in training
# Edit scripts/train_model.py to sample data

# Use more efficient model
# model.type: 'naive_bayes'

# Increase system swap space (Linux/macOS)
```

#### Issue 6: Port Already in Use

**Symptoms:**
- `OSError: [Errno 98] Address already in use`
- `Cannot bind to port 5000`

**Solutions:**
```bash
# Find process using port 5000
# Linux/macOS:
lsof -i :5000
# Windows:
netstat -ano | findstr :5000

# Kill the process
kill -9 PID  # Linux/macOS
taskkill /PID PID /F  # Windows

# Use a different port
# Edit config/config.yml:
# web.port: 5001
# Or set environment variable:
export PORT=5001
```

#### Issue 7: Docker Issues

**Symptoms:**
- `Cannot connect to the Docker daemon`
- `No such container`

**Solutions:**
```bash
# Start Docker daemon
# Linux:
sudo systemctl start docker
# macOS/Windows: Start Docker Desktop

# Rebuild Docker image
docker-compose -f docker/docker-compose.yml build --no-cache

# Check Docker logs
docker logs spam-detector-app

# Remove and recreate container
docker-compose -f docker/docker-compose.yml down
docker-compose -f docker/docker-compose.yml up -d
```

---

## 📈 Performance Optimization

### Configuration Tuning

Edit `config/config.yml` to optimize for your needs:

```yaml
# For FASTER predictions (sacrificing some accuracy)
features:
  max_features: 3000  # Reduce from 5000
  ngram_range: [1, 1]  # Only unigrams
  use_dimension_reduction: true
  n_components: 50

model:
  type: 'naive_bayes'  # Fastest model
  hyperparameter_tuning: false  # Skip tuning

# For BETTER accuracy (sacrificing speed)
features:
  max_features: 10000
  ngram_range: [1, 3]  # Unigrams, bigrams, trigrams
  use_dimension_reduction: false

model:
  type: 'svm'  # Best accuracy
  hyperparameter_tuning: true
  cv_folds: 5

# For BALANCED performance
features:
  max_features: 5000
  ngram_range: [1, 2]  # Unigrams and bigrams

model:
  type: 'logistic_regression'  # Good balance
  hyperparameter_tuning: true
```

### Hardware Recommendations

| Setup | Memory | CPU | Performance | Recommended For |
|-------|--------|-----|-------------|-----------------|
| **Minimal** | 2GB | 2 cores | ~100ms per prediction | Testing, personal use |
| **Recommended** | 4GB | 4 cores | ~50ms per prediction | Production, small teams |
| **Optimal** | 8GB+ | 8 cores+ | ~20ms per prediction | High volume, enterprise |

---

## 🔒 Security Best Practices

### Production Deployment

1. **Change secret key:**
   ```bash
   # Generate a random key
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   
   # Add to .env file
   echo "SECRET_KEY=your-very-secure-random-key-here" >> .env
   ```

2. **Use HTTPS:**
   ```bash
   # Configure SSL certificate
   # Option 1: Using Let's Encrypt
   # Option 2: Using a reverse proxy (Nginx/Apache)
   
   # Nginx example:
   # proxy_pass http://localhost:5000;
   ```

3. **Limit API access:**
   ```yaml
   # config/config.yml
   api:
     rate_limit: 100  # requests per hour
     allowed_origins: ['https://yourdomain.com']
   ```

4. **Regular updates:**
   ```bash
   # Update dependencies
   pip install --upgrade -r requirements.txt
   
   # Retrain model with new data
   python scripts/train_model.py
   ```

5. **Backup models:**
   ```bash
   # Create backup script
   mkdir -p models/backups
   cp models/spam_detector_model.pkl models/backups/model_$(date +%Y%m%d_%H%M%S).pkl
   ```

6. **Monitor logs:**
   ```bash
   # Check application logs
   tail -f logs/app.log
   
   # Check for suspicious activity
   grep -i "error\|warning\|attack" logs/app.log
   ```

### Data Privacy

- **Your emails** are processed locally on your machine
- **No data** is sent to external servers
- **History** is stored in your browser's session only
- **Model** runs completely offline (no internet required)

---

## 📚 Tutorials

### Tutorial 1: First-Time Setup (Step-by-Step)

**For Windows:**
```bash
# 1. Install Python from python.org
# 2. Open Command Prompt or PowerShell
# 3. Clone repository
git clone https://github.com/yourusername/spam-email-detector.git
cd spam-email-detector

# 4. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 5. Install dependencies
pip install -r requirements.txt

# 6. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# 7. Train model
python scripts\train_model.py

# 8. Start application
python web\app.py

# 9. Open browser
start http://localhost:5000
```

**For macOS/Linux:**
```bash
# 1. Install Python (if not installed)
# macOS: brew install python3
# Linux: sudo apt-get install python3 python3-pip

# 2. Clone repository
git clone https://github.com/yourusername/spam-email-detector.git
cd spam-email-detector

# 3. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# 6. Train model
python scripts/train_model.py

# 7. Start application
python web/app.py

# 8. Open browser
open http://localhost:5000
```

### Tutorial 2: Training Custom Model

```python
# custom_train.py
from src.data_loader import DataLoader
from src.preprocessor import TextPreprocessor
from src.feature_extractor import FeatureExtractor
from src.trainer import ModelTrainer
import pandas as pd

# 1. Load your data
# Your CSV should have columns: 'label' (spam/ham) and 'message'
df = pd.read_csv('my_spam_dataset.csv')
print(f"Loaded {len(df)} emails")

# 2. Initialize components
loader = DataLoader()
loader.df = df
loader.clean_data()

preprocessor = TextPreprocessor(
    use_stemming=True,
    remove_stopwords=True
)

# 3. Preprocess
df['processed'] = df['message'].apply(preprocessor.tokenize_and_stem)

# 4. Extract features
extractor = FeatureExtractor(
    max_features=5000,
    ngram_range=(1, 2)
)
X = extractor.fit_transform(df['processed'])
y = df['label']

print(f"Feature matrix shape: {X.shape}")

# 5. Train model
trainer = ModelTrainer(
    model_type='logistic_regression',
    random_state=42
)

trainer.train(X, y)

# 6. Evaluate
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

metrics = trainer.evaluate(X_test, y_test)
print("Evaluation Metrics:")
for metric, value in metrics.items():
    print(f"  {metric}: {value:.4f}")

# 7. Save model
trainer.save_model('models/custom_model.pkl')
extractor.save_vectorizer('models/custom_vectorizer.pkl')
print("Model saved successfully!")
```

### Tutorial 3: API Integration with Flask App

```python
# integrate_with_flask.py
from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)
SPAM_API_URL = "http://localhost:5000/predict"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_email', methods=['POST'])
def check_email():
    """Check if an email is spam using the API"""
    email_content = request.form.get('email', '')
    
    if not email_content:
        return jsonify({'error': 'No email provided'}), 400
    
    try:
        # Call spam detection API
        response = requests.post(
            SPAM_API_URL,
            json={'email': email_content},
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify({
                'prediction': result['prediction'],
                'confidence': result['confidence'],
                'message': f"Email classified as {result['prediction']} with {result['confidence']:.1%} confidence"
            })
        else:
            return jsonify({'error': 'API error'}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Connection error: {str(e)}'}), 500

@app.route('/batch_check', methods=['POST'])
def batch_check():
    """Check multiple emails"""
    emails = request.json.get('emails', [])
    
    if not emails:
        return jsonify({'error': 'No emails provided'}), 400
    
    try:
        response = requests.post(
            f"{SPAM_API_URL}/batch",
            json={'emails': emails},
            timeout=30
        )
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({'error': 'API error'}), 500
            
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Connection error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
```

---

## 📞 Support

### Where to Get Help

| Resource | Link/Contact |
|----------|--------------|
| **GitHub Issues** | https://github.com/yourusername/spam-email-detector/issues |
| **Documentation** | https://spamdetector.readthedocs.io |
| **Email Support** | support@spamdetector.com |
| **Community Forum** | https://community.spamdetector.com |

### Reporting Issues

When reporting issues, please include:

1. **Error message** (copy and paste the full error)
2. **Steps to reproduce** (detailed steps)
3. **System information:**
   ```bash
   python --version
   pip list | grep -E "(numpy|scikit-learn|flask)"
   cat /etc/os-release  # Linux
   # or
   sw_vers  # macOS
   # or
   systeminfo | findstr /B /C:"OS Name" /C:"OS Version"  # Windows
   ```

4. **Screenshots** (if applicable)
5. **Log files** from `logs/app.log`

### Asking Questions

For questions or help, please:
1. **Search existing issues** - Your question may have been answered
2. **Be specific** - Include error messages and system details
3. **Provide context** - What were you trying to do?
4. **Be patient** - We'll get back to you as soon as possible

---

## 📄 License

This project is open-source and available under the **MIT License**.

**You can:**
- ✅ Use it commercially
- ✅ Modify it
- ✅ Distribute it
- ✅ Use it privately

**You must:**
- Include the original copyright notice
- Include the license in your distribution
- Not hold the authors liable

See the [LICENSE](LICENSE) file for the full text.

---

## 🌟 Contributing

We welcome contributions! See our [Contributing Guide](CONTRIBUTING.md).

### Ways to Contribute

1. **Report bugs** - Create an issue
2. **Suggest features** - Open a discussion
3. **Improve documentation** - Submit a PR
4. **Add new features** - Fork and submit a PR
5. **Share your experience** - Write a blog post

### Development Setup

```bash
# Clone and install in development mode
git clone https://github.com/yourusername/spam-email-detector.git
cd spam-email-detector
pip install -e .

# Run tests
pytest tests/ -v

# Format code
black src/ web/ tests/

# Check style
pylint src/ web/

# Run linting
flake8 src/ web/
```

### Code Style Guidelines

- **Python:** Follow PEP 8
- **Formatting:** Use Black
- **Documentation:** Write docstrings
- **Testing:** Include unit tests
- **Commits:** Use semantic commit messages

---

## 📊 Changelog

### v1.0.0 (2024-01-01)
- Initial release
- Web interface
- API endpoints
- Multiple ML models (Naive Bayes, Logistic Regression, SVM, Random Forest)
- Docker support
- Complete documentation
- Unit tests

### v1.1.0 (Planned)
- WebSocket support for real-time predictions
- Authentication and API keys
- Swagger/OpenAPI documentation
- Usage statistics dashboard
- Model versioning
- Mobile app

---

## 🔗 Quick Links

- **Homepage:** http://localhost:5000
- **API Documentation:** http://localhost:5000/api/docs
- **Health Check:** http://localhost:5000/health
- **GitHub:** https://github.com/yourusername/spam-email-detector
- **Issue Tracker:** https://github.com/yourusername/spam-email-detector/issues

---

## 🙏 Acknowledgments

- [NLTK](https://www.nltk.org/) - Natural Language Toolkit
- [Scikit-learn](https://scikit-learn.org/) - Machine Learning library
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Kaggle](https://www.kaggle.com/) - Dataset source
- All contributors and users

---

**Thank you for using the Spam Email Detector!** 📧✨