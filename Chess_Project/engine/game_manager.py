from Chess_Project.engine.board import Board
from Chess_Project.engine.piece import Piece


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

    def is_check(self, color):
        """
        Checks if the given color is in check.
        """
        king_pos = self.find_king(color)
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece and piece[0] != color:
                    if king_pos in self.get_legal_moves((col, row)):
                        return True
        return False

    def find_king(self, color):
        """
        Finds the position of the king of the given color.
        """
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece and piece[0] == color and piece[1] == "king":
                    return (col, row)
        return None

    def is_checkmate(self, color):
        """
        Checks if the given color is in checkmate.
        """
        if not self.is_check(color):
            return False
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece and piece[0] == color:
                    legal_moves = self.get_legal_moves((col, row))
                    for move in legal_moves:
                        original_piece = self.board.board[move[1]][move[0]]
                        self.board.move_piece((col, row), move)
                        if not self.is_check(color):
                            self.board.move_piece(move, (col, row))
                            self.board.board[move[1]][move[0]] = original_piece
                            return False
                        self.board.move_piece(move, (col, row))
                        self.board.board[move[1]][move[0]] = original_piece
        return True
