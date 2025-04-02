https://github.com/naomiblum/python-projects

# filepath: /Users/naomiblum/Documents/GitHub/python-projects/Chess_Project/engine/board.py

class Board:
    def __init__(self):
        self.board = [
            [('black', 'rook'), ('black', 'knight'), ('black', 'bishop'), ('black', 'queen'), ('black', 'king'), ('black', 'bishop'), ('black', 'knight'), ('black', 'rook')],
            [('black', 'pawn')] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [('white', 'pawn')] * 8,
            [('white', 'rook'), ('white', 'knight'), ('white', 'bishop'), ('white', 'queen'), ('white', 'king'), ('white', 'bishop'), ('white', 'knight'), ('white', 'rook')],
        ]

from Chess_Project.engine.board import Board

def main():
    board = Board()  # יצירת אובייקט של הלוח
    print("Initial board state:")
    for row in board.board:
        print(row)

if __name__ == "__main__":
    main()