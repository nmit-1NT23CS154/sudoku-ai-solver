import copy

def is_valid(board, r, c, num):
    for i in range(9):
        if board[r][i] == num or board[i][c] == num:
            return False

    sr, sc = 3*(r//3), 3*(c//3)

    for i in range(3):
        for j in range(3):
            if board[sr+i][sc+j] == num:
                return False

    return True


def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                return r, c
    return None


def solve(board):
    empty = find_empty(board)
    if not empty:
        return True

    r, c = empty

    for num in range(1, 10):
        if is_valid(board, r, c, num):
            board[r][c] = num
            if solve(board):
                return True
            board[r][c] = 0

    return False


def get_solution(board):
    new_board = copy.deepcopy(board)
    solve(new_board)
    return new_board