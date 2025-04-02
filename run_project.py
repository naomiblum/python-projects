#!/usr/bin/env python3
"""
Script to run the project with proper error handling
"""
import sys
import os
import subprocess
import platform

def check_system():
    """Check system information for troubleshooting"""
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python Version: {platform.python_version()}")
    print(f"Current Directory: {os.getcwd()}")
    
    # Check if we're in a virtual environment
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print(f"Running in virtual environment: {in_venv}")
    
    return True

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        print("Installing required packages...")
        # Use --user flag if not in a virtual environment
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--user', '-r', 'requirements.txt'])
        print("All dependencies are installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        print("Trying alternative installation method...")
        try:
            # Try without --user flag
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
            print("All dependencies are installed successfully.")
            return True
        except subprocess.CalledProcessError as e2:
            print(f"Failed to install dependencies: {e2}")
            print("Please install them manually with: pip install -r requirements.txt")
            return False

def setup_environment():
    """Setup any environment variables or configurations needed"""
    # Make sure the project directory is in the Python path
    project_dir = os.getcwd()
    if project_dir not in sys.path:
        sys.path.insert(0, project_dir)
    
    # Create any necessary directories
    for directory in ['data', 'logs', 'output']:
        os.makedirs(directory, exist_ok=True)

def run_main_script():
    """Run the main script of your project"""
    try:
        main_script = 'main.py'
        if os.path.exists(main_script):
            print(f"Running {main_script}...")
            result = subprocess.run([sys.executable, main_script], 
                                  capture_output=True, 
                                  text=True,
                                  check=False)
            print(result.stdout)
            if result.returncode != 0:
                print(f"Error output: {result.stderr}")
                print(f"Process returned with error code {result.returncode}")
        else:
            print(f"Error: {main_script} not found in {os.getcwd()}")
            print("Available Python files:")
            python_files = [f for f in os.listdir('.') if f.endswith('.py')]
            for file in python_files:
                print(f"- {file}")
    except Exception as e:
        print(f"Error running the main script: {e}")

if __name__ == "__main__":
    print("\n=== Starting project setup ===\n")
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    print(f"Changed working directory to: {project_dir}")
    
    if check_system() and check_dependencies():
        setup_environment()
        run_main_script()
    
    print("\n=== Project execution completed ===\n")
