from typing import List, Tuple, Optional, Dict
from .piece import Piece

class Board:
    """Represents the chess board and its state"""
    
    def __init__(self):
        """Initialize an 8x8 board with pieces in starting positions"""
        # Create empty 8x8 board
        self.squares: List[List[Optional[Piece]]] = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()
        
    def setup_pieces(self):
        """Place all pieces in their starting positions"""
        # Setup pawns
        for col in range(8):
            self.squares[1][col] = Piece("black", "pawn", (1, col))
            self.squares[6][col] = Piece("white", "pawn", (6, col))
        
        # Setup other pieces
        piece_order = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        for col in range(8):
            self.squares[0][col] = Piece("black", piece_order[col], (0, col))
            self.squares[7][col] = Piece("white", piece_order[col], (7, col))
    
    def get_piece(self, row: int, col: int) -> Optional[Piece]:
        """Get the piece at the specified position"""
        if 0 <= row < 8 and 0 <= col < 8:
            return self.squares[row][col]
        return None
    
    def move_piece(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Move a piece from one position to another"""
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and 0 <= to_row < 8 and 0 <= to_col < 8):
            return False
        
        piece = self.squares[from_row][from_col]
        if piece is None:
            return False
        
        # Update piece position
        self.squares[to_row][to_col] = piece
        self.squares[from_row][from_col] = None
        piece.position = (to_row, to_col)
        return True
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if a position is valid on the board"""
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_all_pieces(self, color: str) -> List[Tuple[Tuple[int, int], Piece]]:
        """Get all pieces of a specific color"""
        result = []
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col]
                if piece and piece.color == color:
                    result.append(((row, col), piece))
        return result