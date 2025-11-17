"""
Creare uno script python che:

1- Legga il file di dati indicato sopra e crei il corrispettivo DataFrame pandas;
2- Calcoli la massa invariante per ogni evento;
3- Produca un istogramma della massa invariante calcolata;
4- Produca un istogramma della massa invariante in un intervallo ristretto attorno al picco più alto;
SUGGERIMENTO: selezionare l'intervallo in modo tale da lasciare del margine attorno al picco in cui sia apprezzabile il livello di fondo;

Modificare lo script in modo tale che:

5- Definisca una funzione di fit (f_g1) corrispondnete ad una funzoine di Gaus + una polinomiale di primo grado;
6- Esegua il fit dei dati attorno al picco principale con la funzione f_g1;
7- Produca un grafico che mostri: la funzione di fit ottimizzata sovrapposta ai dati, lo scarto fra dati e fit (in un pannello separato) e lo scarto fra dati e fit diviso per l'errore (in un ulteriore pannello separato);
8- Stampi il valore dei parametri del fit e del chi quadro
9- Definisca una seconda funzione di fit (f_g2) corrispondnete alla somma di due funzoini di Gaus con stessa media ma diversa sigma e normalizzazione + una polinomiale di primo grado;
10- Ripeta i passi 2,3 e 4 del punto precedente anche per f_g2
11- Ripetere l'analisi anche per il picco a più alta energia, di che particella potrebbe trattarsi?
"""

import numpy as np
import pandas as pd
import numpy as np
import math
import argparse
import matplotlib.pyplot as plt
from scipy import optimize

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
	
def df_to_ar(df):
	"""
	Funzione che legge il dataframe e crea due array per le due particelle
	
	Parametri 
	----------
	df : dataframe dati che viene letto
	
	Return
	----------
	p1, p2 : array delle due particelle con componenti di energia e impulso
	"""
	p_1 = df[['E1','px1','py1','pz1']].to_numpy()
	p_2 = df[['E2','px2','py2','pz2']].to_numpy()
	
	return p_1, p_2
	
def parse_arguments():
	"""
	Funzione che definisce gli argomenti da passare quando si esegue lo script
	"""
	
	parser = argparse.ArgumentParser(description='Analisi del decadimento di J/Psi in muone-muone')
	
	parser.add_argument('-f', '--file', action='store', default='DATI_E07/Jpsimumu.csv', help='Inserisci il percorso del nuovo file dati di input')
	
	parser.add_argument('--hist', action='store_true', help='Istogramma delle masse invarianti')
   
	parser.add_argument('--fit1', action='store_true', help='Esegue fit con una funzione di Gauss per il segnale')
	parser.add_argument('--fit2', action='store_true', help='Esegue fit con due funzioni di Gauss per il segnale')
	
	return  parser.parse_args()	
	
def mass_inv(p1, p2):
	"""
	Funzione che calcolca la massa invariante per ogni evento
	
	Parametri 
	----------
	p1, p2 : array delle due particelle con componenti di energia e impulso
	
	Return
	----------
	m_inv : array con i risultati della massa invariante per ogni evento
	"""
	E_tot = pow(p1[:,0]+p2[:,0], 2)
	px_tot = pow(p1[:,1]+p2[:,1], 2)
	py_tot = pow(p1[:,2]+p2[:,2], 2)
	pz_tot = pow(p1[:,3]+p2[:,3], 2)
	p_tot = px_tot + py_tot + pz_tot
	m_inv = np.sqrt(E_tot - p_tot)
	
	return m_inv
	
def fit_fg1(x, m, A, s, p0, p1):
	""" 
    Fnzione esponenziale f(x) = A*e^-((x-m)²/2sigma²) + p1x + p0 su cui fare il fit
    
    Parametri
    ----------
    A  : parametro normalizzazione, altezza picco
    p1 : parametro polinomio lineare
    p0 : parametro costante polinomio lineare
    sigma : larghezza della gaussiana
    x : valore su cui calcolare il fit
    m : media della funzione di Gauss
    """
	pol = p1*x + p0
	gaus = A*np.exp( -0.5*(x-m)**2/s**2)
	return pol+gaus

def fit_fg2(x, m, A1, A2, s1,s2, p0, p1):
	""" 
    Fnzioni esponenziali f(x) = A_i*e^-((x-m)²/2sigma_i²) + p1x + p0 su cui fare il fit
    
    Parametri
    ----------
    A_i  : parametro normalizzazione, altezza picco
    p1 : parametro polinomio lineare
    p0 : parametro costante polinomio lineare
    sigma_i : larghezza della gaussiana
    x : valore su cui calcolare il fit
    m : media della funzione di Gauss
    """
	pol = p1*x+p0
	gaus1 = A1*np.exp(-0.5*(x-m)**2 / s1**2)
	gaus2 = A2*np.exp(-0.5*(x-m)**2 / s2**2)

	gaus=gaus1+gaus2

	return pol+gaus

def main():

	# Richiamo delle funzioni
	args = parse_arguments()
	
	# Dati utilizzati e convertiti in dataframe
	df_in = args.file
	df = data_read(df_in)
	
	# Df convertito in due array con le componenenti di energia e impulso delle due particelle
	p1, p2 = df_to_ar(df)
		
	# Calcolo della massa invariante e istogramma
	m_inv = mass_inv(p1, p2)
	
	# Se scelto come argomento mostra solo l'istogramma delle masse
	if args.hist == True:
		plt.hist(m_inv, bins=200, color='mediumblue')
		plt.xlabel(f'Massa invariante $mc^{2}$ in $[GeV]$')
		plt.ylabel(f'Eventi')
		plt.title('Istogramma delle masse invarianti per ogni evento')
		plt.grid(True, linestyle="--", alpha=0.6)
		plt.show()
		
	pnames = None
	params = None
	params_covariance = None
	yfit   = None
	
	if args.fit1 == True or args.fit2 == True:
		
		n, bins , p = plt.hist(m_inv, bins=200, range=(2.85,3.35), color='mediumblue')
		plt.xlabel(f'Massa invariante $mc^{2}$ in $[GeV]$')
		plt.ylabel(f'Eventi')
		plt.title('Istogramma delle masse invarianti')
		plt.grid(True, linestyle="--", alpha=0.6)
		plt.show()
		
		# Fit dei dati dell'istogramma
		x_ar = (bins[:-1]+bins[1:])/2
		y_ar = n
		bw=bins[1]-bins[0]
		
		# Fit con una sola funzione gaussiana
		if args.fit1 == True:
			pnames = ['m', 'A', 'sigma', 'p0', 'p1']
			pstart = np.array([3.1, 200,  0.2, 1, 0])
			params, params_covariance = optimize.curve_fit(fit_fg1, x_ar, y_ar, sigma=np.sqrt(y_ar), absolute_sigma=True, p0=[pstart])
			yfit = fit_fg1(x_ar, params[0], params[1], params[2], params[3], params[4])
			
		# Fit con due funzioni gaussiane
		if args.fit2 == True:
			pnames = ['m', 'A1', 'A2', 'sigma1', 'sigma2', 'p0', 'p1']
			pstart = np.array([3, 200, 50, 0.5, 2,  10, -0.1])            
			params, params_covariance = optimize.curve_fit(fit_fg2, x_ar, y_ar, sigma=np.sqrt(y_ar + 1), absolute_sigma=True, p0=[pstart])
			yfit = fit_fg2(x_ar, params[0], params[1], params[2], params[3], params[4], params[5], params[6])
		
		# Calcolo del chi-quadro
		chi2 =  np.sum( (y_ar - yfit)**2 /y_ar) 
		ndof = len(x_ar)-len(params)
		
		# Plot con la funzione fittata
		fig,ax = plt.subplots(3,1, figsize=(9,9), gridspec_kw={'height_ratios': [3, 1,1]}, sharex=True)
		fig.subplots_adjust(hspace=0)
		ax[0].errorbar(x_ar, y_ar, yerr=np.sqrt(y_ar), fmt='.', label='Data')
		ax[0].plot(x_ar, yfit, color='darkorange', label='Fit')
		ax[0].set_ylabel('Events / {:0.4f} GeV'.format(bw))
		ax[0].legend(fontsize=14, frameon=False)

		ax[1].errorbar(x_ar, y_ar-yfit, yerr=np.sqrt(y_ar), fmt='.')
		ax[1].axhline(y=0, color='darkorange' )
		ax[1].set_ylabel('Data-Fit')
		ax[1].set_ylim(-45,45)  
		ax[1].set_yticks(np.arange(-25, 26, 25))
		ax[1].grid(True, axis='y')

		ax[2].errorbar(x_ar, (y_ar-yfit)/np.sqrt(y_ar), yerr=1, fmt='.')
		ax[2].axhline(y=0, color='darkorange')
		ax[2].set_ylabel(r'(Data-Fit)/$\sigma$')
		ax[2].set_ylim(-4.5,4.5)  
		ax[2].set_yticks(np.arange(-2.5, 2.6, 2.5))
		ax[2].grid(True, axis='y')

		ax[2].set_xlabel(r'$m_{\mu\mu}$ [GeV]')

		fig.align_ylabels()
		plt.show()
				
		# Stampa dei valori analisi dati
		print('--------------------------------------------------------')
		print('           Risultati Fit Massa Invariante               ')
		for name,p,pe in zip(pnames, params, np.sqrt(params_covariance.diagonal()) ):
			print('{:6}  {:>10.4f} +- {:>7.4f}'.format(name,p,pe))

		print('--------------------------------------------------------')
		print('Massa Invarinate = {:>10.4f} +- {:.4f}  Gev/c^2'.format(params[0], np.sqrt(params_covariance[0,0] )) )
		print('Chi2 / ndf: {:4.2f} / {:d} = {:2.3f}'.format( chi2, ndof, chi2/ndof ) )

if __name__=='__main__':

	main()
	
	
	

