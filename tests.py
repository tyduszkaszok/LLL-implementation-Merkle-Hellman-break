import copy
import time
import random
from lattice_crypto import merkle_hellman_gen, encrypt, lo_lattice, lll, scalar_multi
import matplotlib.pyplot as plt

print("Analiza 1: Czas działania LLL w zależności od wymiarowości")
print(50 * "-")

msg_rng = random.Random(67)
ns = list(range(10, 65, 5)) 
execution_time_list = []

for n in ns:
    plain = [msg_rng.randrange(2) for _ in range(n)]
    
    a, w_secret, m_secret, r_secret = merkle_hellman_gen(n=n, seed=67, length=100)
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

#############################################################################################################

print("Analiza 2: Wpływ parametru Delta")
print(50 * "-")

n = 30
msg_rng = random.Random(21)  
plain = [msg_rng.randrange(2) for _ in range(n)]

a, w_secret, m_secret, r_secret = merkle_hellman_gen(n=n, seed=21, length=50)
S = encrypt(a, plain)
L = lo_lattice(a, S)
execution_time_list = []
deltas = [0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.99]

for delta in deltas: 
    L_copy = copy.deepcopy(L)
    
    start_time = time.time()
    L_reduced = lll(L_copy, delta=delta)
    end_time = time.time()
    
    length = float(scalar_multi(L_reduced[0], L_reduced[0])**0.5)
    execution_time = end_time - start_time
    execution_time_list.append(execution_time)
    
    print(f"Delta: {float(delta):.2f} | Długość wektora: {length:.4f} | Czas: {execution_time:.3f} s")

plt.figure(figsize=(10, 6))

plt.plot(deltas, execution_time_list, marker='o', color='purple', linewidth=2.5, label='Czas redukcji LLL')
plt.axvline(x=0.75, color='gray', linestyle='--', linewidth=1.5, label=r'Standardowe $\delta = 0.75$')
plt.title(r"Wpływ parametru Lovásza ($\delta$) na czas działania algorytmu LLL", fontsize=14, pad=10)
plt.xlabel(r"Parametr Lovásza ($\delta$)", fontsize=12)
plt.ylabel("Czas wykonania [sekundy]", fontsize=12)

plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=12)
plt.tight_layout()
plt.show()