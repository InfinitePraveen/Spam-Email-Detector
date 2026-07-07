# 📧 Spam Email Detector

A lightweight spam email detector built with Python, scikit-learn, Flask, and NLP preprocessing. The project includes a training pipeline, evaluation scripts, unit tests, and a web app for classifying email text.

## Project Structure

```text
Spam-Email-Detector/
├── config/                # Model and app configuration
├── data/                  # Raw and processed datasets
├── docs/                  # Project documentation
├── models/                # Trained model and vectorizer files
├── notebooks/             # Exploratory Jupyter notebooks
├── scripts/               # Training and evaluation scripts
│   ├── _train_model.py
│   └── _evaluate_model.py
├── src/                   # Core Python modules
│   ├── _data_loader.py
│   ├── _feature_extractor.py
│   ├── _predictor.py
│   ├── _preprocessor.py
│   ├── _trainer.py
│   └── _utils.py
├── tests/                 # Unit tests
├── web/                   # Flask web app
│   ├── app.py
│   ├── static/
│   └── templates/
├── requirements.txt
├── Makefile
└── README.md
```

## Requirements

- Python 3.10+
- pip

## Setup

```bash
git clone https://github.com/InfinitePraveen/Spam-Email-Detector.git
cd Spam-Email-Detector
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

You can also use the Makefile helpers:

```bash
make install
```

## Train the Model

```bash
python scripts/_train_model.py --config config/config.yml
```

This trains the model and saves the artifacts to the paths defined in the configuration file.

## Evaluate the Model

```bash
python scripts/_evaluate_model.py --config config/config.yml --output evaluation
```

This generates evaluation metrics and charts in the `evaluation/` folder.

## Run the Tests

```bash
pytest -q tests/_test_preprocessor.py tests/_test_model.py tests/_test_predictor.py
```

Or run the full suite with:

```bash
pytest -q
```

## Open the Web App

Start the Flask app:

```bash
python web/app.py
```

Then open your browser at:

```text
http://127.0.0.1:5000
```

You can also use:

```bash
make run
```

## API Usage

The web app exposes a prediction endpoint:

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"email": "Congratulations! You won a prize! Click here to claim it."}'
```

## Docker (Optional)

```bash
docker-compose -f docker/docker-compose.yml up --build
```

## Notes

- The web app uses the trained model and vectorizer from the configured model paths.
- If the model files are missing, the app will run in a limited/demo mode until training is completed.
