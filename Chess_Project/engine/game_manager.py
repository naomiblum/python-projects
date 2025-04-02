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
            # Check if the move is legal
            if end_pos in self.get_legal_moves(start_pos):
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
