from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import chess


images = {}

squareStack = []

superStack = []


status = chess.Board()
pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK',
          'bp', 'br', 'bn', 'bb', 'bq', 'bk']

files = 'abcdefgh'
ranks = '12345678'

def chessboard(request):
    global status
    board = []
    for row in range(8):
        board_row = []

        for col in range(8):
            color = 'white' if (row + col) % 2 == 0 else 'black'
            position = files[7-col] + ranks[row]
            piece = status.piece_at(row * 8 + (7-col))
            if piece:
                piece_color = 'w' if piece.color == chess.WHITE else 'b'
                piece_type = piece.symbol().upper() if piece.color == chess.WHITE else piece.symbol()
                piece_key = f"{piece_color}{piece_type}"
                board_row.append({'color': color, 'piece': piece_key, 'pos': position})
            else:
                board_row.append({'color': color, 'piece': None, 'pos': position})
        
        board.append(board_row)

    return render(request, 'chessapp/chessboard.html', {'board': board})

@csrf_exempt
def select_square(request):
    global status
    global squareStack
    global superStack

    if request.method == 'POST':
        print(squareStack)
        print(superStack)

        data = json.loads(request.body)
        pos = data['pos']
        board = None
        print(f"Square selected: {pos}")
        
        if len(squareStack) < 2:
            superStack.append(pos)
            squareStack.append(pos)
        if (len(squareStack) == 2):
            # print(type(squareStack), flush=True)
            # print("Length of squareStack: ", len(squareStack), flush=True)
            # print("Source: ", squareStack[0], " Dest: ", squareStack[1], flush=True)
            move = None
            if (squareStack[0] != squareStack[1]):
                move = chess.Move.from_uci(squareStack[0] + squareStack[1])
                if not (move in status.legal_moves):
                    move = chess.Move.from_uci(squareStack[0] + squareStack[1] + 'q')

            if (move in status.legal_moves) and (squareStack[0] != squareStack[1]):
                print("valid move", flush=True)
                status.push(move)


                board = []
                for row in range(8):
                    board_row = []

                    for col in range(8):
                        color = 'white' if (row + col) % 2 == 0 else 'black'
                        position = files[7-col] + ranks[row]
                        piece = status.piece_at(row * 8 + (7-col))
                        if piece:
                            piece_color = 'w' if piece.color == chess.WHITE else 'b'
                            piece_type = piece.symbol().upper() if piece.color == chess.WHITE else piece.symbol()
                            piece_key = f"{piece_color}{piece_type}"
                            board_row.append({'color': color, 'piece': piece_key, 'pos': position})
                            # print(piece_key)
                        else:
                            board_row.append({'color': color, 'piece': None, 'pos': position})
                    
                    board.append(board_row)

                if status.is_checkmate():
                    if status.turn:
                        print("Black wins by Checkmate")  # Black wins
                        return JsonResponse({'success': True, 'board': board, 'game': 1} )
                    else:
                        print("White wins by Checkmate")  # White wins
                        return JsonResponse({'success': True, 'board': board, 'game': -1} )


                if status.is_stalemate() or status.is_insufficient_material():
                        print("Game ends with a tie")
                        return JsonResponse({'success': True, 'board': board, 'game': 0} )


            squareStack.clear()
        print(squareStack)
        return JsonResponse({'success': True, 'board': board, 'game': 2} )
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'})