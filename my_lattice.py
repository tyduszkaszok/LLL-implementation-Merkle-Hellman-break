B = [[1, 5, 1],[4, 2, 1],[1, 4, 1]]

import numpy as np
def hadamard_ratio(B):
    B = np.array(B, dtype=float)
    n = B.shape[0]
    det = abs(np.linalg.det(B))
    norms_prod = np.prod(np.linalg.norm(B, axis=1))
    if norms_prod == 0: return 0.0
    return (det / norms_prod) ** (1.0 / n)

#no numpy

def scalar_multi(v1, v2):
    return sum(x * y for x, y in zip(v1, v2))

def gram_schmidt(B):
    n = len(B)
    B_good = []
    mus = [[0 for _ in range(n)] for _ in range(n)]
    for i, b_vec in enumerate(B):
        b_vec_good = list(b_vec)
        for j, prev in enumerate(B_good):
            mu = scalar_multi(b_vec, prev) / scalar_multi(prev, prev)
            mus[i][j] = mu
            b_vec_good = [bg - mu * p for bg, p in zip(b_vec_good, prev)]
        B_good.append(b_vec_good)
    return B_good, mus

B_good, mus = gram_schmidt(B)


def lll(B, delta=0.75):
    k = 1
    n = len(B)
    B_good, mu = gram_schmidt(B)

    def size_reduce():
        for i in range(k-1, -1, -1):
            if abs(mu[k][i]) > 0.5:
                r = round(mu[k][i])
                B[k] = [bk_elem - r * bi_elem for bk_elem, bi_elem in zip(B[k], B[i])]
                for j in range(i):
                    mu[k][j] -= r * mu[i][j]
                mu[k][i] -= r

    while k < n:
        size_reduce()
        
        lhs = scalar_multi(B_good[k], B_good[k]) + (mu[k][k-1]**2) * scalar_multi(B_good[k-1], B_good[k-1])
        rhs = delta * scalar_multi(B_good[k-1], B_good[k-1])

        if lhs < rhs:
            B[k], B[k-1] = B[k-1], B[k]
            B_good, mu = gram_schmidt(B)
            k = max(k - 1, 1)
        else:
            k = k + 1
            
    return B

print(f"Old base vectors: {B}")
print(f"Hamard ratio: {hadamard_ratio(B)}")
print()
B_new = lll(B)
print(f"New base vectors: {B_new}")
print(f"Hamard ratio: {hadamard_ratio(B_new)}")