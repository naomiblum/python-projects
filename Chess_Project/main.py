import os
import sys
from typing import Optional, Tuple, List
import pygame

# Fix imports to match your project structure
from engine.game_manager import GameManager
from gui.board_view import BoardView
from utils.load_pieces import load_piece_images

# Game constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
FPS = 60

def init_pygame() -> pygame.surface.Surface:
    """Initialize Pygame and create window"""
    # Force cleanup of any existing pygame instance
    pygame.quit()
    pygame.init()
    
    if pygame.get_error():
        raise Exception(f"Pygame initialization error: {pygame.get_error()}")
    
    # Create window with error checking
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        if not screen:
            raise Exception("Failed to create display surface")
        pygame.display.set_caption("Chess Game")
        return screen
    except Exception as e:
        raise Exception(f"Display initialization error: {e}")

def handle_move(game: GameManager, pos: Tuple[int, int], selected_square: Optional[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
    """Handle piece movement logic"""
    col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
    current_pos = (col, row)
    
    if selected_square:
        # If a piece is already selected, try to move it
        if game.move_piece(selected_square, current_pos):
            return None  # Reset selection after successful move
        return current_pos  # New selection if move failed
    return current_pos  # First selection

def main():
    """Main function to run the chess game"""
    screen = None
    try:
        # Initialize Pygame and create window
        screen = init_pygame()
        
        # Verify assets directory exists
        assets_path = os.path.join("Chess_Project", "assets", "pieces")
        if not os.path.exists(assets_path):
            raise FileNotFoundError(f"Assets directory not found: {assets_path}")
        
        # Initialize components with specific error handling
        try:
            images = load_piece_images(SQUARE_SIZE)
            if not images:
                raise ValueError("No chess piece images loaded")
            
            game = GameManager()
            if not hasattr(game, 'board'):
                raise AttributeError("GameManager initialized without board")
            
            board_view = BoardView(screen, SQUARE_SIZE)
            
        except FileNotFoundError as e:
            print(f"Missing files error: {e}")
            return
        except Exception as e:
            print(f"Component initialization error: {e}")
            return
        
        # Game state
        clock = pygame.time.Clock()
        running = True
        selected_square = None
        
        # Main game loop
        while running and pygame.display.get_init():
            # Event handling
            for event in pygame.event.get():
                if event.type in (pygame.QUIT, pygame.WINDOWCLOSE):
                    running = False
                    break
                    
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.display.get_active():
                    try:
                        pos = pygame.mouse.get_pos()
                        selected_square = handle_move(game, pos, selected_square)
                    except Exception as e:
                        print(f"Move error: {e}")
                        continue
            
            # Drawing
            if running:  # Only draw if still running
                try:
                    screen.fill((0, 0, 0))  # Clear screen with black
                    board_view.draw_board()
                    board_view.draw_pieces(game.board, images)
                    
                    if selected_square:
                        board_view.highlight_square(selected_square)
                        legal_moves = game.get_legal_moves(selected_square)
                        if legal_moves:
                            board_view.draw_legal_moves(legal_moves)
                    
                    pygame.display.flip()
                    clock.tick(FPS)
                    
                except Exception as e:
                    print(f"Rendering error: {e}")
                    running = False
    
    except Exception as e:
        print(f"Error in game: {e}")
    finally:
        # Ensure proper cleanup
        if pygame.get_init():
            pygame.quit()
        if 'screen' in locals() and screen:
            del screen
        sys.exit()

if __name__ == "__main__":
    main()