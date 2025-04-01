# Chess Game (Pygame)

A turn-based chess game built with Python and Pygame.  
Designed to reinforce object-oriented programming, modular design, and interactive GUIs.

---

## Features

- Full 8×8 chessboard with GUI
- Legal move validation for all pieces
- Turn management (white and black)
- Visual highlighting of selected piece and legal moves
- Piece animations when moved
- Auto-promotion to queen for pawns
- Clean modular structure (GUI & logic separation)

---

## Technologies Used

- **Python 3.13+**
- **Pygame** – for rendering the board and handling events
- **OOP** – each piece is a class; the board and game logic are encapsulated

---

## Project Structure

Chess_Project/
├── main.py                # Game entry point
├── gui/
│   ├── board_view.py      # Handles drawing the board, pieces, and animations
│   ├── images.py          # Loads and scales chess piece images
│   └── init.py
├── engine/
│   ├── game_manager.py    # Manages turns, moves, check, and piece interactions
│   └── init.py
├── assets/
│   └── pieces/            # PNG images of all chess pieces


---

## Topics Covered

- Object-Oriented Programming
- Pygame and GUI design
- Event handling and game loops
- 2D grid logic and coordinate mapping
- Modular project architecture
- Animation with frame-based control
- Asset management (loading images)

---

## How to Run

Make sure you have Python and Pygame installed:

```bash
# Create virtual environment (optional but recommended)
python3 -m venv .venv
source .venv/bin/activate

# Install Pygame
pip install pygame

# Run the game
cd Chess_Project
python main.py