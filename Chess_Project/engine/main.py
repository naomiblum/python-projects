import os
import sys

# Add the Chess_Project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Chess_Project.gui.board_view import BoardView
from Chess_Project.engine.game_manager import GameManager
from Chess_Project.utils.load_piece_images import load_piece_images

def main():
    """
    Main function to initialize and run the game.
    """
    import pygame

    try:
        # Initialize Pygame
        pygame.init()
        screen = pygame.display.set_mode((512, 512))  # Example size
        pygame.display.set_caption("Chess Game")
        clock = pygame.time.Clock()

        # Initialize game components
        game = GameManager()
        images = load_piece_images(64)  # Assuming 64 is the square size
        board_view = BoardView(screen, 64)

        # Draw the initial board state
        board_view.draw_pieces(game.board.board, images)
        pygame.display.flip()

        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(30)

    except Exception as e:
        print(f"Error in main: {e}")
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()

def draw_pieces(self, board, images):
    """
    Draws the chess pieces on the board.
    """
    for row_index, row in enumerate(board):
        for col_index, piece in enumerate(row):
            if piece:
                color, piece_type = piece
                key = f"{color}_{piece_type}"
                if key in images:
                    self.screen.blit(images[key], (col_index * self.square_size, row_index * self.square_size))
                else:
                    print(f"Warning: Missing image for {key}")

def load_piece_images(square_size):
    """
    Loads chess piece images and scales them to the given square size.
    Returns a dictionary with keys like 'black_rook' and 'white_pawn'.
    """
    import pygame
    images = {}
    pieces = [
        "BlackBishop", "BlackKing", "BlackKnight", "BlackPawn", "BlackQueen", "BlackRook",
        "WhiteBishop", "WhiteKing", "WhiteKnight", "WhitePawn", "WhiteQueen", "WhiteRook"
    ]
    for piece in pieces:
        color, piece_type = piece[:5].lower(), piece[5:].lower()
        key = f"{color}_{piece_type}"
        try:
            images[key] = pygame.image.load(f"assets/pieces/{piece}.png")
            images[key] = pygame.transform.scale(images[key], (square_size, square_size))
        except Exception as e:
            print(f"Error loading image for {key}: {e}")
    return images


