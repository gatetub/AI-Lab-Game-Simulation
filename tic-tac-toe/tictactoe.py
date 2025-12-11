"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():

    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    
    if x_count > o_count:
        return O
    else:
        return X

def actions(board):
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY}


def result(board, action):
    if action not in actions(board):
        raise ValueError("Invalid action")
    
    new_board = [row[:] for row in board]  # Deep copy of the board
    current_player = player(board)
    new_board[action[0]][action[1]] = current_player
    return new_board


def winner(board):
    
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    
    return None


def terminal(board):
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)


def utility(board):
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

def minimax(board):
    if terminal(board):
        return None
    
    current_player = player(board)
    
    if current_player == X:
        best_value = -math.inf
        best_action = None
        for action in actions(board):
            value = minimax_value(result(board, action))
            if value > best_value:
                best_value = value
                best_action = action
        return best_action
    else:
        best_value = math.inf
        best_action = None
        for action in actions(board):
            value = minimax_value(result(board, action))
            if value < best_value:
                best_value = value
                best_action = action
        return best_action

def minimax_value(board):
    if terminal(board):
        return utility(board)
    
    if player(board) == X:
        value = -math.inf
        for action in actions(board):
            value = max(value, minimax_value(result(board, action)))
        return value
    else:
        value = math.inf
        for action in actions(board):
            value = min(value, minimax_value(result(board, action)))
        return value