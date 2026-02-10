import numpy as np
import ctypes

"""
1- Produrre la libreria condivisa "serie" (libserie.so) in cui sia definita la funzione fibonacci che accetti in ingresso il numero intero n;
2- Calcoli i valori della successione di Fibonacci fino al termine Fn e restituisca il valore Fn/Fn-1;
3- Produrre il modulo python (serie.py) che tramite ctypes usi la libreria condivisa libserie.so;
4- Definisca la funzione fibonacci che a sua volta usi quella della libreria c serie;
5- Produrre uno script python (run_serie.py) che importi il modulo fibonacci e usi la corrispondnete funzione fibonacci

Modulo python che permette l'utilizzo della funzione di Fibonacci definita in serie.c
"""

# Caricamento libreria che si trova nella cartella corrente
_libserie = np.ctypeslib.load_library('libserie', '.')

# Definizione dei tipi di input e di output
_libserie.fibonacci.argtypes = [ctypes.c_int]
_libserie.fibonacci.restype  = ctypes.c_double

# Utilizzo della libreria
def fibonacci(n):
    return _libserie.fibonacci(int(n))
