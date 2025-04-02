from engine.piece import Piece

class Board:
    """
    מחלקה שמייצגת את לוח השחמט ומנהלת את מצב הכלים.
    """
    def __init__(self):
        self.board = self.create_initial_board()

    def create_initial_board(self):
        """
        יוצר את מצב הלוח ההתחלתי עם כל הכלים במקומם.
        """
        board = [[None for _ in range(8)] for _ in range(8)]
        # הוספת רגלים
        for col in range(8):
            board[1][col] = ("black", "pawn")
            board[6][col] = ("white", "pawn")
        # הוספת כלים אחרים
        pieces = ["rook", "knight", "bishop", "queen", "king", "bishop", "knight", "rook"]
        for col, piece in enumerate(pieces):
            board[0][col] = ("black", piece)
            board[7][col] = ("white", piece)
        return board

    def move_piece(self, start_pos, end_pos):
        """
        מזיז כלי ממיקום אחד לאחר.
        """
        piece = self.board[start_pos[1]][start_pos[0]]
        self.board[start_pos[1]][start_pos[0]] = None
        self.board[end_pos[1]][end_pos[0]] = piece

    def get_piece(self, pos):
        """
        מחזיר את הכלי במיקום מסוים.
        """
        return self.board[pos[1]][pos[0]]

    def is_empty(self, pos):
        """
        Checks if the square at the given position is empty.
        Returns True if the square is empty, False otherwise.
        """
        return self.board[pos[1]][pos[0]] is None

    def display(self):
        """Displays the board state in a user-friendly format."""
        for row in self.board:
            print(" ".join([str(piece) if piece else "." for piece in row]))