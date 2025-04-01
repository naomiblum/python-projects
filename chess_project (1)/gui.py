
import pygame
import os
from logic import GameManager

WHITE = (245, 245, 220)
BLACK = (101, 67, 33)
BLUE = (0, 0, 255)
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
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board, piece_images):
    for row in board.grid:
        for piece in row:
            if piece:
                key = f"{piece.color}_{piece.kind}"
                gui_piece = piece_images.get(key)
                if gui_piece:
                    gui_piece.draw(screen, piece.position)

def draw_turn_indicator(screen, current_turn):
    font = pygame.font.SysFont(None, 32)
    text = font.render(f"Turn: {current_turn.title()}", True, (0, 0, 0))
    screen.blit(text, (10, 10))
