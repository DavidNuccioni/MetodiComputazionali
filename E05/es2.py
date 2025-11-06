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

def melt():
	"""
	Funzione che legge un file csv e li unisce in unico dataframe

    	Parameters
    	------------

    	Return:
    	------------
    	df : dataframe unito
	"""
	
	
	df_0 = pd.read_csv('Dati_E05/hit_times_M0.csv')
	df_1 = pd.read_csv('Dati_E05/hit_times_M1.csv')
	df_2 = pd.read_csv('Dati_E05/hit_times_M2.csv')
	df_3 = pd.read_csv('Dati_E05/hit_times_M3.csv')
	
	df = pd.concat([df_0, df_1, df_2, df_3], ignore_index=True)
	return df
	
	
def ar_hits(df):
	"""
	Funzione che i dati in un array di reco.Hits

    	Parameters
    	------------
    	df : dataframe 

    	Return:
    	------------
    	hits : array di oggetti di tipo Hit
	"""
	
	hits = np.array([reco.Hit( r['mod_id'], r['det_id'], r['hit_time'] ) for i, r in df.iterrows()])
	return hits
	
	
def ar_events(hits):
	"""
	Funzione che raggruppa i dati Hit in un array reco.Event ovvero descrive un evento

    	Parameters
    	------------
    	hits : array di dati hit
    	threshold : valore che separa un hit di due eventi diversi

    	Return:
    	------------
    	events : array di oggetti di tipo Event
	"""
	

	threshold = 200
	df = melt()
	hits = ar_hits(df)
	hits.sort(kind='mergesort') 

	dt = np.diff(hits).astype(float)
	dt_mask = dt > 0
	
	# Mi sono fatto aiutare
	boundaries = np.where(dt > threshold)[0] + 1
	groups = np.split(hits, boundaries)
	
	events = np.array([reco.Event(i) for i in groups if len(i) > 0])

	return events
	

def reconstruct():
	"""
	Funzione principale che crea i grafici richiesti e mostra i risultati
	
	Parameters
	------------
	
	Return:
	------------
	"""
	df = melt()

	hits = ar_hits(df)
	hits.sort(kind='mergesort') 
	print('Numero totale di Hit:', hits.size)

	dt = np.diff(hits).astype(float)
	dt_mask = dt > 0
	
	logbins = np.logspace(0, 6, 100)
	plt.hist(dt[dt_mask], bins=logbins)
	plt.xlabel(r'$\Delta t$ [ns]')
	plt.title('Differenze temporali degli Hit')
	plt.xscale('log')
	plt.yscale('log')
	plt.show()
	
	events = ar_events(hits)
	for ev in events[:10]:
		ev.summary()
		print()
	print('numero totale di Eventi: ', events.size)
	
	# Elementi definiti per creare i plot	
	n_hits = np.array([e.n_hit for e in events])
	durate = np.array([e.dt for e in events])
	events_sorted = sorted(events, key=lambda e: e.t_0)
	diff_times = np.diff([e.t_0 for e in events_sorted])
	
	plt.hist(n_hits, bins=20, color='skyblue', edgecolor='black')
	plt.xlabel("Numero di Hit per Evento")
	plt.ylabel("Conteggio")
	plt.title("Distribuzione del numero di Hit per Evento")
	plt.grid(True, linestyle="--", alpha=0.6)
	plt.show()
	
	plt.hist(durate, bins=20, color='lightgreen', edgecolor='black')
	plt.xlabel("Durata evento [ns]")
	plt.ylabel("Conteggio")
	plt.title("Distribuzione delle durate degli eventi")
	plt.grid(True, linestyle="--", alpha=0.6)
	plt.show()
	
	plt.hist(diff_times, bins=20, color='salmon', edgecolor='black')
	plt.xlabel("Differenza di tempo tra eventi consecutivi [ns]")
	plt.ylabel("Conteggio")
	plt.title("Distribuzione delle differenze temporali tra eventi")
	plt.grid(True, linestyle="--", alpha=0.6)
	plt.show()
	
	# Plot 2D
	
	xmod = [-5,  5, -5,  5]
	ymod = [ 5,  5, -5, -5]

	xdet = [-2.5, 2.5, 0, -2.5,  2.5]
	ydet = [ 2.5, 2.5, 0, -2.5, -2.5]
	
	hits = events[5].ar_hit

	# Coordinate assolute dei singoli hit
	hit_x = np.array([xmod[h.mid] + xdet[h.sid] for h in hits])
	hit_y = np.array([ymod[h.mid] + ydet[h.sid] for h in hits])
	hit_time = np.array([h.time for h in hits])

	# Tempo relativo (rispetto all'inizio evento)
	hit_time_rel = hit_time - hit_time.min()
	
	fig, ax = plt.subplots(figsize=(9, 8))
	
	# Scatter plot
	for xm, ym in zip(xmod, ymod):
        	ax.scatter(xm + np.array(xdet), ym + np.array(ydet), s=200, c='lightgray', edgecolors='gray', linewidths=0.5)
	sc = ax.scatter(hit_x, hit_y, s=240, c=hit_time_rel, cmap='plasma_r', edgecolors='k', vmin=0, vmax=200)


	# Colorbar
	cbar = plt.colorbar(sc, ax=ax, label='Hit $t - t_{start}$ [ns]')
	
	# Disegna bordi dei moduli
	for xm, ym in zip(xmod, ymod):
		ax.add_patch(plt.Rectangle((xm - 5, ym - 5), 10, 10, fill=False, color='gray', lw=1))
	
	# Layout e annotazioni
	ax.set_xlabel('X [m]')
	ax.set_ylabel('Y [m]')
	ax.set_xlim(-10, 10)
	ax.set_ylim(-10, 10)
	ax.set_aspect('equal', adjustable='box')
	ax.grid(False)

	# Titolo esempio
	ax.set_title("Event: 5 - Hits: 6")

	plt.show()


	"""
	for i, ev in enumerate(events[:5]):  # primi 5 eventi
		plot_event(ev)
	"""
if __name__ == "__main__":

    reconstruct()	
