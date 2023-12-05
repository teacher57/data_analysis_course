from numpy import array, zeros
def f(A, row, col):
    B = zeros((len(A) - 1, len(A[0]) - 1))
    a, b = 0, 0
    for i in range(len(A)):
        if i != row:
            b = 0
            for j in range(len(A[i])):
                if j != col:
                    B[i - a][j - b] = A[i][j]
                    
                else:
                    b = 1
        else:
            a = 1
    return B[0][0] * B[1][1] - B[0][1] * B[1][0]
