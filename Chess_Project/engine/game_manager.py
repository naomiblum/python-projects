from typing import List, Tuple, Optional
from .board import Board

class GameManager:
    """Manages the game state, rules and player turns"""
    
    def __init__(self):
        """Initialize a new chess game"""
        self.board = Board()
        self.current_player = "white"
        self.game_over = False
        self.winner = None
        self.move_history = []
    
    def move_piece(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Attempt to move a piece according to chess rules"""
        if self.game_over:
            return False
            
        # Extract positions
        from_col, from_row = from_pos
        to_col, to_row = to_pos
        
        # Get the piece
        piece = self.board.get_piece(from_row, from_col)
        
        # Check if there's a piece and it belongs to current player
        if piece is None or piece.color != self.current_player:
            return False
        
        # Check if the move is valid
        if (to_row, to_col) not in self.get_legal_moves(from_pos):
            return False
        
        # Store move for undo functionality
        captured_piece = self.board.get_piece(to_row, to_col)
        self.move_history.append({
            'from': (from_row, from_col),
            'to': (to_row, to_col),
            'piece': piece,
            'captured': captured_piece,
            'first_move': not piece.has_moved
        })
        
        # Execute the move
        self.board.move_piece((from_row, from_col), (to_row, to_col))
        piece.has_moved = True
        
        # Switch player
        self.current_player = "black" if self.current_player == "white" else "white"
        
        # Check game state (checkmate, stalemate, etc.)
        self._check_game_state()
        
        return True
    
    def get_legal_moves(self, position: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get all legal moves for a piece at the given position"""
        col, row = position
        piece = self.board.get_piece(row, col)
        
        if piece is None or piece.color != self.current_player:
            return []
        
        # Get all possible moves according to piece rules
        possible_moves = piece.get_possible_moves(self.board)
        
        # Filter out moves that would leave the king in check
        legal_moves = []
        for move in possible_moves:
            if self._is_legal_move((row, col), move):
                legal_moves.append(move)
        
        return legal_moves
    
    def _is_legal_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """Check if a move would leave the king in check"""
        # Simplified implementation - in a full chess engine, this would check if the move
        # leaves the player's king in check, which is illegal
        return True
    
    def undo_move(self) -> bool:
        """Undo the last move"""
        if not self.move_history:
            return False
        
        last_move = self.move_history.pop()
        
        # Restore the piece to its original position
        self.board.squares[last_move['from'][0]][last_move['from'][1]] = last_move['piece']
        last_move['piece'].position = last_move['from']
        
        # Restore the captured piece, if any
        self.board.squares[last_move['to'][0]][last_move['to'][1]] = last_move['captured']
        
        # Restore first move status
        if last_move['first_move']:
            last_move['piece'].has_moved = False
        
        # Switch back to previous player
        self.current_player = "black" if self.current_player == "white" else "white"
        
        # Reset game state
        self.game_over = False
        self.winner = None
        
        return True
    
    def _check_game_state(self):
        """Check if the game is over (checkmate, stalemate, etc.)"""
        # This would implement check and checkmate detection
        # For simplicity, we're just providing a stub implementation
        pass
    
    def is_in_check(self, color: str) -> bool:
        """Check if the specified color's king is in check"""
        # Find the king
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == color and piece.type == "king":
                    king_pos = (row, col)
                    break
            if king_pos:
                break
        
        if not king_pos:
            return False  # No king found (shouldn't happen in a real game)
        
        # Check if any opponent piece can capture the king
        opponent_color = "black" if color == "white" else "white"
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == opponent_color:
                    moves = piece.get_possible_moves(self.board)
                    if king_pos in moves:
                        return True
        
        return False