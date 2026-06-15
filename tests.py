import copy
import time
import random
from lattice_crypto import merkle_hellman_gen, encrypt, lo_lattice, lll, scalar_multi
import matplotlib.pyplot as plt

print("Analiza LLL od wymiarowości")
print(50 * "-")

msg_rng = random.Random(67)
ns = list(range(10, 65, 5)) 
execution_time_list = []

for n in ns:
    plain = [msg_rng.randrange(2) for _ in range(n)]
    
    a, w_secret, m_secret, r_secret = merkle_hellman_gen(n=n, target_bits=60, seed=67, length=100)
    S = encrypt(a, plain)
    L = lo_lattice(a, S)
    
    start_time = time.time()
    L_reduced = lll(L, delta=0.75)
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"Wymiar: {n:2d} | Czas trwania: {execution_time:.3f} s")
    execution_time_list.append(execution_time)

n_max = ns[-1]
t_max = execution_time_list[-1]

C4 = t_max / (n_max ** 4)
theo_O4 = [C4 * (n ** 4) for n in ns] 

plt.figure(figsize=(10, 6))
plt.plot(ns, execution_time_list, marker='o', color='blue', linewidth=2.5, label='Czas rzeczywisty')
plt.plot(ns, theo_O4, linestyle='--', color='orange', linewidth=2, label=r'Złożoność teoretyczna operacji $\mathcal{O}(n^4)$') # pominięcie logarytmu - bo B stałe (100)
plt.title(r"Złożoność obliczeniowa LLL (przy stałej wielkości współczynników $B \approx 2^{100}$)", fontsize=14, pad=10)
plt.xlabel("Wymiar kraty (n)", fontsize=12)
plt.ylabel("Czas wykonania [sekundy]", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=12)

plt.tight_layout()
plt.show()