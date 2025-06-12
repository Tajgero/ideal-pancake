# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 00:09:27 2024

@author: Tajgero
"""
# Importy
import turtle as tr
from time import time
# Czyszczenie ekranu i ustawienia początkowe
tr.clearscreen()
Tigrisso = tr.Turtle()
data = {}

# Ustawienia
Tigrisso.speed('fastest')
Tigrisso.shape('square')
Tigrisso.pu()

# Zmiany wektorów
delta_x = 0
delta_y = 0

# Parametry
kroki = 21
petla = 400

# Program
start = time()
for i in range(petla):
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
            
        if Tigrisso.heading() == 0.0:
            delta_x += 21
        elif Tigrisso.heading() == 90.0:
            delta_y += 21
        elif Tigrisso.heading() == 180.0:
            delta_x -= 21
        elif Tigrisso.heading() == 270.0:
            delta_y -= 21
        Tigrisso.teleport(delta_x,delta_y)
    else:
        data[pozycja] = 'white'
        
print(f'Czas wynosił {round(time()-start, 2)} sekund')