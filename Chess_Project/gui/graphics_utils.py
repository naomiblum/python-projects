# Utility functions for graphics

import pygame

def load_image(file_path):
    """Load an image from the given file path."""
    try:
        image = pygame.image.load(file_path)
        return image
    except pygame.error as message:
        print(f"Cannot load image: {file_path}")
        raise SystemExit(message)
