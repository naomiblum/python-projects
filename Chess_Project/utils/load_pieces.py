import os
import pygame
from typing import Dict, Tuple

def load_piece_images(square_size: int) -> Dict[Tuple[str, str], pygame.Surface]:
    """
    Load chess piece images from the assets directory.
    Returns a dictionary mapping (color, piece_type) to Surface objects.
    
    If images can't be loaded, creates placeholder graphics.
    """
    images = {}
    colors = ["white", "black"]
    piece_types = ["pawn", "rook", "knight", "bishop", "queen", "king"]
    
    # Try to load from assets directory
    try:
        assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "pieces")
        
        for color in colors:
            for piece_type in piece_types:
                filename = f"{color}_{piece_type}.png"
                filepath = os.path.join(assets_path, filename)
                
                try:
                    if os.path.exists(filepath):
                        # Load and resize the image
                        img = pygame.image.load(filepath)
                        img = pygame.transform.scale(img, (square_size, square_size))
                        images[(color, piece_type)] = img
                    else:
                        # If file doesn't exist, create placeholder
                        raise FileNotFoundError(f"Image file not found: {filepath}")
                except (pygame.error, FileNotFoundError) as e:
                    print(f"Could not load image {filepath}: {e}")
                    # Create placeholder (this will be handled below)
    
    except Exception as e:
        print(f"Error loading piece images: {e}")
    
    # If any images are missing, create placeholders
    for color in colors:
        for piece_type in piece_types:
            if (color, piece_type) not in images:
                # Create a placeholder surface
                img = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                
                # Draw a colored rectangle
                rect_color = (220, 220, 220) if color == "white" else (50, 50, 50)
                pygame.draw.rect(img, rect_color, (5, 5, square_size-10, square_size-10))
                
                # Add text to indicate piece type
                font = pygame.font.SysFont("Arial", int(square_size/3))
                label = piece_type[0].upper()  # First letter of piece type
                text = font.render(label, True, (0, 0, 0) if color == "white" else (255, 255, 255))
                text_rect = text.get_rect(center=(square_size/2, square_size/2))
                img.blit(text, text_rect)
                
                # Add to images dictionary
                images[(color, piece_type)] = img
    
    return images