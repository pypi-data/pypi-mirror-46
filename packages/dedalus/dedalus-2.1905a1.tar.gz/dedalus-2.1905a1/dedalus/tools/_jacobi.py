import numpy             as np
import scipy             as sp
import scipy.sparse      as sparse
import scipy.linalg      as linear
import scipy.special     as fun
import matplotlib.pyplot as plt

dtype = np.float128

def sparse_symm_to_banded(matrix):
    """Convert sparse symmetric to upper-banded form."""
    diag = matrix.todia()
    B, I  = max(abs(diag.offsets)), diag.data.shape[1]
    banded = np.zeros((B+1, I), dtype=diag.dtype)
    for i, b in enumerate(diag.offsets):
        if b >= 0:
            banded[B-b] = diag.data[i]
    return banded

def grid_guess(Jacobi_matrix,symmetric=True):
    if symmetric:
        J_banded = sparse_symm_to_banded(Jacobi_matrix)
        return (np.sort(linear.eigvals_banded(J_banded).real)).astype(dtype)
    else:
        J_dense = Jacobi_matrix.todense()
        return (np.sort(linear.eigvals(J_dense).real)).astype(dtype)

def remainders(Jacobi_matrix,grid):

    J, z, N = sparse.dia_matrix(Jacobi_matrix).data, grid, len(grid)

    P = np.zeros((N,N),dtype=dtype)
    D = np.zeros((N,N),dtype=dtype)

    P[0] = np.ones(N,dtype=dtype)
    D[1] = P[0]/J[-1][1]

    if np.shape(J)[0] == 3:
        P[1]  = (z-J[1][0])*P[0]/J[-1][1]
        for n in range(2,N):
            P[n] = ((z-J[1][n-1])*P[n-1] - J[0][n-2]*P[n-2])/J[-1][n]
            D[n] = ((z-J[1][n-1])*D[n-1] - J[0][n-2]*D[n-2])/J[-1][n] + P[n-1]/J[-1][n]
        return ((z-J[1][N-1])*P[N-1] - J[0][N-2]*P[N-2]), ((z-J[1][N-1])*D[N-1] - J[0][N-2]*D[N-2]+P[N-1])

    P[1]  = z*P[0]/J[-1][1]
    for n in range(2,N):
        P[n] = (z*P[n-1] - J[0][n-2]*P[n-2])/J[-1][n]
        D[n] = (z*D[n-1] - J[0][n-2]*D[n-2])/J[-1][n] + P[n-1]/J[-1][n]

    # W = P[0]**2
    # for n in range(1,N):
    #     W += P[n]**2

    return (z*P[N-1] - J[0][N-2]*P[N-2]), (z*D[N-1] - J[0][N-2]*D[N-2] + P[N-1])

def gauss_quadrature(Jacobi_matrix,measure=1,niter=3,guess=None,report_error=False):

    if guess == None:
        z = grid_guess(Jacobi_matrix)
    else:
        z = guess

    for i in range(niter):
        P, D = remainders(Jacobi_matrix,z)
        if report_error: print(np.max(np.abs(P/D)))
        z = z - P/D

    w = 1/((1-z**2)*D**2)
    w = (measure/np.sum(w))*w

    return z, w

def three_term_recursion(Jacobi_matrix,grid,max_degree,init):

    J, z, N = sparse.dia_matrix(Jacobi_matrix).data, grid, max_degree+1

    P     = np.zeros((N,len(grid)),dtype=dtype)
    P[0]  = init

    if np.shape(J)[0] == 3:
        P[1]  = (z-J[1][0])*P[0]/J[-1][1]
        for n in range(2,N):
            P[n] = ((z-J[1][n-1])*P[n-1] - J[0][n-2]*P[n-2])/J[-1][n]
        return P

    P[1]  = z*P[0]/J[-1][1]
    for n in range(2,N):
        P[n] = (z*P[n-1] - J[0][n-2]*P[n-2])/J[-1][n]
    return P

def polish_norm(functions,weights):
    for k in range(len(functions)):
        functions[k] = functions[k]/np.sqrt(np.sum(weights*functions[k]**2))

def Jacobi_quadrature(max_degree,a,b,niter=3,report_error=False):

    mu = measure(a,b)
    J  = Jacobi_operator('J',a,b,max_degree)
    return gauss_quadrature(J,measure=mu,niter=niter,report_error=report_error)

def Jacobi_envelope(a,b,a0,b0,z):

    mu = measure(a,b)
    return np.exp( ((a-a0)/2)*np.log(1-z) + ((b-b0)/2)*np.log(1+z) )/np.sqrt(mu)

def Jacobi_recursion(max_degree,a,b,grid,init):

    J  = Jacobi_operator('J',a,b,max_degree)

    return three_term_recursion(J,grid,max_degree,init)

def push(operator,data):
    return (operator).dot(data)

def pull(operator,data):
    return (operator.transpose()).dot(data)

def measure(a,b):
    return np.exp( (a+b+1)*np.log(2) + fun.gammaln(a+1) + fun.gammaln(b+1) - fun.gammaln(a+b+2) )

def Jacobi_operator(op,a,b,max_degree):

    def diag(bands,locs):
        return sparse.dia_matrix((bands,locs),shape=(len(bands[0]),len(bands[0])))

    N = max_degree+1
    n = np.arange(0,N,dtype=dtype)
    na, nb, nab, nnab = n+a, n+b, n+a+b, 2*n+a+b

    # (1-z) <a,b| = <a-1,b| A-
    if op == 'A-' and (a>0):
        if a+b==0:
            middle = na/(2*n+1)
            lower  = (nb+1)/(2*n+1)
            middle[0]  = 2*a
        else:
            middle = 2*na*nab/(nnab*(nnab+1))
            lower  = 2*(n+1)*(nb+1)/((nnab+1)*(nnab+2))
        return diag([-np.sqrt(lower),np.sqrt(middle)],[-1,0])

    # <a,b| = <a+1,b| A+
    if op == 'A+':
        if a+b == 0 or a+b == -1:
            middle = (na+1)/(2*n+1)
            upper  = nb/(2*nab+1)
            middle[0], upper[0] = (1+a)*(1-(a+b)), 0
        else:
            middle = 2*(na+1)*(nab+1)/((nnab+1)*(nnab+2))
            upper  = 2*n*nb/(nnab*(nnab+1))
        return diag([np.sqrt(middle),-np.sqrt(upper)],[0,+1])

    # (1+z) <a,b| = <a,b-1| B-
    if op == 'B-' and (b > 0):
        if a+b == 0:
            middle = nb/(2*n+1)
            lower  = (na+1)/(2*n+1)
            middle[0] = 2*b
        else:
            middle = 2*nb*nab/(nnab*(nnab+1))
            lower  = 2*(n+1)*(na+1)/((nnab+1)*(nnab+2))
        return diag([np.sqrt(lower),np.sqrt(middle)],[-1,0])

    # <a,b| = <a,b+1| B+
    if op == 'B+':
        if a+b == 0 or a+b == -1:
            middle = (nb+1)/(2*n+1)
            upper  = na/(2*nab+1)
            middle[0], upper[0] = (1+b)*(1-(a+b)), 0
        else:
            middle = 2*(nb+1)*(nab+1)/((nnab+1)*(nnab+2))
            upper  = 2*n*na/(nnab*(nnab+1))
        return diag([np.sqrt(middle),np.sqrt(upper)],[0,+1])

    # ( a - (1-z)*d/dz ) <a,b| = <a-1,b+1| C-
    if op == 'C-' and (a > 0):
        return diag([np.sqrt(na*(nb+1))],[0])

    # ( b + (1+z)*d/dz ) <a,b| = <a+1,b-1| C+
    if op == 'C+' and (b > 0):
        return diag([np.sqrt((na+1)*nb)],[0])

    # ( a(1+z) - b(1-z) - (1-z^2)*d/dz ) <a,b| = <a-1,b-1| D-
    if op == 'D-' and (a > 0) and (b > 0):
        return diag([np.sqrt((n+1)*nab)],[-1])

    # d/dz <a,b| = <a+1,b+1| D+
    if op == 'D+':
        return diag([np.sqrt(n*(nab+1))],[+1])

    # z <a,b| = <a,b| J
    if op == 'J':
        A, B = Jacobi_operator('A+',a,b,max_degree), Jacobi_operator('B+',a,b,max_degree)
        return 0.5*( pull(B,B) - pull(A,A) )

    if op == 'z=+1':
        operator = np.sqrt(nnab+1)*np.sqrt(fun.binom(na,a))*np.sqrt(fun.binom(nab,a))
        if a+b==-1:
            operator[0] = np.sqrt(np.sin(np.pi*np.abs(a))/np.pi)
        return operator

    if op == 'z=-1':
        operator = ((-1)**n)*np.sqrt(nnab+1)*np.sqrt(fun.binom(nb,b))*np.sqrt(fun.binom(nab,b))
        if a+b==-1:
            operator[0] = np.sqrt(np.sin(np.pi*np.abs(b))/np.pi)
        return operator



# Interfacing with Dedalus
output_dtype = np.float64

def build_grid(N, a, b):
    grid, weights = Jacobi_quadrature(N-1, a, b)
    return grid.astype(output_dtype)

def build_weights(N, a, b):
    grid, weights = Jacobi_quadrature(N-1, a, b)
    return weights.astype(output_dtype)

def build_polynomials(M, a, b, grid):
    init = Jacobi_envelope(a, b, a, b, grid)
    poly = Jacobi_recursion(M-1, a, b, grid, init)
    return poly.astype(output_dtype)

def conversion_matrix(N, a0, b0, a1, b1):
    if not (a1-a0).is_integer():
        raise ValueError("a0 and a1 must be integer-separated")
    if not (b1-b0).is_integer():
        raise ValueError("b0 and b1 must be integer-separated")
    if a0 > a1:
        raise ValueError("a0 must be less than or equal to a1")
    if b0 > b1:
        raise ValueError("b0 must be less than or equal to b1")

    conv = sparse.identity(N).tocsr()
    for da in range(int(a1-a0)):
        Ap = Jacobi_operator('A+', a0+da, b0, N-1).tocsr()
        conv = Ap * conv
    for db in range(int(b1-b0)):
        Bp = Jacobi_operator('B+', a1, b0+db, N-1).tocsr()
        conv = Bp * conv
    return conv.tocsr().astype(output_dtype)

def differentiation_matrix(N, a, b):
    diff = Jacobi_operator('D+', a, b, N-1)
    return diff.tocsr().astype(output_dtype)

def jacobi_matrix(N, a, b):
    J = Jacobi_operator('J', a, b, N-1)
    return J.tocsr().astype(output_dtype)

def interpolation_vector(N, a, b, x):
    J = Jacobi_operator('J', a, b, N-1)
    if np.isscalar(x):
        x = np.array([x])
    interp = three_term_recursion(J, x, N-1, 1)
    return interp.T.copy().astype(output_dtype)
