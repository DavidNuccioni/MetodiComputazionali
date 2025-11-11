"""
Creare uno script python che:
1- Legga il file di dati;
2- Produca il grafico dei segnali dell'oscilloscopio;
3- Calcoli la derivata del segnale attraverso la differenza centrale;
4- Produca il grafico della derivata calcolata;
5- Ricavi posizione e valore dei minimi dei segnali;
6- Trovi le coincidenze fra i due segnali;
8- Stimi l'efficienza dei due canali dell'oscilloscopio;
SUGGERIMENTO: per il calcolo della differenza centrale definire una funzione;
SUGGERIMENTO: per la differenza centrale provare più valori di n ed individuare quello più adatto ai dati.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import argparse

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
	
def deriv(ar_der, nh):
	"""
	Funzione che implementa il calcolo della differenza centrale
	f'(i) =  [f(i+nh)-f(i-nh)] / [x(i+nh)-x[i-nh]]
	
	Parameters
	-----------
	df_a : dataframe dei dati trasformato in array
	nh : costante sul quakle si fa la differenza centrale
	
	Return
	-----------
	nume/den : fornisce la differenza centrale sul tempo per un singolo segnale
	"""

	num = ar_der[:,1][nh:] - ar_der[:,1][:-nh]
	den = ar_der[:,0][nh:] - ar_der[:,0][:-nh]

	for ih in range(int(nh/2)):
		
		num = np.append(ar_der[:,1][nh-ih-1] - ar_der[:,1][0], num)
		num = np.append(num, ar_der[:,1][-1] - ar_der[:,1][-(nh-ih)])
		
		den = np.append(ar_der[:,0][nh-ih-1] - ar_der[:,0][0], den)
		den = np.append(den, ar_der[:,0][-1] - ar_der[:,0][-(nh-ih)])
		
	return num/den

def parse_arguments():
	"""
	Funzione che definisce gli argomenti da passare quando si esegue lo script
	"""
	
	parser = argparse.ArgumentParser(description='Calcolo della differenza centrale di due segnali di un oscciloscopio')
	
	parser.add_argument('-f', '--file', action='store', default='DATI_E06/oscilloscope.csv', help='Inserisci il percorso del nuovo file dat di input')
	
	parser.add_argument('-nh', '--nh', type=int, action='store', default=6000, help='Inserisci il numero nh su cui calcolare la differenza centrale')
	
	return  parser.parse_args()	
	
def main():	
	
	# Richiamo delle funzioni
	args = parse_arguments()
	
	# Dati utilizzati
	df_in = args.file
	df = data_read(df_in)
	
	# Plot dei segnali dell'oscilloscopio sovrapposti
	plt.subplots(figsize=(10, 8))
	plt.title('Segnali Oscilloscopio')
	plt.plot(df['time'], df['signal1'], color='tomato', label='Signal 1')
	plt.plot(df['time'], df['signal2'], color='cornflowerblue', label='Signal 2')                 
	plt.legend(fontsize=14)
	plt.xlabel('Time')
	plt.ylabel('Volt')
	plt.show()
	
#	fig, ax = plt.subplots(1,2, figsize=(15,8))
#	ax[0].plot(df['time'], df['signal1'], color='tomato', label='Signal 1')
#	ax[1].plot(df['time'], df['signal2'], color='cornflowerblue', label='Signal 2')
#	ax[0].set_xlabel('Time')
#	ax[1].set_xlabel('Time')
#	ax[0].set_ylabel('Volt')
#	ax[1].set_ylabel('Volt')
#	ax[0].legend(fontsize=14)
#	ax[1].legend(fontsize=14)
#	ax[0].set_ylabel('Y')
#	ax.set_title('Segnali Oscilloscopio')
#	plt.show()
	
	nh = args.nh 
	df_a = df.to_numpy()
	ris_plt = np.empty([])
	
	# Creo i grafici che stamperò dopo il ciclo for
	# Grafici separati
#	fig, ax = plt.subplots(1,2, figsize=(15,8))
	
	# Grafici sovrapposti
	fig, ax_s = plt.subplots(figsize=(15,8))
	colors = ['tomato', 'royalblue']
	
	for i in range(df_a.shape[1]-1):
		
		# Creo array con le colonne del tempo e del segnale 
		ar_der = df_a[:, [0,i+1]]
		
		# Calcolo della derivata
		der = deriv(ar_der, nh)
		
		# Plot separati
#		ax[i].plot(df['time'], der, color=colors[i], label=f'Signal {i+1}')
#		ax[i].set_xlabel('Time')
#		ax[i].set_ylabel(f'Volt')
#		ax[i].legend(fontsize=14)
	
		# Plot sovrapposti
		ax_s.plot(df['time'], der, color=colors[i], label=f'Signal {i+1}')
		ax_s.set_xlabel('Time')
		ax_s.set_ylabel(f'Volt')
		ax_s.legend(fontsize=14)
		
	plt.show()
	
	# ⚠️Soluzioni del prof⚠️
	# Convoluzione per attenuare il rumore
	dc1 = deriv(df_a[:, [0,1]], nh)
	dc2 = deriv(df_a[:, [0,2]], nh)
	der_sig1 = np.convolve(dc1, np.ones(5), 'same')
	der_sig2 = np.convolve(dc2, np.ones(5), 'same')

	# Plot delle derivate dei segnali sovrapposte
	plt.subplots(figsize=(10, 8))
	plt.title(f'Derivata Segnali Oscilloscopio - hn={nh} ns - media 5', fontsize=16)
	plt.plot(df['time'], der_sig1, color='limegreen',   label='Canale 1')
	plt.plot(df['time'], der_sig2, color='darkorange',  label='Canale 2')                 
	plt.legend(fontsize=14)
	plt.xlabel('t [ns]')
	plt.ylabel('V/s [mV/ns]')
	
	plt.show()
	
	# Selezione punti con derivata vicina allo zero e segnale superiore alla soglia
	mask_sig1 = (np.abs(der_sig1)< 0.015 ) & (df_a[:,1] < -10)
	mask_sig2 = (np.abs(der_sig2)< 0.015 ) & (df_a[:,2] < -10)
	
	# Accorpamento dei due canali
	tpeak_sig1 = np.empty(0)
	vpeak_sig1 = np.empty(0)
	tsum = df_a[:,0][mask_sig1][0]
	nsum = 1
	for it in range( 1, len(df_a[:,0][mask_sig1])):
		if ( (df_a[:,0][mask_sig1][it]-df_a[:,0][mask_sig1][it-1]) > 20)  or (it == (len(df_a[:,0][mask_sig1]))-1):
			print(tsum)
			tpeak_sig1 = np.append(tpeak_sig1, tsum)
			idx = np.argmin(np.abs(df_a[:,0] - tsum))
			vpeak_sig1 = np.append(vpeak_sig1, df_a[idx, 1])
			tsum = df_a[:,0][mask_sig1][it]
			
	tpeak_sig2 = np.empty(0)
	vpeak_sig2 = np.empty(0)
	tsum = df_a[:,0][mask_sig2][0]
	nsum = 1
	for it in range( 1, len(df_a[:,0][mask_sig2])):
		if ( (df_a[:,0][mask_sig2][it]-df_a[:,0][mask_sig2][it-1]) > 20)  or (it == (len(df_a[:,0][mask_sig2]))-1):
			print(tsum)
			tpeak_sig2 = np.append(tpeak_sig2, tsum)
			idx = np.argmin(np.abs(df_a[:,0] - tsum))
			vpeak_sig2 = np.append(vpeak_sig2, df_a[idx, 1])
			tsum = df_a[:,0][mask_sig2][it]          
	
	# Plot dei segnali dei massimi e minimi
	plt.subplots(figsize=(10,8))
	plt.title('Segnali Oscilloscopio con Minimi identificati', fontsize=16, color='slategray')
	plt.plot(df_a[:,0], df_a[:,1], color='limegreen', label='Canale 1')
	plt.plot(df_a[:,0], df_a[:,2], color='darkorange', label='Canale 2')
	plt.plot(tpeak_sig1, vpeak_sig1, 'o', color='darkgreen', label='Min. Canale 1')
	plt.plot(tpeak_sig2, vpeak_sig2, 'o', color='red', label='Min. Canale 2')
	plt.legend(fontsize=14)
	plt.xlabel('t [ns]')
	plt.ylabel('V [mV]')
	plt.ylim(-90, 10)
	plt.show()	           
	
	# Calcolo delle coincidenze
	tcoin1 = np.empty(0)
	tcoin2 = np.empty(0)
	vcoin1 = np.empty(0)
	vcoin2 = np.empty(0)

	window = 200
	for t1, v1 in zip(tpeak_sig1, vpeak_sig1):

		for t2, v2 in zip(tpeak_sig2, vpeak_sig2):
			if np.abs(t2-t1) < window:
				tcoin1 = np.append(tcoin1, t1)
				tcoin2 = np.append(tcoin2, t2)
				vcoin1 = np.append(vcoin1, v1)
				vcoin2 = np.append(vcoin2, v2)
			if t2 > t1 :
				break
	
	# Stampa delle informazioni sulle coincidenze e efficienza oscilloscopio
	print('--------------------------------------------')
	print(' Numero Coincidenze        :', len(tcoin1) )
	print(' Tempo Coincidenze Canale 1:', tcoin1)
	print(' Tempo Coincidenze Canale 2:', tcoin2)
	print(' Coincidenze t2-t1         :', tcoin2-tcoin1)
	print(' Efficenza Canale 1        : {:.2f}'.format( len(tcoin1)/len(tpeak_sig2)) )
	print(' Efficenza Canale 2        : {:.2f}'.format( len(tcoin2)/len(tpeak_sig1)) )
    	
	
	
	
	
	
		
if __name__ == "__main__":

	main()
