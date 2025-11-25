"""
1- Definire una funzione per le equazioni differeziali che descrivono il moto del pendolo semplice;
2- Risolvere l'equzione differnziale attraverso scipy.integrate.odeint con le seguenti caratteristiche: l = 0.5m, theta_0 = 45°, omega_0 = 0;
3- Produrre il grafico di theta in funzione del tempo;
4- Risolvere l'eqauazione per diverse condizioni iniziali: l = 1m, theta_0 = 45° e l = 0.5m, theta_0 = 30°;
5- Confrontare in maniera appropriata il grafico di theta vs t per le diverse condizioni iniziali;
"""

import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

def drdt_ar(r, t, l, g):
	"""
	Funzione che definisce l'equazione differenziale del pendolo
	
	Parametri
	-----------
	r : vettore con variabili theta omega
	t : variabile tempo
	l : lunghezza del pendolo
	
	Return 
	-----------
	drdt : array con le variabili che vengono calcolate successivamente
	"""
	dthdt = r[1]
	domdt = -g/l * np.sin(r[0])
	drdt = [dthdt,domdt]
	return drdt
    
#⚠️ Animazione ripresa dalle soluzioni ⚠️
def animate_pendulum(i, x, y, dt, line, mass, text):
	"""
	Funzione per animazione pendolo

	Assegna la posizione  istante per istante  agli ogetti da animare
	Il fulcro del pendolo è posizionato alle coordinate (0,0)

	Parametri
	----------

	i    : indice del frame da rappresenare (obbligatorio con FuncAnimatuin)
	x    : array con coordinate x della massa del pendolo in funzione del tempo
	y    : array con coordinate y della massa del pendolo in funzione del tempo
	dt   : distanza temporale fra i punti dell'array dei tempi con cui si è risolta l'equazione del moto
	line : oggetto grafico  che rappresenta il filo di sospensione (plt.plot([0,x[i]],[0,yi[i]]))
	mass : oggetto grafico  che rappresenta la massa del pendolo   (plt.plot(   x[i],    yi[i] ))
	text : testo con tempo che scorre

	Output
	-----------
	return line, mass, text
	"""

	line_x = [0, x[i]]
	line_y = [0, y[i]]
	line.set_data(line_x,line_y)

	mass_x = x[i]
	mass_y = y[i]
	mass.set_data(mass_x,mass_y)

	time_template = 'time = %.1fs'
	text.set_text(time_template % (i*dt))

	return line, mass, text
	
def parser_arguments():
	"""
	Funzione che definisce gli argomenti dello script
	"""

	parser = argparse.ArgumentParser(description='Soluzione del moto del pendolo (omega_0 = 0)')

	parser.add_argument('--C1', action='store_true', help='Risolve la equazione per l = 0.5m e theta_0 = 45°')
	parser.add_argument('--C2', action='store_true', help='Risolve la equazione per l = 1m e theta_0 = 45°')
	parser.add_argument('--C3', action='store_true', help='Risolve la equazione per l = 0.5m e theta_0 = 30°')

	return  parser.parse_args()
	
def main():

	# Parametri dell'equazione e condizione iniziale uguale per tutti 
	g = 9.81				# [m/s²]
	omega0 = 0				# [rad/s]
	
	# Scelta delle diverse condizioni iniziali e parametri tramite argomento
	args = parser_arguments()
	
	if args.C1:
		
		l = 0.5 				# [m]
		theta0 = np.radians(45) # [rad]
		cond_ini = (theta0, omega0)
		
	elif args.C2:
	
		l = 1.0 				# [m]
		theta0 = np.radians(45) # [rad]
		cond_ini = (theta0, omega0)
		
	elif args.C3:
		
		l = 0.5 				# [m]
		theta0 = np.radians(30) # [rad]
		cond_ini = (theta0, omega0)
		
	else: 
		print('Nessuna opzione specificata')
		print('usare opzione --help per maggiori info')
		return
		

	# Condizioni iniziali al punto di massima oscillazione (theta=theta0, omega=emega0=0) 

	# Condizioni iniziali al punto di massima oscillazione (theta=theta0*2/3, omega=emega0=0) 

	# Vettore del tempo
	dt = 0.01
	time_vec = np.arange(0, 5, dt)

	# Soluzione equazione differenziale
	pend  = integrate.odeint(drdt_ar, cond_ini, time_vec, args=(l,g)) 

	# Grafico della soluzione 
	plt.subplots(figsize=(9,7))
	plt.title('Pendolo', fontsize=16)
	plt.plot(time_vec, np.degrees(pend[:,0]), label=r'$\theta_0 = 45^{\circ}$ l=0.5 $m$')
	#plt.plot(ptimes, np.degrees(psol45_2[:,0]), label=r'$\theta_0 = 45^{\circ}$ l=1.0 $m$')
	#plt.plot(ptimes, np.degrees(psol30_1[:,0]), label=r'$\theta_0 = 30^{\circ}$ l=0.5 $m$')
	plt.xlabel('t [s]',            fontsize=14)
	plt.ylabel(r'$\theta$  [deg]', fontsize=14)
	plt.xticks( fontsize=14 )
	plt.yticks( fontsize=14 )
	plt.legend( fontsize=14, ncol=3, bbox_to_anchor=(-0.01, 1.0, 1.0, 0.15), loc='lower left', framealpha=0  )
	plt.show()

	# ⚠️ Animazione presa dalle soluioni ⚠️
	#------------------- Animazione  ------------------------------------#

	# proiezione su asse x e y della soluzione. 
	x1 =  1*np.sin(pend[:, 0])
	y1 = -1*np.cos(pend[:, 0])


	# Figura per animazione 
	fig = plt.figure(figsize=(9,8))
	ax  = fig.add_subplot(111, autoscale_on=False, xlim=(-1.5, 1.5), ylim=(-1.5, 1.5))
	ax.grid()


	# Oggetti da animare (linea, massa, testo)
	pendulum_line, = ax.plot([], [], 'o-', lw=2, markersize=5,  color='slategray')
	pendulum_mass, = ax.plot([], [], 'o',        markersize=15, color='darkred'  )
	time_text      = ax.text(0.05, 0.9, '', transform=ax.transAxes, fontsize=16)

	# Animazione 
	pendulum_ani = animation.FuncAnimation(
		fig,                        # Figura per animazione
		animate_pendulum,           # Funzione per animazione con calcolo oggetti ad ogni istante
		np.arange(1, len(y1)),      # valori su cui iterare ( corripondnete all'indice i in animate)
		fargs=( x1,y1,dt, pendulum_line, pendulum_mass, time_text), # argomenti aggiuntivi della funzione animate 
		interval=25,                # Intervallo fra due frame successivi (ms)
		blit=True)                  # Ottimizzazione grafica
	plt.show()



if __name__ == "__main__":

	main()
