#!/bin/bash
# Deployment script for Spam Email Detector

set -e  # Exit on error

echo "=========================================="
echo "SPAM EMAIL DETECTOR - DEPLOYMENT SCRIPT"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Check if running as root
if [ "$EUID" -eq 0 ]; then 
    print_warning "Running as root is not recommended"
fi

# 1. Check Python version
echo "Checking Python version..."
if command -v python3 &>/dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    print_status "Python version: $PYTHON_VERSION"
else
    print_error "Python3 is not installed"
    exit 1
fi

# 2. Create virtual environment
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# 3. Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# 4. Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
print_status "Dependencies installed"

# 5. Download NLTK data
echo "Downloading NLTK data..."
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
print_status "NLTK data downloaded"

# 6. Create directories
echo "Creating necessary directories..."
mkdir -p models data/raw logs evaluation
print_status "Directories created"

# 7. Check for model
echo "Checking for trained model..."
if [ ! -f "models/spam_detector_model.pkl" ]; then
    print_warning "Model not found. Training new model..."
    python scripts/train_model.py
    print_status "Model trained successfully"
else
    print_status "Model found: models/spam_detector_model.pkl"
fi

# 8. Run tests (optional)
if [ "$1" == "--test" ]; then
    echo "Running tests..."
    pytest tests/ -v
    print_status "Tests completed"
fi

# 9. Start the application
echo "Starting the application..."
if [ "$1" == "--docker" ]; then
    # Docker deployment
    echo "Deploying with Docker..."
    docker-compose -f docker/docker-compose.yml up -d
    print_status "Docker container started"
else
    # Local deployment
    echo "Starting Flask application..."
    export FLASK_APP=web/app.py
    export FLASK_ENV=production
    
    # Check if Gunicorn is installed
    if pip show gunicorn &>/dev/null; then
        echo "Starting with Gunicorn..."
        gunicorn --bind 0.0.0.0:5000 --workers 4 --timeout 120 web.app:app &
        print_status "Gunicorn started on port 5000"
    else
        echo "Starting with Flask (development mode)..."
        python web/app.py &
        print_status "Flask started on port 5000"
    fi
fi

echo "=========================================="
print_status "Deployment complete!"
echo ""
echo "Application URL: http://localhost:5000"
echo "API Endpoint:    http://localhost:5000/predict"
echo "Health Check:    http://localhost:5000/health"
echo ""
echo "To stop the application:"
echo "  - For Flask: Ctrl+C"
echo "  - For Gunicorn: pkill gunicorn"
echo "  - For Docker: docker-compose -f docker/docker-compose.yml down"
echo "=========================================="