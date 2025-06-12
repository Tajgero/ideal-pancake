def czy_prime(n):
    '''Sprawdza, czy podana liczba n jest liczbą pierwszą'''
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
	
def suma_dzielnikow(n):
    '''Podaje sumę dzielników i sprawdza czy to liczba pierwsza'''
    dzielniki = []
    suma = 0
    for i in range (1, n + 1):
        if n % i == 0:
            dzielniki.append(i)
    if len(dzielniki) == 2:
        print('Hmm widzę że to prajm namber\n')
    for dodaj in dzielniki:
        suma += dodaj
    return suma

def odwroc_string(s):
    '''Odwraca podany string'''
    return s[::-1]

def suma_cyfr(n):
    '''Podaje sumę cyfr danej liczby n'''
    total = 0
    while n > 0:
        total += n % 10
        n //= 10
    return total

def sum_list(lst):
    '''Zwraca sumę wszystkich elementów podanej listy'''
    total = 0
    for num in lst:
        total += num
    return total
	
def srednia(lst):
    '''Zwraca średnią arytmetyczną podanej listy'''
    if len(lst) == 0:
        return 0
    return sum(lst) / len(lst)
	
def fizz_buzz(od, do):
    '''Wypisuje Fizz Buzz w podanym zasięgu liczb dla wielokrotności 3 i 5'''
    for i in range(od, do + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)
			
def NWD(a, b):
    '''Wypisuje największy wspólny dzielnik algorytmem Euklidesa'''
    while b:
        a, b = b, a % b
    return a
	
def czy_palindrom(s):
    '''Sprawdza czy jest to palindrom'''
    return s == s[::-1]

def silnia(n):
    '''To jest lepsza silnia iteracyjna'''
    if n < 0 or not isinstance(n, int):
       raise RuntimeError('\nLiczba nie jest całkowita i naturalna!')
    else:
        x = 1
        for i in range(1, n + 1):
            x *=  i
        return x
		
def silnia2(n):
    '''To jest silnia rekurencyjna'''    
    if n > 0:
        wynik = n * silnia(n-1)
    else:
        wynik = 1
    return wynik
	
def Fib(n):
    '''Wyznacza ciąg Fibbonaciego iteracyjnie z RunTimeError oraz
	wykorzystaniem programowania dynamicznego'''
    if n < 0 or not isinstance(n, int):
       raise RuntimeError('\nLiczba nie jest całkowita i naturalna!')
    else:
        pass
    
    # Lista ciągu
    liczby = [0,1]
    
    # Wykonuję algorytm od indeksu F_2 do F_n, i = abstrakcyjny numer iteracji
    if n >= 2:
        for i in range(2, n+1):
            wynik = liczby[i-2] + liczby[i-1]
            liczby.append(wynik)
    elif n == 1:
        liczby = [0,1]
    else:
        liczby = [0]   
         
    return liczby
	
def Fib2(n):
    '''Wyznacza rekurencyjnie n-ty wyraz ciągu Fibbonacciego'''
    if n < 0:
        print("\n\tNie da sie policzyc wartosci takiego wyrazu ciagu Fibonacciego, sprobuj podac wartosc wieksza od 0")
    elif n == 0:
        return 0
    elif n == 1 or n == 2:
        return 1
    else:
        wartosc = Fib2(n - 1) + Fib2(n - 2)
        return wartosc
		
def Fib3(n):
    '''Wyznacza dynamicznie ciąg Fibonacciego (do danej liczby) w liście'''
    result = []
    a, b = 0, 1
    while a < n:
        result.append(a)
        a, b = b, a + b
    return result
		
		
def zawijak_znakow(text, znaki):
    '''Zawija tekst w ilości znaków i usuwa spację przed kolejną nową linią'''
    linijki = ([text[i:i+znaki] for i in range(0, len(text), znaki)])
    linijki = [slowa_w_linijce.lstrip() for slowa_w_linijce in linijki]        
    return '\n'.join(linijki)

def zawijak_slow(text, slowa):
    '''Zawija tekst w ilości słów na linię'''
    lista_slow = text.split()
    linijki = [' '.join(lista_slow[i:i+slowa]) for i in range(0, len(lista_slow), slowa)]
    return '\n'.join(linijki)

def komplementarne_dna(dna):
    '''Podaje sekwencję DNA komplementarną (str)'''
    dna = dna.upper()
    table = {
    'A': 'T',
    'T': 'A',
    'C': 'G',
    'G': 'C'
    }
    return ''.join([table[nukleotyd] for nukleotyd in dna])

def lista_liczb_input():
    '''Inputem podaj po jednej liczbie i otrzymaj listę (Enter kończy funkcję)'''
    liczby = []
    i = 1
    while True:
        try:
            liczba = int(input(f'Podaj {i} liczbę lub Enter: '))
            liczby.append(liczba)
            i += 1
        except ValueError:
            break
    return liczby