import chess

import chess

# Initialize a board to the starting position
board = chess.Board()

# Print the board
print(board)

print()
print()

# Making moves in standard notation
board.push_san("e4")
board.push_san("e5")
board.push_san("Nf3")
board.push_san("Nc6")
print(board)
print(board.__dict__)