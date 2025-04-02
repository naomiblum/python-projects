from engine.board import ChessBoard
from engine.piece import ChessPiece


class GameManager:
    def __init__(self):
        self.board = ChessBoard()
        self.current_turn = 'white'
        self.winner = None
        self.last_moved_piece = None
        self.load_starting_position()

    def load_starting_position(self):
        positions = {
            'rook': [(0, 0), (7, 0), (0, 7), (7, 7)],
            'knight': [(1, 0), (6, 0), (1, 7), (6, 7)],
            'bishop': [(2, 0), (5, 0), (2, 7), (5, 7)],
            'queen': [(3, 0), (3, 7)],
            'king': [(4, 0), (4, 7)],
            'pawn': [(i, 1) for i in range(8)] + [(i, 6) for i in range(8)]
        }
        for kind, pos_list in positions.items():
            for pos in pos_list:
                color = 'white' if pos[1] <= 1 else 'black'
                piece = ChessPiece(kind, color, pos)
                self.board.place_piece(piece)

    def switch_turn(self):
        self.current_turn = 'black' if self.current_turn == 'white' else 'white'

    def is_in_check(self, color):
        king_pos = None
        for row in self.board.grid:
            for piece in row:
                if piece and piece.kind == 'king' and piece.color == color:
                    king_pos = piece.position
        if not king_pos:
            return False
        for row in self.board.grid:
            for piece in row:
                if piece and piece.color != color:
                    if king_pos in piece.get_valid_moves(self.board):
                        return True
        return False

    def is_checkmate(self, color):
        if not self.is_in_check(color):
            return False
        for row in self.board.grid:
            for piece in row:
                if piece and piece.color == color:
                    original_pos = piece.position
                    for move in piece.get_valid_moves(self.board):
                        captured = self.board.get_piece_at(move)
                        self.board.move_piece(original_pos, move)
                        if not self.is_in_check(color):
                            self.board.move_piece(move, original_pos)
                            if captured:
                                self.board.place_piece(captured)
                            return False
                        self.board.move_piece(move, original_pos)
                        if captured:
                            self.board.place_piece(captured)
        return True

    def move_piece(self, from_pos, to_pos):
        if self.winner:
            return f"המשחק נגמר. {self.winner} ניצח."

        piece = self.board.get_piece_at(from_pos)
        if not piece:
            return "אין כלי שם."

        if piece.color != self.current_turn:
            return f"זה לא התור של {self.current_turn}."

        if to_pos not in piece.get_valid_moves(self.board):
            return "מהלך לא חוקי."

        captured = self.board.get_piece_at(to_pos)
        self.board.move_piece(from_pos, to_pos)
        self.last_moved_piece = f"{piece.color}_{piece.kind}"

        if captured and captured.kind == 'king':
            self.winner = self.current_turn
            return f"המלך נאכל! {self.winner} ניצח."

        next_turn = 'black' if self.current_turn == 'white' else 'white'
        if self.is_checkmate(next_turn):
            self.winner = self.current_turn
            return f"שח-מט! {self.winner} ניצח."

        self.switch_turn()
        return f"{piece.kind} עבר מ-{from_pos} ל-{to_pos}. עכשיו תור {self.current_turn}."

    def is_own_piece(self, pos):
        piece = self.board.get_piece_at(pos)
        return piece and piece.color == self.current_turn

    def get_legal_moves(self, pos):
        piece = self.board.get_piece_at(pos)
        if piece and piece.color == self.current_turn:
            return piece.get_valid_moves(self.board)
        return []
