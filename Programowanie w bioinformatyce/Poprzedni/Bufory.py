# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 19:12:17 2024

@author: Tajgero - Robienie buforu
"""

pKa_table = {
'octanowy':4.76, 'pikolinowy':5.39, 'fosforanowy':2.148,
'borowy':9.237, 'kakodylowy':6.25
}


# Witaj
print("Na podstawie równania Hendersona-Hasselbacha stworzę Ci cud bufor\n")

# Pokazuje bufory w słowniczku
for pH, pKa in pKa_table.items():
    print(pH, pKa)
    
# Wartości początkowe
pKa = input("\nPodaj pKa buforu lub wpisz z listy:\n")

if pKa in pKa_table:
    pKa = pKa_table[pKa]
else:
    pKa = float(pKa)

pH = float(input("Podaj docelowe pH buforu\n"))

if pH < pKa - 1.5 or pH > pKa + 1.5:
    raise Exception("pH nie mieści się w zakresie buforowym!")
    
# Obliczenie stosunku zasady do kwasu z Hendersona-Hasselbacha
stosunek = 10**(pH - pKa)

# Całkowite stężenie buforu
C = float(input("Podaj docelowe stężenie buforu [mM]\n")) / 1000

# Układ równań
kwas = C/(stosunek + 1)
zasada = C - kwas

# Obliczenie objętości
V = float(input("Podaj docelową objętość buforu [mL]\n")) / 1000

# Obliczenie moli
mol_zasada = zasada * V
mol_kwas = kwas * V

# Obliczenie potrzebnej objętości zasady i kwasu
C_zasada = float(input("Podaj stężenie zasady [M]\n"))
C_kwas = float(input("Podaj stężenie kwasu [M]\n"))

V_zasada = mol_zasada*1000/C_zasada
V_kwas = mol_kwas*1000/C_kwas
V_woda = V*1000 - (V_zasada + V_kwas)

print(f"\nPotrzebujesz {V_zasada:.2f} mL zasady {C_zasada} M oraz {V_kwas:.2f} mL kwasu {C_kwas} M i dopełnij do {V*1000} mL wodą (~{V_woda:.2f}) mL")
print(f"{mol_zasada:.6f} moli zasady oraz {mol_kwas:.6f} moli kwasu")