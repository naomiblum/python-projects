import sys
import os

# Add the parent directory to sys.path to ensure the engine module is accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'agent')))
try:
    from engine.game_manager import GameManager
except ModuleNotFoundError:
    # Verify the correct path for the 'engine' module
    engine_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'engine'))
    if engine_path not in sys.path:
        sys.path.append(engine_path)
    try:
        from engine.game_manager import GameManager
    except ModuleNotFoundError:
        raise ImportError("Ensure the 'engine' directory exists and contains 'game_manager.py'. Check the import path.")
# קבועים עיצוביים
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
    colors = [pygame.Color("white"), pygame.Color("gray")]
    for row in range(8):
        for col in range(8):
            color = colors[(row + col) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen, board, images):
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece and piece.color and piece.kind:
                key = f"{piece.color}_{piece.kind}"
                if key in images:
                    images[key].draw(screen, (col, row))

def draw_turn_indicator(screen, current_turn):
    font = pygame.font.SysFont('Arial', 24, bold=True)
    text = font.render(f"Turn: {current_turn.title()}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

def highlight_square(screen, position, color=HIGHLIGHT_COLOR):
    x, y = position
    rect = pygame.Rect(x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, color, rect, 4)

def draw_legal_moves(screen, legal_moves):
    for move in legal_moves:
        highlight_square(screen, move, color=(0, 255, 0))

def animate_move(screen, start_pos, end_pos, piece_image, board, piece_images, duration=0.5):
    clock = pygame.time.Clock()
    frames = int(duration * 60)
    dx = (end_pos[0] - start_pos[0]) * SQUARE_SIZE / frames
    dy = (end_pos[1] - start_pos[1]) * SQUARE_SIZE / frames

    for frame in range(frames):
        screen.fill((0, 0, 0))
        draw_board(screen)
        draw_pieces(screen, board, piece_images)
        x = start_pos[0] * SQUARE_SIZE + dx * frame
        y = start_pos[1] * SQUARE_SIZE + dy * frame
        screen.blit(piece_image, (x, y))
        pygame.display.flip()
        clock.tick(60)
