# -*- coding: utf-8 -*-
"""
Program do analizy rzutów kostką: 
- Zlicza wyniki rzutów,
- Tworzy statystykę,
- Wyświetla histogram w konsoli,
- Generuje wykres słupkowy za pomocą matplotlib.
"""
import random as r
from matplotlib import pyplot as plt

# Tworzy histogram
def Histo(dane):
    """
   Funkcja wyświetla histogram w formie tekstowej.
   Każdy wynik (od 1 do 6) jest wyświetlany z odpowiednią liczbą znaków '#' (bez skalowania).
   
   Args:
   dane (dict): Słownik, gdzie kluczami są wyniki rzutów (1-6), a wartościami liczba wystąpień danego wyniku.
   """
    for i in dane:
        print(f"{i}:({dane.get(i):>2}) -> {dane.get(i)*'#'}")



# Uwzględnia skalowanie względem najdłuższego słupka w histogramie 
def Histo2(dane):
    """
    Funkcja wyświetla histogram w formie tekstowej, skalując go w zależności od 
    największej wartości w słowniku, aby dostosować długość słupków '#' do wielkości konsoli.
    
    Args:
    dane (dict): Słownik z wynikami rzutów i ich liczbą wystąpień.
    """
    maximum = max(dane.values())
    
    # Skalowanie: Jeżeli największa wartość jest mniejsza niż 50, użyj jednostkowego skalu,
    # w przeciwnym razie skaluj tak, aby najdłuższy słupek nie był dłuższy niż 50 znaków.
    if maximum < 50:
        hasz = 1
    else:
        hasz = int(maximum/50)
    
    # Iterujemy po wynikach i wyświetlamy je w postaci tekstowego histogramu
    for i in dane:
        print(f"{i:>20}:({dane.get(i):>2}) -> {int(dane.get(i)/hasz)*'#'}")
        
        
        
def Histo3(dane):
    """
    Funkcja rysuje wykres słupkowy dla danych.
    
    Args:
    dane (dict): Słownik z wynikami rzutów i ich liczbą wystąpień.
    """
    x = dane.keys()
    y = dane.values()
    
    plt.bar(x, y)



# Funkcja główna
if __name__ == '__main__':
    # Zbieramy dane wejściowe od użytkownika
    ile = int(input("Helloł, podaj ile razy rzucić kostką: "))
    
    # Inicjujemy słownik z wynikami (każdy wynik od 1 do 6 ma początkową wartość 0)
    stat = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    
    # Symulujemy rzuty kostką
    for i in range(ile):
        oczka = r.randint(1, 6)  # Losujemy wynik rzutu (od 1 do 6)
        stat[oczka] += 1  # Zwiększamy licznik dla odpowiedniego wyniku
    
    # Wyświetlamy statystykę
    print("\nStatystyka to:\n")
    Histo2(stat)  # Histogram tekstowy ze skalowaniem
    
    # Tworzymy wykres słupkowy
    Histo3(stat)  # Wykres
    plt.show()  # Wyświetlamy wykres
    