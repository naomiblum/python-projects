import pygame
import os

def load_piece_images(square_size):
    """
    Load chess piece images scaled to the given square size.
    
    Args:
        square_size: Size of a board square in pixels
        
    Returns:
        dict: Dictionary mapping piece names to pygame surfaces
    """
    images = {}
    base_path = os.path.join(os.path.dirname(__file__), "../assets/pieces")
    
    # Create assets directory if it doesn't exist
    if not os.path.exists(base_path):
        os.makedirs(base_path)
        print(f"Created directory: {base_path}")
        print("Please add piece images to this directory.")
        return images
        
    piece_types = ["pawn", "knight", "bishop", "rook", "queen", "king"]
    colors = ["white", "black"]
    
    for color in colors:
        for piece_type in piece_types:
            filename = f"{color}_{piece_type}.png"
            full_path = os.path.join(base_path, filename)
            
            try:
                image = pygame.image.load(full_path)
                images[f"{color}_{piece_type}"] = pygame.transform.scale(
                    image, (square_size, square_size)
                )
            except pygame.error:
                print(f"Couldn't load image: {full_path}")
                # Create placeholder
                surface = pygame.Surface((square_size, square_size), pygame.SRCALPHA)
                if color == "white":
                    pygame.draw.circle(surface, (255, 255, 255), 
                                     (square_size//2, square_size//2), 
                                     square_size//3)
                else:
                    pygame.draw.circle(surface, (0, 0, 0), 
                                     (square_size//2, square_size//2), 
                                     square_size//3)
                images[f"{color}_{piece_type}"] = surface
    
    return images