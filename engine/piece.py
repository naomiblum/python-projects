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
        row, col = start_pos
        if self.type == "pawn":
            # לוגיקה לרגלי
            direction = -1 if self.color == "white" else 1
            new_row = row + direction
            if 0 <= new_row < 8:
                # תנועה קדימה
                if board[new_row][col] is None:
                    moves.append((col, new_row))
                # תקיפה באלכסון
                if col > 0 and board[new_row][col - 1] is not None and board[new_row][col - 1][0] != self.color:
                    moves.append((col - 1, new_row))
                if col < 7 and board[new_row][col + 1] is not None and board[new_row][col + 1][0] != self.color:
                    moves.append((col + 1, new_row))
        elif self.type == "knight":
            # לוגיקה לפרש
            pass
        # המשך לוגיקה לכל כלי
        return moves
