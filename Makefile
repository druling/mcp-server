include .env
export

.PHONY: run dev lint test clean

# Start the app using your run.py (with settings from config.py)
run:
	PYTHONPATH=. python src/run.py

# Start the app directly with uvicorn, using reload for development
dev:
	PYTHONPATH=. uvicorn src.main:app --host 0.0.0.0 --port=${PORT} --reload

# Run linting with ruff or flake8
lint:
	ruff src

# Run tests using pytest
test:
	PYTHONPATH=. pytest tests/

# Remove __pycache__ and .pyc files
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -name "*.pyc" -delete
