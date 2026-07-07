# Makefile

.PHONY: help install run test clean docker-build docker-run

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make run          - Run Flask application"
	@echo "  make test         - Run tests"
	@echo "  make clean        - Clean temporary files"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"

install:
	pip install -r requirements.txt
	python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

run:
	python web/app.py

test:
	pytest tests/ -v --cov=src --cov-report=html

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".coverage" -delete
	rm -rf htmlcov/
	rm -rf dist/
	rm -rf build/
	rm -rf *.egg-info/

docker-build:
	docker-compose -f docker/docker-compose.yml build

docker-run:
	docker-compose -f docker/docker-compose.yml up

docker-stop:
	docker-compose -f docker/docker-compose.yml down

format:
	black src/ web/ tests/

lint:
	pylint src/ web/ --fail-under=8