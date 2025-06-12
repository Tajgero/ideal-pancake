# Liczy sumy kolejnych czynników kondygnacji (silnik operacji)
def silnia_sum(n):
    '''To jest silnia sumaryczna'''
    if n < 0 or not isinstance(n, int):
       raise RuntimeError('\nLiczba nie jest całkowita i naturalna!')
    else:
        x = 0
        for i in range(0, n + 1):
            x +=  i
        return x

# Liczba kondygnacji trójkąta    
x = int(input("Wpisz ilość kondygnacji trójkąta, wyliczę ile trójkątów jest wewnątrz\n"))
y = 0

# Obliczanie iteracyjne coraz większych trójkątów

for i in range(1, x + 1):
    y += silnia_sum(i)

# Trójkąty odwrócone jednostkowe (zaczyna liczyć od 2 kondygnacji)
if x >= 2:
    y += silnia_sum(x-1)

# Trójkąty odwrócone o większych kondygnacjach (nowy ciąg) (zaczyna liczyć od 4 kondygnacji)
if x >= 4:
    for i in range(4, x + 1, 2):
        i -= 1
        y += silnia_sum(x-i)
    
print(f"Ilość trójkątów wynosi: {y}")
