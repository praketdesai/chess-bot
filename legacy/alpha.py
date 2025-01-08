
from best import evaluate_board

def minimax_alpha_beta(board, depth, alpha, beta, is_maximizing):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    if is_maximizing:
        max_eval = -float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth-1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break  # Beta cut-off
        return max_eval
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval = minimax_alpha_beta(board, depth-1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break  # Alpha cut-off
        return min_eval

def best_move_alpha_beta(board, depth):
    best_score = -float('inf')
    move_chosen = None
    alpha = -float('inf')
    beta = float('inf')
    for move in board.legal_moves:
        board.push(move)
        score = minimax_alpha_beta(board, depth-1, alpha, beta, False)
        board.pop()
        if score > best_score:
            best_score = score
            move_chosen = move
        alpha = max(alpha, score)
    return move_chosen