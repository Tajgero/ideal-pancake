from random import random as rand
from matplotlib import pyplot as plt

print('Bende cos szacował Pi na podstawie MonteCarlo')

liczba_strzalow = int(input('Podaj liczbę strzałów: '))

licznik_kolo = 0

for i in range(liczba_strzalow):
    x = rand()*2 - 1
    y = rand()*2 - 1
    
    if x**2 + y**2 < 1:
        
        licznik_kolo += 1
        # plt.plot(x, y, ',', color='g')
    # else:
        # plt.plot(x, y, ',', color='c')
    
    
    
liczba_pi = (4*licznik_kolo) / liczba_strzalow

# plt.axis('square')
# plt.show()

print(f'\nPrzybliżona liczba Pi wynosi {liczba_pi}')