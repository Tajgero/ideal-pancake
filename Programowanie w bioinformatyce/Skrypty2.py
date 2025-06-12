# 1. Wykres kinetyki reakcji enzymatycznej (Michaelis-Menten)
import matplotlib.pyplot as plt
import numpy as np

def michaelis_menten(S, Vmax, Km):
    '''Oblicza prędkość reakcji na podstawie równania Michaelisa-Menten'''
    return (Vmax * S) / (Km + S)

# Przykładowe dane
S = np.linspace(0, 10, 100)  # Stężenie substratu
Vmax = 10
Km = 2

# Wykres
v = michaelis_menten(S, Vmax, Km)
plt.plot(S, v, label=f'Vmax={Vmax}, Km={Km}')
plt.xlabel('[S] (mM)')
plt.ylabel('V (mmol/min)')
plt.title('Kinetyka reakcji enzymatycznej')
plt.legend()
plt.grid()
plt.show()


# 2. Porównanie sekwencji DNA z obliczeniem różnic
def porownaj_dna(seq1, seq2):
    '''Porównuje dwie sekwencje DNA i oblicza procent zgodności'''
    if len(seq1) != len(seq2):
        raise ValueError('Sekwencje muszą mieć tę samą długość!')
    zgodne = sum(1 for a, b in zip(seq1, seq2) if a == b)
    procent_zgodnosci = (zgodne / len(seq1)) * 100
    return procent_zgodnosci

# Przykład
dna1 = "ACGTTGCA"
dna2 = "ACGTCGCA"
print(f"Procent zgodności: {porownaj_dna(dna1, dna2):.2f}%")


# 3. Histogram liczby wyrzuconych oczek (tekstowy)
import random

def histogram_kostki(rzuty, liczba_rzutow):
    '''Tworzy histogram liczby oczek na podstawie rzutów kostką'''
    wyniki = [random.randint(1, 6) for _ in range(liczba_rzutow)]
    for i in range(1, 7):
        print(f'{i}: {"*" * wyniki.count(i)}')

# Przykład
histogram_kostki(6, 50)


# 4. Tworzenie histogramu ze słów z pliku tekstowego
def histogram_slow(plik):
    '''Tworzy histogram liczby wystąpień słów w pliku tekstowym'''
    with open(plik, 'r') as f:
        tekst = f.read().lower()
    slowa = tekst.split()
    histogram = {slowo: slowa.count(slowo) for slowo in set(slowa)}
    for slowo, liczba in histogram.items():
        print(f'{slowo}: {"*" * liczba}')

# Przykład
# Zapisz w pliku "tekst.txt" przykładowy tekst
histogram_slow('tekst.txt')


# 5. Wycinek kolumn i wierszy z macierzy Numpy
import numpy as np

# Tworzenie macierzy
macierz = np.arange(1, 21).reshape(4, 5)
print("Oryginalna macierz:\n", macierz)

# Wycięcie kolumny i wiersza
kolumna = macierz[:, 2]  # Trzecia kolumna
wiersz = macierz[1, :]   # Drugi wiersz
print("Trzecia kolumna:", kolumna)
print("Drugi wiersz:", wiersz)


# 6. Kombinacje za pomocą itertools
import itertools

def generuj_kombinacje(lista, r):
    '''Generuje wszystkie kombinacje r-elementowe z podanej listy'''
    return list(itertools.combinations(lista, r))

# Przykład
elementy = ['A', 'B', 'C', 'D']
print(generuj_kombinacje(elementy, 2))


# 7. Liczenie RMSD między dwiema cząsteczkami
import numpy as np

def rmsd(atoms1, atoms2):
    '''Oblicza RMSD między dwiema cząsteczkami na podstawie współrzędnych'''
    if len(atoms1) != len(atoms2):
        raise ValueError('Obie cząsteczki muszą mieć tę samą liczbę atomów!')
    differences = np.array(atoms1) - np.array(atoms2)
    return np.sqrt(np.mean(np.sum(differences**2, axis=1)))

# Przykład
molekula1 = [[0, 0, 0], [1, 0, 0], [0, 1, 0]]
molekula2 = [[0.1, 0, 0], [1, 0.1, 0], [0, 1, 0.2]]
print(f'RMSD: {rmsd(molekula1, molekula2):.4f}')


# 8. Generowanie tablicy prawdopodobieństwa rzutów kośćmi
import numpy as np

def tablica_prawdopodobienstwa():
    '''Generuje tablicę prawdopodobieństwa rzutów dwiema kośćmi'''
    macierz = np.zeros((6, 6), dtype=int)
    for i in range(6):
        for j in range(6):
            macierz[i, j] = i + j + 2
    return macierz

# Przykład
print(tablica_prawdopodobienstwa())


# 9. Odczyt i zapis pliku z wynikami obliczeń
def zapisz_histogram_do_pliku(histogram, nazwa_pliku):
    '''Zapisuje histogram do pliku tekstowego'''
    with open(nazwa_pliku, 'w') as f:
        for klucz, wartosc in histogram.items():
            f.write(f'{klucz}: {"*" * wartosc}\n')

# Przykład
histogram = {'1': 3, '4': 2, '6': 1, '12': 1, '15': 2}
zapisz_histogram_do_pliku(histogram, 'wynik.txt')


# 1. Sprawdzanie, czy liczba jest parzysta
def czy_parzysta(n):
    '''Sprawdza, czy liczba jest parzysta'''
    return n % 2 == 0

# Przykład
print(czy_parzysta(4))  # True
print(czy_parzysta(7))  # False


# 2. Wyznaczanie najmniejszej i największej liczby w liście
def znajdz_min_max(lst):
    '''Zwraca najmniejszą i największą liczbę z listy'''
    return min(lst), max(lst)

# Przykład
print(znajdz_min_max([3, 5, 1, 9, 2]))  # (1, 9)


# 3. Odwracanie kolejności elementów w liście
def odwroc_liste(lst):
    '''Odwraca kolejność elementów w liście'''
    return lst[::-1]

# Przykład
print(odwroc_liste([1, 2, 3, 4]))  # [4, 3, 2, 1]


# 4. Sprawdzanie, czy liczba jest doskonała
def czy_doskonala(n):
    '''Sprawdza, czy liczba jest doskonała'''
    dzielniki = [i for i in range(1, n) if n % i == 0]
    return sum(dzielniki) == n

# Przykład
print(czy_doskonala(6))  # True (6 = 1 + 2 + 3)
print(czy_doskonala(28)) # True


# 5. Generowanie ciągu arytmetycznego
def ciag_arytmetyczny(a1, r, n):
    '''Generuje ciąg arytmetyczny'''
    return [a1 + i * r for i in range(n)]

# Przykład
print(ciag_arytmetyczny(1, 2, 5))  # [1, 3, 5, 7, 9]


# 6. Liczby doskonale podzielne przez zadaną wartość
def podzielne_przez(lst, dzielnik):
    '''Zwraca liczby podzielne przez dzielnik'''
    return [x for x in lst if x % dzielnik == 0]

# Przykład
print(podzielne_przez([10, 15, 20, 25, 30], 5))  # [10, 15, 20, 25, 30]


# 7. Zmiana tekstu na wielkie litery
def na_duze_litery(tekst):
    '''Zmienia tekst na wielkie litery'''
    return tekst.upper()

# Przykład
print(na_duze_litery("hello world"))  # HELLO WORLD


# 8. Obliczanie średniej ważonej
def srednia_wazona(wartosci, wagi):
    '''Oblicza średnią ważoną'''
    if len(wartosci) != len(wagi):
        raise ValueError("Listy muszą być tej samej długości")
    return sum(v * w for v, w in zip(wartosci, wagi)) / sum(wagi)

# Przykład
print(srednia_wazona([3, 5, 7], [1, 2, 1]))  # 5.0


# 9. Generowanie liczby losowej z zakresu
import random

def losowa_liczba(a, b):
    '''Generuje losową liczbę z zakresu [a, b]'''
    return random.randint(a, b)

# Przykład
print(losowa_liczba(1, 10))  # np. 7


# 10. Sortowanie listy w odwrotnej kolejności
def sortuj_odwrotnie(lst):
    '''Sortuje listę w odwrotnej kolejności'''
    return sorted(lst, reverse=True)

# Przykład
print(sortuj_odwrotnie([3, 1, 4, 1, 5]))  # [5, 4, 3, 1, 1]


# 11. Obliczanie sumy liczb w ciągu (rekurencyjnie)
def suma_ciagu(n):
    '''Oblicza sumę liczb w ciągu od 1 do n'''
    if n == 1:
        return 1
    return n + suma_ciagu(n - 1)

# Przykład
print(suma_ciagu(5))  # 15 (1 + 2 + 3 + 4 + 5)


# 12. Liczenie samogłosek w tekście
def liczba_samoglosek(tekst):
    '''Liczy liczbę samogłosek w tekście'''
    samogloski = 'aeiouyąęó'
    return sum(1 for znak in tekst.lower() if znak in samogloski)

# Przykład
print(liczba_samoglosek("Ala ma kota"))  # 5


# 13. Sprawdzanie, czy liczba jest kwadratem liczby całkowitej
def czy_kwadrat(n):
    '''Sprawdza, czy liczba jest kwadratem liczby całkowitej'''
    return int(n**0.5) ** 2 == n

# Przykład
print(czy_kwadrat(16))  # True
print(czy_kwadrat(20))  # False
