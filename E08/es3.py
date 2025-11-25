"""
Produrre uno script python che, date delle condizioni iniziali a piacere (x0, y0, vx0, vy0) e con omegax e omegay configurabile:
1- Risolva l'equazione differenziale;
2- Generi un grafico di x, y, vx, vy;
3- Generi un grafico della traiettoria y vs x per un intervallo di tempo a scelta;
Provare i risultati per diverse combinazione dei parametri configurabili.
"""
import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import argparse

# ⚠️ Animazione presa dalle soluioni ⚠️
def animate(i, x, y, dt, line, mass, text):

    """
    Funzione pe animazione pendolo

    Assegna la posizione  istante per istante  agli ogetti da animare
    Il fulcro del pendolo è posizionato alle coordinate (0,0)

    Parametri
    ----------

    i    : indice del frame da rappresenare (obbligatorio con FuncAnimatuin)
    x    : array con coordinate x della massa del pendolo in funzione del tempo
    y    : array con coordinate y della massa del pendolo in funzione del tempo
    dt   : distanza temporale fra i punti dell'array dei tempi con cui si è risolta l'equazione del moto
    line :
    mass : oggetto grafico  che rappresenta la massa del pendolo   (plt.plot(   x[i],    yi[i] ))
    text : testo con tempo che scorre

    Output
    -----------
    return line, mass, text
    """
    
    line_x = x[:i]
    line_y = y[:i]
    line.set_xdata(line_x)
    line.set_ydata(line_y)

    mass_x = x[i]
    mass_y = y[i]
    mass.set_xdata(mass_x)
    mass.set_ydata(mass_y)

    time_template = 'time = %.1fs'
    text.set_text(time_template % (i*dt))

    return line, mass, text
    
def parser_arguments():
	"""
	Funzione che definisce gli argomenti da passare quando si esegue lo script
	"""
	parser = argparse.ArgumentParser(description='Soluzione del moto oscillatore 2D')

	parser.add_argument('-p', '--par', action='store_true', help='Inserisci i nuovi parametri del sistema')
	parser.add_argument('-d', '--default', action='store_true', help='Esegeui con i parametri di default')
	
	return  parser.parse_args()

def sist_eq(r, t, om_x, om_y):

	"""
	Funzione che definisce l'equazione differenziale del'oscillatore 2D
	
	Parametri
	-----------
    drdt(rv, t, omega) derivate per equazione differenziale dell'oscillatore 2D
    r 	 : vettore con variabili x, y, dx/dt, dy/dt
    t 	 : variabile tempo
    om_x : pulsazione oscillatore per x
    om_y : pulsazione oscillatore per y
    
    Return
    -----------
    sist_ar : array con le variabili che vengono calcolate successivamente
	"""
	dxdt = r[2]
	dydt = r[3]
	dvxdt = -om_x**2 * r[0]
	dvydt = -om_y**2 * r[1]
	sist_ar = (dxdt, dydt, dvxdt, dvydt)    
	return sist_ar

def main():
    
	# Scelta delle diverse condizioni iniziali e parametri tramite argomento
	args = parser_arguments()
	
	if args.default:
		
		# Parametri
		om_x = 1.0
		om_y = 4.5

		# Condizioni iniziali
		x0  =  4.5
		y0  = -3
		v_0x =  1
		v_0y =  5
		cond_ini = (x0, y0, v_0x, v_0y)
		
	elif args.par:
	
		
		# Inserimento parametri
		om_xi = input('inserisci omega_x ')
		om_x  = float(om_xi)
		om_yi = input('inserisci omega_y ')
		om_y  = float(om_yi)
		
		# Inserimento condizioni iniziali
		x0i = input('inserisci x0 ')
		x0  = float(x0i)
		y0i = input('inserisci y0 ')
		y0  = float(y0i)
		v_0xi = input('inserisci v_0x ')
		v_0x  = float(v_0xi)
		v_0yi = input('inserisci v_0y ')
		v_0y  = float(v_0yi)
		cond_ini = (x0, y0, v_0x, v_0y)
			
	else: 
		print('Nessuna opzione specificata')
		print('usare opzione --help per maggiori info')
		return
	
	# Vettore del tempo 
	dt = 0.01 
	time_vec = np.arange(0, 60, dt)

	# Soluzione dell'equazione differenziale
	osc2D  = integrate.odeint(sist_eq, cond_ini, time_vec, args=(om_x,om_y))


	# Grafico della soluzione
	fig,ax = plt.subplots(2,1, figsize=(12,10), sharex=True)
	ax[0].plot(time_vec, osc2D[:,0], color='cornflowerblue' , label='X')
	ax[0].plot(time_vec, osc2D[:,1], color='orange' ,         label='Y')
	ax[0].set_xlabel('time [s]')
	ax[0].set_ylabel('X/Y  [m]')
	ax[0].legend()
	ax[1].plot(time_vec, osc2D[:,2], color='cornflowerblue')
	ax[1].plot(time_vec, osc2D[:,3], color='orange')
	ax[1].set_xlabel('time [s]')
	ax[1].set_ylabel('v    [m/s]')
	plt.show()

	# Grafico della traiettoria 
	plt.plot(osc2D[:,0], osc2D[:,1], color='cornflowerblue')
	plt.plot(x0,y0, 'o', color='red')
	plt.xlabel('X [m]')
	plt.ylabel('Y [m]')
	plt.show()


	# ⚠️ Animazione presa dalle soluioni ⚠️
    #------------------- Animazione  ------------------------------------#

	# Figura per animazione 
	fig = plt.figure(figsize=(9,8))
	ax  = fig.add_subplot(111, autoscale_on=False, xlim=(-6, 6), ylim=(-6, 6))

	# Oggetti da animare (linea, massa, testo)
	line, = ax.plot([], [], '-', lw=1,   color='slategray')
	mass, = ax.plot([x0], [y0], 'o',        markersize=15, color='darkred'  )
	time_text      = ax.text(0.05, 0.9, '', transform=ax.transAxes, fontsize=16)

	# Animazione 
	ani = animation.FuncAnimation(
		fig,                                                      # Figura per animazione
		animate,                                                  # Funzione per animazione con calcolo oggetti ad ogni istante
		np.arange(1, len(time_vec)),                                # valori su cui iterare ( corripondnete all'indice i in animate)
		fargs=( osc2D[:,0],osc2D[:,1],dt, line, mass, time_text), # argomenti aggiuntivi della funzione animate
		interval=5,                                               # Intervallo fra due frame successivi (ms)
		blit=True)                                                # Ottimizzazione grafica

	plt.xlabel('X [m]')
	plt.ylabel('Y [m]')
	plt.show()

if __name__ == "__main__":

    main()
