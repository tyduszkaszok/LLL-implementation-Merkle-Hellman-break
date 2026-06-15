import numpy as np
import random
import math

def hadamard_ratio(B): # współczynnik Hadamarda
    n = len(B)
    B_np = np.array(B, dtype=float)
    sign, log_det = np.linalg.slogdet(B_np)
    if sign == 0: 
        return 0.0
    log_norms_sum = 0
    for row in B:
        sq_norm = sum(int(x)**2 for x in row) 
        if sq_norm == 0: 
            return 0.0
        log_norms_sum += 0.5 * math.log(sq_norm)
    try:
        return math.exp((log_det - log_norms_sum) / n)
    except OverflowError:
        return 0.0

def scalar_multi(v1, v2): # iloczyn skalarny dwóch wektorów
    return sum(x * y for x, y in zip(v1, v2))

def gram_schmidt(B): # ortogonalizacja Grama-Schmidta
    n = len(B) # liczba wektorów bazy
    B_good = [] # nowa, "dobra" baza
    mus = [[0 for _ in range(n)] for _ in range(n)] # macierz współczynników rzutowania mu
    for i, b_vec in enumerate(B): # przechodzenie wierszami, czyli wektorami starej bazy
        b_vec_good = list(b_vec)
        for j, prev in enumerate(B_good): # pobieranie zortogonalizowanych już wektorów
            mu = scalar_multi(b_vec, prev) / scalar_multi(prev, prev) # obliczanie mu z każdym poprzedzającym wektorem nowej bazy
            mus[i][j] = mu
            b_vec_good = [bg - mu * p for bg, p in zip(b_vec_good, prev)] # obliczanie nowego wektora bazy ortogonalnej
        B_good.append(b_vec_good)
    return B_good, mus

def lll(B, delta=0.75):
    k = 1 # jak w oryginalnym algorytmie, zaczynamy od drugiego k (względem zerowego indeksu)
    n = len(B)
    B_good, mu = gram_schmidt(B) # pobranie idealnie zortogonalizowanej bazy referencyjnej

    def size_reduce():
        for i in range(k-1, -1, -1): # przechodzenie każdego wiersza macierzy mu kolumnami od końca
            if abs(mu[k][i]) > 0.5: # warunek redukcji
                r = round(mu[k][i]) 
                B[k] = [bk_elem - r * bi_elem for bk_elem, bi_elem in zip(B[k], B[i])] # redukcja rozmiaru wektora b_k - zmniejszanie rzutu na pozostałe wektory bazy
                for j in range(i):
                    mu[k][j] -= r * mu[i][j] # aktualizacja wszystkich poprzedzających współczynników mu_kj 
                mu[k][i] -= r # aktualizacja bieżącego współczynnika mu

    while k < n: 
        size_reduce()
        
        lhs = scalar_multi(B_good[k], B_good[k]) + (mu[k][k-1]**2) * scalar_multi(B_good[k-1], B_good[k-1]) # lewa strona warunku Lovásza
        rhs = delta * scalar_multi(B_good[k-1], B_good[k-1]) # prawa strona warunku Lovásza

        if lhs < rhs:
            B[k], B[k-1] = B[k-1], B[k] # zamiana kolejności wektorów w bazie
            B_good, mu = gram_schmidt(B) # ponowna ortogonalizacja Grama-Schmidta uwzględniająca nową kolejność
            k = max(k - 1, 1)
        else:
            k = k + 1
            
    return B

def gcd(a, b): # algorytm Euklidesa największego wspólnego dzielnika
    if a == 0:
        return b
    return gcd(b % a, a)

def merkle_hellman_gen(n=10, seed=0, length=40):
    rng = random.Random(seed)
    w = [rng.randrange(2, 10)]
    for _ in range(n-1): # tworzymy ciąg superrosnący
        w.append(sum(w) + rng.randrange(1, 10)) # tworzenie klucza prywatnego
    m = max(sum(w) + rng.randrange(1, 100), 1 << length) # wybieramy m tak duże, aby zminimalizować gęstość
    while True:
        r = rng.randrange(2, m) #szukamy r względnie pierwszego z m
        if gcd(r, m) == 1:
            break
    a = [(r*i)%m for i in w]
    return a, w, m, r

def encrypt(a, x): # szyfrowanie wiadomości
    return sum(a_i*x_i for a_i, x_i in zip(a, x))

def lo_lattice(a, S):
    n = len(a)
    L = [[0]*(n+1)  for _ in range(n+1)] # tworzymy pustą kratę n+1 x n+1
    for i in range(n): # zapełniamy przekątna 2 -> zmodyfikowaną przez Costera et al. kratę przeskalowujemy przez 2 by pozbyć się ułamków w ostatnim rzędzie
        L[i][i] = 2
    for i in range(n):
        L[i][n] = 2*a[i] # zapełniamy ostatnią kolumnę a_i -> zakładamy, że N = 1
    for j in range(n):
        L[n][j] = 1 # zapełniamy ostatni rząd 1 (czyli 0.5 * 2 zgodnie z pierwszym ulepszeniem Costera-Jouxa)
    L[n][n] = 2*S

    return L

def bits_from_short_vec(v, n): # proces odzyskiwania bitów wiadomości jako x_i = (1 - v_i)/2
    out = []
    for x in v[:n]:
        xi = int(round(x))
        if xi == 1:   out.append(0)
        elif xi == -1: out.append(1)
        else: return None
    return out
