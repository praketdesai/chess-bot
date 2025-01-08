import os
import time
os.environ["SDL_AUDIODRIVER"] = "dummy"
from alpha import best_move_alpha_beta
# we did this to ignore audio cause we don't need that

import random

# Generate a random integer between 1 and 10 (inclusive)

import chess
import pygame

# Initialize pygame
pygame.init()

# Set up display
width, height = 480, 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Chess Board')

# Load images
images = {}
pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK',
          'bp', 'br', 'bn', 'bb', 'bq', 'bk']
for piece in pieces:
    images[piece] = pygame.image.load(f"../images/{piece}.png")

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

board = chess.Board()



def draw_board(screen):
    """Draw the chessboard and pieces."""
    colors = [pygame.Color("white"), pygame.Color("gray")]
    square_size = width // 8
    for r in range(8):
        for c in range(8):
            color = colors[(r + c) % 2]
            pygame.draw.rect(screen, color, pygame.Rect(c * square_size, r * square_size, square_size, square_size))
            piece = board.piece_at(r * 8 + c)
            if piece:
                piece_color = 'w' if piece.color == chess.WHITE else 'b'
                piece_type = piece.symbol().upper() if piece.color == chess.WHITE else piece.symbol()
                piece_key = f"{piece_color}{piece_type}"
                screen.blit(images[piece_key], pygame.Rect(c * square_size, r * square_size, square_size, square_size))


def handle_text_input(events, active, user_text):
    """Handle text input from the user."""
    for event in events:
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
            else:
                active = False

        if active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                user_text = user_text[:-1]
            elif event.key == pygame.K_RETURN:
                print(f"Entered text: {user_text}")
                try:
                    board.push_san(user_text)
                    if board.is_checkmate():
                        if board.turn:
                            return -9999  # Black wins
                        else:
                            return 9999   # White wins
                    if board.is_stalemate() or board.is_insufficient_material():
                        return 0
                    time.sleep(.25)
                    board.push(best_move_alpha_beta(board, 3))

                except:
                    user_text = ""
                    print("Invalid move")

                user_text = ""
            else:
                user_text += event.unicode

    return active, user_text


def botbot():
    if board.is_checkmate():
        if board.turn:
            return -9999  # Black wins
        else:
            return 9999   # White wins
    if board.is_stalemate() or board.is_insufficient_material():
        return 0
    index = 0
    time.sleep(.25)
    board.push(best_move_alpha_beta(board, 3))

    index += 1
    pygame.display.flip()

def draw_input_box(screen, active, user_text):
    """Draw the input box and display the user's text."""
    input_color = BLACK if active else GRAY
    pygame.draw.rect(screen, input_color, input_box, 2)

    text_surface = font.render(user_text, True, BLACK)
    screen.blit(text_surface, (input_box.x + 10, input_box.y + 10))
    return user_text


# Input box setup
font = pygame.font.Font(None, 48)
input_box = pygame.Rect(10, 500, 460, 50)  # Input box position and size
user_text = ""
active = False  # Tracks whether the input box is active
board.push(best_move_alpha_beta(board, 3))

# Initialize the chess board

# Main loop
running = True
while running:
    events = pygame.event.get()  # Gather all events
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # Draw everything
    window.fill(WHITE)
    draw_board(window)
    active, user_text = handle_text_input(events, active, user_text)
    draw_input_box(window, active, user_text)
    # botbot()
    # if (not active):
    #     board.push_san(user_text)

    pygame.display.flip()

pygame.quit()
