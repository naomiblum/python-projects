import pygame
import os
from logic import GameManager

WHITE = (245, 245, 220)
BLACK = (101, 67, 33)
HIGHLIGHT_COLOR = (255, 255, 0)
SQUARE_SIZE = 100

class GUIPiece:
    def __init__(self, image):
        self.image = image

    def draw(self, screen, position):
        x, y = position
        screen.blit(self.image, (x * SQUARE_SIZE, y * SQUARE_SIZE))

def load_piece_images():
    piece_images = {}
    piece_types = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    colors = ['white', 'black']
    for color in colors:
        for piece in piece_types:
            filename = f"{color.capitalize()}{piece.capitalize()}.png"
            path = os.path.join("assets", "pieces", filename)
            if os.path.exists(path):
                image = pygame.image.load(path)
                image = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))
                piece_images[f"{color}_{piece}"] = GUIPiece(image)
    return piece_images

def draw_board(screen):
    texture_white = pygame.image.load("assets/textures/white_square.png")
    texture_black = pygame.image.load("assets/textures/black_square.png")
    texture_white = pygame.transform.scale(texture_white, (SQUARE_SIZE, SQUARE_SIZE))
    texture_black = pygame.transform.scale(texture_black, (SQUARE_SIZE, SQUARE_SIZE))
    
    for row in range(8):
        for col in range(8):
            texture = texture_white if (row + col) % 2 == 0 else texture_black
            screen.blit(texture, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def draw_pieces(screen, board, piece_images):
    for row in board.grid:
        for piece in row:
            if piece:
                key = f"{piece.color}_{piece.kind}"
                gui_piece = piece_images.get(key)
                if gui_piece:
                    gui_piece.draw(screen, piece.position)

def draw_turn_indicator(screen, current_turn):
    font = pygame.font.SysFont('Arial', 32, bold=True)
    text = font.render(f"Turn: {current_turn.title()}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

def highlight_square(screen, position, color=HIGHLIGHT_COLOR):
    x, y = position
    rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, color, rect, 5)

def animate_move(screen, start_pos, end_pos, piece_image, duration=0.5):
    clock = pygame.time.Clock()
    start_x, start_y = start_pos
    end_x, end_y = end_pos
    frames = int(duration * 60)  # Assuming 60 FPS
    delta_x = (end_x - start_x) * SQUARE_SIZE / frames
    delta_y = (end_y - start_y) * SQUARE_SIZE / frames

    for frame in range(frames):
        screen.fill((0, 0, 0))  # Clear screen or redraw the board
        draw_board(screen)
        draw_pieces(screen, board, piece_images)  # Redraw all pieces
        x = start_x * SQUARE_SIZE + frame * delta_x
        y = start_y * SQUARE_SIZE + frame * delta_y
        screen.blit(piece_image, (x, y))
        pygame.display.flip()
        clock.tick(60)

def draw_legal_moves(screen, legal_moves):
    for move in legal_moves:
        highlight_square(screen, move, color=(0, 255, 0))
