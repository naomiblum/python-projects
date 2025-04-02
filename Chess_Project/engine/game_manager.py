from .board import Board
from .piece import Piece
from typing import List, Tuple, Optional

class GameManager:
    """
    Manages the game state, including player turns, move validation, and executing moves.
    """
    def __init__(self):
        self.board = Board()
        self.current_turn = "white"
        self.game_state = "playing"  # playing, check, checkmate, stalemate
        self.move_history = []

    def move_piece(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> bool:
        """
        Executes a move if it's legal.
        """
        piece = self.board.board[start_pos[1]][start_pos[0]]
        if piece and piece[0] == self.current_turn:
            # Check if the move is legal
            if end_pos in self.get_legal_moves(start_pos):
                # Store move in history
                self.move_history.append((start_pos, end_pos, piece))
                
                # Execute move
                self.board.move_piece(start_pos, end_pos)
                
                # Switch turns
                self.current_turn = "black" if self.current_turn == "white" else "white"
                
                # Update game state
                self.update_game_state()
                return True
        return False

    def get_legal_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """
        Returns all legal moves for a piece at a given position.
        """
        piece = self.board.board[pos[1]][pos[0]]
        if piece:
            moves = Piece(piece[0], piece[1]).valid_moves(self.board.board, pos)
            # Filter moves that would put own king in check
            return [move for move in moves if not self.would_be_in_check(pos, move)]
        return []

    def is_in_check(self, color: str) -> bool:
        """
        Determines if the specified color's king is in check.
        """
        # Find king position
        king_pos = None
        for y in range(8):
            for x in range(8):
                piece = self.board.board[y][x]
                if piece and piece[0] == color and piece[1] == "king":
                    king_pos = (x, y)
                    break
        
        if not king_pos:
            return False
            
        # Check if any opponent piece can capture the king
        opponent = "black" if color == "white" else "white"
        for y in range(8):
            for x in range(8):
                piece = self.board.board[y][x]
                if piece and piece[0] == opponent:
                    moves = Piece(piece[0], piece[1]).valid_moves(self.board.board, (x, y))
                    if king_pos in moves:
                        return True
        return False

    def would_be_in_check(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> bool:
        """
        Check if making a move would result in the current player being in check.
        """
        # Make temporary move
        temp_board = self.board.copy()
        temp_board.move_piece(start_pos, end_pos)
        
        # Check if current player's king would be in check
        return self.is_in_check(self.current_turn)

    def update_game_state(self) -> None:
        """
        Updates the game state (check, checkmate, stalemate).
        """
        if self.is_in_check(self.current_turn):
            if self.is_checkmate():
                self.game_state = "checkmate"
            else:
                self.game_state = "check"
        elif self.is_stalemate():
            self.game_state = "stalemate"
        else:
            self.game_state = "playing"

    def is_checkmate(self) -> bool:
        """
        Determines if the current player is in checkmate.
        """
        # If not in check, can't be in checkmate
        if not self.is_in_check(self.current_turn):
            return False
            
        # Check if any piece can make a move that gets out of check
        for y in range(8):
            for x in range(8):
                piece = self.board.board[y][x]
                if piece and piece[0] == self.current_turn:
                    legal_moves = self.get_legal_moves((x, y))
                    if legal_moves:  # If there's at least one legal move
                        return False
        return True
        
    def is_stalemate(self) -> bool:
        """
        Determines if the current player is in stalemate.
        """
        # If in check, it's not stalemate
        if self.is_in_check(self.current_turn):
            return False
            
        # Check if any piece can make a legal move
        for y in range(8):
            for x in range(8):
                piece = self.board.board[y][x]
                if piece and piece[0] == self.current_turn:
                    legal_moves = self.get_legal_moves((x, y))
                    if legal_moves:  # If there's at least one legal move
                        return False
        return True