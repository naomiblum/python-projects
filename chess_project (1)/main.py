
import pygame
from logic import GameManager
from gui import load_piece_images, draw_board, draw_pieces, draw_turn_indicator, SQUARE_SIZE, BLUE

WIDTH, HEIGHT = SQUARE_SIZE * 8, SQUARE_SIZE * 8

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chess Game")
    clock = pygame.time.Clock()

    piece_images = load_piece_images()
    manager = GameManager()
    selected_pos = None

    running = True
    while running:
        clock.tick(60)
        draw_board(screen)
        draw_pieces(screen, manager.board, piece_images)
        draw_turn_indicator(screen, manager.current_turn)

        if selected_pos:
            x, y = selected_pos
            pygame.draw.rect(screen, BLUE, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                clicked_pos = (mx // SQUARE_SIZE, my // SQUARE_SIZE)
                if selected_pos:
                    message = manager.move_piece(selected_pos, clicked_pos)
                    print(message)
                    selected_pos = None
                else:
                    piece = manager.board.get_piece_at(clicked_pos)
                    if piece and piece.color == manager.current_turn:
                        selected_pos = clicked_pos

    pygame.quit()

if __name__ == '__main__':
    main()
