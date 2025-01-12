import numpy as np


def vertical_lines(array):
    n_cols = len(array[0])
    n_rows = len(array)
    return [[array[j][i] for j in range(n_rows)] for i in range(n_cols)]


def diagonals(array, reverse=False):
    if reverse:
        for row in array:
            row.reverse()
    n_cols = len(array[0])
    n_rows = len(array)
    return [np.diagonal(array, offset=i) for i in range(1 - n_rows, n_cols)]


def reverse_lines(lines):
    reversed_lines = lines.copy()
    for line in reversed_lines:
        line.reverse()
    return reversed_lines
