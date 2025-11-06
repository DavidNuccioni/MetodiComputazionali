"""
Punto 1:
Creare uno script python che esegua le seguenti operazioni:
- Legga uno o più file di input;
- Produca un istogramma dei tempi per uno dei moduli (file);
- Produca un istogramma delle differenze di tempi fra Hit consecutivi per uno dei moduli;
SUGGERIMENTO: usare il log10

Punto 2:
Creare il file reco.py che definisca la classe Hit.
Un oggetto di tipo Hit deve contenere informazioni su:
Id Modulo;
Id Sensore;
Time Stamp rivelazione.
Oggetti di tipo Hit devono essere ordinabili in base al Time Stamp ed eventualmente in base alla Id del Modulo e del Sensore.

Punto 3:
Creare uno script python che svolga le seguenti operazioni:
- Importi il modulo reco;
- Legga i file di dati e, per ognuno di essi, produca un array di reco.Hit;
SUGGERIMENTO: creare un funzione da richiamare per ogni file;
- Produca un array che corrisponda alla conbinazione, ordinata temporalmente, di tutti i reco.Hit;
SUGGERIMENTO: valutare l'utilizzo dell' overloading degli operatori > e < (__gt__, __lt__)
SUGGERIMANTO: utilizzare funzonalità numpy per ordinare gli elementi di un array (sort)
- Produca un istogramma dei (
) fra reco.Hit consecutivi;
SUGGERIMENTO: valutare l'utilizzo dell' overloading degli operatori + o - (__add__, __sub__)

Punto 4:
modificare il file reco.py in modo che:
Definisca anche la classe Event
Un oggetto di tipo Event deve contenere informazioni su:
Numero di Hit
Time Stamp del primo Hit
Time Stamp dell'ultimo Hit
Durata temporale
Array di tutti gli Hit

Punto 5:
Modificare lo script di analisi della Prima Parte aggiungendo funzionalità in modo che:
- Crei un array di oggeti di tipo reco.Event a partire dall'array ordinato di reco.Hit applicando auna finestra temorale ai tra reco.Hit consecutivi
SUGGERIMENTO: creare un funzione apposita
- Stampi informazioni dettagliate per i primi 10 reco.Event
SUGGERIMENTO: verificare che le informazioni stampate non contengano indizi di errore
- Produca l'istogramma del numero di reco.Hit per reco.Event
- Produca l'istogramma della durata dei reco.Event
- Produca l'istogramma delle differenze di tempo fra reco.Event consecutivi
- Produca il grafico 2D del numero di hit nell'evento in funzione della durata * SUGGERIMENTO: usare plt.scatter

Punto 6:
Estendere lo script precedente producendo la rappresentazione grafica dei primi 10 reco.Event (come nell'esempio iniziale)
OPZIONALE: includere nella rappresentazione grafica degli eventi anche l'informazione temporale atraverso il colore dei simboli.
Vedi esempio ed informazioni sul codice di seguito.
"""

import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import sys, os 
import reco

# Punto 1 
"""
# Leggo i file che sono in una sotto cartella 
df0 = pd.read_csv('Dati_E05/hit_times_M0.csv')
df1 = pd.read_csv('Dati_E05/hit_times_M1.csv')
df2 = pd.read_csv('Dati_E05/hit_times_M2.csv')
df3 = pd.read_csv('Dati_E05/hit_times_M3.csv')


# Creo l'istogramma dei tempi per il modulo 0 
n, bis, hist_0 = plt.hist(df0['hit_time'], bins=100, color='limegreen', alpha=0.7)
plt.show()

# Crea l'istogramma delle differenze temporali
n, bis, hist_0 = plt.hist(df0['hit_time'].diff(), bins=np.logspace(0, 2, 100), color='limegreen', alpha=0.7)
plt.xscale('log')
plt.show()
"""

# I punti seguenti dell'esercizio sono anche sul file reco.py

# Leggo i file che sono in una sotto cartella 
df_0 = 'Dati_E05/hit_times_M0.csv'
df_1 = 'Dati_E05/hit_times_M1.csv'
df_2 = 'Dati_E05/hit_times_M2.csv'
df_3 = 'Dati_E05/hit_times_M3.csv'

def ar_hits(df_i):
	"""
	Funzione che legge un file csv e inserisce i dati in un array di reco.Hits

    	Parameters
    	------------
    	df_i : percorso del file di dati

    	Return:
    	------------
    	hits : array di oggetti di tipo Hit
	"""
	
	df = pd.read_csv(df_i)
	hits = np.array([reco.Hit( r['mod_id'], r['det_id'], r['hit_time'] ) for i, r in df.iterrows()])
	return hits
		
	
def reconstruct():
	"""
	Funzione principale che ordina i dati e crea i grafici richiesti
	
	Parameters
	------------
	
	Return:
	------------
	"""	
	
# Utilizzo la funzione ar_hits per inserire i dataframe in 4 array
	M_0 = ar_hits(df_0)
	M_1 = ar_hits(df_1)
	M_2 = ar_hits(df_2)
	M_3 = ar_hits(df_3)
	
# Concateno i 4 array in unico array e stampo il numero di hits
	hits = np.concatenate((M_0, M_1, M_2, M_3))
	hits.sort(kind='mergesort') # mergesort aiuta ad ordinare meglio tenendo dati uguali
	print('Numero totale di Hit:', hits.size)
	
# Calcolo la differenza temporale tra due elementi dell'array e converto in float, applico maschera per avere dt positivi
	dt = np.diff(hits).astype(float)
	dt_mask = dt > 0
	
# Grafico tempi Hit con bin logaritmicamente spaziati e assi in scala logaritmica
	logbins = np.logspace(0, 6, 100)
	plt.hist(dt[dt_mask], bins=logbins)
	plt.xlabel(r'$\Delta t$ [ns]')
	plt.title('Differenze temporali degli Hit')
	plt.xscale('log')
	plt.yscale('log')
	plt.show()


if __name__ == "__main__":

    reconstruct()	
