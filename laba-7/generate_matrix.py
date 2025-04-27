import random

def generate_matrix(rows=16, cols=16):
    matrix = [[random.randint(0, 1) for _ in range(cols)] for _ in range(rows)]
    return matrix

def print_matrix(matrix):
    for row in matrix:
        print(' '.join(map(str, row)))
