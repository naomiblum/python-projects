class ChessBoard:
    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]

    def place_piece(self, piece):
        x, y = piece.position
        self.grid[y][x] = piece

    def move_piece(self, from_pos, to_pos):
        piece = self.get_piece_at(from_pos)
        if piece:
            self.grid[from_pos[1]][from_pos[0]] = None
            self.grid[to_pos[1]][to_pos[0]] = piece
            piece.position = to_pos

    def get_piece_at(self, pos):
        x, y = pos
        return self.grid[y][x]
