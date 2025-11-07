# -*- coding: utf-8 -*-
"""
Created on Fri May 24 12:25:08 2024

@author: Tajgero - Projekt
"""

from Bio import PDB

# Zawijaie znaków
def zawijak_znakow(text, znaki):
    linijki = ([text[i:i+znaki] for i in range(0, len(text), znaki)])
    linijki = [slowa_w_linijce.lstrip() for slowa_w_linijce in linijki]        
    return '\n'.join(linijki)

pdb = input('Podaj kod PDB:\n')

# Łatwiejsze czytanie metod PDB
sciagacz = PDB.PDBList()
czytacz = PDB.PDBParser()

# Wczytuję plik
plik = sciagacz.retrieve_pdb_file(pdb, pdir='.', file_format='pdb', overwrite=True)

# Wczytuję strukturę do pamięci
struktura = czytacz.get_structure(pdb, plik)

# Zbieranie danych o strukturze
rozdzielczość = struktura.header["resolution"]
metoda = struktura.header["structure_method"]
nazwa = struktura.header["name"]
literatura = struktura.header["journal_reference"]
czasteczka = struktura.header["compound"]["1"]["molecule"]

# Printowanie informacji
print(f'\nNazwa: {nazwa}\n')

# Jak NMR to ilość modeli, jak nie to normalna rozdzielczość
if 'nmr' in metoda:
    print(f'Rozdzielczość: {len(struktura)}\n')
else:
    print(f'Rozdzielczość: {rozdzielczość}\n')
    
print(f'Wykorzystana metoda: {metoda}\n') 
print(f'Literatura: {literatura}\n')
print(f'Struktura zawiera cząsteczkę: {czasteczka}\n')

# Robienie liczników aminokwasów, wody, ligandów
licznik_amino = 0
licznik_woda = 0
licznik_ligand = 0
licznik_cystein = 0

for licznik in struktura.get_residues():
    
    # Licznik aminokwasów
    if licznik.id[0] == ' ':
        licznik_amino += 1
        
    # Licznik wody
    if licznik.id[0] == 'W':
        licznik_woda += 1
        
    # Licznik liganda
    if licznik.id[0][0] == 'H':
        licznik_ligand += 1
        
    # Ilość cystein
    if licznik.resname == 'CYS':
        licznik_cystein += 1
        
    if licznik.id[0] == ' ':
        a2 = licznik['CA']
        
        
print(f'Ilość aminokwasów: {licznik_amino}')
print(f'Ilość wody: {licznik_woda}')
print(f'Ilość ligandów: {licznik_ligand}')
print(f'Ilość cystein: {licznik_cystein}\n')

# Odległość aminokwasów węgla alfa z łańcucha 1
a1 = struktura[0].child_list[0].child_list[0]['CA']
print(f'Odległość między węglami alfa pierwszego i\nostatniego aminokwasu wynosi: {a1 - a2:.4f}')



