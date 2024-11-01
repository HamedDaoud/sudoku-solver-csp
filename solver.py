import numpy as np
from collections import deque

def initialize_domains(board):
    domains = {}
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                domains[(i, j)] = set(range(1, 10))
            else:
                domains[(i, j)] = {board[i][j]}
    return domains

# AC-3 Functions
def apply_ac3_algorithm(domains):
    queue = deque([(xi, xj) for xi in domains for xj in get_neighboring_cells(xi)])
    while queue:
        (xi, xj) = queue.popleft()
        if apply_revision(domains, xi, xj):
            if len(domains[xi]) == 0:
                return False
            for xk in get_neighboring_cells(xi) - {xj}:
                queue.append((xk, xi))
    return True

def apply_revision(domains, xi, xj):
    revised = False
    for x in set(domains[xi]):
        if not any(is_value_consistent(x, y) for y in domains[xj]):
            domains[xi].remove(x)
            revised = True
    return revised

def is_value_consistent(x, y):
    return x != y

def get_neighboring_cells(cell):
    row, col = cell
    neighbors = set()
    for i in range(9):
        if i != col:
            neighbors.add((row, i))
        if i != row:
            neighbors.add((i, col))
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if (i, j) != cell:
                neighbors.add((i, j))
    return neighbors

# Backtracking Search Functions
def find_best_empty_location(board, domains):
    min_remaining_values = 10 # MRV
    best_cell = None
    for (row, col), domain in domains.items():
        if board[row][col] == 0 and len(domain) < min_remaining_values:
            min_remaining_values = len(domain)
            best_cell = (row, col)
    return best_cell

def is_value_safe(board, row, col, num):
    if num in board[row] or num in board[:, col]:
        return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    if num in board[start_row:start_row + 3, start_col:start_col + 3]:
        return False
    return True

def apply_forward_checking(domains, row, col, value):
    new_domains = {k: v.copy() for k, v in domains.items()}
    new_domains[(row, col)] = {value}
    for i in range(9):
        if (row, i) in new_domains and i != col:
            new_domains[(row, i)].discard(value)
            if len(new_domains[(row, i)]) == 0:
                return None
        if (i, col) in new_domains and i != row:
            new_domains[(i, col)].discard(value)
            if len(new_domains[(i, col)]) == 0:
                return None
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if (i, j) in new_domains and (i, j) != (row, col):
                new_domains[(i, j)].discard(value)
                if len(new_domains[(i, j)]) == 0:
                    return None
    return new_domains

def apply_backtracking_with_forward_checking(board, domains):
    empty_loc = find_best_empty_location(board, domains)
    if not empty_loc:
        return True
    row, col = empty_loc
    values = sorted(domains[(row, col)], key=lambda val: least_constraining_value_heuristic(board, row, col, val))
    
    for value in values:
        if is_value_safe(board, row, col, value):
            board[row][col] = value
            new_domains = apply_forward_checking(domains, row, col, value)
            if new_domains is not None and apply_backtracking_with_forward_checking(board, new_domains):
                return True
            board[row][col] = 0
    return False

# Heuristic Functions
def least_constraining_value_heuristic(board, row, col, value):
    constraint_count = 0
    for i in range(9):
        if board[row][i] == 0 and value in board[row]:
            constraint_count += 1
        if board[i][col] == 0 and value in board[:, col]:
            constraint_count += 1
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == 0 and value in board[start_row:start_row + 3, start_col:start_col + 3]:
                constraint_count += 1
    return constraint_count


# Solve Sudoku function
def solve_sudoku(board):
    board_np = np.array(board)
    domains = initialize_domains(board_np)
    if apply_ac3_algorithm(domains) and apply_backtracking_with_forward_checking(board_np, domains):
        return board_np.tolist()
    return None