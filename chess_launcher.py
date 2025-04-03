#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import argparse

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def find_python_executable(game_path):
    """Find the appropriate Python executable to use."""
    # First check if there's a virtual environment in the game directory
    game_dir = os.path.dirname(game_path)
    venv_path = os.path.join(game_dir, 'myenv')
    
    if os.path.exists(venv_path):
        venv_python = os.path.join(venv_path, 'bin', 'python')
        if os.path.exists(venv_python):
            print(f"Using virtual environment Python: {venv_python}")
            return venv_python
            
    # If no virtual environment, use the system Python
    print(f"Using system Python: {sys.executable}")
    return sys.executable

def run_project_by_name(project_name):
    """Run a project directly by its directory name"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_path = os.path.join(current_dir, project_name)
    
    if not os.path.exists(project_path):
        print(f"Error: Project directory '{project_name}' not found")
        return False
        
    # Check for main.py in the project directory
    main_path = os.path.join(project_path, 'main.py')
    if not os.path.exists(main_path):
        print(f"Error: main.py not found in {project_path}")
        return False
        
    # Find Python executable to use
    python_exec = find_python_executable(main_path)
    
    # Run the main.py file
    print(f"Running {project_name}/main.py...")
    
    try:
        # Change to project directory
        old_dir = os.getcwd()
        os.chdir(project_path)
        
        # Run the project
        subprocess.run([python_exec, 'main.py'])
        
        # Return to original directory
        os.chdir(old_dir)
        return True
    except Exception as e:
        print(f"Error running project: {e}")
        return False

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Chess Game Launcher')
    parser.add_argument('project', nargs='?', help='Project directory name to run directly')
    args = parser.parse_args()
    
    # If a project name is provided, run it directly
    if args.project:
        run_project_by_name(args.project)
        return

    # Otherwise, show the interactive menu
    clear_screen()
    print("==================================")
    print("       CHESS GAME LAUNCHER        ")
    print("==================================")
    print()
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Current directory: {current_dir}")
    
    # Find available chess games
    available_games = []
    
    # Look for possible project names (current and suggested new names)
    possible_project_dirs = ['Chess_Project', 'Chess_Game', 'ChessGame']
    
    for project_dir in possible_project_dirs:
        project_path = os.path.join(current_dir, project_dir)
        if os.path.exists(project_path):
            main_py = os.path.join(project_path, 'main.py')
            if os.path.exists(main_py):
                available_games.append((f"{project_dir} Main", main_py))
            
            check_structure = os.path.join(project_path, 'check_structure.py')
            if os.path.exists(check_structure):
                available_games.append((f"Check {project_dir} Structure", check_structure))
    
    # Add standalone games
    simple_chess = os.path.join(current_dir, 'simple_chess.py')
    if os.path.exists(simple_chess):
        available_games.append(("Simple Text Chess", simple_chess))
    
    chess_game = os.path.join(current_dir, 'chess_game.py')
    if os.path.exists(chess_game):
        available_games.append(("Standard Chess Game", chess_game))
    
    # Add project renaming tool
    rename_script = os.path.join(current_dir, 'rename_project.py')
    if os.path.exists(rename_script):
        available_games.append(("Rename Project Tool", rename_script))
    
    # Display available games
    if available_games:
        print("\nAvailable chess games:")
        for i, (name, path) in enumerate(available_games, 1):
            print(f"{i}. {name} ({path})")
    else:
        print("\nNo chess games found!")
        return
    
    # Display direct run information
    print("\nTip: You can run a project directly by its folder name:")
    print("    python chess_launcher.py Chess_Project")
    
    # Get user choice
    choice = input("\nEnter your choice (number) or 'q' to quit: ")
    if choice.lower() == 'q':
        return
    
    try:
        choice = int(choice)
        if 1 <= choice <= len(available_games):
            game_name, game_path = available_games[choice-1]
            
            print(f"\nLaunching {game_name}...")
            print(f"Path: {game_path}")
            
            # Find appropriate Python executable
            python_executable = find_python_executable(game_path)
            
            # Run the selected game
            game_dir = os.path.dirname(game_path)
            os.chdir(game_dir)
            
            print("\nStarting in 3 seconds...")
            import time
            time.sleep(3)
            
            subprocess.run([python_executable, game_path])
        else:
            print("\nInvalid choice. Please try again.")
    except ValueError:
        print("\nInvalid input. Please enter a number.")

if __name__ == "__main__":
    main()
