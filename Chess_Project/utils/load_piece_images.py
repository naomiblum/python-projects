import pygame
import os

def load_piece_images(square_size):
    """
    Loads and scales chess piece images to fit the board squares.

    Args:
        square_size (int): The size of each square on the chessboard.

    Returns:
        dict: A dictionary mapping piece names (e.g., 'wK', 'bQ') to their scaled images.
    """
    images = {}
    pieces = ['wK', 'wQ', 'wR', 'wB', 'wN', 'wP', 'bK', 'bQ', 'bR', 'bB', 'bN', 'bP']
    base_path = os.path.join(os.path.dirname(__file__), 'assets', 'pieces')

    for piece in pieces:
        try:
            image_path = os.path.join(base_path, f"{piece}.png")
            image = pygame.image.load(image_path)
            images[piece] = pygame.transform.scale(image, (square_size, square_size))
        except Exception as e:
            print(f"Error loading image for {piece}: {e}")

    return images
