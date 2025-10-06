#!/bin/bash
set -e
# Run all tests with project root as PYTHONPATH
# Tests are designed to run independently of any .env file

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
export PYTHONPATH="$PROJECT_ROOT"

# Ensure tests don't accidentally use any .env file
# All test environment is controlled via conftest.py
unset OPENAI_API_KEY EMAIL_FROM EMAIL_TO EMAIL_PASSWORD 2>/dev/null || true

echo "Running tests without .env file dependency..."
coverage run -m pytest -s tests
coverage report -m