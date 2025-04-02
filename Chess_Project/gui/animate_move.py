import pygame
import time
from typing import Tuple, Dict, Optional

class MoveAnimator:
    """Handles smooth animation of chess piece movements."""
    
    def __init__(self, screen: pygame.Surface, square_size: int, animation_speed: float = 0.2):
        """
        Initialize the move animator.
        
        Args:
            screen: The pygame screen surface to draw on
            square_size: Size of each square in pixels
            animation_speed: Duration of animation in seconds (default: 0.2)
        """
        self.screen = screen
        self.square_size = square_size
        self.animation_speed = animation_speed
        self.animating = False
        self.piece_image = None
        self.start_pos = (0, 0)
        self.end_pos = (0, 0)
        self.start_time = 0
        
    def start_animation(self, start_square: Tuple[int, int], end_square: Tuple[int, int], 
                       piece_image: pygame.Surface):
        """
        Start animating a piece movement.
        
        Args:
            start_square: Starting board position (col, row)
            end_square: Ending board position (col, row)
            piece_image: Image of the piece to animate
        """
        self.start_pos = (start_square[0] * self.square_size, start_square[1] * self.square_size)
        self.end_pos = (end_square[0] * self.square_size, end_square[1] * self.square_size)
        self.piece_image = piece_image
        self.start_time = time.time()
        self.animating = True
        
    def update(self, board_drawer) -> bool:
        """
        Update the animation state and draw the current frame.
        
        Args:
            board_drawer: Function to redraw the board under the animation
            
        Returns:
            bool: Whether the animation is still running
        """
        if not self.animating:
            return False
            
        # Calculate progress (0.0 to 1.0)
        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.animation_speed, 1.0)
        
        # Calculate current position with easing
        eased_progress = self._ease_out_quad(progress)
        current_x = self.start_pos[0] + (self.end_pos[0] - self.start_pos[0]) * eased_progress
        current_y = self.start_pos[1] + (self.end_pos[1] - self.start_pos[1]) * eased_progress
        
        # Redraw board
        board_drawer()
        
        # Draw piece at current position
        self.screen.blit(self.piece_image, (current_x, current_y))
        pygame.display.flip()
        
        # Check if animation is complete
        if progress >= 1.0:
            self.animating = False
            
        return self.animating
        
    def _ease_out_quad(self, x: float) -> float:
        """
        Quadratic easing function for smoother animation.
        
        Args:
            x: Input progress (0.0 to 1.0)
            
        Returns:
            float: Eased progress value
        """
        return 1 - (1 - x) * (1 - x)
        
    def is_animating(self) -> bool:
        """Check if an animation is currently in progress."""
        return self.animating

def animate_move(screen: pygame.Surface, board_view, board, images: Dict,
                start_pos: Tuple[int, int], end_pos: Tuple[int, int], 
                fps: int = 60, duration: float = 0.2) -> None:
    """
    Animate a piece moving from start to end position.
    
    Args:
        screen: Pygame screen surface
        board_view: BoardView instance to draw the board
        board: Board instance containing piece data
        images: Dictionary of piece images
        start_pos: Starting position (col, row)
        end_pos: Ending position (col, row)
        fps: Frames per second for animation
        duration: Animation duration in seconds
    """
    # Get the piece image
    x, y = start_pos
    piece = board.board[y][x]
    if not piece:
        return
        
    piece_key = f"{piece[0]}_{piece[1]}"
    if piece_key not in images:
        return
        
    piece_img = images[piece_key]
    
    # Calculate animation parameters
    start_x, start_y = x * board_view.square_size, y * board_view.square_size
    end_x, end_y = end_pos[0] * board_view.square_size, end_pos[1] * board_view.square_size
    
    # Number of frames for the animation
    num_frames = int(fps * duration)
    
    # Temporarily remove piece from board for drawing
    temp_piece = board.board[y][x]
    board.board[y][x] = None
    
    # Animation loop
    clock = pygame.time.Clock()
    for frame in range(num_frames + 1):
        # Clear screen and draw board
        screen.fill((0, 0, 0))
        board_view.draw_board()
        board_view.draw_pieces(board.board, images)
        
        # Calculate current position with easing
        progress = frame / num_frames
        eased_progress = 1 - pow(1 - progress, 3)  # Cubic ease-out
        
        current_x = start_x + (end_x - start_x) * eased_progress
        current_y = start_y + (end_y - start_y) * eased_progress
        
        # Draw the moving piece
        screen.blit(piece_img, (current_x, current_y))
        
        # Update display and control frame rate
        pygame.display.flip()
        clock.tick(fps)
    
    # Restore the piece at the new position
    board.board[end_pos[1]][end_pos[0]] = temp_piece