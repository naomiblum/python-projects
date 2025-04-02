## Chess Game in Python

A fully functional chess game with real-time UI, legal move logic, smooth animations, info panel, and an AI opponent — all built from scratch using Python and Pygame.

---

## Features

- Full implementation of chess rules: piece movement, turn logic, check, and checkmate
- Object-oriented design with clean code structure
- Sidebar info panel showing selected piece details
- Highlighting of legal moves and check states
- Smooth animation on piece movement
- Undo functionality
- AI opponent (random and greedy mode)

---

## Technologies Used

- Python 3.10
- Pygame
- Object-Oriented Programming
- Basic AI Algorithms (Random / Greedy move selection)

---

## System Architecture

```text
project-root/
│
├── main.py                      # Main game loop and event handling
│
├── engine/                      # Core logic and game mechanics
│   ├── game_manager.py          # Manages turns, game state, AI logic
│   ├── board.py                 # Board representation and operations
│   └── piece.py                 # ChessPiece class and valid move logic
│
├── gui/                         # User Interface rendering and interaction
│   ├── board_view.py            # Drawing the board, pieces, UI elements
│   ├── animate_move.py          # Smooth movement animations
│   └── graphics_utils.py        # Sidebar info panel, icons, visuals
│
├── assets/                      # Visual resources
│   ├── pieces/                  # PNGs of chess pieces
│   └── icons/                   # Sidebar icons for each piece type
│
└── README.md                    # Project documentation
```

---

## Theoretical Concepts

- **Object-Oriented Architecture** — separation of concerns (board, piece, logic, GUI)
- **State Modeling** — each board state is validatable and reversible
- **Legal Move Generation** — move filtering based on game state (avoiding check)
- **AI Decision-Making** — implemented random and greedy bots based on material gain
- **UX Principles** — real-time feedback, animations, clear info presentation

---

## How to Run

1. Clone the repo:

```bash
git clone https://github.com/your-username/chess-game.git
cd chess-game
```

2. Install dependencies:

```bash
pip install pygame
```

1. Run the game:

```bash
python main.py
```

```bash
python main.py
```

---

## Troubleshooting

If the game doesn't run, try the following:

- Make sure you have Python 3.6 or higher installed.
- Ensure that Pygame is installed correctly (`pip install pygame`).
- Verify that all image files are in the `assets/pieces/` directory.
- Check for any error messages in the console and address them accordingly.

---

## Screenshots & Demo

> *(add images once everything runs smoothly)*

- ![Screenshot](assets/screenshot.png)
- ![Demo](assets/demo.gif)

---

## What I Learned

- How to translate complex systems like chess into structured OOP code
- Managing internal state changes with clarity and predictability
- Creating graphical interfaces with live feedback and user interaction
- Implementing simple AI decision systems and integrating them into gameplay
- Organizing a real-world codebase with modular, scalable design

---

## Next Possible Enhancements

- Sound effects on move and capture
- Smarter AI using Minimax or Alpha-Beta pruning
- Full draw conditions (repetition, insufficient material)
- Move history display and saving/loading games
- Online multiplayer mode (future plan)

---

## Author

Naomi Blum  
[LinkedIn](https://www.linkedin.com/in/your-profile)  
[GitHub](https://github.com/your-username)
.
