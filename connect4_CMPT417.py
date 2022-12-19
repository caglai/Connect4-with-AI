'''
CMPT 417 - Intelligent Systems 
Fall 2022 

Mahtab Rae, mnazari
Cagla Istanbulluoglu, cistanbu
Hareet Dhillon, hareetd

'''

'''
Connect 4 Game - 2 ML Players using different algorithm to play

1) MiniMax
2) Alpha-Beta MiniMax 
3) Genetic Algorithm MiniMax
4) Monte Carlo Search Tree

'''

'''
Resources

[1] Connect4-Python Visualization
https://github.com/KeithGalli/Connect4-Python

[2] Programming a Connect-4 game on Python
https://oscarnieves100.medium.com/programming-a-connect-4-game-on-python-f0e787a3a0cf

[3] Connect Four Game in Python
https://www.askpython.com/python/examples/connect-four-game#:~:text=The%20objective%20of%20the%20game,by%20playing%20the%20right%20moves

[4] The Rules of Connect 4
https://www.gamesver.com/the-rules-of-connect-4-according-to-m-bradley-hasbro/

[5] How to Program Connect 4 in Python!
https://www.youtube.com/watch?v=UYgyRArKDEs&t=29s

[6] Minimax
https://en.wikipedia.org/wiki/Minimax

[7] Minimax algorithm in python using tic tac toe
https://stackoverflow.com/questions/64644532/minimax-algorithm-in-python-using-tic-tac-toe

[8] Algorithms Explained – minimax and alpha-beta pruning
https://www.youtube.com/watch?v=l-hh51ncgDI

[9] MCTS algorithm exlained
http://fractalytics.io/application-of-mcts-within-the-connect4-game 

[10] MCTS algorithm exlained
https://github.com/Alfo5123/Connect4 


'''

'''
Rule 1 : 7 columns (or stacks) and 6 rows
Rule 2 : 2 players take turn placing pieces
Rule 3 : Moves can be horizantal and vertical
Rule 4 : Winner is who can stack 4 pieces of their own denomination horizontal, vertical or diagonal

'''
# ---------------------------
# Libraries
# ---------------------------
import numpy as np
import random
import pygame
import sys
import math

import mcts

# ---------------------------
# Global Variables
# ---------------------------
BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

PLAYER = 0
AI = 1

EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2

WINDOW_LENGTH = 4
SQUARESIZE = 100

# ---------------------------
# Connect4 Game Visualization
# ---------------------------
# Reference [1]

def create_board():
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT-1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score positive sloped diagonal
    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT-3):
        for c in range(COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0

def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations
'''
def pick_best_move(board, piece):

    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col
'''
def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):		
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == AI_PIECE: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()

# ---------------------------
# Extra functions needed
# ---------------------------
def evaluate(board):
    if is_winner(board):
        if winning_move(board, AI_PIECE):
            return 1
        if winning_move(board, PLAYER_PIECE):
            return -1
    else: 
        return 0 # Game Over
    return score_position(board, AI_PIECE)

def is_board_full(board):
    return len(get_valid_locations(board)) == 0

def is_winner(board):
    if winning_move(board, AI_PIECE) or winning_move(board, PLAYER_PIECE):
        return True
    else:
        return False

# ---------------------------
# Algorithms 
# ---------------------------
# 1) MiniMax
# 2) MiniMax Alpha - Beta
# 3) Genetics Algorithm MiniMax
# 4) Monte Carlo Search Tree (MCTS)
# ---------------------------

# Reference: [6] & [7] & [8]
def minimax(board, depth, maximizingPlayer):
    
    board_full = is_board_full(board)
    the_winner = is_winner(board)

    if (depth == 0 or board_full or  the_winner) :
        return (None, evaluate(board))
    
    children = get_valid_locations(board)
    column = children[0]

    if maximizingPlayer:
        maxValue = -math.inf
        column = random.choice(children)
        for col in children:
            board_copy = board.copy()
            new_evaluation = minimax(board_copy, depth-1, False)[1]
            if new_evaluation > maxValue:
                maxValue = new_evaluation
                column = col
        return column, maxValue
    
    else: #minimizingPlayer
        minValue = -math.inf
        column = random.choice(children)
        for col in children:
            board_copy = board.copy()
            new_evaluation = minimax(board_copy, depth-1, True)[1]
            if new_evaluation < minValue:
                minValue = new_evaluation
                column = col
        return column, minValue

# Reference: [6] & [7] & [8]
def minimaxab(board, depth, alpha, beta, maximizingPlayer):
    
    board_full = is_board_full(board)
    the_winner = is_winner(board)

    if (depth == 0 or board_full or  the_winner) :
        return (None, evaluate(board))
    
    children = get_valid_locations(board)
    column = children[0]

    if maximizingPlayer:
        maxValue = -math.inf
        column = random.choice(children) 
        for col in children:
            board_copy = board.copy()
            new_evaluation = minimaxab(board_copy, depth-1, alpha, beta, False)[1]
            if new_evaluation > maxValue:
                maxValue = new_evaluation
                column = col
            alpha = max(alpha, new_evaluation)
            if alpha >= beta:
                break
        return column, maxValue
    
    else: #minimizingPlayer
        minValue = -math.inf
        column = random.choice(children)
        for col in children:
            board_copy = board.copy()
            new_evaluation = minimaxab(board_copy, depth-1, alpha, beta, True)[1]
            if new_evaluation < minValue:
                minValue = new_evaluation
                column = col
            beta = min(beta, new_evaluation)
            if alpha >= beta:
                break            
        return column, minValue

# $$$: should be implemented by us
def genetics(board, depth,maximizingPlayer):
    pass

# Reference: [99] & [10]
def MCTS(board, depth, maximizingPlayer):
    return mcts.run(board, depth, maximizingPlayer)


# ---------------------------
# Run the Game
# ---------------------------
# $$$ Reference [1]:  should be implemented by us
# $$$ We need to implement making choices between players : 
# $$$ 1) 2 AI player with Genetics and Monte Carlo algorithms
# $$$ 2) 1 AI and 1 Human player with same algorithm ( choice between 4 algorithm )

board = create_board()
print_board(board)
game_over = False

pygame.init()

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            posx = event.pos[0]
            if turn == PLAYER:
                pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
            #print(event.pos)
            # Ask for Player 1 Input
            if turn == PLAYER:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, PLAYER_PIECE)

                    if winning_move(board, PLAYER_PIECE):
                        label = myfont.render("Player 1 wins!!", 1, RED)
                        screen.blit(label, (40,10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    print_board(board)
                    draw_board(board)


    # # Ask for Player 2 Input
    if turn == AI and not game_over:				

        #col = random.randint(0, COLUMN_COUNT-1)
        #col = pick_best_move(board, AI_PIECE)
        #col, score = minimaxab(board, ROW_COUNT-1, -math.inf, math.inf, True)
        # col, score = minimax(board, ROW_COUNT-1, True)
        col, score = MCTS(board, ROW_COUNT-1, True)

        if is_valid_location(board, col):
            #pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                screen.blit(label, (40,10))
                game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2

    if game_over:
        pygame.time.wait(3000)
