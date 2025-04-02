from typing import List, Tuple, Optional

class Board:
    """
    Represents the chess board and handles piece placement and movement.
    """
    def __init__(self):
        # Initialize empty board
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_board()
        
    def setup_board(self):
        """Set up the initial chess board configuration."""
        # Place pawns
        for col in range(8):
            self.board[1][col] = ("black", "pawn")
            self.board[6][col] = ("white", "pawn")
            
        # Place other pieces
        back_row = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        for col in range(8):
            self.board[0][col] = ("black", back_row[col])
            self.board[7][col] = ("white", back_row[col])
            
    def move_piece(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> bool:
        """
        Move a piece from start_pos to end_pos.
        
        Args:
            start_pos: Starting position (x, y)
            end_pos: Ending position (x, y)
            
        Returns:
            bool: Whether the move was successful
        """
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # Ensure coordinates are valid
        if not (0 <= x1 < 8 and 0 <= y1 < 8 and 0 <= x2 < 8 and 0 <= y2 < 8):
            return False
            
        # Get piece at start position
        piece = self.board[y1][x1]
        if not piece:
            return False
            
        # Move piece
        self.board[y2][x2] = piece
        self.board[y1][x1] = None
        
        # Handle pawn promotion (simplified)
        if piece[1] == "pawn" and (y2 == 0 or y2 == 7):
            self.board[y2][x2] = (piece[0], "queen")
            
        return True
        
    def get_piece(self, pos: Tuple[int, int]) -> Optional[Tuple[str, str]]:
        """
        Get the piece at the given position.
        
        Args:
            pos: Position (x, y)
            
        Returns:
            Tuple[str, str] or None: Piece as (color, type) or None if empty
        """
        x, y = pos
        if 0 <= x < 8 and 0 <= y < 8:
            return self.board[y][x]
        return None
        
    def copy(self):
        """
        Create a deep copy of the board.
        
        Returns:
            Board: New board instance with the same state
        """
        new_board = Board()
        new_board.board = [[self.board[y][x] for x in range(8)] for y in range(8)]
        return new_board