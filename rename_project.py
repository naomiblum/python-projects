#!/usr/bin/env python3
import os
import sys
import shutil

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    clear_screen()
    print("=================================")
    print("      PROJECT RENAME TOOL        ")
    print("=================================")
    print()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current directory: {current_dir}")
    
    # Check if Chess_Project exists
    old_name = 'Chess_Project'
    old_path = os.path.join(current_dir, old_name)
    
    if not os.path.exists(old_path):
        print(f"\nError: {old_name} directory not found at {old_path}")
        return
    
    print(f"\nFound project directory: {old_path}")
    
    # Ask for new name
    new_name = input("\nEnter new name for the project (e.g., Chess_Game): ")
    if not new_name:
        print("No name entered. Exiting.")
        return
    
    # Clean up the name
    new_name = new_name.strip().replace(' ', '_')
    new_path = os.path.join(current_dir, new_name)
    
    # Check if destination already exists
    if os.path.exists(new_path):
        print(f"\nError: {new_path} already exists!")
        overwrite = input("Do you want to remove it first? (y/n): ")
        if overwrite.lower() == 'y':
            print(f"Removing {new_path}...")
            try:
                shutil.rmtree(new_path)
            except Exception as e:
                print(f"Error removing directory: {e}")
                return
        else:
            print("Operation cancelled.")
            return
    
    # Confirm the action
    print(f"\nReady to rename: {old_path} → {new_path}")
    confirm = input("Proceed? (y/n): ")
    
    if confirm.lower() != 'y':
        print("Operation cancelled.")
        return
    
    # Perform the rename
    try:
        print(f"Renaming {old_name} to {new_name}...")
        shutil.move(old_path, new_path)
        print("\nDirectory renamed successfully!")
        
        # Additional steps - update code references if needed
        print("\nYou may need to update any code that references the old project name.")
        print("Don't forget to update any import statements in your Python files.")
        
        # Offer to run the check_structure script to verify
        check_structure = os.path.join(new_path, 'check_structure.py')
        if os.path.exists(check_structure):
            run_check = input("\nRun check_structure.py to verify the new project? (y/n): ")
            if run_check.lower() == 'y':
                print(f"\nRunning {check_structure}...")
                import time
                time.sleep(1)
                
                # Determine Python executable
                venv_python = os.path.join(new_path, 'myenv', 'bin', 'python')
                python_exec = venv_python if os.path.exists(venv_python) else sys.executable
                
                current_dir = os.getcwd()
                os.chdir(new_path)
                os.system(f"{python_exec} check_structure.py")
                os.chdir(current_dir)
        
    except Exception as e:
        print(f"Error during rename: {e}")
    
    print("\nDone.")

if __name__ == "__main__":
    main()
