from itertools import combinations

# Sprawdza czy liczba pierwsza
def czy_prime(n):
    '''Sprawdza, czy podana liczba n jest liczbą pierwszą'''
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Używane cyfry i długości cyfr
cyfry = [1,2,3,4,5,6]
pola = [1,2,3,4,5,6]

# Słownik kombinacji
prime_sums = {i:[] for i in range(1,7)}

# Dla długości cyfr, w tym dla każdej w niej kombinacji, liczy sumę kombinacji
for r in pola:
    for kombinacja in combinations(cyfry, r):
        suma_kombinacji = sum(kombinacja)
        
        # Gdy liczba pierwsza to dodaje odpowiednią kombinację do słownika kombinacji dla każdego pola (r). pola:[kombinacja -> tuple, suma_kombinacji]
        if czy_prime(suma_kombinacji):
            prime_sums[r].append((kombinacja, suma_kombinacji))

with open("Sumy.txt", "w") as file:
    for pola, sumowania in prime_sums.items():
        print(f"\nSumy cyfr o długościach: {pola}, które są liczbami pierwszymi:", file=file)
        
        for kombinacja, suma_kombinacji in sumowania:
            print(f"Kombinacja: {kombinacja}, Suma: {suma_kombinacji}", file=file)