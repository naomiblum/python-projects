import os
import sys

class SimplePiece:
    def __init__(self, color, piece_type):
        self.color = color
        self.type = piece_type
        
    def __str__(self):
        symbols = {
            'white': {'pawn': '♙', 'rook': '♖', 'knight': '♘', 'bishop': '♗', 'queen': '♕', 'king': '♔'},
            'black': {'pawn': '♟', 'rook': '♜', 'knight': '♞', 'bishop': '♝', 'queen': '♛', 'king': '♚'}
        }
        return symbols[self.color][self.type]

class SimpleBoard:
    def __init__(self):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()
        
    def setup_pieces(self):
        # Set up pawns
        for col in range(8):
            self.board[1][col] = SimplePiece('black', 'pawn')
            self.board[6][col] = SimplePiece('white', 'pawn')
            
        # Set up other pieces
        back_row = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for col in range(8):
            self.board[0][col] = SimplePiece('black', back_row[col])
            self.board[7][col] = SimplePiece('white', back_row[col])
    
    def get_piece(self, row, col):
        if 0 <= row < 8 and 0 <= col < 8:
            return self.board[row][col]
        return None
    
    def move_piece(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        if not (0 <= from_row < 8 and 0 <= from_col < 8 and 0 <= to_row < 8 and 0 <= to_col < 8):
            return False
            
        piece = self.board[from_row][from_col]
        if piece is None:
            return False
            
        # Simple move (no rule checking)
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = None
        return True

class SimpleChessGame:
    def __init__(self):
        self.board = SimpleBoard()
        self.current_player = 'white'
        
    def display_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n  Simple Chess Game\n")
        print("    a b c d e f g h")
        print("  +-----------------+")
        
        for row in range(8):
            print(f"{8-row} | ", end="")
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece:
                    print(f"{piece} ", end="")
                else:
                    # Alternating colors for empty squares
                    print("· " if (row + col) % 2 == 0 else "· ", end="")
            print(f"| {8-row}")
            
        print("  +-----------------+")
        print("    a b c d e f g h")
        print(f"\nCurrent player: {self.current_player}")
    
    def parse_position(self, pos_str):
        if len(pos_str) != 2:
            return None
        col = ord(pos_str[0].lower()) - ord('a')
        row = 8 - int(pos_str[1])
        if 0 <= row < 8 and 0 <= col < 8:
            return row, col
        return None
    
    def play(self):
        while True:
            self.display_board()
            print("\nEnter move (e.g., 'e2 e4') or 'q' to quit:")
            move = input("> ").strip().lower()
            
            if move == 'q':
                print("Thanks for playing!")
                break
                
            parts = move.split()
            if len(parts) != 2:
                print("Invalid format. Use 'e2 e4' format.")
                input("Press Enter to continue...")
                continue
                
            from_pos = self.parse_position(parts[0])
            to_pos = self.parse_position(parts[1])
            
            if from_pos is None or to_pos is None:
                print("Invalid position.")
                input("Press Enter to continue...")
                continue
            
            piece = self.board.get_piece(*from_pos)
            if piece is None:
                print("No piece at that position.")
                input("Press Enter to continue...")
                continue
                
            if piece.color != self.current_player:
                print(f"It's {self.current_player}'s turn.")
                input("Press Enter to continue...")
                continue
            
            if self.board.move_piece(from_pos, to_pos):
                # Switch player after successful move
                self.current_player = 'black' if self.current_player == 'white' else 'white'
            else:
                print("Invalid move.")
                input("Press Enter to continue...")

if __name__ == "__main__":
    game = SimpleChessGame()
    game.play()
