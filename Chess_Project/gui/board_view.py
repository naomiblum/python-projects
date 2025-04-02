import pygame


# Removed duplicate import
# Constants
WHITE = (245, 245, 220)
BLACK = (101, 67, 33)
HIGHLIGHT_COLOR = (255, 255, 0)
SQUARE_SIZE = 100

class BoardView:
    """
    אחראי על הצגת הלוח והכלים על המסך.
    """
    def __init__(self, screen, square_size):
        self.screen = screen
        self.square_size = square_size

    def draw_board(self):
        """
        מצייר את לוח השחמט.
        """
        colors = [(255, 255, 255), (0, 0, 0)]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                pygame.draw.rect(self.screen, color, 
                                 (col * self.square_size, row * self.square_size, 
                                  self.square_size, self.square_size))

    def draw_pieces(self, board, images):
        """
        Draws the chess pieces on the board.
        """
        for row_index, row in enumerate(board):
            for col_index, piece in enumerate(row):
                if piece:
                    color, piece_type = piece
                    key = f"{color}_{piece_type}"
                    if key in images:
                        self.screen.blit(images[key], (col_index * self.square_size, row_index * self.square_size))
                    else:
                        print(f"Warning: Missing image for {key}")  # Debugging: Warn about missing images

    def highlight_square(self, pos):
        """
        מדגיש ריבוע מסוים.
        """
        pygame.draw.rect(self.screen, (0, 255, 0), 
                         (pos[0] * self.square_size, pos[1] * self.square_size, 
                          self.square_size, self.square_size), 3)

    def draw_legal_moves(self, moves):
        """
        מצייר את המהלכים החוקיים.
        """
        for move in moves:
            pygame.draw.circle(self.screen, (0, 255, 0), 
                               (move[0] * self.square_size + self.square_size // 2, 
                                move[1] * self.square_size + self.square_size // 2), 10)

def draw_turn_indicator(screen, turn):
    """Draws an indicator to show whose turn it is."""
    font = pygame.font.Font(None, 36)
    text = font.render(f"{turn.capitalize()}'s turn", True, (255, 255, 255))
    screen.blit(text, (10, 10))

def highlight_square(screen, square, square_size=SQUARE_SIZE):
    """Highlights the selected square."""
    s = pygame.Surface((square_size, square_size))
    s.set_alpha(100)
    s.fill((255, 255, 0))  # Yellow color
    screen.blit(s, (square[0] * square_size, square[1] * square_size))

def draw_legal_moves(screen, legal_moves, square_size=SQUARE_SIZE):
    """Draws circles on the legal moves."""
    for move in legal_moves:
        center_x = move[0] * square_size + square_size // 2
        center_y = move[1] * square_size + square_size // 2
        pygame.draw.circle(screen, (0, 255, 0), (center_x, center_y), 15)  # Green color
