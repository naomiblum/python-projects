import os
import pygame
import sys

# Initialize pygame for image creation
pygame.init()

# Ensure the script can be run directly
if __name__ == "__main__":
    print("Generating chess piece images...")
    
    # Define paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    assets_path = os.path.join(project_root, "assets")
    pieces_path = os.path.join(assets_path, "pieces")
    
    # Create directories if they don't exist
    os.makedirs(pieces_path, exist_ok=True)
    
    # Size of the pieces
    size = 80
    
    # Basic surface to work with
    temp_surface = pygame.Surface((size, size), pygame.SRCALPHA)
    
    # Define colors
    white_piece_color = (240, 240, 240)  # Almost white
    white_outline_color = (150, 150, 150)  # Grey outline
    black_piece_color = (50, 50, 50)      # Almost black
    black_outline_color = (20, 20, 20)    # Deep black outline
    
    # Define piece designs - simple shapes for each piece
    piece_designs = {
        "pawn": lambda surface, color, outline: 
            [pygame.draw.circle(surface, color, (size//2, size//3), size//5),
             pygame.draw.rect(surface, color, (size//3, size//3, size//3, size//2)),
             pygame.draw.ellipse(surface, outline, (size//3, size//3, size//3, size//2), 2),
             pygame.draw.circle(surface, outline, (size//2, size//3), size//5, 2)],
             
        "rook": lambda surface, color, outline:
            [pygame.draw.rect(surface, color, (size//4, size//4, size//2, size//2)),
             pygame.draw.rect(surface, color, (size//6, size//6, 2*size//3, size//6)),
             pygame.draw.rect(surface, outline, (size//4, size//4, size//2, size//2), 2),
             pygame.draw.rect(surface, outline, (size//6, size//6, 2*size//3, size//6), 2)],
             
        "knight": lambda surface, color, outline:
            [pygame.draw.polygon(surface, color, [(size//4, size//4), (size//3, 3*size//4), 
                                               (2*size//3, 3*size//4), (3*size//4, size//4)]),
             pygame.draw.polygon(surface, outline, [(size//4, size//4), (size//3, 3*size//4), 
                                                 (2*size//3, 3*size//4), (3*size//4, size//4)], 2),
             pygame.draw.line(surface, outline, (size//4, size//4), (size//3, size//6), 2),
             pygame.draw.line(surface, outline, (3*size//4, size//4), (2*size//3, size//6), 2)],
             
        "bishop": lambda surface, color, outline:
            [pygame.draw.polygon(surface, color, [(size//2, size//6), (size//3, 2*size//3), 
                                               (2*size//3, 2*size//3)]),
             pygame.draw.circle(surface, color, (size//2, size//4), size//8),
             pygame.draw.polygon(surface, outline, [(size//2, size//6), (size//3, 2*size//3), 
                                                 (2*size//3, 2*size//3)], 2),
             pygame.draw.circle(surface, outline, (size//2, size//4), size//8, 2)],
             
        "queen": lambda surface, color, outline:
            [pygame.draw.polygon(surface, color, [(size//2, size//6), (size//3, 2*size//3), 
                                               (size//2, 3*size//4), (2*size//3, 2*size//3)]),
             pygame.draw.circle(surface, color, (size//2, size//5), size//8),
             pygame.draw.polygon(surface, outline, [(size//2, size//6), (size//3, 2*size//3), 
                                                 (size//2, 3*size//4), (2*size//3, 2*size//3)], 2),
             pygame.draw.circle(surface, outline, (size//2, size//5), size//8, 2)],
             
        "king": lambda surface, color, outline:
            [pygame.draw.polygon(surface, color, [(size//2, size//6), (size//3, 2*size//3), 
                                               (size//2, 3*size//4), (2*size//3, 2*size//3)]),
             pygame.draw.line(surface, color, (size//2, size//8), (size//2, size//4), 4),
             pygame.draw.line(surface, color, (size//2-size//10, size//6), (size//2+size//10, size//6), 4),
             pygame.draw.polygon(surface, outline, [(size//2, size//6), (size//3, 2*size//3), 
                                                 (size//2, 3*size//4), (2*size//3, 2*size//3)], 2),
             pygame.draw.line(surface, outline, (size//2, size//8), (size//2, size//4), 1),
             pygame.draw.line(surface, outline, (size//2-size//10, size//6), (size//2+size//10, size//6), 1)]
    }
    
    # Generate each piece
    pieces_generated = 0
    colors = ["white", "black"]
    for color in colors:
        piece_color = white_piece_color if color == "white" else black_piece_color
        outline_color = white_outline_color if color == "white" else black_outline_color
        
        for piece_type in piece_designs:
            # Clear surface
            temp_surface.fill((0, 0, 0, 0))
            
            # Draw the piece
            piece_designs[piece_type](temp_surface, piece_color, outline_color)
            
            # Save the image
            filename = f"{color}_{piece_type}.png"
            filepath = os.path.join(pieces_path, filename)
            pygame.image.save(temp_surface, filepath)
            
            pieces_generated += 1
            print(f"Generated: {filepath}")
    
    print(f"Successfully generated {pieces_generated} chess piece images in {pieces_path}")
    print("You can now run the chess game with these images.")
    print("Commands to run:")
    print(f"  cd {project_root}")
    print("  python main.py")
    
    # Clean up
    pygame.quit()
