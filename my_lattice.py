B = [[2137, 67], [3.0, 1.0]]
import numpy as np
def scalar_multi(v1, v2):
    sum = 0
    for v1_i, v2_i in zip(v1, v2):
        sum += v1_i * v2_i
    return sum

def gram_schmidt(B):
    n = len(B[0])
    B_good = [B[0]]
    for b_vec in B[1:]:
        mu = [scalar_multi(b_vec, b_good)/scalar_multi(b_good, b_good) for b_good in B_good]
        for m, b_vec_good in enumerate(B_good):
            for i in range(n):
                b_vec[i] = b_vec[i] - mu[m]*b_vec_good[i]
        B_good.append(b_vec)
    return B_good

print(gram_schmidt(B))


def gram_schmidt(B):
    B = np.array(B, dtype=float)
    n = B.shape[0]
    Bs = np.zeros_like(B)
    mu = np.zeros((n, n))
    for i in range(n):
        Bs[i] = B[i].copy()
        for j in range(i):
            denom = float(Bs[j] @ Bs[j])
            mu[i, j] = float(B[i] @ B[j]) / denom if denom > 0 else 0.0
            Bs[i] = Bs[i] - mu[i, j]*Bs[j]
    return Bs, mu

# Sanity check: B*[i] is orthogonal to B*[j] for j < i.
Bs, mu = gram_schmidt(B)
print('B  =', Bs)