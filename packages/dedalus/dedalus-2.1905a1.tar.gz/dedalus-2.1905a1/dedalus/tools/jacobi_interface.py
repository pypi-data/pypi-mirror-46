

import numpy as np
from scipy import sparse


def build_grid(N, a, b):
    return np.linspace(-1, 1, N)

def build_weights(N, a, b):
    return np.ones(N)

def conversion_matrix(N, a0, b0, a1, b1):
    return sparse.csr_matrix((N, N))

def differentiation_matrix(N, a, b):
    return sparse.csr_matrix((N, N))

def build_polynomials(M, a, b, grid):
    N = grid.size
    return np.zeros((M, N))







def interpolation_vector(N, a, b, x):
    return np.zeros(N)

def intergration_vector(N, a, b):
    return np.zeros(N)

def build_polynomials(M, a, b, grid):
    N = grid.size
    return np.zeros((M, N))
