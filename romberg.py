import math

def romberg(f, a, b, n):
    
    R = [[0.0] * n for _ in range(n)]

    R[0][0] = (b - a) * (f(a) + f(b)) / 2

    for i in range(1, n):

        m = 2 ** i
        h = (b - a) / m

        sum = 0

        for k in range(1, m, 2):
            sum += f(a + k * h)

        R[i][0] = 0.5 * R[i - 1][0] + h * sum

        for j in range(1, i + 1):
            R[i][j] = ( 4**j * R[i][j - 1] - R[i - 1][j - 1]) / (4**j - 1)

    return R