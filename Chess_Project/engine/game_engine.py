from .board import Board
from .piece import Piece
from typing import Optional, Tuple, List, Dict, Any

class GameEngine:
    """
    Advanced game engine for chess with comprehensive rule enforcement
    and AI capabilities.
    """
    def __init__(self):
        self.board = Board()
        self.current_turn = "white"
        self.move_history = []
        self.game_state = "playing"  # playing, check, checkmate, stalemate, draw
        self.castle_rights = {
            "white_kingside": True,
            "white_queenside": True,
            "black_kingside": True,
            "black_queenside": True
        }
        self.last_move = None
        self.halfmove_clock = 0  # For 50-move rule
        self.fullmove_number = 1  # Increments after black's move
        
    def initialize_game(self):
        """Reset the game to its initial state."""
        self.board = Board()
        self.current_turn = "white"
        self.move_history = []
        self.game_state = "playing"
        self.castle_rights = {
            "white_kingside": True, 
            "white_queenside": True,
            "black_kingside": True, 
            "black_queenside": True
        }
        self.last_move = None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        
    def is_valid_move(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> bool:
        """Check if a move is valid according to chess rules."""
        if not (0 <= start_pos[0] < 8 and 0 <= start_pos[1] < 8):
            return False
        if not (0 <= end_pos[0] < 8 and 0 <= end_pos[1] < 8):
            return False
            
        piece = self.board.get_piece(start_pos)
        if not piece or piece[0] != self.current_turn:
            return False
            
        return end_pos in self.get_legal_moves(start_pos)
        
    def make_move(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> bool:
        """
        Execute a chess move if it's valid.
        
        Handles special moves like castling, en passant, and pawn promotion.
        Updates game state, move history, and turn.
        
        Returns:
            bool: Whether the move was successful
        """
        if not self.is_valid_move(start_pos, end_pos):
            return False
            
        # Get the piece and track if it's a capture or pawn move
        piece = self.board.get_piece(start_pos)
        target = self.board.get_piece(end_pos)
        is_capture = target is not None
        is_pawn_move = piece[1] == "pawn"
        
        # Update halfmove clock (reset on capture or pawn move)
        if is_capture or is_pawn_move:
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1
            
        # Store the move for future reference (en passant, etc.)
        self.last_move = (start_pos, end_pos, piece)
        self.move_history.append(self.last_move)
        
        # Handle castling
        if piece[1] == "king" and abs(end_pos[0] - start_pos[0]) == 2:
            # Kingside castling
            if end_pos[0] > start_pos[0]:
                rook_start = (7, start_pos[1])
                rook_end = (end_pos[0] - 1, end_pos[1])
            # Queenside castling
            else:
                rook_start = (0, start_pos[1])
                rook_end = (end_pos[0] + 1, end_pos[1])
                
            # Move the rook
            self.board.move_piece(rook_start, rook_end)
            
        # Handle en passant capture
        if piece[1] == "pawn" and end_pos[0] != start_pos[0] and not target:
            # Remove the captured pawn
            captured_pawn_pos = (end_pos[0], start_pos[1])
            self.board.board[captured_pawn_pos[1]][captured_pawn_pos[0]] = None
            
        # Execute the move
        self.board.move_piece(start_pos, end_pos)
        
        # Update castle rights if king or rook moves
        if piece[1] == "king":
            if piece[0] == "white":
                self.castle_rights["white_kingside"] = False
                self.castle_rights["white_queenside"] = False
            else:
                self.castle_rights["black_kingside"] = False
                self.castle_rights["black_queenside"] = False
        elif piece[1] == "rook":
            if start_pos == (0, 7) and piece[0] == "white":
                self.castle_rights["white_queenside"] = False
            elif start_pos == (7, 7) and piece[0] == "white":
                self.castle_rights["white_kingside"] = False
            elif start_pos == (0, 0) and piece[0] == "black":
                self.castle_rights["black_queenside"] = False
            elif start_pos == (7, 0) and piece[0] == "black":
                self.castle_rights["black_kingside"] = False
                
        # Update full move number
        if self.current_turn == "black":
            self.fullmove_number += 1
            
        # Switch turns
        self.current_turn = "white" if self.current_turn == "black" else "black"
        
        # Update game state (check, checkmate, etc.)
        self.update_game_state()
        
        return True
    
    def get_legal_moves(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Get all legal moves for a piece, considering check and special moves."""
        piece = self.board.get_piece(pos)
        if not piece:
            return []
            
        # Get basic moves based on piece type
        piece_obj = Piece(piece[0], piece[1])
        moves = piece_obj.valid_moves(
            self.board.board, 
            pos, 
            self.last_move,
            self.castle_rights
        )
        
        # Filter moves that would put/leave king in check
        return [move for move in moves if not self.would_be_in_check(pos, move)]
    
    def update_game_state(self):
        """Update game state (check, checkmate, stalemate, draw)."""
        if self.is_in_check(self.current_turn):
            if self.is_checkmate():
                self.game_state = "checkmate"
            else:
                self.game_state = "check"
        elif self.is_stalemate():
            self.game_state = "stalemate"
        elif self.is_draw():
            self.game_state = "draw"
        else:
            self.game_state = "playing"
    
    def is_in_check(self, color: str) -> bool:
        """Check if the specified color's king is in check."""
        # Find king position
        king_pos = None
        for y in range(8):
            for x in range(8):
                piece = self.board.board[y][x]
                if piece and piece[0] == color and piece[1] == "king":
                    king_pos = (x, y)
                    break
            if king_pos:
                break
                
        if not king_pos:
            return False  # No king found (shouldn't happen in normal chess)
            
        # Check if any opponent piece can capture the king
        opponent = "white" if color == "black" else "black"
        for y in range(8):
            for x in range(8):
                piece = self.board.board[y][x]
                if piece and piece[0] == opponent:
                    piece_obj = Piece(piece[0], piece[1])
                    if piece_obj.threatens_square((x, y), king_pos, self.board.board):
                        return True
        return False
    
    def is_checkmate(self) -> bool:
        """Check if current player is in checkmate."""
        if not self.is_in_check(self.current_turn):
            return False
            
        # If any piece has legal moves, it's not checkmate
        for y in range(8):
            for x in range(8):
                piece = self.board.board[y][x]
                if piece and piece[0] == self.current_turn:
                    if self.get_legal_moves((x, y)):
                        return False
        return True
    
    def is_stalemate(self) -> bool:
        """Check if current player is in stalemate."""
        if self.is_in_check(self.current_turn):
            return False
            
        # If no piece has legal moves, it's stalemate
        for y in range(8):
            for x in range(8):
                piece = self.board.board[y][x]
                if piece and piece[0] == self.current_turn:
                    if self.get_legal_moves((x, y)):
                        return False
        return True
    
    def is_draw(self) -> bool:
        """Check for other draw conditions (50-move rule, insufficient material)."""
        # 50-move rule
        if self.halfmove_clock >= 100:  # 50 moves = 100 half-moves
            return True
            
        # Insufficient material
        return self._has_insufficient_material()
    
    def _has_insufficient_material(self) -> bool:
        """Check if there's insufficient material for checkmate."""
        # Count pieces
        piece_counts = {"white": {}, "black": {}}
        for y in range(8):
            for x in range(8):
                piece = self.board.board[y][x]
                if piece:
                    color, p_type = piece
                    if p_type not in piece_counts[color]:
                        piece_counts[color][p_type] = 0
                    piece_counts[color][p_type] += 1
        
        # King vs King
        if len(piece_counts["white"]) == 1 and len(piece_counts["black"]) == 1:
            return True
            
        # King + minor piece vs King
        if (len(piece_counts["white"]) == 1 and 
            len(piece_counts["black"]) == 2 and 
            (piece_counts["black"].get("bishop", 0) == 1 or 
             piece_counts["black"].get("knight", 0) == 1)):
            return True
            
        if (len(piece_counts["black"]) == 1 and 
            len(piece_counts["white"]) == 2 and 
            (piece_counts["white"].get("bishop", 0) == 1 or 
             piece_counts["white"].get("knight", 0) == 1)):
            return True
            
        return False
    
    def would_be_in_check(self, start_pos: Tuple[int, int], end_pos: Tuple[int, int]) -> bool:
        """Check if moving a piece would result in the player's king being in check."""
        # Make temporary move
        original_piece = self.board.board[start_pos[1]][start_pos[0]]
        target_piece = self.board.board[end_pos[1]][end_pos[0]]
        
        # Execute move on board
        self.board.board[end_pos[1]][end_pos[0]] = original_piece
        self.board.board[start_pos[1]][start_pos[0]] = None
        
        # Check if king is in check
        in_check = self.is_in_check(self.current_turn)
        
        # Undo move
        self.board.board[start_pos[1]][start_pos[0]] = original_piece
        self.board.board[end_pos[1]][end_pos[0]] = target_piece
        
        return in_check
        
    def get_ai_move(self, difficulty: str = "easy") -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get an AI move based on the current board state and difficulty."""
        import random
        
        # Get all pieces of the current player
        player_pieces = []
        for y in range(8):
            for x in range(8):
                piece = self.board.board[y][x]
                if piece and piece[0] == self.current_turn:
                    player_pieces.append((x, y))
                    
        # No pieces left
        if not player_pieces:
            return None
            
        # Collect all legal moves
        all_moves = []
        for piece_pos in player_pieces:
            legal_moves = self.get_legal_moves(piece_pos)
            for move in legal_moves:
                all_moves.append((piece_pos, move))
                
        # No legal moves
        if not all_moves:
            return None
            
        # Easy: Random move
        if difficulty == "easy":
            return random.choice(all_moves)
            
        # Medium: Prioritize captures and checks
        elif difficulty == "medium":
            # Rate each move
            rated_moves = []
            for start, end in all_moves:
                score = 0
                
                # Check if it's a capture
                target = self.board.get_piece(end)
                if target:
                    piece = self.board.get_piece(start)
                    target_value = Piece(target[0], target[1]).get_piece_value()
                    piece_value = Piece(piece[0], piece[1]).get_piece_value()
                    
                    # Favor capturing high-value pieces with low-value pieces
                    score += target_value - piece_value/10
                
                # Check if move puts opponent in check
                self.board.move_piece(start, end)
                opponent = "white" if self.current_turn == "black" else "black"
                if self.is_in_check(opponent):
                    score += 1
                    
                    # Check for checkmate
                    old_turn = self.current_turn
                    self.current_turn = opponent
                    if self.is_checkmate():
                        score += 100  # Very high score for checkmate
                    self.current_turn = old_turn
                
                # Undo the move
                self.board.move_piece(end, start)
                if target:
                    self.board.board[end[1]][end[0]] = target
                
                rated_moves.append((start, end, score))
            
            # Sort by score and pick one of the top moves
            rated_moves.sort(key=lambda x: x[2], reverse=True)
            top_moves = rated_moves[:max(1, len(rated_moves)//3)]
            selected = random.choice(top_moves)
            return (selected[0], selected[1])
            
        # Hard: Add position evaluation and simple lookahead
        else:
            # More sophisticated AI would go here
            # For now, just use medium difficulty
            return self.get_ai_move("medium")
            
    def get_game_state_for_saving(self) -> Dict[str, Any]:
        """Prepare the current game state for saving to a file."""
        return {
            "board": [[self.board.board[y][x] for x in range(8)] for y in range(8)],
            "current_turn": self.current_turn,
            "game_state": self.game_state,
            "castle_rights": self.castle_rights,
            "move_history": self.move_history,
            "halfmove_clock": self.halfmove_clock,
            "fullmove_number": self.fullmove_number
        }
        
    def load_game_state(self, state: Dict[str, Any]) -> bool:
        """Load a game state from a saved dictionary."""
        try:
            # Reconstruct the board
            self.board = Board()
            for y in range(8):
                for x in range(8):
                    self.board.board[y][x] = state["board"][y][x]
                    
            # Load other state variables
            self.current_turn = state["current_turn"]
            self.game_state = state["game_state"]
            self.castle_rights = state["castle_rights"]
            self.move_history = state["move_history"]
            self.halfmove_clock = state["halfmove_clock"]
            self.fullmove_number = state["fullmove_number"]
            
            # Set last move if there's move history
            if self.move_history:
                self.last_move = self.move_history[-1]
            else:
                self.last_move = None
                
            return True
        except (KeyError, IndexError) as e:
            print(f"Error loading game state: {e}")
            return False