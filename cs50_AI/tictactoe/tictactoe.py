"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_counter = 0
    o_counter = 0
    for row in board:
        for col in row:
            if board[row][col] == X:
                x_counter += 1
            elif board[row][col] == O:
                o_counter += 1
    
    if x_counter > o_counter:
        return O
    else:
        # Always first in initial game and alternates
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] == EMPTY:
                actions.add((i, j))
                
    # Return indexes of a board with EMPTY fields
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid action")
    
    # Create deepcopy of board object to retain AI mechanics
    board = deepcopy(board)
    
    i, j = action
    
    # Return new board (i, j of action) based on player action (X or O)
    board[i][j] = player(action)


def check_col(board):
    pass# TODO

def check_row(board):
    pass# TODO

def check_diag(board):
    pass# TODO


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if check_col or check_row or check_diag:
        return X
        return O
    else:
        return None
    # TODO
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            pass


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    
    # 1. If there is a winner    
    if winner(board) == X or winner(board) == O:
        return True
    
    # 2. If all spaces are empty, game still plays
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] == EMPTY:
                return False
            
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            pass


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # TODO
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            pass
        