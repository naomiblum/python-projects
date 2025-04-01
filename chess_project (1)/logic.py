
class ChessPiece:
    def __init__(self, kind, color, position):
        self.kind = kind  # "pawn", "rook", etc.
        self.color = color  # "white" or "black"
        self.position = position  # (x, y)
        self.has_moved = False

    def move(self, to_position):
        self.position = to_position
        self.has_moved = True
        if self.kind == 'pawn':
            if (self.color == 'white' and self.position[1] == 7) or                (self.color == 'black' and self.position[1] == 0):
                self.kind = 'queen'  # Auto-promotion to queen

    def get_valid_moves(self, board):
        x, y = self.position
        valid_moves = []

        def on_board(a, b):
            return 0 <= a < 8 and 0 <= b < 8

        if self.kind == 'pawn':
            dir = 1 if self.color == 'white' else -1
            one_step = (x, y + dir)
            if on_board(*one_step) and not board.get_piece_at(one_step):
                valid_moves.append(one_step)
                two_step = (x, y + 2 * dir)
                if not self.has_moved and not board.get_piece_at(two_step):
                    valid_moves.append(two_step)
            for dx in [-1, 1]:
                diag = (x + dx, y + dir)
                if on_board(*diag):
                    target = board.get_piece_at(diag)
                    if target and target.color != self.color:
                        valid_moves.append(diag)

        elif self.kind == 'knight':
            for dx, dy in [(1, 2), (2, 1), (-1, 2), (-2, 1),
                           (1, -2), (2, -1), (-1, -2), (-2, -1)]:
                nx, ny = x + dx, y + dy
                if on_board(nx, ny):
                    target = board.get_piece_at((nx, ny))
                    if not target or target.color != self.color:
                        valid_moves.append((nx, ny))

        elif self.kind == 'king':
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if on_board(nx, ny):
                        target = board.get_piece_at((nx, ny))
                        if not target or target.color != self.color:
                            valid_moves.append((nx, ny))

        elif self.kind in ['rook', 'bishop', 'queen']:
            directions = []
            if self.kind in ['rook', 'queen']:
                directions += [(1, 0), (-1, 0), (0, 1), (0, -1)]
            if self.kind in ['bishop', 'queen']:
                directions += [(1, 1), (-1, 1), (1, -1), (-1, -1)]

            for dx, dy in directions:
                for i in range(1, 8):
                    nx, ny = x + dx * i, y + dy * i
                    if not on_board(nx, ny):
                        break
                    target = board.get_piece_at((nx, ny))
                    if not target:
                        valid_moves.append((nx, ny))
                    elif target.color != self.color:
                        valid_moves.append((nx, ny))
                        break
                    else:
                        break

        return valid_moves


class ChessBoard:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]

    def place_piece(self, piece):
        x, y = piece.position
        self.grid[y][x] = piece

    def get_piece_at(self, pos):
        x, y = pos
        return self.grid[y][x]

    def move_piece(self, from_pos, to_pos):
        piece = self.get_piece_at(from_pos)
        if piece:
            self.grid[from_pos[1]][from_pos[0]] = None
            self.grid[to_pos[1]][to_pos[0]] = piece
            piece.move(to_pos)


class GameManager:
    def __init__(self):
        self.board = ChessBoard()
        self.current_turn = 'white'
        self.winner = None
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

        if captured and captured.kind == 'king':
            self.winner = self.current_turn
            return f"המלך נאכל! {self.winner} ניצח."

        next_turn = 'black' if self.current_turn == 'white' else 'white'
        if self.is_checkmate(next_turn):
            self.winner = self.current_turn
            return f"שח-מט! {self.winner} ניצח."

        self.switch_turn()
        return f"{piece.kind} עבר מ-{from_pos} ל-{to_pos}. עכשיו תור {self.current_turn}."
