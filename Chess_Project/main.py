import pygame
import os
import sys

# Add the Chess_Project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from engine.game_manager import GameManager
from gui.board_view import BoardView, draw_turn_indicator, highlight_square, draw_legal_moves
from utils.load_piece_images import load_piece_images

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = 100

def main():
    """
    Main function to run the chess game.
    """
    try:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Chess Game")
    except Exception as e:
        print(f"Error initializing Pygame: {e}")
        return

    clock = pygame.time.Clock()
    running = True
    selected_square = None

    try:
        game = GameManager()
        images = load_piece_images(SQUARE_SIZE)
        board_view = BoardView(screen, SQUARE_SIZE)
    except Exception as e:
        print(f"Error initializing game components: {e}")
        return

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE
                if selected_square:
                    if game.move_piece(selected_square, (col, row)):
                        selected_square = None
                    else:
                        selected_square = (col, row)
                else:
                    selected_square = (col, row)

        # Draw the board and pieces
        screen.fill((0, 0, 0))  # Clear the screen
        board_view.draw_board()
        board_view.draw_pieces(game.board.board, images)
        if selected_square:
            board_view.highlight_square(selected_square)
            legal_moves = game.get_legal_moves(selected_square)
            board_view.draw_legal_moves(legal_moves)
        draw_turn_indicator(screen, game.current_turn)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
