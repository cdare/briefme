#!/bin/bash
set -e
# Run all tests with project root as PYTHONPATH

PROJECT_ROOT="$(cd "$(dirname "$0")"/.. && pwd)"
export PYTHONPATH="$PROJECT_ROOT"

coverage run -m pytest -s tests
coverage report -m