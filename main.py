import pygame
from gui.board_view import (
    draw_board,
    draw_pieces,
    draw_turn_indicator,
    highlight_square,
    draw_legal_moves,
    animate_move,
    draw_info_panel
)
from gui.images import load_piece_images
from engine.game_manager import GameManager

# Constants
WIDTH, HEIGHT = 800, 800
SQUARE_SIZE = 100

def main():
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
        draw_info_panel(screen, game)

        if selected_square:
            legal_moves = game.get_legal_moves(selected_square)
            highlight_square(screen, selected_square)
            draw_legal_moves(screen, legal_moves)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
