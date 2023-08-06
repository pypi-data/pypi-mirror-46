import numpy

def is_magic_square(numbers):
    print ('Ver 1.2')
    suma = 0;
    n = len(numbers)
    for i in range(n):
        suma += numbers[i][i]  # Przekatna 1
    suma_wiersz, suma_kol, suma_przek2 = 0, 0, 0;
    for i in range(n):
        for j in range(n):
            suma_wiersz += numbers[i][j]
            suma_kol += numbers[j][i]
        if suma_wiersz != suma or suma_kol != suma:
            return False
        suma_wiersz = 0
        suma_kol = 0
    for i in range(n):
        suma_przek2 += numbers[i][n-i-1]
    if suma_przek2 != suma:
        return False
    return True



