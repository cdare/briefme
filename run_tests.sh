#!/bin/bash
# Run all tests with project root as PYTHONPATH

PROJECT_ROOT="$(cd "$(dirname "$0")"/.. && pwd)"
export PYTHONPATH="$PROJECT_ROOT"

python -m unittest discover -s tests -p 'test_*.py'
