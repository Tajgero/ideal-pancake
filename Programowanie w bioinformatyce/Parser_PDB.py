'''Parser ekstrachuje informacje i wyciąga informację z danych
żeby można było z nich coś wykorzystać'''
from os.path import isfile
from itertools import combinations as comb
from matplotlib import pyplot as plt

def wczytanie_nazwy_pliku():
    """Wczytuje tylko nazwę pliku"""
    
    plik = input('Podaj nazwę pliku: ')
    
    if not isfile(plik):
        if isfile(plik + '.pdb'):
            plik = plik + '.pdb'
        else:
            plik = ''
            
    return plik


def wczytanie_PDB(nazwa_pliku):
    '''Otwiera PDB i tworzy statystykę ilości aminokwasków'''
    # if not isfile(nazwa_pliku):
    #     return nazwa_pliku = ''
    
    stat = {}
    seq = []
    coord_SG = []
    with open(nazwa_pliku, 'r') as f:
        
        for linia in f:
            klucz = linia[:6]
            
            if klucz == 'ATOM  ':
                nazwa_aa = linia[17:20].strip() # <0,1,2,3...) 
                nazwa_atomu = linia[12:16].strip()
                numer_aa = linia[22:26].strip()
                wsp = (float(linia[30:38].strip()),
                        float(linia[38:46].strip()),
                        float(linia[46:54].strip())
                        )
                
                # print(nazwa_aa)
                # print(nazwa_atomu)
                # print(numer_aa)
                # print(wsp)
                
                
                if nazwa_atomu == 'CA':
                    seq.append(nazwa_aa) # Tworzy sekwencję AA
                    if nazwa_aa in stat:
                        stat[nazwa_aa] += 1
                    else:
                        stat[nazwa_aa] = 1
                        
                # Tworzenie słownika w pustej liście na podstawie klucz-wartość
                if nazwa_atomu == 'SG':
                     coord_SG.append({'nr': numer_aa, 'wsp': wsp})
                    
                    
    seq2 = translate_31(seq)
    seq2 = ''.join(seq2)
    
    # Robi paczkę i zwraca statystykę i sekwencję
    paczka = {}
    paczka['stat'] = stat
    paczka['seq'] = seq
    paczka['seq2'] = seq2
    paczka['cysteiny'] = coord_SG
    return paczka

                
def analiza_PDB(dane_z_PDB):
    """Analizuje dane np. odległości cystein, pokazuje histogram aminokwasów"""
    
# =============================================================================
# Mostki disiarczkowe
# =============================================================================
    
    # Tworzy kombinacje cystein, potem liczy dla każdej pary
    # kombinacji odległość i wypluwa listę
    # kombinacje_cystein = list(comb(dane_z_PDB['cysteiny'], 2)) # Kombinacje podwójne cystein
    # lista_odl_cystein = [dist(kombinacje_cystein[kombinacja_nr][0], kombinacje_cystein[kombinacja_nr][1]) 
    #                       for kombinacja_nr in range(0, len(kombinacje_cystein))]
    
    # l_mostkow = len([odl for odl in lista_odl_cystein if odl < 5])
    
    # print(lista_odl_cystein)
    
    
    # Inny sposób
    l_mostkow = []
    
    for cys1, cys2 in comb(dane_z_PDB['cysteiny'], 2):
        odl = dist(cys1, cys2)
        
        if odl < 3:
            l_mostkow.append((cys1['nr'], cys2['nr'], odl)) # lista mostków (cys1, cys2, odl)
            print(f"Mostki występują między cysteinami {cys1['nr']} - {cys2['nr']}")
            
    # print(dane_z_PDB)
    if l_mostkow == []:
        print('Brak mostków między cysteinami')
    else:
        print(f'Liczba mostków disiarczkowych wynosi: {len(l_mostkow)}')
    
    histo(dane_z_PDB['stat'])
        
# =============================================================================
# Histogram aminokwasów
# =============================================================================

def histo(dane):    
    x = dane.keys()
    y = dane.values()
    plt.xticks(rotation = 45)
    plt.bar(x, y)
    plt.show()

# =============================================================================
# Inne przydatne funkcje
# =============================================================================

def dist(cys1, cys2): # tu: for i in dane['cysteiny']: i[...]; i == cys
    """Liczy odległości par dict: ['wsp'] tuple"""    

    # cys1 = str(cys1)
    # cys2 = str(cys2)
    
    # for i in dane['cysteiny']:
    #     if i['nr'] == cys1:
    #         cys1 = i['wsp']
    #     if i['nr'] == cys2:
    #         cys2 = i['wsp']
            
    deltax = cys1['wsp'][0] - cys2['wsp'][0]
    deltay = cys1['wsp'][1] - cys2['wsp'][1]
    deltaz = cys1['wsp'][2] - cys2['wsp'][2]
    
    odl = (deltax**2 + deltay**2 + deltaz**2)**0.5
    
    return odl


def translate_31(sekwencja):
    aminokwasy = {
    'ALA': 'A',  # Alanina
    'ARG': 'R',  # Arginina
    'ASN': 'N',  # Asparagina
    'ASP': 'D',  # Kwas asparaginowy
    'CYS': 'C',  # Cysteina
    'GLN': 'Q',  # Glutamina
    'GLU': 'E',  # Kwas glutaminowy
    'GLY': 'G',  # Glicyna
    'HIS': 'H',  # Histydyna
    'ILE': 'I',  # Izoleucyna
    'LEU': 'L',  # Leucyna
    'LYS': 'K',  # Lizyna
    'MET': 'M',  # Metionina
    'PHE': 'F',  # Fenyloalanina
    'PRO': 'P',  # Prolina
    'SER': 'S',  # Seryna
    'THR': 'T',  # Treonina
    'TRP': 'W',  # Tryptofan
    'TYR': 'Y',  # Tyrozyna
    'VAL': 'V'   # Walina
    }

    return [aminokwasy[aa] for aa in sekwencja]


# =============================================================================
# Program
# =============================================================================
if __name__ == '__main__':

        
    print('Heloł, analizuję PDB o podanej przez CIEBIE nazwie:\n')

    while True: # Zapewnia powrót programu przy błędzie
        nazwa = wczytanie_nazwy_pliku()
        
        if nazwa == '':
            print('Brak pliku, spróbuj ponownie\n')
        else:
            dane = wczytanie_PDB(nazwa)
            analiza_PDB(dane)
            break