"""
Main script to run the project
"""
import os
import sys

def check_python_version():
    """Verify Python version is compatible"""
    required_version = (3, 6)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"Error: This project requires Python {required_version[0]}.{required_version[1]} or higher")
        print(f"Your current Python version is {current_version[0]}.{current_version[1]}")
        return False
    return True

def print_environment_info():
    """Print environment information for debugging"""
    print("\n--- Environment Information ---")
    print(f"Python version: {sys.version}")
    print(f"Current directory: {os.getcwd()}")
    print(f"Python executable: {sys.executable}")
    print("--- End Environment Info ---\n")

def main():
    """Main function of the project"""
    if not check_python_version():
        return
    
    print_environment_info()
    
    try:
        # Import project-specific modules
        print("Importing required modules...")
        import numpy as np
        import pandas as pd
        import matplotlib.pyplot as plt
        
        print("All modules imported successfully!")
        
        # Add your project code here
        print("Starting project execution...")
        # Example: 
        # data = pd.read_csv('data/example.csv')
        # print(data.head())
        
        print("Project execution completed successfully!")
        
    except ImportError as e:
        print(f"Error importing modules: {e}")
        print("Please make sure all dependencies are installed by running:")
        print("pip install -r requirements.txt")
    except Exception as e:
        print(f"Error during execution: {e}")

if __name__ == "__main__":
    main()
