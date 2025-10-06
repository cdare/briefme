#!/bin/bash
# Setup script for pre-commit hooks

set -e

echo "Setting up pre-commit hooks for briefme..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Error: Not in a git repository. Please run 'git init' first."
    exit 1
fi

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit..."
    pip install pre-commit
else
    echo "pre-commit is already installed"
fi

# Install additional development dependencies
echo "Installing development dependencies..."
pip install -r requirements-dev.txt

# Install the pre-commit hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Run pre-commit on all files to check setup
echo "Running pre-commit on all files to test setup..."
pre-commit run --all-files || true

echo ""
echo "✅ Pre-commit setup complete!"
echo ""
echo "Pre-commit will now run automatically on each commit to:"
echo "  • Format code with black"
echo "  • Check code style with flake8"
echo "  • Sort imports with isort"
echo "  • Run tests with pytest"
echo "  • Check for common issues (trailing whitespace, etc.)"
echo ""
echo "To run pre-commit manually: pre-commit run --all-files"
echo "To skip pre-commit for a commit: git commit --no-verify"
