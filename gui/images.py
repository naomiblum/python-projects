import os
import pygame

def load_piece_images():
    images = {}
    base_path = os.path.join("assets", "pieces")
    for color in ['w', 'b']:
        for piece in ['K', 'Q', 'R', 'B', 'N', 'P']:
            name = color + piece
            path = os.path.join(base_path, name + ".png")
            images[name] = pygame.transform.scale(pygame.image.load(path), (100, 100))
    return images
