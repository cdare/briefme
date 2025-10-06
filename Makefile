.PHONY: help install install-dev test lint format clean setup-pre-commit run

# Default target
help:
	@echo "Available commands:"
	@echo "  install         Install production dependencies"
	@echo "  install-dev     Install development dependencies"
	@echo "  test            Run tests"
	@echo "  lint            Run linting (flake8)"
	@echo "  format          Format code (black + isort)"
	@echo "  clean           Clean cache and build files"
	@echo "  setup-pre-commit Setup pre-commit hooks"
	@echo "  run             Run the briefme application"
	@echo "  ci              Run all CI checks (format, lint, test)"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt -r requirements-dev.txt

test:
	coverage run -m pytest -s tests

lint:
	flake8 briefme/ tests/
	@echo "✅ Linting passed"

format:
	black briefme/ tests/
	isort briefme/ tests/
	@echo "✅ Code formatted"

format-check:
	black --check briefme/ tests/
	isort --check-only briefme/ tests/
	@echo "✅ Code format is correct"

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/

setup-pre-commit:
	./setup-pre-commit.sh

run:
	python -m briefme.main

# Run all CI checks
ci: format-check lint test
	@echo "✅ All CI checks passed"

# Run pre-commit on all files
pre-commit:
	pre-commit run --all-files
