# Troubleshooting Guide

## Quick Start
If you're having problems, try these commands in order:
```bash
# Make sure you're in the project directory
cd /Users/naomiblum/Documents/GitHub/python-projects

# Make the run script executable
chmod +x run_project.py

# Install dependencies with pip
pip install --user -r requirements.txt

# Run the project
python run_project.py
```

## Common Issues and Solutions

### 1. ImportError or ModuleNotFoundError
If you see an error like "No module named X":
```bash
# Try with the --user flag
pip install --user -r requirements.txt

# If using Anaconda:
conda install numpy pandas matplotlib scikit-learn
```

### 2. Permission Errors
If you encounter permission errors:
```bash
# Make the script executable
chmod +x run_project.py

# Or run with Python directly
python run_project.py
```

### 3. Python Version Compatibility
This project requires Python 3.6 or higher. Check your version:
```bash
python --version

# If you have multiple Python versions, try:
python3 --version
```

If needed, specify Python 3 explicitly:
```bash
python3 run_project.py
```

### 4. Data File Not Found
Make sure all data files are in the correct location:
```bash
# Create necessary directories
mkdir -p data logs output
```

### 5. Path Issues
If the script can't find modules in the same project:
```bash
# Set the PYTHONPATH environment variable
export PYTHONPATH=$PYTHONPATH:/Users/naomiblum/Documents/GitHub/python-projects
```

### 6. Virtual Environment
Consider using a virtual environment:
```bash
# Create virtual environment
python -m venv venv

# Activate it (on macOS/Linux)
source venv/bin/activate

# Activate it (on Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 7. Debugging
For detailed debugging output:
```bash
# Run with verbose output
python -v run_project.py
```

## Getting Help
If you continue to experience issues:
1. Check the exact error message
2. Look for error messages in logs/error.log (if available)
3. Try running the main.py file directly: `python main.py`
4. Contact the project maintainer with specific error details
