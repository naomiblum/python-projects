import os
import sys
import shutil

# Print working directory
print(f"Current working directory: {os.getcwd()}")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")
print(f"Script location: {os.path.abspath(__file__)}")

# Check parent project directory
proj_root = os.path.dirname(os.path.abspath(__file__))
print(f"\nProject root detected as: {proj_root}")

# Check if assets directory exists
assets_path = os.path.join(proj_root, 'assets')
if os.path.exists(assets_path):
    print(f"Assets directory exists at: {assets_path}")
else:
    print(f"Assets directory DOES NOT exist at: {assets_path}")
    print(f"Creating assets directory...")
    os.makedirs(assets_path, exist_ok=True)
    print(f"Assets directory created successfully.")
    
# Check if pieces directory exists
pieces_path = os.path.join(assets_path, 'pieces')
if os.path.exists(pieces_path):
    print(f"Pieces directory exists at: {pieces_path}")
else:
    print(f"Pieces directory DOES NOT exist at: {pieces_path}")
    print(f"Creating pieces directory...")
    os.makedirs(pieces_path, exist_ok=True)
    print(f"Pieces directory created successfully.")

# Check for other necessary directories
gui_path = os.path.join(proj_root, 'gui')
if not os.path.exists(gui_path):
    print(f"GUI directory does not exist at: {gui_path}")
    print(f"Creating GUI directory...")
    os.makedirs(gui_path, exist_ok=True)
    print(f"GUI directory created successfully.")

engine_path = os.path.join(proj_root, 'engine')
if not os.path.exists(engine_path):
    print(f"Engine directory does not exist at: {engine_path}")
    print(f"Creating engine directory...")
    os.makedirs(engine_path, exist_ok=True)
    print(f"Engine directory created successfully.")

utils_path = os.path.join(proj_root, 'utils')
if not os.path.exists(utils_path):
    print(f"Utils directory does not exist at: {utils_path}")
    print(f"Creating utils directory...")
    os.makedirs(utils_path, exist_ok=True)
    print(f"Utils directory created successfully.")

# Check for the specific file that's missing
pawn_path = os.path.join(pieces_path, 'white_pawn.png')
if os.path.exists(pawn_path):
    print(f"white_pawn.png exists at: {pawn_path}")
else:
    print(f"white_pawn.png DOES NOT exist at: {pawn_path}")
    print("Note: Missing piece images will be replaced with placeholder graphics.")
    
# Check if all necessary Python files exist
print("\nChecking for necessary Python files:")
board_view_path = os.path.join(gui_path, 'board_view.py')
if not os.path.exists(board_view_path):
    print(f"Warning: Missing {board_view_path}")

for engine_file in ['board.py', 'game_manager.py', 'piece.py']:
    file_path = os.path.join(engine_path, engine_file)
    if not os.path.exists(file_path):
        print(f"Warning: Missing {file_path}")

for package_init in [gui_path, engine_path, utils_path]:
    init_path = os.path.join(package_init, '__init__.py')
    if not os.path.exists(init_path):
        print(f"Warning: Missing {init_path}, creating empty file...")
        with open(init_path, 'w') as f:
            f.write("# Package initialization file\n")
        print(f"Created {init_path}")

# Check if alternative chess games are available
print("\nChecking for alternative chess games:")
simple_chess = os.path.join(proj_root, 'simple_chess.py')
chess_game = os.path.join(proj_root, 'chess_game.py')

if os.path.exists(simple_chess):
    print(f"✓ Found {simple_chess}")
    print("  This version doesn't require image files and should work immediately.")
else:
    print(f"✗ Could not find {simple_chess}")

if os.path.exists(chess_game):
    print(f"✓ Found {chess_game}")
    print("  This version doesn't require image files and should work immediately.")
else:
    print(f"✗ Could not find {chess_game}")

print("\nDirectory setup complete. You can now run the chess game.")
print("Commands to run:")
print(f"  cd {proj_root}")
print("  python simple_chess.py   # For text-based version")
print("  python main.py           # For graphical version with placeholders")
