from typing import List, Tuple, Optional

class Piece:
    """Represents a chess piece with its properties and movement rules"""
    
    def __init__(self, color: str, piece_type: str, position: Tuple[int, int]):
        """Initialize a chess piece"""
        self.color = color      # 'white' or 'black'
        self.type = piece_type  # 'pawn', 'rook', 'knight', 'bishop', 'queen', 'king'
        self.position = position  # (row, col)
        self.has_moved = False  # Track if the piece has moved (for castling and pawn double-move)
    
    def get_possible_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for this piece on the current board"""
        row, col = self.position
        moves = []
        
        # Different movement patterns based on piece type
        if self.type == "pawn":
            moves = self._get_pawn_moves(board)
        elif self.type == "rook":
            moves = self._get_rook_moves(board)
        elif self.type == "knight":
            moves = self._get_knight_moves(board)
        elif self.type == "bishop":
            moves = self._get_bishop_moves(board)
        elif self.type == "queen":
            moves = self._get_queen_moves(board)
        elif self.type == "king":
            moves = self._get_king_moves(board)
            
        return moves
    
    def _get_pawn_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for a pawn"""
        row, col = self.position
        moves = []
        
        # Direction depends on color
        direction = -1 if self.color == "white" else 1
        
        # Forward move
        if board.is_valid_position(row + direction, col) and board.get_piece(row + direction, col) is None:
            moves.append((row + direction, col))
            
            # Double move from starting position
            start_row = 6 if self.color == "white" else 1
            if row == start_row and board.get_piece(row + 2*direction, col) is None:
                moves.append((row + 2*direction, col))
        
        # Capture moves
        for c_offset in [-1, 1]:
            capture_col = col + c_offset
            if board.is_valid_position(row + direction, capture_col):
                target = board.get_piece(row + direction, capture_col)
                if target and target.color != self.color:
                    moves.append((row + direction, capture_col))
        
        return moves
    
    def _get_rook_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for a rook"""
        return self._get_sliding_moves(board, [(0, 1), (1, 0), (0, -1), (-1, 0)])
    
    def _get_bishop_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for a bishop"""
        return self._get_sliding_moves(board, [(1, 1), (1, -1), (-1, -1), (-1, 1)])
    
    def _get_queen_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for a queen"""
        return self._get_sliding_moves(board, [
            (0, 1), (1, 0), (0, -1), (-1, 0),  # Rook moves
            (1, 1), (1, -1), (-1, -1), (-1, 1)  # Bishop moves
        ])
    
    def _get_knight_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for a knight"""
        row, col = self.position
        moves = []
        
        # All potential knight moves
        offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        
        for r_offset, c_offset in offsets:
            new_row, new_col = row + r_offset, col + c_offset
            if board.is_valid_position(new_row, new_col):
                target = board.get_piece(new_row, new_col)
                if target is None or target.color != self.color:
                    moves.append((new_row, new_col))
        
        return moves
    
    def _get_king_moves(self, board) -> List[Tuple[int, int]]:
        """Get all possible moves for a king"""
        row, col = self.position
        moves = []
        
        # All adjacent squares
        for r_offset in [-1, 0, 1]:
            for c_offset in [-1, 0, 1]:
                if r_offset == 0 and c_offset == 0:
                    continue  # Skip the current position
                
                new_row, new_col = row + r_offset, col + c_offset
                if board.is_valid_position(new_row, new_col):
                    target = board.get_piece(new_row, new_col)
                    if target is None or target.color != self.color:
                        moves.append((new_row, new_col))
        
        # Castling logic would go here
        
        return moves
    
    def _get_sliding_moves(self, board, directions) -> List[Tuple[int, int]]:
        """Helper method for getting moves for sliding pieces (rook, bishop, queen)"""
        row, col = self.position
        moves = []
        
        for r_dir, c_dir in directions:
            for i in range(1, 8):  # Maximum 7 steps in any direction
                new_row, new_col = row + i * r_dir, col + i * c_dir
                
                if not board.is_valid_position(new_row, new_col):
                    break  # Out of bounds
                
                target = board.get_piece(new_row, new_col)
                if target is None:
                    moves.append((new_row, new_col))  # Empty square
                elif target.color != self.color:
                    moves.append((new_row, new_col))  # Capture
                    break  # Can't move past a piece
                else:
                    break  # Can't move past own piece
        
        return moves