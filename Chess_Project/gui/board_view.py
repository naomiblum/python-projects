import pygame
from typing import List, Tuple, Dict, Optional

class BoardView:
    """Class for rendering the chess board and pieces."""
    
    def __init__(self, screen: pygame.Surface, square_size: int):
        self.screen = screen
        self.square_size = square_size
        self.colors = {
            "light": (240, 217, 181),  # Light squares
            "dark": (181, 136, 99),    # Dark squares
            "highlight": (124, 252, 0, 150),  # Selected piece highlight
            "legal_move": (106, 90, 205, 150)  # Legal move indicator
        }
        # Initialize fonts
        self.font = pygame.font.SysFont(None, 24)
        self.coordinate_font = pygame.font.SysFont(None, 20)

    def draw_board(self):
        """Draw the chess board squares."""
        for row in range(8):
            for col in range(8):
                color = self.colors["light"] if (row + col) % 2 == 0 else self.colors["dark"]
                rect = pygame.Rect(
                    col * self.square_size, 
                    row * self.square_size, 
                    self.square_size, 
                    self.square_size
                )
                pygame.draw.rect(self.screen, color, rect)
                
        # Draw coordinates
        for i in range(8):
            # Draw rank numbers (1-8)
            text = self.coordinate_font.render(str(8 - i), True, (0, 0, 0))
            self.screen.blit(text, (5, i * self.square_size + 5))
            
            # Draw file letters (a-h)
            text = self.coordinate_font.render(chr(97 + i), True, (0, 0, 0))
            self.screen.blit(text, (i * self.square_size + self.square_size - 15, 
                                  8 * self.square_size - 20))

    def draw_pieces(self, board: List[List], images: Dict[str, pygame.Surface]):
        """Draw the pieces on the board with smooth scaling."""
        for row in range(8):
            for col in range(8):
                piece = board[row][col]
                if piece:
                    color, piece_type = piece
                    key = f"{color}_{piece_type}"
                    if key in images:
                        piece_img = images[key]
                        # Scale image if needed
                        if piece_img.get_width() != self.square_size:
                            piece_img = pygame.transform.smoothscale(
                                piece_img, (self.square_size, self.square_size)
                            )
                        self.screen.blit(piece_img, 
                                       (col * self.square_size, row * self.square_size))
                    else:
                        print(f"Warning: No image for {key}")

    def highlight_square(self, pos: Tuple[int, int], color: Optional[Tuple] = None):
        """Highlight a square with optional custom color."""
        col, row = pos
        s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        s.fill(color or self.colors["highlight"])
        self.screen.blit(s, (col * self.square_size, row * self.square_size))

    def draw_legal_moves(self, legal_moves: List[Tuple[int, int]], 
                        capture_moves: Optional[List[Tuple[int, int]]] = None):
        """Highlight legal moves, with different indicators for captures."""
        for move in legal_moves:
            row, col = move
            s = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
            
            # Different visualization for capture moves
            if capture_moves and move in capture_moves:
                pygame.draw.circle(s, (255, 0, 0, 128), 
                                 (self.square_size//2, self.square_size//2), 
                                 self.square_size//3)
            else:
                pygame.draw.circle(s, self.colors["legal_move"], 
                                 (self.square_size//2, self.square_size//2), 
                                 self.square_size//6)
                
            self.screen.blit(s, (col * self.square_size, row * self.square_size))

    def draw_game_status(self, game_state: str, current_turn: str):
        """Draw game status (check, checkmate, stalemate)."""
        status_text = f"Game Status: {game_state.capitalize()}"
        turn_text = f"Current Turn: {current_turn.capitalize()}"
        
        status = self.font.render(status_text, True, (255, 255, 255))
        turn = self.font.render(turn_text, True, (255, 255, 255))
        
        # Draw with background
        pygame.draw.rect(self.screen, (0, 0, 0), (10, 10, status.get_width() + 20, 60))
        self.screen.blit(status, (20, 20))
        self.screen.blit(turn, (20, 45))

    def render(self, board: List[List], images: Dict[str, pygame.Surface], 
               game_state: str = "playing", current_turn: str = "white", 
               last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None):
        """Render the complete board state."""
        self.draw_board()
        
        # Highlight last move if exists
        if last_move:
            start, end = last_move
            self.highlight_square(start, self.colors["highlight"])
            self.highlight_square(end, self.colors["highlight"])
            
        self.draw_pieces(board, images)
        self.draw_game_status(game_state, current_turn)
