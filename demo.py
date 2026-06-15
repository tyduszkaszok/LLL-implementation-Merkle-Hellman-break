import numpy as np
import math 
import random
from lattice_crypto import merkle_hellman_gen, encrypt, lo_lattice, lll, bits_from_short_vec, hadamard_ratio

print("Pokaz projektu: ")
msg_rng = random.Random(42)
ns = [10, 30, 60]
length = 60
for i in range(0, 3):
    print(f"Przykład nr {i+1}")
    n = ns[i]
    print(f"Długość wiadomości: {n}")
    plain = [msg_rng.randrange(2) for _ in range(n)]
    a, w_secret, m_secret, r_secret = merkle_hellman_gen(n=n, seed=42, length=length)
    S = encrypt(a, plain)
    L = lo_lattice(a, S)
    d = round(n / math.log2(max(a)), 4)
    print(f"Gęstość: {d}")
    print(f"Skośność początkowej bazy: {hadamard_ratio(L):.3f}")
    L_reduced = lll(L, delta=0.75)
    print(f"Skośność zredukowanej bazy: {hadamard_ratio(L_reduced):.3f}")

    recovered = None
    for row in L_reduced:
        if abs(row[-1]) > 1e-6: 
            continue  
        bits = bits_from_short_vec(row, n)
        if bits is None: 
            bits = bits_from_short_vec([-x for x in row], n)
        if bits is not None: 
            recovered = bits; break
    print(f"Szyfrogram: {S}")
    print(f'Wiadomość zdeszyfrowana = {recovered}')
    print(f'Wiadomość oryginalna = {plain}')
    if recovered == plain:
        print('Łamanie zakończone sukcesem!')
    else:
        print('Niepowodzenie!')

    print()
    print(50*"=")
    print()
