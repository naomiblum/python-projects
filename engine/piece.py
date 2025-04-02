class ChessPiece:
    def __init__(self, kind, color, position):
        self.kind = kind
        self.color = color
        self.position = position

    def get_valid_moves(self, board):
        moves = []
        if self.kind == 'pawn':
            moves = self.get_pawn_moves(board)
        elif self.kind == 'rook':
            moves = self.get_rook_moves(board)
        elif self.kind == 'knight':
            moves = self.get_knight_moves(board)
        elif self.kind == 'bishop':
            moves = self.get_bishop_moves(board)
        elif self.kind == 'queen':
            moves = self.get_queen_moves(board)
        elif self.kind == 'king':
            moves = self.get_king_moves(board)
        return moves

    def get_pawn_moves(self, board):
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1
        x, y = self.position

        # Move forward
        if board.get_piece_at((x, y + direction)) is None:
            moves.append((x, y + direction))
            if y == start_row and board.get_piece_at((x, y + 2 * direction)) is None:
                moves.append((x, y + 2 * direction))

        # Capture diagonally
        for dx in [-1, 1]:
            if 0 <= x + dx < 8 and 0 <= y + direction < 8:
                target = board.get_piece_at((x + dx, y + direction))
                if target and target.color != self.color:
                    moves.append((x + dx, y + direction))

        return moves

    def get_rook_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target = board.get_piece_at((nx, ny))
                if target is None:
                    moves.append((nx, ny))
                elif target.color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break
                nx += dx
                ny += dy

        return moves

    def get_knight_moves(self, board):
        moves = []
        x, y = self.position
        knight_moves = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]

        for dx, dy in knight_moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board.get_piece_at((nx, ny))
                if target is None or target.color != self.color:
                    moves.append((nx, ny))

        return moves

    def get_bishop_moves(self, board):
        moves = []
        x, y = self.position
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target = board.get_piece_at((nx, ny))
                if target is None:
                    moves.append((nx, ny))
                elif target.color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break
                nx += dx
                ny += dy

        return moves

    def get_queen_moves(self, board):
        return self.get_rook_moves(board) + self.get_bishop_moves(board)

    def get_king_moves(self, board):
        moves = []
        x, y = self.position
        king_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]

        for dx, dy in king_moves:
            nx, ny = x + dx, y + dy
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board.get_piece_at((nx, ny))
                if target is None or target.color != self.color:
                    moves.append((nx, ny))

        return moves
