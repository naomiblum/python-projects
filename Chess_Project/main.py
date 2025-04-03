import os
import sys
from typing import Optional, Tuple, List
import pygame

# Initialize pygame early to catch any errors
pygame.init()

# Fix any imports to match your project structure
try:
    from engine.game_manager import GameManager
    from gui.board_view import BoardView
    from utils.load_pieces import load_piece_images
except ImportError as e:
    print(f"Error importing project modules: {e}")
    print("Please make sure all required files and directories exist.")
    print("Run check_structure.py to verify your project structure.")
    sys.exit(1)

# Game constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = WIDTH // 8
FPS = 60

def init_pygame() -> pygame.surface.Surface:
    """Initialize Pygame and create window"""
    # Create window with error checking
    try:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        if not screen:
            raise Exception("Failed to create display surface")
        pygame.display.set_caption("Chess Game")
        
        # Initialize font for BoardView
        pygame.font.init()
        
        return screen
    except Exception as e:
        print(f"Display initialization error: {e}")
        sys.exit(1)

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
        
        # Fix assets path - use relative path from current file
        assets_path = os.path.join(os.path.dirname(__file__), "assets", "pieces")
        
        # Create assets directory if it doesn't exist
        os.makedirs(assets_path, exist_ok=True)
        
        print(f"Using assets path: {assets_path}")
        
        # Initialize components with specific error handling
        try:
            # Use placeholders if images can't be loaded
            images = load_piece_images(SQUARE_SIZE)
            
            game = GameManager()
            if not hasattr(game, 'board'):
                raise AttributeError("GameManager initialized without board")
            
            board_view = BoardView(screen, SQUARE_SIZE)
            # Initialize fonts for coordinates in BoardView
            board_view.coordinate_font = pygame.font.SysFont("Arial", 18)
            board_view.font = pygame.font.SysFont("Arial", 18)
            
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
                    
                    # Draw game status
                    game_state = "check" if game.is_in_check(game.current_player) else "playing"
                    board_view.draw_game_status(game_state, game.current_player)
                    
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

    
