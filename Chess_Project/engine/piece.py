# Logic for chess pieces

class Piece:
    """
    מחלקה שמייצגת כלי שחמט.
    """
    def __init__(self, color, type):
        self.color = color
        self.type = type

    def __repr__(self):
        return f"{self.color} {self.type}"

    def valid_moves(self, board, start_pos):
        """
        מחזיר את כל המהלכים החוקיים לכלי.
        """
        moves = []
        if self.type == "pawn":
            # לוגיקה לרגלי
            direction = -1 if self.color == "white" else 1
            row, col = start_pos
            if 0 <= row + direction < 8:
                if board[row + direction][col] is None:
                    moves.append((col, row + direction))
        elif self.type == "knight":
            # לוגיקה לפרש
            pass
        # המשך לוגיקה לכל כלי
        return moves
