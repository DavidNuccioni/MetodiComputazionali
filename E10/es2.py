import numpy as np
import matplotlib.pyplot as plt
import argparse
"""
1- Produrre un modulo python che definisca una procedura di Random Walk in due dimensioni con le seguenti caratteristiche:
	-La diffusione ha un passo costante di lunghezza s;
	-Ad ogni passo lo spostamento può andare con uguale probabilità in ogni direzione (probabilità costante per phi=[0;2pi], con: Dx = s*cosphi Dy = s*sinphi
	- Il modulo deve mettere a disposizione una funzione che, data la lunghezza del passo s e il numero di passi N restituisca due array con rispettivamente lo spostamento lungo l'asse X e l'asse Y per ognuno degli N passi rispetto al punto di partenza.

2- Definire uno script python che importi il modulo precedentemente definito per:
	-Produrre un grafico 2D delle posizioni di 5 random walker per 1000 passi;
	SUGGERIMENTO: utilizzare una lista di array o un array 2D;
	-Produrre ung grafico con due pannelli che mostri nel primo pannello lo stesso grafico del punto A e nel secondo pannello il quadrato della distanza dal punto di partenza in funzione dei passi per gli stessi 5 random walker.
"""
def parser_arguments():
	"""
	Funzione che definisce gli argomenti da passare quando si esegue il codice
	"""
	
	parser = argparse.ArgumentParser(description='Diffusione 2D simmetrica')
	parser.add_argument('-t', '--traj', action='store_true', help='Stampa le traiettorie delle particelle')
	parser.add_argument('-s', '--sqm', action='store_true', help='Confronta le distanze quadratiche medie dei walker')
	
	return  parser.parse_args()

def scatter_particle():
	"""
	Randomizza la direzione del walker in maniera casuale 
	"""	
	
	# Definizioni del valore che vengono generati casualmente per phi
	phi = np.random.uniform(0.0, 2.0*np.pi)
	
	# Definizione dei versori
	dir_x = np.cos(phi)
	dir_y = np.sin(phi)
	rand_dir = [dir_x, dir_y]
	
	return rand_dir
	
def random_walk2D(N_wal):
	"""
	Esegue il random walk e ne restituisce array con traiettoria del walker
	"""
	# Lista per triaettorie
	position = [(0.0,0.0,0.0)]	
	
	# Inizio della diffusione
	#---------------------------------------------------------------------
	# Creazione walker al centro del sistema 	
	x = 0.0							
	y = 0.0						
	
	for j in range(Nstep):
		
		# Randomizzazione direzione particella
		dir_i = scatter_particle()		# Array con componenti direzione casuale 
		
		# Movimento della particella 
		x_new = x + (s * dir_i[0])
		y_new = y + (s * dir_i[1])	

		# Salva la traiettoria
		position.append((x_new, y_new))	

		# Aggiornamento variabili
		x = x_new 
		y = y_new 
	#---------------------------------------------------------------------
	
	return position

def main():
		
	# Grafico per traiettorie
	if args.traj:
		
		plt.figure()
		
		# Plot delle traiettorie di 5 walker
		c = ['limegreen', 'olivedrab', 'chocolate', 'royalblue', 'darkorchid']
		for w in range(N_wal):
		
			# Esegue la diffusione random walk
			traj = random_walk2D(N_wal)	
			x = [pos[0] for pos in traj]
			y = [pos[1] for pos in traj]
			plt.plot(x, y,  color=c[w], label=f'Walker {w+1}', zorder=1)

		plt.scatter(0.0, 0.0, color='red', s=30, zorder=10)
		plt.xlabel(r'$\Delta x$')
		plt.ylabel(r'$\Delta y$')
		plt.title("Grafico delle traiettorie di 5 walker")
		plt.legend()
		plt.show()
		
	# Confronto traiettorie e distanza quadratica media
	if args.sqm:
	
		c = ['limegreen', 'olivedrab', 'chocolate', 'royalblue', 'darkorchid']
		fig, ax = plt.subplots(1,2, figsize=(14,8))
		
		for w in range(N_wal):
			
			traj = random_walk2D(N_wal)	
			sqm = []
			x = [pos[0] for pos in traj]
			y = [pos[1] for pos in traj]
			
			for i in range(len(traj)):
				r2 = np.sqrt(traj[i][0]**2+traj[i][1]**2)
				sqm.append(r2)
			
			steps = np.arange(len(traj))
			
			ax[0].plot(x, y, color=c[w], label=f'Walker {w+1}', zorder=1)
			ax[1].plot(steps, sqm, color=c[w], label=f'Walker {w+1}')

		ax[0].set_xlabel(r'$\Delta x$')
		ax[0].set_ylabel(r'$\Delta y$')
		ax[0].scatter(0.0, 0.0, color='red', s=30, zorder=10)

		ax[1].set_xlabel('step')
		ax[1].set_ylabel(r'$d^2$')
		
		plt.show()
		
		print(len(traj))
		print(len(sqm))
	
		
if __name__=='__main__':

	args = parser_arguments()
	
	# Definizione delle variabili e parametri iniziali
	N_wal = 5
	Nstep = 1000
	s = 1
	
	main()
	
