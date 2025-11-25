"""
Scrivere uno script python che:
1- Risolva l'equazione differenziale per V_out dato V_in;
2- Definisca V_in per il tempo t = [0;10] tale che V_in = 1 per t pari e V_in = -1 per t dispari
SUGGERIMENTO: per distinguere fra valori pari o dispari convertire in intero ed usare l' operatore %
SUGGERIMENTO: V_in dipende dal tempo ed è nota, nell'implementazione della soluzione dell'equazione differenziale va ricavata in funzione del tempo t
3- Produca un grafico di V_in e V_out per RC = 4, 1, 0.25 con la condizione iniziale V_out0 = 0;
4- Salvi i risultati (t, V_in, V_out) in un file CSV. I risultati per V_out per i tre valori di RC vanno salvati nello stesso file.
OPZIONALE ripetere i passi precendenti con un potenziale V_in diverso.
"""

import numpy as np
import pandas as pd
from scipy import integrate
import matplotlib.pyplot as plt
import argparse

def Vin(t):
	"""
	Funzione che definisce il potenziale V_in 
	
	Parametri:
	-----------
	t : valore del tempo 
	
	Return: 
	-----------
	+1 per valori di t pari
	-1 per valori di t dispari
	"""

	if np.isscalar(t):
		if int(t)%2 == 0:
			return 1
		else:
			return -1
	else:
		V_in = np.ones(len(t))
		odd_mask = t.astype(int) %2 != 0
		V_in[odd_mask] = -1
	
		return V_in
	
def Vout_ar(V_out, t, rc, V_in):
	"""
	Funzione che definisce l'equazione differenziale del circuito RC

	Parametri:
	-----------
	V_out : variabile potenziale V_out
	t     : variabile tempo
	rc    : costante dell'equazione
	V_in  : Variabile potenziale V_in

	Return:
	-----------
	
	"""
	dV_outdt = (Vin(t) - V_out) / rc
	
	return dV_outdt
	
	
def parser_arguments():
	"""
	Funzione che definisce gli argomenti da passare quando si esegue lo script
	"""
	parser = argparse.ArgumentParser(description='Soluzione circuito RC passa basso.', usage      ='python3 es4.py --opzione')
	parser.add_argument('-4', '--rc4', action='store_true', help='Esegui con parametro rc = 4')
	
	parser.add_argument('-1', '--rc1', action='store_true', help='Esegui con parametro rc = 1')
	
	parser.add_argument('-0', '--rc0', action='store_true', help='Esegui con parametro rc = 0.25')
	
	parser.add_argument('--save', action='store_true', help='Soluzione salvata in un file CircuitoRC.csv')
	
	return parser.parse_args()
	
def main():

	# Scelta dei diversi parametri tramite argomento
	args = parser_arguments()
	
	if args.rc4:
		
		rc = 4
	
	elif args.rc1:
	
		rc = 1

	elif args.rc0:
		
		rc = 0.25
		
	else: 
		print('Nessuna opzione specificata')
		print('usare opzione --help per maggiori info')
		return
		
	# Condizione iniziale
	V_out0 = 0
	
	# Vettore del temporale
	dt = 0.01
	time_vec = np.arange(1, 10, dt)
	
	# Soluzione equazione differenziale 
	solRC = integrate.odeint(Vout_ar, y0=V_out0, t=time_vec, args=(rc, Vin))
	
	# Grafico della soluzione
	plt.subplots(figsize=(9,7))
	plt.title(r'$V_{in}$ ', fontsize=16, color='magenta')
	plt.plot(time_vec, Vin(time_vec),  label='$V_{in}$', color='magenta')
	plt.plot(time_vec, solRC, label='$V_{out}$'  )
	plt.legend(loc='upper right', fontsize=14)
	plt.xlabel('t [s]')
	plt.ylabel('V [V]')
	plt.legend( fontsize=14, ncol=4, bbox_to_anchor=(-0.01, 1.0, 1.0, 0.25), loc='lower left', framealpha=0  )
	plt.show()
	
	# Salvataggio dei dati 
	if args.save == True:
	
		# Creazione dataframe vuoto
		dfrc = pd.DataFrame(data={ 
		'Time'	: time_vec,
		'V_in'	: Vin(time_vec),
		'V_out'	: solRC.flatten(),
		})
		
		# Salvataggio del dataframe
		csvname = 'CircuitoRC.csv'
		dfrc.to_csv(csvname, index=False)
		print('Risultato salvato in', csvname)
	
if __name__=='__main__':

	main()
	





