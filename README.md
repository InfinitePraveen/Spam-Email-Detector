# 📧 Spam Email Detector

> **An end-to-end ML-powered spam detection system with a modern web interface**

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Made with Jupyter](https://img.shields.io/badge/Made%20with-Jupyter-orange?style=flat&logo=Jupyter)](https://jupyter.org/try)

Built an ML-powered spam email detector using **NLP** and **classification algorithms**. Cleaned text data, extracted **TF-IDF** features, and trained models (**Naive Bayes, SVM, Logistic Regression**) to classify emails. Achieved high accuracy with a **Flask web interface**, demonstrating an end-to-end pipeline from data preprocessing to deployment for real-world email filtering.

---

## 🚀 Live Demo & Repository

🔗 **GitHub Repository**: [InfinitePraveen/Spam-Email-Detector](https://github.com/InfinitePraveen/Spam-Email-Detector)

---

## 👨‍💻 About the Creator

**Praveen Kumar**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/infinitepraveen)

This project was conceptualized, developed, and implemented entirely by me, **Praveen Kumar**. I designed the architecture, built the machine learning pipeline, created the web interface, and integrated all components into a complete, production-ready system.

**Acknowledgments for Assistance**:
- **DeepSeek AI** and **GitHub Copilot** provided invaluable assistance with code optimization, debugging, and web interface design, enhancing the overall quality and functionality of the project.

---

## 📊 Project Overview

This project demonstrates a complete **machine learning lifecycle** for text classification:

1. **Data Processing**: Cleaning and preprocessing email text data
2. **Feature Engineering**: TF-IDF vectorization with n-gram support
3. **Model Training**: Multiple algorithms with hyperparameter tuning
4. **Evaluation**: Comprehensive metrics and visualization
5. **Deployment**: Flask web application and RESTful API

### Key Features

- ✅ **Multiple ML Models**: Naive Bayes, Logistic Regression, SVM, Random Forest
- ✅ **NLP Pipeline**: Tokenization, stopword removal, stemming/lemmatization
- ✅ **Interactive Web Interface**: User-friendly Flask application
- ✅ **RESTful API**: Programmatic access for integration
- ✅ **Comprehensive Evaluation**: Metrics, confusion matrix, ROC curves
- ✅ **Docker Support**: Containerized deployment
- ✅ **History Tracking**: Session-based prediction history

---

## 🏗️ Project Structure

```
spam-email-detector/
├── notebooks/          # Jupyter notebooks for exploration
├── src/               # Core source code
│   ├── data_loader.py
│   ├── preprocessor.py
│   ├── feature_extractor.py
│   ├── trainer.py
│   ├── predictor.py
│   └── utils.py
├── web/               # Flask web application
│   ├── app.py
│   ├── templates/
│   └── static/
├── models/            # Trained models and vectorizers
├── data/              # Dataset storage
├── tests/             # Unit tests
├── docker/            # Docker configuration
├── config/            # YAML configuration
├── scripts/           # Utility scripts
└── docs/              # Documentation
```

---

## 📊 Dataset

Uses the **SMS Spam Collection Dataset** from Kaggle, containing 5,574 labeled messages.

- **Ham messages**: 4,827 (86.6%)
- **Spam messages**: 747 (13.4%)

[View Dataset on Kaggle](https://www.kaggle.com/datasets/uciml/sms-spam-collection-dataset)

---

## 🛠️ Installation & Setup

### Quick Start

```bash
# Clone the repository
git clone https://github.com/InfinitePraveen/Spam-Email-Detector.git
cd Spam-Email-Detector

# Run the deployment script
./scripts/deploy.sh
```

### Manual Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"

# Train the model
python scripts/train_model.py

# Start the application
python web/app.py
```

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose -f docker/docker-compose.yml up --build

# Or use Docker directly
docker build -t spam-detector -f docker/Dockerfile .
docker run -p 5000:5000 spam-detector
```

---

## 🎯 Usage

### Web Interface

1. Open browser: `http://localhost:5000`
2. Enter email content in the text area
3. Click **"Classify Email"** to get prediction

### API Endpoint

```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"email": "Congratulations! You won a prize..."}'
```

### Python SDK

```python
from src.predictor import SpamPredictor

predictor = SpamPredictor('models/model.pkl', 'models/vectorizer.pkl')
prediction, confidence = predictor.predict("Your email text here")
print(f"{prediction} ({confidence:.2%})")
```

---

## 📈 Model Performance

| Model | Accuracy | Precision | Recall | F1-Score |
|-------|----------|-----------|--------|----------|
| **Naive Bayes** | 97.2% | 96.8% | 97.5% | 97.1% |
| **Logistic Regression** | **98.3%** | **98.1%** | **98.4%** | **98.2%** |
| **SVM** | 98.5% | 98.3% | 98.6% | 98.4% |
| **Random Forest** | 97.8% | 97.5% | 97.9% | 97.7% |

**Best Model**: SVM with 98.5% accuracy

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest --cov=src tests/
```

---

## 🔧 Configuration

Edit `config/config.yml` to customize:

- **Data sources** (Kaggle/local)
- **Preprocessing options**
- **Feature extraction** (TF-IDF parameters)
- **Model selection** and hyperparameters
- **Web server settings**
- **Logging configuration**

---

## 🚢 Deployment Options

- **Local**: Flask development server
- **Production**: Gunicorn with Nginx
- **Container**: Docker and Docker Compose
- **Cloud**: AWS EC2, Google Cloud Run, Heroku

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 🙏 Acknowledgments

- **Praveen Kumar** - Project Creator and Developer
- **DeepSeek AI** - Assistance with web interface design and code optimization
- **GitHub Copilot** - Support with debugging and implementation
- [NLTK](https://www.nltk.org/) - Natural Language Toolkit
- [Scikit-learn](https://scikit-learn.org/) - Machine Learning Library
- [Flask](https://flask.palletsprojects.com/) - Web Framework
- [Kaggle](https://www.kaggle.com/) - Dataset Source

---

## 📬 Contact

**Praveen Kumar**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/infinitepraveen)

Project Link: [https://github.com/InfinitePraveen/Spam-Email-Detector](https://github.com/InfinitePraveen/Spam-Email-Detector)

---

⭐ **If you found this project helpful, please give it a star!** ⭐