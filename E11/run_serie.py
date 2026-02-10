import numpy as np
import serie as sr

"""
1- Produrre la libreria condivisa "serie" (libserie.so) in cui sia definita la funzione fibonacci che accetti in ingresso il numero intero n;
2- Calcoli i valori della successione di Fibonacci fino al termine Fn e restituisca il valore Fn/Fn-1;
3- Produrre il modulo python (serie.py) che tramite ctypes usi la libreria condivisa libserie.so;
4- Definisca la funzione fibonacci che a sua volta usi quella della libreria c serie;
5- Produrre uno script python (run_serie.py) che importi il modulo fibonacci e usi la corrispondnete funzione fibonacci

Modulo python per calcolare il rappporto della sequenza di Fibonacci
"""

try:

	# Valore del termine da calcolare nella serie di Fibonacci scelto dall'utente
	n_inp = input("Inserisci il numero su cui calcolare il rapporto della successione di Fibonacci: ")
	n = int(n_inp)

	# Stampa del risultato
	print(f'Il rapporto tra il termine {n} e il termine {n-1} della serie di Fibonacci è: {sr.fibonacci(n)}')
	
	
except ValueError:

    print("Errore: numero non valido, deve essere un numero intero")

