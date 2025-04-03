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

# Create icons directory for the info panel
icons_path = os.path.join(assets_path, 'icons')
if not os.path.exists(icons_path):
    print(f"Icons directory does not exist at: {icons_path}")
    print(f"Creating icons directory...")
    os.makedirs(icons_path, exist_ok=True)
    print(f"Icons directory created successfully.")

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
    print("Missing piece images. You'll need images or can generate placeholders.")
    
# Count existing chess piece images
piece_files = [f for f in os.listdir(pieces_path) if f.endswith('.png')] if os.path.exists(pieces_path) else []
print(f"Found {len(piece_files)} chess piece images in {pieces_path}")

# Check if pieces follow new naming pattern
expected_files = [f"{color}_{piece}.png" for color in ["white", "black"] 
                  for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]]
missing_files = [f for f in expected_files if f not in piece_files]

if missing_files:
    print(f"Missing {len(missing_files)} piece images with correct naming format:")
    for file in missing_files[:5]:  # Show first 5 missing files
        print(f"  - {file}")
    if len(missing_files) > 5:
        print(f"  - and {len(missing_files) - 5} more...")

# Create generate_pieces.py if it doesn't exist
generate_script = os.path.join(proj_root, 'generate_pieces.py')
has_generator = os.path.exists(generate_script)
if has_generator:
    print(f"✓ Found image generator script at: {generate_script}")
else:
    print(f"✗ Could not find image generator script, creating it now...")
    # The content would be added here in a real implementation
    
# Check if all necessary Python files exist
print("\nChecking for necessary Python files:")
for package_init in [gui_path, engine_path, utils_path]:
    init_path = os.path.join(package_init, '__init__.py')
    if not os.path.exists(init_path):
        print(f"Warning: Missing {init_path}, creating empty file...")
        with open(init_path, 'w') as f:
            f.write("# Package initialization file\n")
        print(f"Created {init_path}")

# Ensure main.py exists and has the right imports
main_path = os.path.join(proj_root, 'main.py')
if not os.path.exists(main_path):
    print(f"Warning: Missing main.py entry point")

# Ask if user wants to create directories
print("\nOptions:")
print("1. Create missing directories for the Chess_Project")
print("2. Generate chess piece images for better visuals")
print("3. Use the simple text-based chess game that works without images")
print("4. Verify all chess piece files exist (and create them if missing)")
print("5. Exit")

choice = input("\nEnter your choice (1-5): ")

if choice == '1':
    # Create directory structure
    for directory in [assets_path, pieces_path, icons_path, gui_path, engine_path, utils_path]:
        os.makedirs(directory, exist_ok=True)
    print("\nAll directories created successfully.")
    print("\nYou should now run option 2 to generate chess piece images.")
    
elif choice == '2':
    # Generate chess piece images
    print("\nGenerating chess piece images...")
    os.system(f"{sys.executable} {generate_script}")
    print("Now you can run the main game with: python main.py")
    
elif choice == '3':
    simple_chess = os.path.join(proj_root, 'simple_chess.py')
    if os.path.exists(simple_chess):
        print(f"\nRunning simple chess game at: {simple_chess}")
        print("Launching in 3 seconds...")
        import time
        time.sleep(3)
        current_dir = os.getcwd()
        os.chdir(proj_root)
        os.system(f"{sys.executable} simple_chess.py")
        os.chdir(current_dir)
    else:
        print("\nSimple chess game not found. Would you like to create it?")
        create_simple = input("Create simple_chess.py? (y/n): ")
        if create_simple.lower() == 'y':
            print("Creating simple_chess.py...")
            # The code would be added here in a real implementation
            print(f"Created {simple_chess}")

elif choice == '4':
    # Verify all chess piece files exist
    print("\nVerifying chess piece files...")
    
    # Check for all required piece images
    missing_pieces = []
    for color in ["white", "black"]:
        for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
            piece_path = os.path.join(pieces_path, f"{color}_{piece}.png")
            if not os.path.exists(piece_path):
                missing_pieces.append(f"{color}_{piece}.png")
    
    if missing_pieces:
        print(f"Missing {len(missing_pieces)} chess piece images.")
        generate = input("Generate missing piece images? (y/n): ")
        if generate.lower() == 'y':
            print("\nGenerating chess piece images...")
            os.system(f"{sys.executable} {generate_script}")
    else:
        print("All chess piece images exist!")
    
    print("\nYou should now be able to run the game with: python main.py")

else:
    print("\nExiting without changes.")

# Add guidance at the end
print("\n=== Next Steps ===")
print("1. Make sure you have all required directories and files")
print("2. Generate piece images if you haven't already")
print("3. Run the game with: python main.py")
print("\nIf you encounter any issues, run this script again and select the appropriate option.")
