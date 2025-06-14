"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy
from random import shuffle

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
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] == X:
                x_counter += 1
            elif board[i][j] == O:
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
    actions = list()
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] == EMPTY:
                actions.append((i, j))
                
    shuffle(actions) # More random actions
    
    # Return indexes of a board with EMPTY fields
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid action")
    
    # Create deepcopy of board object to retain AI mechanics
    new_board = deepcopy(board)
    
    i, j = action
    
    # Return new board (i, j of action) based on player state (X or O)
    new_board[i][j] = player(new_board)
    
    return new_board


def check_row_col(board, player) -> bool:
    """
    For winner function to check if row
    or column is complete and return symbol.
    """
    # Board is square so ...
    for i in range(len(board)):
        
        # Checks if any row have exactly same symbol
        if board[i][0] == board[i][1] == board[i][2] == player:
            return True
        
        # Checks if any column have exactly same symbol
        elif board[0][i] == board[1][i] == board[2][i] == player:
            return True
        
    return False
            

def check_diag(board, player) -> bool:
    """
    For winner function to check if diagonal is complete and return symbol.
    
    Board indices:
   
   (0,0)| 0,1 |(0,2)
    ____|_____|____
        |     |               Diagonal win if list[0] or list[1]:
    1,0 |(1,1)| 1,2    ===>  [[(0,0), (1,1), (2,2)],
    ____|_____|____           [(2,0), (1,1), (0,2)]]
        |     |
   (2,0)| 2,1 |(2,2)
    """
            
    if board[0][0] == board[1][1] == board[2][2] == player:
        return True
    
    elif board[2][0] == board[1][1] == board[0][2] == player:
        return True
    
    return False


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if check_row_col(board, X) or check_diag(board, X):
        return X
    elif check_row_col(board, O) or check_diag(board, O):
        return O
    else:
        return None


def fast_win(board, player):
    """
    If AI can win instantly in next move, return action or False otherwise
    """
    for action in actions(board):
        board_next_move = result(board, action)
        if check_diag(board_next_move, player) or check_row_col(board_next_move, player):
            return action
    
    return False


def terminal(board) -> bool:
    """
    Returns True if game is over, False otherwise.
    """
    
    # 1. If there is a winner no matter which    
    if winner(board):
        return True
    
    # 2. If all spaces are empty, game still plays
    for i, row in enumerate(board):
        for j, col in enumerate(row):
            if board[i][j] == EMPTY:
                return False
            
    return True


def utility(board) -> int:
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    

def minimax(board: list[list, list, list]) -> tuple:
    """
    Returns the optimal action for the current player on the board.
    
    X - maximizer
    O - minimizer
    player(board) - X or O turn
    actions(board) - set of actions to make
    utility(board) - when terminal state: X = 1, O = -1, Tie = 0
    result(board, action) - new board based on state, action and
                            player turn already taken in this func
    """
    # Main board which will split into different result boards recursively depending
    # on player X or O
    
    
    # 1. If game over, then AI stops
    if terminal(board) == True:
        return None
        
    # 2. Recursive algorithm in functions minValue, maxValue independently
    # In this place, returning value must have some optimal moves and best
    # possible outcome of a game
    elif player(board) == X: # MAX player
        best_value, best_action = maxValue(board)
        
        # 2a. If in next AI will win, then return that action
        if action := fast_win(board, player=O):
            return action
        
    elif player(board) == O: # MIN player
        
        # 2b. If in next AI will win, then return that action
        if action := fast_win(board, player=O):
            return action
        
        best_value, best_action = minValue(board)
    
    return best_action
        
    # TODO -> A,B Pruning
    
def minValue(board) -> tuple:
    """
    Recursive reasoning:
    Returns value 1, 0 or -1 for minimizing possible terminal states of a game
    taken by player, who is trying to minimize outcome of this game
    """
    # Base case for maxValue function -> stops when recursion is complete it
    if terminal(board):
        return utility(board), None # None is essential since I can now call tuple as [0] index
    
    v = math.inf # Actions always better than this (for the first time)
    
    # Recursive alternating max and min functions
    for action in actions(board):
        v_new = min(v, maxValue(result(board, action))[0])
        
        # Keep track of best move and replacing utility return number
        if v_new < v:
            v = v_new
            best_move = action

    return v_new, best_move


def maxValue(board) -> tuple:
    """
    Recursive reasoning:
    Returns value 1, 0 or -1 for maximizing possible terminal states of a game
    taken by player, who is trying to minimize outcome of this game
    """
    # Base case for minValue function
    if terminal(board):
        return utility(board), None # None is essential since I can now call tuple as [0] index
    
    v = -math.inf # Actions always better than this (for the first time) -> stops when recursion is complete it
    
    # Recursive alternating max and min functions
    for action in actions(board):
        v_new = max(v, minValue(result(board, action))[0])
        
        # Keep track of best move and replacing utility return number
        if v_new > v:
            v = v_new
            best_move = action
  
    return v_new, best_move

