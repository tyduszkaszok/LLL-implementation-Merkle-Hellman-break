# Kryptoanaliza systemu Merkle'a-Hellmana przy użyciu algorytmu LLL

Niniejsze repozytorium zawiera implementację ataku na kryptosystem plecakowy Merkle'a-Hellmana z wykorzystaniem kryptoanalizy kratowej (algorytmu LLL). 

## Struktura projektu

Projekt składa się z trzech głównych modułów:

* **`lattice_crypto.py`** – Główny plik z logiką matematyczną i kryptograficzną. Zawiera implementacje kluczowych funkcji, takich jak generowanie kluczy plecakowych, ortogonalizacja Grama-Schmidta (GSO), redukcja rozmiaru oraz pełny algorytm Lenstry-Lenstry-Lovásza (LLL).
* **`demo.py`** – Skrypt demonstracyjny prezentujący praktyczne łamanie kryptosystemu (odzyskiwanie ukrytej wiadomości) dla kilku różnych długości ciągów binarnych.
* **`tests.py`** – Skrypt służący do empirycznej analizy wydajności. Przeprowadza testy badające dwa kluczowe aspekty algorytmu: czas działania LLL w zależności od wymiaru bazy kraty oraz wpływ wielkości parametru tolerancji $\delta$ na skuteczność i czas redukcji.

## Jak uruchomić?

Aby przetestować działanie ataku, wystarczy uruchomić skrypt demonstracyjny:
```bash
python demo.py