import sys, os
import numpy as np
import pandas as pd
from scipy import constants, fft, optimize
import matplotlib.pyplot as plt
import argparse

"""
Produrre uno script python che:

1- Legga i file di dati e generi un DataFrame pandas per ciascuno di essi;
2- Generi un grafico di tutte le curve di luce (Flusso vs Giorno Giuliano) sovrapposte con una legenda che identifichi le sorgenti;
3 -Generi un unico grafico con 3 pannelli sovrapposti, in ogni pannello deve comparire la curva di luce di una sorgente;
4- Calcoli la trasformata di Fourier delle curve di luce;
5- Generi un grafico con gli spettri di potenza delle diverse sorgenti in 3 pannelli diversi, provare a fare un fit per stimare l'andamento 1/f^b;
6- Generi un grafico con gli spettri di potenza delle diverse sorgenti sovrapposte in un unico pannello;
7- Generi un grafico con gli spettri di potenza delle diverse sorgenti sovrapposti e normalizzati ai rispettivi coefficiente di ordine zero, spiegare significato della normalizzazione?
8- Per una o più sorgenti:
	-Applichi un filtro ai coefficienti di Fourier selezionando solo le componenti che descrivono l'andamento generale in funzione del tempo (escludendo futtuazioni di breve periodo);
	-Applichi un secondo filtro ai coefficienti di Fourier selezionando solo le componenti ad alta frequenzain modo tale che sia complementare al primo filtro;
	-Calcoli la trafsformata di Fourier inversa a partire dai coefficienti filtarti;
	-Produca un grafico che confronti il segale originale con quelli filtrati;
SUGGERIMENTO: per ottimizzare la scrittura del codice, provare ad usare un dictionary per immagazzinare le informazioni sulle diverse sorgenti in modo da sfruttare i cicli for per le diverse operazioni.
"""

def parse_arguments():

    parser = argparse.ArgumentParser(description='Plot and fit noise data.', usage='python3 lightcurve_fft.py --option')
    parser.add_argument('--lc', action='store_true', help='Plot input Light Curves')
    parser.add_argument('--psplot', action='store_true', help='Plots about FFT and Power Spectrum')
    parser.add_argument('--psfit', action='store_true', help='Perform and Plot Power Spectrum Fit')
    parser.add_argument('--psfilter', action='store_true', help='Apply and Plot Power Spectrum Filter')
    
    return  parser.parse_args(args=None if sys.argv[1:] else ['--help'])
    
   
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

	# Creazione dictionary per i dati 
	source_dict = {'Bl Lac': {'file' : 'DATI_E09/4FGL_J2202.7+4216_weekly_9_15_2023_mcf.csv', 'class': 'BLL'},
		         '3C 279' : {'file' : 'DATI_E09/4FGL_J1256.1-0547_weekly_9_15_2023_mcf.csv', 'class': 'FSRQ'},
		         '3C 454.3' : {'file' : 'DATI_E09/4FGL_J2253.9+1609_weekly_9_15_2023_mcf.csv', 'class': 'FSRQ'}
		           }
		           
	# Lettura dati e creazione Dataframe nel dictionary
	for source in source_dict:

		dfsource = pd.read_csv( source_dict[source]['file'] )
		source_dict[source].update( {'df' : dfsource } )


	# Grafico dei segnali in ingresso
	if args.lc == True:
	
		# Plot sorgenti 
		fig,ax = plt.subplots(figsize=(9,6))
		for source in source_dict:
			plt.plot(source_dict[source]['df']['Julian Date'], source_dict[source]['df']['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'], label=source)

		plt.legend()
		plt.xlabel('Julian Date')
		plt.ylabel('Photon Flux [0.1-100 GeV](photons cm-2 s-1)')
		plt.show()

		# Plot sorgente FSRQ e BLL separati
		fig,ax = plt.subplots(3,1,figsize=(10,11), sharex=True)
		ia = 0
		for source in source_dict:

			sc = 'darkorange'
			if source_dict[source]['class'] == 'FSRQ':
				sc = 'limegreen'

			ax[ia].plot(source_dict[source]['df']['Julian Date'], source_dict[source]['df']['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'],  color = sc, label=source) 
			ax[ia].legend()            
			ax[ia].set_ylabel('photons cm-2 s-1')
			ia+=1

		ax[ia-1].set_xlabel('Julian Date')
		plt.show()

	
	# Calcolo FFT
	for source in source_dict:            

		# Delta t
		dt = source_dict[source]['df']['Julian Date'][1]-source_dict[source]['df']['Julian Date'][0]

		# FFT e frequenze
		cc = fft.fft(source_dict[source]['df']['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'].values)
		ff = fft.fftfreq(len(cc), d=dt)

		# Aggiunta risulatti FFT a dictionary con info sorgenti
		source_dict[source].update({ 'c' : cc, 'freq' : ff })


	# Grafico spettri di potenze
	if args.psplot == True:

		fig,ax = plt.subplots(figsize=(9,6))

		for source in source_dict:            

			sc = 'darkorange'
			if source_dict[source]['class'] == 'FSRQ':
				sc = 'limegreen'

			tmp_len = len(source_dict[source]['c'])//2
			ps0 = np.absolute(source_dict[source]['c'][0])**2                
			plt.plot( source_dict[source]['freq'][:tmp_len], (np.absolute(source_dict[source]['c'][:tmp_len])**2)/ps0,  color=sc, label=source)

		plt.xscale('log')
		plt.yscale('log')
		plt.xlabel('f [1/d]')
		plt.legend()
		plt.show()


	# Calcolo del fit
	if args.psfit == True:
	
		fig,ax = plt.subplots(3,1,figsize=(10,11), sharex=True)
		ia = 0

		for source in source_dict:

			tmp_len = len(source_dict[source]['c'])//2
			pv, pc = optimize.curve_fit(func_fit , source_dict[source]['freq'][2:tmp_len], np.absolute(source_dict[source]['c'][2:tmp_len])**2, p0=[1e-16, 2])
			print('Parameters Fit Sample 1', pv)

			sc = 'darkorange'
			if source_dict[source]['class'] == 'FSRQ':
				sc = 'limegreen'
			
			ax[ia].plot( source_dict[source]['freq'][:tmp_len], np.absolute(source_dict[source]['c'][:tmp_len])**2,  color=sc, label=source)
			ax[ia].plot( source_dict[source]['freq'][:tmp_len], func_fit(source_dict[source]['freq'][:tmp_len], pv[0], pv[1] ), color='darkred'   )
			#ax[ia].plot( source_dict[source]['freq'][1:tmp_len], func_fit(source_dict[source]['freq'][1:tmp_len], 1e-16, 2 ), color='darkred'   )
			ax[ia].legend()            
			ax[ia].set_ylabel('')
			ax[ia].set_xscale('log')
			ax[ia].set_yscale('log')

			ax[ia].text(0.1, 0.1, r'$\beta$ = {:1.2f} $\pm$ {:1.2f}'.format(pv[1], np.sqrt(pc[1,1])), fontsize=14, transform=ax[ia].transAxes, color=sc)
			ia+=1
			
		ax[ia-1].set_xlabel('f [1/d]')
		plt.show()


	# Filtro dello spettro di potenze
	if args.psfilter == True:
	
		fig,ax = plt.subplots(3,1,figsize=(12,11), sharex=True, tight_layout=True)
		ia = 0

		for source in source_dict:

			## Copio coefficienti di Fourier e applico maschera
			ccsig  =source_dict[source]['c'].copy()
			ccnoise=source_dict[source]['c'].copy()
			psmask = source_dict[source]['freq'] > 2e-2             
			ccsig[   psmask]=0
			ccnoise[~psmask]=0

			# Ricavo la serie temporale filtrata attraverso la trasformata di Fourer inversa
			filtered_sig   = (fft.ifft(ccsig  )).astype(float)
			filtered_noise = (fft.ifft(ccnoise)).astype(float)


			sc = 'darkorange'
			if source_dict[source]['class'] == 'FSRQ':
				sc = 'limegreen'

			ax[ia].plot(source_dict[source]['df']['Julian Date'], source_dict[source]['df']['Photon Flux [0.1-100 GeV](photons cm-2 s-1)'],  color=sc, label=source)
			ax[ia].plot( source_dict[source]['df']['Julian Date'], filtered_sig,    color='darkblue', label='Filtered Light Curve')
			ax[ia].plot( source_dict[source]['df']['Julian Date'], filtered_noise,  color='darkred',  label='Filtered High Freq. Noise')
			ax[ia].legend()                            
			ia+=1

		ax[ia-1].set_xlabel('Julian Date')
		ax[ia-1].set_ylabel('Photon Flux [0.1-100 GeV](photons cm-2 s-1)')
		plt.show()

if __name__=='__main__':

	# Richiamo funzione degli argomenti
	args = parse_arguments()

	# Richiamo funzione principale
	noise()
    
    
    
