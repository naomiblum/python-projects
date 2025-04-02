from typing import List, Tuple, Optional

# Logic for chess pieces

class Piece:
    """Class that represents a chess piece."""
    
    def __init__(self, color: str, type: str):
        self.color = color
        self.type = type

    def __repr__(self) -> str:
        return f"{self.color} {self.type}"

    def valid_moves(self, board: List[List], pos: Tuple[int, int], last_move: Optional[Tuple] = None, castle_rights: dict = None) -> List[Tuple[int, int]]:
        """Returns all valid moves for the piece, considering special moves."""
        moves = []
        
        # Basic moves based on piece type
        if self.type == "pawn":
            moves.extend(self._pawn_moves(board, pos))
            # Add en passant moves if applicable
            if last_move:
                moves.extend(self._en_passant_moves(board, pos, last_move))
        elif self.type == "king":
            moves.extend(self._king_moves(board, pos))
            # Add castling moves if applicable
            if castle_rights:
                moves.extend(self._castling_moves(board, pos, castle_rights))
        elif self.type == "knight":
            moves.extend(self._knight_moves(board, pos))
        elif self.type == "bishop":
            moves.extend(self._diagonal_moves(board, pos))
        elif self.type == "rook":
            moves.extend(self._straight_moves(board, pos))
        elif self.type == "queen":
            moves.extend(self._diagonal_moves(board, pos))
            moves.extend(self._straight_moves(board, pos))
            
        return moves

    def _is_valid_pos(self, pos: Tuple[int, int]) -> bool:
        """Check if position is on board."""
        row, col = pos
        return 0 <= row < 8 and 0 <= col < 8

    def _can_move_to(self, board: List[List], pos: Tuple[int, int]) -> bool:
        """Check if piece can move to position."""
        if not self._is_valid_pos(pos):
            return False
        piece = board[pos[0]][pos[1]]
        return piece is None or piece[0] != self.color

    def _pawn_moves(self, board: List[List], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid pawn moves."""
        moves = []
        row, col = pos
        direction = 1 if self.color == "black" else -1
        start_row = 1 if self.color == "black" else 6

        # Forward move
        new_pos = (row + direction, col)
        if self._is_valid_pos(new_pos) and board[new_pos[0]][new_pos[1]] is None:
            moves.append(new_pos)
            # Double move from start
            if row == start_row:
                new_pos = (row + 2 * direction, col)
                if board[new_pos[0]][new_pos[1]] is None:
                    moves.append(new_pos)

        # Captures
        for dcol in [-1, 1]:
            new_pos = (row + direction, col + dcol)
            if self._is_valid_pos(new_pos):
                piece = board[new_pos[0]][new_pos[1]]
                if piece and piece[0] != self.color:
                    moves.append(new_pos)

        return moves

    def _knight_moves(self, board: List[List], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid knight moves."""
        moves = []
        row, col = pos
        offsets = [(-2, -1), (-2, 1), (-1, -2), (-1, 2),
                  (1, -2), (1, 2), (2, -1), (2, 1)]

        for drow, dcol in offsets:
            new_pos = (row + drow, col + dcol)
            if self._can_move_to(board, new_pos):
                moves.append(new_pos)

        return moves

    def _diagonal_moves(self, board: List[List], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid diagonal moves."""
        moves = []
        row, col = pos
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            while self._is_valid_pos((new_row, new_col)):
                piece = board[new_row][new_col]
                if piece is None:
                    moves.append((new_row, new_col))
                elif piece[0] != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += drow
                new_col += dcol

        return moves

    def _straight_moves(self, board: List[List], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid straight moves."""
        moves = []
        row, col = pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for drow, dcol in directions:
            new_row, new_col = row + drow, col + dcol
            while self._is_valid_pos((new_row, new_col)):
                piece = board[new_row][new_col]
                if piece is None:
                    moves.append((new_row, new_col))
                elif piece[0] != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += drow
                new_col += dcol

        return moves

    def _king_moves(self, board: List[List], pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get valid king moves."""
        moves = []
        row, col = pos
        directions = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1),           (0, 1),
                     (1, -1),  (1, 0),  (1, 1)]

        for drow, dcol in directions:
            new_pos = (row + drow, col + dcol)
            if self._can_move_to(board, new_pos):
                moves.append(new_pos)

        return moves

    def _en_passant_moves(self, board: List[List], pos: Tuple[int, int], last_move: Optional[Tuple]) -> List[Tuple[int, int]]:
        """Get valid en passant captures."""
        moves = []
        if not last_move:
            return moves

        row, col = pos
        last_start, last_end, last_piece = last_move
        
        # Check if last move was a pawn double move
        if (last_piece[1] == "pawn" and 
            abs(last_end[0] - last_start[0]) == 2 and 
            last_end[1] == col + 1 or last_end[1] == col - 1):
            
            direction = 1 if self.color == "black" else -1
            if row == (3 if self.color == "white" else 4):
                moves.append((row + direction, last_end[1]))
                
        return moves

    def _castling_moves(self, board: List[List], pos: Tuple[int, int], castle_rights: dict) -> List[Tuple[int, int]]:
        """Get valid castling moves."""
        moves = []
        if self.type != "king":
            return moves
            
        # Check kingside castling
        if castle_rights.get(f"{self.color}_kingside"):
            if all(board[pos[0]][col] is None for col in range(pos[1] + 1, 7)):
                moves.append((pos[0], pos[1] + 2))
                
        # Check queenside castling
        if castle_rights.get(f"{self.color}_queenside"):
            if all(board[pos[0]][col] is None for col in range(pos[1] - 1, 0, -1)):
                moves.append((pos[0], pos[1] - 2))
                
        return moves

    def _promotion_square(self, pos: Tuple[int, int]) -> bool:
        """Check if pawn has reached promotion square."""
        if self.type != "pawn":
            return False
            
        row, _ = pos
        return (row == 0 and self.color == "white") or (row == 7 and self.color == "black")

    def can_capture(self, pos: Tuple[int, int], target_pos: Tuple[int, int], board: List[List]) -> bool:
        """Check if piece can capture target position."""
        return target_pos in self.valid_moves(board, pos)

    def threatens_square(self, pos: Tuple[int, int], target_pos: Tuple[int, int], board: List[List]) -> bool:
        """Check if piece threatens a square (for check detection)."""
        if self.type == "pawn":
            # Pawns threaten diagonally
            row, col = pos
            direction = 1 if self.color == "black" else -1
            threatened = [(row + direction, col + dcol) for dcol in [-1, 1]]
            return target_pos in threatened and self._is_valid_pos(target_pos)
        else:
            return target_pos in self.valid_moves(board, pos)

    def get_piece_value(self) -> int:
        """Get the relative value of the piece."""
        values = {
            "pawn": 1,
            "knight": 3,
            "bishop": 3,
            "rook": 5,
            "queen": 9,
            "king": 0  # King's value is symbolic
        }
        return values.get(self.type, 0)