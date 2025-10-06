# Pre-commit Setup for briefme

This document explains how to set up and use pre-commit hooks for the briefme project.

## Quick Setup

Run the setup script to install and configure everything:

```bash
./setup-pre-commit.sh
```

This will:
- Install pre-commit and related tools
- Install the pre-commit hooks in your git repository
- Run an initial check on all files

## Manual Setup

If you prefer to set up manually:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Test the setup
pre-commit run --all-files
```

## What the Pre-commit Hooks Do

The pre-commit configuration runs these checks on every commit:

### Code Quality
- **Black**: Formats Python code consistently (79 char line length)
- **isort**: Sorts and organizes imports
- **flake8**: Checks code style and potential issues

### General Checks
- **trailing-whitespace**: Removes trailing whitespace
- **end-of-file-fixer**: Ensures files end with a newline
- **check-yaml**: Validates YAML files
- **check-merge-conflict**: Detects merge conflict markers
- **debug-statements**: Finds leftover debug statements

### Testing
- **pytest**: Runs the test suite to ensure code changes don't break functionality

## Using Pre-commit

### Automatic (Recommended)
Pre-commit runs automatically on each commit. If any check fails, the commit is blocked until you fix the issues.

### Manual
Run pre-commit manually:

```bash
# Check all files
pre-commit run --all-files

# Check only staged files
pre-commit run

# Run a specific hook
pre-commit run black
pre-commit run flake8
pre-commit run pytest
```

### Skip Pre-commit (Use Sparingly)
If you need to commit without running pre-commit:

```bash
git commit --no-verify -m "Emergency fix"
```

## Using Make Commands

The project includes a Makefile with convenient commands:

```bash
# Run all CI checks (format-check, lint, test)
make ci

# Format code
make format

# Check code format without changing files
make format-check

# Run linting
make lint

# Run tests
make test

# Run tests with coverage
make test-cov

# Setup pre-commit
make setup-pre-commit
```

## CI/CD Integration

The same tools used in pre-commit are also configured for GitHub Actions CI/CD in `.github/workflows/ci.yml`. This ensures consistency between local development and CI environments.

## Configuration Files

- `.pre-commit-config.yaml`: Pre-commit hook configuration
- `pyproject.toml`: Tool configuration (black, isort, pytest, mypy)
- `requirements-dev.txt`: Development dependencies
- `Makefile`: Common development tasks

## Troubleshooting

### Pre-commit is slow
The first run is slower as it sets up virtual environments for each tool. Subsequent runs are much faster.

### Black and flake8 conflicts
The configuration is set up to avoid common conflicts (E203, W503 ignored in flake8).

### Tests failing in pre-commit
Ensure your `.env.tests` file is properly configured for test environment isolation.

### Skipping hooks temporarily
You can skip specific hooks:

```bash
SKIP=pytest git commit -m "WIP: work in progress"
```
