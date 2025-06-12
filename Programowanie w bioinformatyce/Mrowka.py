"""
Created on Wed Oct 23 17:57:04 2024

Mrówka Langtona

@author: Tajgero
"""
# Importy
import turtle as tr
from time import time
from Licznik_pygame import start_licznik

znacznik = 0

# Czyszczenie ekranu i ustawienia początkowe
tr.clearscreen()
Tigrisso = tr.Turtle()
data = {}

# Ustawienia
Tigrisso.speed('fastest')
Tigrisso.shape('square')
Tigrisso.resizemode('user')
Tigrisso.shapesize(0.5,0.5)
Tigrisso.pu()

# Parametry
kroki = 11
petla = 25000


# Program
start = time()
for i in range(petla):
    # Uruchomienie licznika kroków
    znacznik += 1
    # start_licznik(i, petla)
    
    # Pobieranie aktualnej pozycji
    pozycja = str(Tigrisso.pos())
    
    if pozycja in data:
        kolor = data.get(pozycja)
        
        if kolor == 'white':
            data[pozycja] = 'black'
            Tigrisso.fillcolor('black')
            Tigrisso.pencolor('black')
            Tigrisso.stamp()
            Tigrisso.rt(90)
        
        if kolor == 'black':
            data[pozycja] = 'white'
            Tigrisso.fillcolor('white')
            Tigrisso.pencolor('white')
            Tigrisso.stamp()
            Tigrisso.lt(90)
            
        Tigrisso.fd(kroki)
    else:
        data[pozycja] = 'white'
        
print(f'Czas wynosił {round(time()-start, 2)} sekund')