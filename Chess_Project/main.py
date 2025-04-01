import pygame
from gui.board_view import (
    draw_board,
    draw_pieces,
    draw_turn_indicator,
    highlight_square,
    draw_legal_moves,
    animate_move
)
from gui.images import load_piece_images
from engine.game_manager import GameManager  # type: ignore

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = 100

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")

    clock = pygame.time.Clock()
    running = True
    selected_square = None

    # Load game logic and images
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
                clicked = (row, col)

                if selected_square:
                    move_result = game.move_piece(selected_square, clicked)
                    if move_result:
                        piece = game.board[clicked[0]][clicked[1]]
                        piece_image = images.get(piece)
                        if piece_image:
                            animate_move(screen, selected_square, clicked, piece_image, game.board, images)
                    selected_square = None
                else:
                    if game.select_piece(row, col):
                        selected_square = (row, col)

        # Drawing
        draw_board(screen)
        draw_pieces(screen, game.board, images)
        draw_turn_indicator(screen, game.current_turn)

        if selected_square:
            # Placeholder: replace with game.get_legal_moves(selected_square) if available
            legal_moves = []
            highlight_square(screen, selected_square)
            draw_legal_moves(screen, legal_moves)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
