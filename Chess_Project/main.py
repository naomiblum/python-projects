import pygame
import os
import shutil
from Chess_Project.gui.board_view import (
    draw_board,
    draw_pieces,
    draw_turn_indicator,
    highlight_square,
    draw_legal_moves,
    animate_move
)
from Chess_Project.gui.images import load_piece_images
from Chess_Project.engine.game_manager import GameManager

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = 100

# Define source and destination directories
source_files = ["engine", "gui", "main.py", "assets", "theory.md"]
destination_dir = "Chess_Project"

# Check if the destination directory exists, create if not
if not os.path.exists(destination_dir):
    os.makedirs(destination_dir)

# Move each file/directory to the destination directory
for item in source_files:
    try:
        shutil.move(item, destination_dir)
        print(f"Successfully moved '{item}' to '{destination_dir}'.")
    except Exception as e:
        print(f"Error moving '{item}' to '{destination_dir}': {e}")

# Main entry point for the chess game
def main():
    print("Welcome to Chess Game!")
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game – Smart Edition")

    clock = pygame.time.Clock()
    running = True
    selected_square = None

    game = GameManager()
    images = load_piece_images()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                col = pos[0] // SQUARE_SIZE
                row = pos[1] // SQUARE_SIZE
                clicked = (col, row)

                if col < 8:
                    if selected_square:
                        move_result = game.move_piece(selected_square, clicked)
                        if move_result:
                            piece_key = game.last_moved_piece
                            if piece_key in images:
                                piece_image = images[piece_key].image
                                animate_move(screen, selected_square, clicked, piece_image, game.board, images)
                        selected_square = None
                    else:
                        if game.is_own_piece(clicked):
                            selected_square = clicked

        draw_board(screen)
        draw_pieces(screen, game.board, images)
        draw_turn_indicator(screen, game.current_turn)

        if selected_square:
            legal_moves = game.get_legal_moves(selected_square)
            highlight_square(screen, selected_square)
            draw_legal_moves(screen, legal_moves)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
