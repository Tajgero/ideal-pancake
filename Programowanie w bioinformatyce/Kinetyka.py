# -*- coding: utf-8 -*-
"""
Tworzy kinetykę enzymatyczną z aktywnościami i liczy vm i vmax,
robi krzywą michaelisa menten, podaje wspolczynniki i robi wykres
"""
from os.path import isfile
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from sys import argv


def wczytywanie_nazwy_pliku(plik):
    """Wczytuje tylko nazwę pliku (type: .txt)"""
    
    # plik = 'dane' # Szybkie wczytywanie
    
    if not isfile(plik):
        if isfile(plik + '.txt'): # Dodaje txt do nazwy pliku, gdy pliku nie ma to brak nazwy
            plik = plik + '.txt'
        else:
            plik = ''
            
    return plik
    

def wczytywanie_danych(plik):
    """Wczystuje wiersze, które nie mają na początku #"""
    macierz = []
    
    with open(plik, 'r') as f: # r - read
        for linia in f:
            
            if linia.strip()[0] != "#": # Linie bez tych, które mają początek "#"
                linia = linia.replace(',', '.') # Zmiana przecinków na kropki wszędzie
                wiersz = linia.split()
                wiersz = [float(liczba) for liczba in wiersz] # Zamienia na liczby
                macierz.append(wiersz)
                
    macierz = np.array(macierz) # Zamienia na array
    return macierz # Lista wierszy w macierzy
        

def kinetyka(dane):
    """Właściwa analiza danych"""
    
    x = dane[:, 0] # 1 kolumna
    y = dane[:, 1:] # Reszta jest macierzą
    y_sredni = np.average(y, axis=1) # W poziomie
    # print(y_sredni)
    # print(dane)
    # print(x,y)
    
    vmax = np.max(y) # Vmax to max y 
    km = np.average([x[0], x[1]]) # Km to średnia macierz z 1 wartości i 2 wartości dla x
    
    # Fitujemy pod względem funkcji MM dla x, średnie y, dla wartości p0: km, vmax
    km_vmax, error = curve_fit(MM_function, x, y_sredni, p0=[km, vmax])
    
    paczka = {}
    paczka['kolumna'] = x
    paczka['dane'] = y
    paczka['dane_srednie'] = y_sredni
    paczka['Km'] = km_vmax[0] # km z fittowania
    paczka['Vmax'] = km_vmax[1] # vmax z fittowania
    return paczka


def Wykres(dane, nazwa_pliku):
    """Tworzy wykres dla danych"""
    
    plt.figure() # Nowa przestrzeń rysowania
    
    x_points = dane['kolumna']
    y_points = dane['dane']
    y_points_m = dane['dane_srednie']
    vmax = dane['Vmax']
    km = dane['Km']
    
    new_x = np.arange(0, np.max(x_points), 0.1) # Range tylko dla macierzy
    new_y = [MM_function(i, km, vmax) for i in new_x] # Wskazuje prędkość dla każdego X i robi krzywą
    plt.plot(new_x, new_y, '-', color='blue') # Nowy fittowany wykres
    
    plt.title('Kinetyka reakcji')
    plt.xlabel('Stężenie substratu [mM]', fontsize=12)
    plt.ylabel(r'Aktywność enzymu [$\frac{nmol}{min*mg}$]', fontsize=12)
    
    plt.plot(x_points, y_points, 'x', color='green') # Punkty pomiarowe
    plt.plot(x_points, y_points_m, 'o', color='black') # Czarne kropy
    # plt.plot(x_points, y_points_m, '-', color='black') # Łączy linią
    
    plt.grid(linewidth=0.5, linestyle=':')    #siatka na wykresie
    #plt.arrow(0, 907, 2.4, 0)                #linia na wykresie (pozioma)
    
    # plt.plot(new_x, new_y,'x') # Reprezentacja funkcji Michaelisa-Menten
    # plt.plot(x_points, y_points_m, 'o', color='black') # Czarne punkty
    # plt.plot(x_points, y_points_m, '-', color='black') # Łączy linią
    
    # Startuje od 0 punktu
    plt.xlim(left = 0)
    plt.ylim(bottom = 0)
    
    # plt.axhline(y=vmax, color='r', linestyle='dashed')  # Vmax linia pozioma
    plt.plot(km, vmax/2, 'o', color='red') # Km kropka
    
    plt.text(12.5, 1000, '$K_m$', size=20, ha='right') # Km
    plt.text(12.5, 800, '$V_{max}$', size=20, ha='right') # Vmax
    plt.text(13, 1000, f'= {km:.2f}', size=20) # Km wartość
    plt.text(13, 800, f'= {vmax:.2f}', size=20) # Vmax wartość
    plt.arrow(0, vmax/2, km, 0, linewidth=0.3, linestyle=':', color='red') # Linia do Km pozioma
    plt.arrow(km, vmax/2, 0, -vmax/2, linewidth=0.3, linestyle=':', color='red') # Linia do Km pionowa
    plt.grid(linewidth=0.5, linestyle=':')
    
    # plt.text(12, 1000, r'$\frac{10}{35}$', size='20')
    # plt.text(15, 800, r'$\sum_{i=1}^{100}$', size='20')
    # plt.text(20, 1400, r'$\infty_1^{100}$', size='20')
    # plt.text(20, 1200, r'$\left(\sqrt[3]{100}\right)$', size='20')
    
    nazwa_rysunku = nazwa_pliku[:-4] + '_rysunek.png'
    plt.savefig(nazwa_rysunku, dpi=600, bbox_inches='tight')
    
    # return plt.show()


def MM_function(x, km, vmax):
    """Funkcja tworząca krzywą michaelisa menten czy coś"""
    mm = (vmax * x) / (km + x)
    return mm

# =============================================================================
#       Program
# =============================================================================
if __name__ == '__main__':
    
    while True: # Zapewnia powrót programu przy błędzie
    
        if len(argv) == 1:
            pliki = input('Podaj nazwę pliku: ').split()
        else:
            pliki = argv[1:]
        
        for plik in pliki:
            nazwa = wczytywanie_nazwy_pliku(plik)
        
            if nazwa == '':
                print(f'Brak pliku {plik}, spróbuj ponownie\n')
            else:
                dane = wczytywanie_danych(nazwa)
                wynik = kinetyka(dane)
                Wykres(wynik, nazwa)
                break