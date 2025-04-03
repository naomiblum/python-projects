import chess
import chess.svg
import os

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_board(board):
    """Print the chess board in ASCII format."""
    print("  a b c d e f g h")
    print(" +-----------------+")
    for i in range(8):
        rank = 8 - i
        print(f"{rank}| ", end="")
        for j in range(8):
            piece = board.piece_at(chess.square(j, 7 - i))
            if piece is None:
                print(". ", end="")
            else:
                print(f"{piece.symbol()} ", end="")
        print(f"|{rank}")
    print(" +-----------------+")
    print("  a b c d e f g h")

def main():
    # Create a new chess board
    board = chess.Board()
    
    # Game loop
    while not board.is_game_over():
        clear_screen()
        print_board(board)
        
        # Show whose turn it is
        print(f"\n{'White' if board.turn else 'Black'} to move")
        
        # Get user move
        move_str = input("\nEnter your move (e.g., 'e2e4'): ")
        
        try:
            # Parse move
            move = chess.Move.from_uci(move_str)
            
            # Check if the move is legal
            if move in board.legal_moves:
                board.push(move)
            else:
                input("Illegal move! Press Enter to continue...")
        except:
            input("Invalid input! Press Enter to continue...")
    
    # Game over
    clear_screen()
    print_board(board)
    print("\nGame over!")
    
    # Show result
    if board.is_checkmate():
        winner = "Black" if board.turn else "White"
        print(f"{winner} wins by checkmate!")
    elif board.is_stalemate():
        print("Draw by stalemate!")
    elif board.is_insufficient_material():
        print("Draw by insufficient material!")
    elif board.is_seventyfive_moves():
        print("Draw by 75-move rule!")
    elif board.is_fivefold_repetition():
        print("Draw by fivefold repetition!")
    else:
        print("Draw!")

if __name__ == "__main__":
    main()
