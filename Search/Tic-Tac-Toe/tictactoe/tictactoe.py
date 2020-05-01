"""
Tic Tac Toe Player
"""

import math
import copy

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
    num_X = 0
    num_O = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                num_X += 1
            elif board[i][j] == O:
                num_O += 1

    return O if num_X > num_O else X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                actions.add((i, j))

    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    new_board = copy.deepcopy(board)
    if action is None or board[action[0]][action[1]] != EMPTY:
        raise Exception

    new_board[action[0]][action[1]] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    winner = vertical_winner(board)
    if winner is None:
        winner = horizontal_winner(board)
        if winner is None:
            winner = diagonal_winner(board)

    return winner


def horizontal_winner(board):

    for i in range(3):
        if board[i][0] is not None and board[i][0] == board[i][1] and board[i][1] == board[i][2]:
            return board[i][0]

    return None


def vertical_winner(board):

    for i in range(3):
        if board[0][i] is not None and board[0][i] == board[1][i] and board[1][i] == board[2][i]:
            return board[0][i]
    return None


def diagonal_winner(board):
    if board[1][1] is not None and ((board[0][0] == board[1][1] and board[1][1] == board[2][2]) or (
            board[2][0] == board[1][1] and board[1][1] == board[0][2])):
        return board[1][1]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """

    if winner(board) is not None:
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return False

    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    current_winner = winner(board)
    if current_winner == X:
        return 1
    elif current_winner == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return utility(board)

    is_max_player = player(board) == X

    if is_max_player:
        value = -99999
        current_action = None
        for action in actions(board):
            v = min_value_pruning(result(board, action), -9999, 9999)  # If max_player takes `action`, min_value returns the response from adversary min_player
            if v > value:
                value = v
                current_action = action

        return current_action
    else:  # is min_player
        value = 99999
        current_action = None
        for action in actions(board):
            v = max_value_pruning(result(board, action), -9999, 9999)  # If min_player takes `action`, max_value returns the response from adversary max_player
            if v < value:
                value = v
                current_action = action

        return current_action


# With pruning functions

def max_value_pruning(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = -9999

    for action in actions(board):
        v = max(v, min_value_pruning(result(board, action), alpha, beta))
        if v >= beta:
            return v
        alpha = max(alpha, v)
    return v


def min_value_pruning(board, alpha, beta):
    if terminal(board):
        return utility(board)
    v = 9999
    for action in actions(board):
        v = min(v, max_value_pruning(result(board, action), alpha, beta))
        if v <= alpha:
            return v
        beta = min(beta, v)
    return v

# Without pruning functions

def max_value(board):
    if terminal(board):
        return utility(board)
    v = -9999
    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    if terminal(board):
        return utility(board)
    v = 9999
    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v
