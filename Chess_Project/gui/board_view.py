import sys
import os
import pygame

# Add the parent directory to sys.path to ensure the engine module is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agent')))
try:
    from Chess_Project.engine.board import ChessBoard
    from Chess_Project.engine.piece import ChessPiece
except ModuleNotFoundError:
    # Verify the correct path for the 'engine' module
    engine_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Chess_Project', 'engine'))
    if engine_path not in sys.path:
        sys.path.append(engine_path)
    try:
        from Chess_Project.engine.board import ChessBoard
        from Chess_Project.engine.piece import ChessPiece
    except ModuleNotFoundError:
        raise ImportError("Ensure the 'engine' directory exists and contains 'board.py' and 'piece.py'. Check the import path.")

# Graphical representation of the chessboard

class BoardView:
    def __init__(self):
        # Initialize the board view
        # ...existing code...
        pass

    def render(self):
        # Render the board
        # ...existing code...
        pass
