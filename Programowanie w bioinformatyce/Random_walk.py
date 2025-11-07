"""
Created on Mon Oct 21 09:00:00 2024

@author: Tajgero
"""
import turtle as tr
import random as r
from matplotlib import pyplot as plt
rand = r.randint


tr.clearscreen()

# Ustawienia
Tigrisso = tr.Turtle()
Tigrisso.speed('fastest')
Tigrisso.shape('turtle')
Tigrisso.pensize(3)
Tigrisso.pencolor('orange')
liczba_krokow = 100

traj = []

# Program
for i in range(liczba_krokow):
    
    kat = rand(-180, 179)
    kroki = rand(0, 60)
    
    if kat < 0:
        Tigrisso.pencolor('purple')
    else:
        Tigrisso.pencolor('orange')
    
    Tigrisso.forward(kroki)
    Tigrisso.right(kat)
    
    traj.append(Tigrisso.position())

    # for i in range(10):
    #     Tigrisso.right(40)
    #     Tigrisso.forward(20)
    
# Wykres
x = [i[0] for i in traj]
y = [i[1] for i in traj]

plt.plot(x, y)