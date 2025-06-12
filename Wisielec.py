import random

# Słownik z listy wisielca
with open('E:\Wideo\Śmieszny Python\lista_wisielec.txt', 'r') as file:
    słowa = file.readlines()



# Parametry liczniki
zgaduj = random.choice(słowa).lower()
próby = 3
zgadnięte_litery = []
wykorzystane_litery = []
trafione = []



# Stan gry i start programu
while próby > -1:
    print(f'Słowo ma {len(zgaduj)} liter')
    print(f'Pozostało {próby} żyć')
    print(f'Wykorzystane litery {wykorzystane_litery}')
    print(f'Trafione litery {trafione}')
    
    ###Zrobić by została sprawdzona czy jest w słowie, potem czy użyta i podzielić na trafione i chybione
    
    # Podaj literę
    litera = input('\nPodaj literę: ').lower()[0]
    
    
    # Sprawdź czy litera została użyta
    if litera not in wykorzystane_litery:
        wykorzystane_litery.append(litera)
    else:
        print('\nLitera została użyta!\n')
        
    
    # Sprawdź czy podana litera jest w słowie
    if litera in zgaduj:
        print('\n---Super, zgadłeś literę!---\n')
        zgadnięte_litery.append(litera)
    else:
        print('\nNiestety, ta litera nie jest w słowie :c\n')
        próby -= 1
        
         
    # Sprawdź, czy gracz odgadł całe słowo (dla każdej litery w zgadniętych literach sprawdza czy litera jest w danym słowie)
    if all(litera in zgadnięte_litery for litera in zgaduj):
        print(f'\nGratulacje! Odgadnięte słowo to: {zgaduj}\n')
        break
    elif próby == 0:
        print(f'\nNiestety, skończyły się próby. Słowo do odgadnięcia to: {zgaduj}\n')
        break
    else:
        pass