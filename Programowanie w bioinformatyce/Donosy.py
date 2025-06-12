# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 08:45:01 2024

@author: Tajgero
"""

from Kostka import Histo2

print("Robię coś, zobaczymy co")
stat = {}

nazwa = input("Podaj mi nazwę pliku do wczytania: ")

f = open(nazwa, 'r')

for linia in f:
    linia = linia.lower().replace(',', ' ').replace('.', ' ')
    slowa = linia.split()
    
    for slowo in slowa:
        if len(slowo) < 4:
            continue
        
        if len(slowo) > 5:
            slowo = slowo[:-3]
            
        if len(slowo) > 7:
            slowo = slowo[:7]
        
        if slowo in stat:
            stat[slowo] += 1
        else:
            stat[slowo] = 1



f.close()
      
print('Statystyka słów: \n\n')
Histo2(stat)