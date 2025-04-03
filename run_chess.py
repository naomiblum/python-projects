#!/usr/bin/env python3
"""
Simple script to run a Chess Project by directory name.
Automatically finds the correct Python interpreter and runs main.py
"""
import os
import sys
import subprocess
import argparse
import shutil

def find_python_in_venv(project_dir):
    """Find Python interpreter in a virtual environment if it exists"""
    venv_path = os.path.join(project_dir, 'myenv')
    if os.path.exists(venv_path):
        if os.name == 'nt':  # Windows
            python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
        else:  # Unix/Mac
            python_path = os.path.join(venv_path, 'bin', 'python')
            
        if os.path.exists(python_path):
            return python_path
    
    return sys.executable  # Default to system Python

def create_minimal_assets(project_path):
    """Create minimal assets structure to avoid errors"""
    assets_path = os.path.join(project_path, "assets")
    pieces_path = os.path.join(assets_path, "pieces")
    
    # Create directories
    os.makedirs(pieces_path, exist_ok=True)
    
    # Check if there are any PNG files already
    has_png = False
    if os.path.exists(pieces_path):
        for file in os.listdir(pieces_path):
            if file.endswith('.png'):
                has_png = True
                break
    
    # If no PNG files, create minimal placeholder file
    if not has_png:
        # Create a simple 1x1 white pixel PNG
        try:
            from PIL import Image
            for color in ["white", "black"]:
                for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
                    img = Image.new('RGBA', (100, 100), (255, 255, 255, 0))
                    # Add a colored square
                    for x in range(20, 80):
                        for y in range(20, 80):
                            img.putpixel((x, y), (255, 255, 255, 255) if color == "white" else (0, 0, 0, 255))
                    # Save the file
                    img.save(os.path.join(pieces_path, f"{color}_{piece}.png"))
            print(f"Created placeholder piece images in {pieces_path}")
        except ImportError:
            print("Warning: PIL/Pillow not installed, cannot create placeholder images")
            # Create empty files instead
            for color in ["white", "black"]:
                for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
                    with open(os.path.join(pieces_path, f"{color}_{piece}.png"), 'w') as f:
                        f.write("")
            print(f"Created empty placeholder files in {pieces_path}")
    
    return True

def check_project_structure(project_path):
    """Check if project structure is correct and assets exist"""
    # Check for main.py
    main_path = os.path.join(project_path, 'main.py')
    if not os.path.exists(main_path):
        print(f"Error: main.py not found in {project_path}")
        # Check if it's in a subdirectory
        for root, dirs, files in os.walk(project_path):
            if 'main.py' in files:
                relative_path = os.path.relpath(root, project_path)
                print(f"Found main.py in subdirectory: {relative_path}")
                print(f"Full path: {os.path.join(root, 'main.py')}")
                print("Suggestion: Try running that directory instead")
                return False
        return False
    
    # Check for assets directory
    assets_path = os.path.join(project_path, 'assets')
    if not os.path.exists(assets_path):
        print(f"Warning: assets directory not found in {project_path}")
        print("Creating assets directory structure...")
        create_minimal_assets(project_path)
    
    # Check for assets/pieces directory
    pieces_path = os.path.join(assets_path, 'pieces')
    if not os.path.exists(pieces_path):
        print(f"Warning: pieces directory not found in {assets_path}")
        print("Creating pieces directory...")
        create_minimal_assets(project_path)
    
    return True

def run_project(project_name=None):
    """Run a chess project by name"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # If no project name given, use default
    if not project_name:
        # Try to find any Chess-related directories
        chess_dirs = []
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path) and ('chess' in item.lower() or 'שחמט' in item):
                # Check if it has a main.py
                if os.path.exists(os.path.join(item_path, 'main.py')):
                    chess_dirs.append(item)
        
        if chess_dirs:
            if len(chess_dirs) == 1:
                project_name = chess_dirs[0]
                print(f"Automatically selected project: {project_name}")
            else:
                print("Found multiple chess projects:")
                for i, name in enumerate(chess_dirs, 1):
                    print(f"{i}. {name}")
                choice = input("Select a project (number): ")
                try:
                    idx = int(choice) - 1
                    if 0 <= idx < len(chess_dirs):
                        project_name = chess_dirs[idx]
                    else:
                        print("Invalid selection")
                        return False
                except ValueError:
                    print("Invalid input")
                    return False
        else:
            # Fall back to the default list
            possible_dirs = ['Chess_Project', 'Chess_Game', 'ChessGame']
            for d in possible_dirs:
                if os.path.exists(os.path.join(current_dir, d)):
                    project_name = d
                    break
            
        if not project_name:
            print("Error: No chess project directory found")
            return False
    
    # Check that project exists
    project_path = os.path.join(current_dir, project_name)
    if not os.path.exists(project_path):
        print(f"Error: Project '{project_name}' not found in {current_dir}")
        return False
    
    # Validate project structure
    print(f"Checking project structure for {project_name}...")
    if not check_project_structure(project_path):
        return False
    
    # Find Python executable
    python_exec = find_python_in_venv(project_path)
    print(f"Using Python: {python_exec}")
    print(f"Running: {project_name}/main.py")
    
    # Install required packages if not present
    try:
        subprocess.run([python_exec, '-c', 'import pygame'], stderr=subprocess.DEVNULL)
    except:
        print("Installing required package: pygame")
        subprocess.run([python_exec, '-m', 'pip', 'install', 'pygame'])
    
    # Run the project
    try:
        old_dir = os.getcwd()
        os.chdir(project_path)
        print(f"Changed working directory to: {project_path}")
        print("Starting main.py...")
        result = subprocess.run([python_exec, 'main.py'])
        os.chdir(old_dir)
        
        if result.returncode != 0:
            print(f"\nError: The program exited with code {result.returncode}")
            print("This means there was an error during execution.")
            print("\nTrying to run check_structure.py to diagnose issues...")
            check_path = os.path.join(project_path, 'check_structure.py')
            if os.path.exists(check_path):
                os.chdir(project_path)
                subprocess.run([python_exec, 'check_structure.py'])
                os.chdir(old_dir)
            
        return result.returncode == 0
    except Exception as e:
        print(f"Error running project: {e}")
        return False

def run_simple_chess_directly():
    """Run the simple text-based chess game directly"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    simple_chess = os.path.join(current_dir, 'simple_chess.py')
    chess_game = os.path.join(current_dir, 'chess_game.py')
    
    python_exec = sys.executable
    
    # If simple_chess.py exists, run it
    if os.path.exists(simple_chess):
        print(f"Running simple text chess game: {simple_chess}")
        subprocess.run([python_exec, simple_chess])
        return True
    # Otherwise try chess_game.py
    elif os.path.exists(chess_game):
        print(f"Running chess game: {chess_game}")
        subprocess.run([python_exec, chess_game])
        return True
    else:
        print("Error: Could not find a chess game to run")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a Chess Project by directory name')
    parser.add_argument('project', nargs='?', help='Project directory name (default: autodetect)')
    parser.add_argument('--create-assets', action='store_true', help='Create missing assets directories')
    parser.add_argument('--list', action='store_true', help='List available chess projects')
    parser.add_argument('--simple', action='store_true', help='Run simple text-based chess game directly')
    args = parser.parse_args()
    
    # Run simple chess game if requested
    if args.simple:
        run_simple_chess_directly()
        sys.exit(0)
    
    # List all chess-related directories if requested
    if args.list:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        print("Available chess projects:")
        found = False
        
        for item in os.listdir(current_dir):
            item_path = os.path.join(current_dir, item)
            if os.path.isdir(item_path) and ('chess' in item.lower() or 'שחמט' in item):
                has_main = os.path.exists(os.path.join(item_path, 'main.py'))
                found = True
                status = "[OK]" if has_main else "[No main.py]"
                print(f"  {item} {status}")
        
        if not found:
            print("  No chess projects found")
        sys.exit(0)
    
    # If --create-assets flag is provided, create assets before running
    if args.create_assets and args.project:
        project_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.project)
        if os.path.exists(project_path):
            create_minimal_assets(project_path)
    
    run_project(args.project)
