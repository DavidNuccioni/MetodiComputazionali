import sys, os
import numpy as np
import pandas as pd
from scipy import constants, fft, optimize
import matplotlib.pyplot as plt
import argparse

"""
Realizzare uno script python che:

1- Legga i tre file messi a disposizione;
2- Produca un grafico dei tre segnali di ingresso;
3- Calcoli la trasformata di Fourier dei segnali di ingreso e produca il grafico dello spettro di potenza;
SUGGERIMENTO: utilizzare assi logaritmici.
4- Faccia il fit dei tre spettri di potenza per determinarne l'andamento in funzione della frequenza (1/f^b) e identifichi il tipo di rumore per ogni serie di dati sulla base dell'esponente beta ottenuto;
5- Confronti i tre spettri di potenza e i relativi fit enterpretare i risultati conforntando i tre spettri di potenza assieme ai segnali
"""


def parser_arguments():

	parser = argparse.ArgumentParser(description='Plot and fit noise data.', usage ='python3 noise_fft.py  --option')
	parser.add_argument('-ip', '--sigplot', action='store_true', help='Plot input data signal')
	parser.add_argument('-ps', '--psplot', action='store_true', help='FFT and Power Spectrum plots')
	parser.add_argument('-pf', '--psfit', action='store_true', help='Power Spectrum Fit')
	
	return parser.parse_args(args=None if sys.argv[1:] else ['--help'])
	
def func_fit(f, N, beta):
	"""
	Funzione per il fit Spettro Potenza di diversi tipi di rumore
	
	Parameters
	--------------------------------------------
	f : frequenze
    N : normalizzazione
    beta : esponente per dipendenza da frequenza
    
    Return
    --------------------------------------------
    func : Funzione per il fit
	"""

	func = N/f**beta

	return func

def noise():

	
	# Grafico dei segnali in ingresso
	if args.sigplot:
		
		fig,ax = plt.subplots(figsize=(9,6))
		plt.plot(df1['time'], df1['meas'], color='cyan', label='Sample 1')
		plt.plot(df2['time'], df2['meas'], color='green',label='Sample 2')
		plt.plot(df3['time'], df3['meas'], color='orange', label='Sample 3')
		plt.legend()
		plt.xlabel('time [s]')
		plt.xlabel('Signal')
		plt.show()
	
	# FFT su segnale 1
	dt1 = df1['time'][1]-df1['time'][0]
	c1  = fft.fft(df1['meas'].values)
	f1  = fft.fftfreq(len(c1), d=dt1)

	# FFT su segnale 2
	dt2 = df2['time'][1]-df2['time'][0]
	c2  = fft.fft(df2['meas'].values)
	f2  = fft.fftfreq(len(c2), d=dt2)

	# FFT su segnale 3
	dt3 = df3['time'][1]-df3['time'][0]
	c3  = fft.fft(df3['meas'].values)
	f3  = fft.fftfreq(len(c3), d=dt3)
	
	# Grafico spettro di potenza dei segnali
	if args.psplot:
	
		fig,ax = plt.subplots(figsize=(9,6))
		plt.plot(f1[:len(c1)//2], np.absolute(c1[:len(c1)//2])**2, color='cyan', label='Sample 1')
		plt.plot(f2[:len(c2)//2], np.absolute(c2[:len(c2)//2])**2, color='green', label='Sample 2')
		plt.plot(f3[:len(c3)//2], np.absolute(c3[:len(c3)//2])**2, color='orange', label='Sample 3')
		plt.xscale('log')
		plt.yscale('log')
		plt.xlabel('f [Hz]')
		plt.ylabel(r'$\left| c_k\right|^2$')
		plt.legend(fontsize=14)
		plt.show()
		
	# Calcola il fit e mostra il grafico
	if args.psfit == True:
	
		# Fit Sample 1
		pv1, pc1 = optimize.curve_fit(func_fit, f1[2:len(c1)//2], np.absolute(c1[2:len(c1)//2])**2, p0=[1, 1])
		print('Parameters Fit Sample 1:', pv1)

		# Fit Sample 2
		pv2, pc2 = optimize.curve_fit(func_fit , f2[5:len(c2)//2], np.absolute(c2[5:len(c2)//2])**2, p0=[1, 1])
		print('Parameters Fit Sample 2:', pv2)
		
		
		# Fit Sample 3
		pv3, pc3 = optimize.curve_fit(func_fit , f3[5:len(c3)//2], np.absolute(c3[5:len(c3)//2])**2, p0=[1, 1])
		print('Parameters Fit Sample 3:', pv3)
		
		
		# Grafico del fit sui segnali
		plt.style.use('dark_background')
		fig,ax = plt.subplots(figsize=(9,6))
		plt.plot(f1[:len(c1)//2], np.absolute(c1[:len(c1)//2])**2, color='white', label=r'Sample 1: $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv1[1], np.sqrt(pc1[1,1])))
		plt.plot(f2[:len(c2)//2], np.absolute(c2[:len(c2)//2])**2, color='pink', label=r'Sample 2: $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv2[1], np.sqrt(pc2[1,1])))
		plt.plot(f3[:len(c3)//2], np.absolute(c3[:len(c3)//2])**2, color='tomato', label=r'Sample 3: $\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv3[1], np.sqrt(pc3[1,1])))

		plt.plot(f1[1:len(c1)//2], func_fit(f1[1:len(c1)//2], pv1[0], pv1[1]), color='slategray')
		plt.plot(f2[1:len(c2)//2], func_fit(f2[1:len(c2)//2], pv2[0], pv2[1]), color='magenta')
		plt.plot(f3[1:len(c3)//2], func_fit(f3[1:len(c3)//2], pv3[0], pv3[1]), color='darkred')

		plt.legend(fontsize=14, frameon=False)
		plt.xscale('log')
		plt.yscale('log')
		plt.xlabel('f [Hz]')
		plt.ylabel(r'$\left| c_k\right|^2$')
		plt.show()

	
if __name__=="__main__":

	# Lettura file dati e trasformazione in DataFrame
	df1 = pd.read_csv('DATI_E09/data_sample1.csv')
	df2 = pd.read_csv('DATI_E09/data_sample2.csv')
	df3 = pd.read_csv('DATI_E09/data_sample3.csv')

	# Richiamo funzione degli argomenti
	args = parser_arguments()
	
	noise()
