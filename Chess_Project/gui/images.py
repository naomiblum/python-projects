import pygame
import os

def load_piece_images(square_size):
    """
    טוען את תמונות הכלים.
    """
    images = {}
    base_path = os.path.join(os.path.dirname(__file__), "../assets/pieces")
    for piece in ["pawn", "knight", "bishop", "rook", "queen", "king"]:
        for color in ["white", "black"]:
            key = f"{color}_{piece}"
            path = os.path.join(base_path, f"{key}.png")
            try:
                image = pygame.transform.scale(pygame.image.load(path), 
                                               (square_size, square_size))
                images[key] = image
            except FileNotFoundError:
                print(f"Error: Missing file {path}")
    return images
