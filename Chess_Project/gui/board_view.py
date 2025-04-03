import pygame
from typing import List, Tuple, Dict, Any, Optional

class BoardView:
    """Handles rendering of the chess board and pieces"""
    
    def __init__(self, screen: pygame.Surface, square_size: int):
        """Initialize the board view"""
        self.screen = screen
        self.square_size = square_size
        
        # Colors for the board
        self.light_square = (240, 217, 181)  # Light brown
        self.dark_square = (181, 136, 99)    # Dark brown
        self.highlight_color = (124, 252, 0, 128)  # Semi-transparent green
        self.move_indicator = (50, 200, 50, 150)   # Semi-transparent green circle
        
        # Fonts for drawing text - initialized in main.py
        self.coordinate_font = None
        self.font = None
    
    def draw_board(self):
        """Draw the chess board squares"""
        for row in range(8):
            for col in range(8):
                # Calculate position and color
                x, y = col * self.square_size, row * self.square_size
                color = self.light_square if (row + col) % 2 == 0 else self.dark_square
                
                # Draw the square
                pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))
                
        # Draw coordinates
        for i in range(8):
            # Draw rank numbers (1-8)
            text = self.coordinate_font.render(str(8 - i), True, (0, 0, 0))
            self.screen.blit(text, (5, i * self.square_size + 5))
            
            # Draw file letters (a-h)
            text = self.coordinate_font.render(chr(97 + i), True, (0, 0, 0))
            self.screen.blit(text, (i * self.square_size + self.square_size - 15, 
                                  8 * self.square_size - 20))

    def draw_pieces(self, board, images: Dict[Tuple[str, str], pygame.Surface]):
        """Draw the chess pieces on the board"""
        for row in range(8):
            for col in range(8):
                piece = board.get_piece(row, col)
                if piece:
                    # Get the image for this piece type and color
                    img_key = (piece.color, piece.type)
                    if img_key in images:
                        # Calculate position to center the piece in the square
                        x = col * self.square_size
                        y = row * self.square_size
                        self.screen.blit(images[img_key], (x, y))
                    else:
                        # Fallback if image not found: draw a colored rectangle with text
                        x = col * self.square_size + 5
                        y = row * self.square_size + 5
                        size = self.square_size - 10
                        color = (200, 200, 200) if piece.color == "white" else (50, 50, 50)
                        pygame.draw.rect(self.screen, color, (x, y, size, size))
                        
                        # Add initial of piece type
                        font = pygame.font.SysFont("Arial", 24)
                        text = font.render(piece.type[0].upper(), True, 
                                          (0, 0, 0) if piece.color == "white" else (255, 255, 255))
                        text_rect = text.get_rect(center=(
                            x + size // 2,
                            y + size // 2
                        ))
                        self.screen.blit(text, text_rect)
    
    def highlight_square(self, square: Tuple[int, int]):
        """Highlight the selected square"""
        col, row = square
        x, y = col * self.square_size, row * self.square_size
        
        # Draw a semi-transparent highlight
        highlight = pygame.Surface((self.square_size, self.square_size), pygame.SRCALPHA)
        highlight.fill(self.highlight_color)
        self.screen.blit(highlight, (x, y))
    
    def draw_legal_moves(self, moves: List[Tuple[int, int]]):
        """Draw indicators for legal moves"""
        for row, col in moves:
            # Calculate center position of the square
            x = col * self.square_size + self.square_size // 2
            y = row * self.square_size + self.square_size // 2
            
            # Draw a circle to indicate a legal move
            pygame.draw.circle(self.screen, self.move_indicator, (x, y), self.square_size // 6)

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
