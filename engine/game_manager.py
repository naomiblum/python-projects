from engine.board import Board
from engine.piece import Piece


class GameManager:
    """
    מנהל את מצב המשחק, כולל תור השחקן, חוקיות מהלכים, וביצוע מהלכים.
    """
    def __init__(self):
        self.board = Board()
        self.current_turn = "white"

    def move_piece(self, start_pos, end_pos):
        """
        מבצע מהלך אם הוא חוקי.
        """
        piece = self.board.board[start_pos[1]][start_pos[0]]
        if piece and piece[0] == self.current_turn:
            # בדיקת חוקיות המהלך
            if self.is_legal_move(start_pos, end_pos):
                self.board.move_piece(start_pos, end_pos)
                self.current_turn = "black" if self.current_turn == "white" else "white"
                return True
        return False

    def get_legal_moves(self, pos):
        """
        מחזיר את כל המהלכים החוקיים לכלי במיקום מסוים.
        """
        piece = self.board.board[pos[1]][pos[0]]
        if piece:
            return Piece(piece[0], piece[1]).valid_moves(self.board.board, pos)
        return []

    def is_legal_move(self, start_pos, end_pos):
        """
        בודק האם המהלך חוקי
        """
        piece = self.board.get_piece(start_pos)
        if piece is None:
            return False
        
        # Check if the piece belongs to the current player
        if piece[0] != self.current_turn:
            return False
        
        # Get valid moves for the piece
        valid_moves = Piece(piece[0], piece[1]).valid_moves(self.board.board, start_pos)
        
        # Check if the end_pos is in the valid moves
        return end_pos in valid_moves
