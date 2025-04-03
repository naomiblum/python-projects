import os
import pygame

def load_piece_images(square_size):
    """
    Loads chess piece images and scales them to the given square size.
    Returns a dictionary with keys like 'black_rook' and 'white_pawn'.
    """
    images = {}
    pieces = [
        "BlackBishop", "BlackKing", "BlackKnight", "BlackPawn", "BlackQueen", "BlackRook",
        "WhiteBishop", "WhiteKing", "WhiteKnight", "WhitePawn", "WhiteQueen", "WhiteRook"
    ]
    
    # Directory containing piece images
    pieces_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "pieces")
    
    for piece in pieces:
        color, piece_type = piece[:5].lower(), piece[5:].lower()
        key = f"{color}_{piece_type}"
        try:
            img_path = os.path.join(pieces_dir, f"{piece}.png")
            if os.path.exists(img_path):
                images[key] = pygame.image.load(img_path)
                images[key] = pygame.transform.scale(images[key], (square_size, square_size))
            else:
                print(f"Warning: Image file not found: {img_path}")
        except Exception as e:
            print(f"Error loading image for {key}: {e}")
    
    if not images:
        print("No chess piece images were loaded. Check your assets/pieces directory.")
    else:
        print(f"Successfully loaded {len(images)} chess piece images")
    
    return images
