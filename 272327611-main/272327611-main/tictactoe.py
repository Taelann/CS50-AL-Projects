
"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY]
    ]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)

    if x_count == o_count:
        return X

    return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))

    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise ValueError("Invalid action")

    new_board = [row[:] for row in board]

    i, j = action
    new_board[i][j] = player(board)

    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not EMPTY:
            return row[0]

    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j]:
            if board[0][j] is not EMPTY:
                return board[0][j]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2]:
        if board[0][0] is not EMPTY:
            return board[0][0]

    if board[0][2] == board[1][1] == board[2][0]:
        if board[0][2] is not EMPTY:
            return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    for row in board:
        if EMPTY in row:
            return False

    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    game_winner = winner(board)

    if game_winner == X:
        return 1

    if game_winner == O:
        return -1

    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        best_value = -math.inf
        best_action = None

        for action in actions(board):
            new_board = result(board, action)
            value = min_value(new_board)

            if value > best_value:
                best_value = value
                best_action = action

        return best_action

    else:
        best_value = math.inf
        best_action = None

        for action in actions(board):
            new_board = result(board, action)
            value = max_value(new_board)

            if value < best_value:
                best_value = value
                best_action = action

        return best_action


def max_value(board):
    """
    Returns the maximum utility achievable by X.
    """
    if terminal(board):
        return utility(board)

    value = -math.inf

    for action in actions(board):
        new_board = result(board, action)
        value = max(value, min_value(new_board))

    return value


def min_value(board):
    """
    Returns the minimum utility achievable by O.
    """
    if terminal(board):
        return utility(board)

    value = math.inf

    for action in actions(board):
        new_board = result(board, action)
        value = min(value, max_value(new_board))

    return value
