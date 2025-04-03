import os
import pygame
from typing import Dict, Tuple

def load_piece_images(square_size: int) -> Dict[Tuple[str, str], pygame.Surface]:
    """
    Load chess piece images from the assets directory.
    Returns a dictionary mapping (color, piece_type) to Surface objects.
    
    Supports both naming formats:
    - color_piece.png (e.g., white_pawn.png) 
    - ColorPiece.png (e.g., WhitePawn.png)
    
    If images can't be loaded, creates placeholder graphics.
    """
    images = {}
    colors = ["white", "black"]
    piece_types = ["pawn", "rook", "knight", "bishop", "queen", "king"]
    
    # Try to load from assets directory
    try:
        assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "pieces")
        
        # First try the lowercase format (color_piece.png)
        for color in colors:
            for piece_type in piece_types:
                # Try lowercase format first (white_pawn.png)
                filename = f"{color}_{piece_type}.png"
                filepath = os.path.join(assets_path, filename)
                
                if os.path.exists(filepath):
                    try:
                        # Load and resize the image
                        img = pygame.image.load(filepath)
                        img = pygame.transform.scale(img, (square_size, square_size))
                        images[(color, piece_type)] = img
                        print(f"Loaded image: {filepath}")
                        continue  # Skip alternate format if this one worked
                    except pygame.error as e:
                        print(f"Error loading {filepath}: {e}")
                
                # Try camelcase format if lowercase format failed (WhitePawn.png)
                cap_color = color.capitalize()
                cap_piece = piece_type.capitalize()
                alt_filename = f"{cap_color}{cap_piece}.png"
                alt_filepath = os.path.join(assets_path, alt_filename)
                
                if os.path.exists(alt_filepath):
                    try:
                        img = pygame.image.load(alt_filepath)
                        img = pygame.transform.scale(img, (square_size, square_size))
                        images[(color, piece_type)] = img
                        print(f"Loaded image: {alt_filepath}")
                    except pygame.error as e:
                        print(f"Error loading {alt_filepath}: {e}")
    
    except Exception as e:
        print(f"Error loading piece images: {e}")
    
    # If any images are missing, create placeholders
    for color in colors:
        for piece_type in piece_types:
            if (color, piece_type) not in images:
                print(f"Creating placeholder for {color} {piece_type}")
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
    
    # Print summary
    loaded_count = len(images)
    print(f"Loaded {loaded_count} chess piece images (including placeholders)")
    
    return images