import chess
import chess.engine

def evaluate_board(board):
    # Simple evaluation: material count
    if board.is_checkmate():
        if board.turn:
            return -9999  # Black wins
        else:
            return 9999   # White wins
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # Define piece values
    values = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0
    }

    score = 0
    for piece_type in values:
        score += len(board.pieces(piece_type, chess.WHITE)) * values[piece_type]
        score -= len(board.pieces(piece_type, chess.BLACK)) * values[piece_type]
    return score

def minimax(board, depth, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if is_maximizing:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, False)
            board.pop()
            max_eval = max(max_eval, eval)
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth-1, True)
            board.pop()
            min_eval = min(min_eval, eval)
        return min_eval

def best_move(board, depth):
    best_score = -float('inf')
    move_chosen = None
    for move in board.legal_moves:
        board.push(move)
        score = minimax(board, depth-1, False)
        board.pop()
        if score > best_score:
            best_score = score
            move_chosen = move
    return move_chosen

# Example usage
board = chess.Board()
move = best_move(board, depth=3)
print("Best move:", board.san(move))