"""
Creare uno script python che:

1- Legga il file vel_vs_time.csv scaricato;
2- Produca un grafico della velocità in funzione del tempo;
3- Calcoli la distanza percorsa in funzione del tempo (utilizzando scipy.integrate.simpson);
4- Produca il grafico della distanza percorsa in funzione del tempo;
5- Utilizzare il modulo argparse per permettere di selezionare il garfico da visualizzare o il file da leggere al momento dell'esecuzione.
SUGGERIMENTO: assicurarsi di comprendere bene il comportamento della funzione scipy.integrate.simpson agli estremi dell'intervallo di integrazione.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import argparse
from scipy import integrate
from tabulate import tabulate

def data_read(df_in):
	"""
	Funzione che legge il dataframe e ne stampa delle informazioni
	
	Parametri 
	----------
	df_in : file dati che viene letto
	
	Return
	----------
	df : file convertito in dataframe 
	"""
	df = pd.read_csv(df_in)
	print(f'Colonne dataframe: {df.columns}')
	print(f'Dimensioni dataframe: {df.shape}')
	
	return df
	
def int_simp(df):
	"""
	Funzione che calcola l'integrale con il metodo integrate.simpson
	
	Parametri
	----------
	df : Dataframe contente i dati su cui fare l'integrale
	
	Return
	----------
	delta_x : Array contenente il risultato dell'integrale: la distanza
	"""
	
	Delta_x = np.empty(0)
	
	for i, r in df.iterrows():
		dx_ = integrate.simpson(df['v'][:i+1], dx=0.5)
		Delta_x = np.append(Delta_x, dx_)
		
	return Delta_x

def parse_arguments():
	"""
	Funzione che definisce gli argomenti da passare quando si esegue lo script
	"""
	
	parser = argparse.ArgumentParser(description='Studio cinematica di un corpo: accelerazione e velocità')
	
	parser.add_argument('-f', '--file', action='store', default='DATI_E06/vel_vs_time.csv', help='Inserisci il percorso del nuovo file dat di input')
	
	parser.add_argument('-v', '--vel', action='store_true', help='Mostra il grafico Velocità-Tempo')
	
	parser.add_argument('-d', '--dist', action='store_true', help='Mostra il grafico Spazio-Tempo')
	
	parser.add_argument('-t', '--data', action='store_true', help='Stampa la tabella dei dati')
	
	
	return  parser.parse_args()	
	
def main():

	# Dati utilizzati
	df_in = args.file	
	
	# Richiamo delle funzioni
	df = data_read(df_in)
	dist = int_simp(df)
	args = parse_arguments()
	
	if args.vel == True:
		# Plot Velocità in funzione del Tempo
		plt.plot(df['t'], df['v'], color='tomato')
		plt.xlabel(r'Time $s[]$')
		plt.ylabel(r'Velocity $[m/s]$')
		plt.title('Grafico velocità in funzione del tempo')
		plt.grid(True, linestyle="--", alpha=0.6)
		plt.show()
		
	if args.dist == True:
		# Plot Distanza in funzione del Tempo
		plt.plot(df['t'], dist, color='teal')
		plt.xlabel(r'Time $s[]$')
		plt.ylabel(r'Space $[m]$')
		plt.title('Grafico spazio in funzione del tempo')
		plt.grid(True, linestyle="--", alpha=0.6)
		plt.show()

	if args.data == True:
		# Stampa i dati in una tabella
		print(f'Dati del file {df_in}:\n{tabulate(df, headers='keys', tablefmt='github')}')
		
	if args.data == False and args.vel == False and args.dist == False:
		# Se non viene fornito un argomento stampa il consiglio di usare --help
		print('Inserisci: python3 es1.py --help, per vedere gli argomenti')
	
	
if __name__ == "__main__":

	main()
