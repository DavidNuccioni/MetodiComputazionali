



import sys,os
import es1_funct as fu

# Scelgo un valore per l'intero n in input
n_inp = input('Inserisci il massimo intero su cui calcolare la somma: ')
ni = int(n_inp)

somma = fu.somma(ni)
print('La somma dei primi ', ni, 'numeri naturali è: ', somma)

somma_sq = fu.somma_sqrt(ni)
print('La somma delle radici dei primi ', ni, 'numeri naturali è: ', somma_sq)

sompro = fu.som_pro(ni)
print('La somma e il prodotto dei primi ', ni, 'numeri naturali è: ', sompro)

# Scelgo un valore per l'indice in input
na_inp = input('Scegli indice per la serie di potenze: ')
na = int(na_inp)

serie_pow = fu.som_pow(ni, na)
print('Il risutlato della serie di potenze è ', serie_pow)
