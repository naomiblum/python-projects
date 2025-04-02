#!/bin/bash
# Simple setup script for the project

echo "=== Setting up Python Project ==="

# Navigate to project directory
cd "$(dirname "$0")"
echo "Current directory: $(pwd)"

# Make scripts executable
chmod +x run_project.py
echo "Made run_project.py executable"

# Create necessary directories
mkdir -p data logs output
echo "Created necessary directories"

# Check Python version
python_version=$(python --version 2>&1)
echo "Detected: $python_version"

# Check if pip is available
if command -v pip &>/dev/null; then
    echo "Installing dependencies..."
    pip install --user -r requirements.txt
    echo "Dependencies installed"
else
    echo "pip not found. Please install pip first."
fi

echo "=== Setup complete ==="
echo "To run the project: ./run_project.py or python run_project.py"
