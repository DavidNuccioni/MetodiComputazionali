import sys, os
import numpy as np
import matplotlib.pyplot as plt
import argparse
import timeit
from numba import jit

"""
1- Studiare la funzione f(z) = z² + c e implementare uno script python che utilizzi un equivalente della suddetta funzione per generare un'immagine frattale in cui il colore è proporzionale al numero di iterazioni necessarie per stabilire la divergenza con modalità di esecuzione a scelta fra:
	- Puro codice python;
	- Compilazione JIT di Numba;
SUGGERIMENTO: esplorare i valori dell'opzione norm di imshow per il migliore risultato;
SUGGERIMENTO: esplorare i valori dell'opzione cmap di imshow per visualizzare l'immagine;
2- Variare i parametri size ed iterations e confrontare la velocità per le due modalità di esecuzione;
3- Definire una nuova funzione multibrot, simile a mandelbrot ma dove l'esponente può essere scelto e ripetere i passi precedenti;
"""

def parse_arguments():
	"""
	Funzione che definisce gli argomenti da passare quando si esegue lo script
	"""
	
	parser = argparse.ArgumentParser(description='Calcolo della funzione di Mandelbrot con python puro o tramite Numba', usage ='python3 mandelbrot.py [--options]')
   
	parser.add_argument('-n', '--nb', action='store_true', help='Esegue funzione con Numba')
	parser.add_argument('-p', '--py', action='store_true', help='Esegue funzione con Python puro')
	parser.add_argument('-f', '--func', action='store_true', help='Esegue per una funzione con esponenete a scelta, utilizza Numba')
	parser.add_argument('-s', '--size', type=int, action='store', default=400, help='Cambia il valore di size')
	parser.add_argument('-i', '--iter', type=int, action='store', default=100, help='Cambia il valore di iterations')
	
	return  parser.parse_args(args=None if sys.argv[1:] else ['--help'])


def mandel_py(size, iterations):
    
    m = np.zeros((size, size))
    
    for i in range(size):
    
        for j in range(size):
           
            c = (-2 + 3. / size * j +
                 1j * (1.5 - 3. / size * i))
            z = 0
    
            for n in range(iterations):
    
                if np.abs(z) <= 10:
                    z = z * z + c
                    m[i, j] = n
                else:
                    break
    return m


@jit
def mandel_numba(size, iterations):
    
    m = np.zeros((size, size))
    
    for i in range(size):
        
        for j in range(size):
          
            c = (-2 + 3. / size * j +
                 1j * (1.5 - 3. / size * i))
            z = 0
            
            for n in range(iterations):
                
                if np.abs(z) <= 10:
                    z = z * z + c
                    m[i, j] = n
                else:
                    break
    return m

@jit
def multibrot_numba(size, iterations, k):
	
	m = np.zeros((size, size))
	
	for i in range(size):
	
		for j in range(size):
	
			c = (-2 + 3. / size * j +
				 1j * (1.5 - 3. / size * i))
			z = 0
	
			for n in range(iterations):
	
				if np.abs(z) <= 10:
					z = z ** k + c
					m[i, j] = n
				else:
					break
	return m


def main():


	if args.py:
	
		m = mandel_py(size,iterations)
		tempo = timeit.timeit(lambda: mandel_py(size, iterations), number=1)
		
		print(f"\n----------------------------------------")
		print(f"Tempo di esecuzione: {tempo:.4f} secondi")
		print(f"----------------------------------------\n")
		
		
	elif args.nb:
	
		m = mandel_numba(size, iterations)
		tempo = timeit.timeit(lambda: mandel_numba(size, iterations), number=1)
		
		print(f"\n----------------------------------------")
		print(f"Tempo di esecuzione: {tempo:.4f} secondi")
		print(f"----------------------------------------\n")

	elif args.func:
	
		try:
			
			k_inp = input('\nScegliere esponente della funzione: ')
			k = float(k_inp)
			
		except ValueError:
			
			print("\nErrore: numero non valido, deve essere un numero reale (utilizzare 0.0 per la virgola)\n")
			return
			
		m = multibrot_numba(size, iterations, k)
		tempo = timeit.timeit(lambda: multibrot_numba(size, iterations, k), number=1)
		
		print(f"\n----------------------------------------")
		print(f"Tempo di esecuzione: {tempo:.4f} secondi")
		print(f"----------------------------------------\n")
		 
		 
	fig, ax = plt.subplots(1, 1, figsize=(10, 10))
	ax.imshow(np.log(m), cmap=plt.cm.hot)
	ax.set_axis_off()
	plt.show()

if __name__=='__main__':

	args = parse_arguments()
	size = args.size
	iterations = args.iter 
	main()
	
