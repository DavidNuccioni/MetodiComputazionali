"""
Partendo dalla formula per il periodo, produrre uno script python che:
1- Calcoli il periodo in funzione del punto di partenza (utilizzando scipy.integrate.simpson);
2- Produca un grafico di T in funzione di x_0
3- Ripetere l'analisi precedente per un'energia potenziale del tipo e confrontare i risultati
4- Provare formule alternative per (rispettando la condizione di simmetria rispetto all'origine) e confrontare i risultati.
5- Utilizzare il modulo argparse per permettere all'utente di scegliere le opzioni sul potenziale da visualizzare
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import argparse
from scipy import integrate

def V6(x, k):
	"""
	Definisce un potenziale del tipo V(x,k)=kx^6    
	
	Parameters
	-----------
	x : valore della x 
	k : costante del potenziale in input
	
	Return
	-----------
	V_x : restituisce la forma del potenziale
	"""
	
	return k*x**6

def V4(x, k):
	"""
	Definisce un potenziale del tipo V(x,k)=kx^4
		
	Parameters
	-----------
	x : valore della x 
	k : costante del potenziale in input
	
	Return
	-----------
	V_x : restituisce la forma del potenziale
	"""    
	
	
	return k*x**4

def V2(x, k):
	"""
	Definisce un potenziale del tipo V(x,k)=kx^2    
		
	Parameters
	-----------
	x : valore della x 
	k : costante del potenziale in input
	
	Return
	-----------
	V_x : restituisce la forma del potenziale
	"""
	
	return k*x**2

def V3mezzi(x, k):
	"""
	Definisce un potenziale del tipo V(x,k)=k|x|^3/2
		
	Parameters
	-----------
	x : valore della x 
	k : costante del potenziale in input
	
	Return
	-----------
	V_x : restituisce la forma del potenziale
	"""
	
	return k*np.power(np.abs(x),1.5)

def integr(V_x, k, m):
	"""
	Calcola l'integrale e successivamente il periodo di oscillazione su varie ampiezze, restituendo un array con tuple costituite da periodo e ampiezza
	
	Parameters
	-----------
	V_x : poteniale 
	k : costante del potenziale
	
	Return
	-----------
	ris :  array con periodo di oscillazione e ampiezza
	
	"""
	
	dx = 0.01
	T = []
	x0_list = []
	
	for x0 in np.arange(0.5, 5.05, 0.1):
		
		x0_list.append(x0)
		xx = np.arange(0.0, x0, dx)
		integrand = 1./np.sqrt((V_x(x0, k) - V_x(xx, k)))
		
		inte = integrate.simpson(integrand, xx)
	
		T = np.append(T, np.sqrt(8*m)*inte)
		
	ris = list(zip(x0_list, T))
		
	return ris

def parse_arguments():
	"""
	Funzione che definisce gli argomenti da passare quando si esegue lo script
	"""
	
	parser = argparse.ArgumentParser(description='Periodo oscillatore anarmonico con diversi potenziali')
	
	parser.add_argument('-V1', '--pot_6', action='store_true', help=r'Potenziale con $x^6$')

	parser.add_argument('-V2', '--pot_4', action='store_true', help=r'Potenziale con $x^4$')
	
	parser.add_argument('-V3', '--pot_2', action='store_true', help=r'Potenziale con $x^2$')
	
	parser.add_argument('-V4', '--pot_3mezzi', action='store_true', help=r'Potenziale con $x^(3/2)$')
	
	parser.add_argument('-k', '--k', type=float, default=1.0, help='Valore della costante k')
	
	parser.add_argument('-m', '--m', type=float, default=1.0, help='Valore della massa m')
	
	return  parser.parse_args()

def main():
	
	# Richiamo degli argomenti scelti dall'utente
	args = parse_arguments()
	
	# Inizializzazioni costanti m e k
	k = args.k
	m = args.m
	
	# Definizione del potenziale scelto come argomento
	V_x = None
	nome = None
	if args.pot_6 == True:
		
		V_x = V6
		nome = '$V_{(x,k)}=kx^{6}$'
		
	if args.pot_4 == True:
	
		V_x = V4
		nome = '$V_{(x,k)}=kx^{2}$'
	
	if args.pot_2 == True:
	
		V_x = V2
		nome = '$V_{(x,k)}=kx^{4}$'
		
	if args.pot_3mezzi == True:
	
		V_x = V3mezzi
		nome = '$V_{(x,k)}=k|x|^{3/2}$'
		
	if args.pot_6 == False and args.pot_4 == False and args.pot_2 == False and args.pot_3mezzi == False:
		# Se non viene fornito un argomento stampa il consiglio di usare --help
		print('Inserisci: python3 es2.py --help, per vedere gli argomenti')
	
	# Calcolo del periodo e trasformazione dati in un dataframe
	ris = integr(V_x, k, m)
	df = pd.DataFrame(ris, columns=['Ampiezza', 'Periodo'])
	
	# Plot potenziale
	
	xx = np.arange(-5,5.05, 0.1)
	plt.figure()
	plt.plot(xx, V_x(xx, k), color='slategray')
	plt.axvline(color='k', linewidth=0.5)
	plt.xlabel('$x$')
	plt.ylabel('$V_{(x)}$')
	plt.title(f'Grafico del potenziale: {nome}')
	plt.show()
	
	# Plot di T in funzione di x_0
	plt.figure()
	plt.plot(df['Ampiezza'], df['Periodo'] , color='cornflowerblue')
	plt.xlabel('$x_{0}$')
	plt.ylabel('$T$')
	plt.title(f'Grafico del periodo in funzione di $x_{0}$ di: {nome}')
	plt.show()
	
if __name__ == '__main__':

	main()
