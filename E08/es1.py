"""
Partendo dai parametri: m=0.2, k=2, C=0.5 e dalle condizioni inziali: x_0=0, v_0=0
Produrre uno script python che:
1- Risolva l'equazione differenziale per l'oscillatore forzato in modo tale che la funzione che descrive la forza esterna F(t) possa essere passata come parametro;
2- Produca il grafico di F(t), x(t) e v(t) per una forza sinusoidale F(t)=2sin(omega t) con un valore di omega a scelta;
3- Produca il grafico dell'ampiezza di oscillazione massima in funzione del valore di omega per la forza sinusoidale F(t)=2sin(omega t)
4- Esplorare e adattare i risultati dei punti 2 e 3 per altre forme funzionali di F(t);
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate
import argparse

def F1(om_f, time_vec):
	"""
	Funzione che definisce la forza esterna che viene passata come parametro alla funzione che risolve l'equazione differenziale, con omega scelto arbitrariamente
	
	F(t) = 2 * sin( omega t)
	"""
	F = 2 * np.sin(om_f * time_vec)

	return F


def F2(om_f, time_vec):
	"""
	Funzione che definisce la forza esterna che viene passata come parametro alla funzione che risolve l'equazione differenziale, con omega scelto arbitrariamente
	
	F(t) = 2 * sin(omega t) + sin (2*omega t)
	"""
	F = 2 * np.sin(om_f * t) + np.sin(2 * om_f * time_vec)

	return F


def F3(om_f, time_vec):
	"""
	Funzione che definisce la forza esterna che viene passata come parametro alla funzione che risolve l'equazione differenziale, con omega scelto arbitrariamente
	
	F(t) = 2(t/tau)² * exp(-t/tau)
	"""
	F = 2 * (time_vec * om_f)**2 * np.exp(-time_vec * om_f)

	return F
	

def drdt_ar(r, time_vec, gamma, omega_0, F, m, om_f):
	"""
	Funzione che crea array con le variabili da inserire nell'equazione differenziale
	
	Parametri
	------------
	F : Forza esterna
	r   : Vettore con variabili x, dx/dt, F
	t   : Variabile tempo
	g   : costnate gamma
	o   : costante omega
	
	Return
	------------
	
	drdt : Array con variabili che vengono calcolate successivamente
	"""	
	dxdt = r[1]
	dydt = -2 * gamma * r[1] - omega_0**2 * r[0] + F(om_f, time_vec)/m
	drdt = [dxdt, dydt]

	return drdt


def parser_arguments():
	"""
	Funzione che definisce gli argomenti dello script
	"""
	
	parser = argparse.ArgumentParser(description='Soluzione del moto di un oscillatore forzato')
	
	parser.add_argument('--F2', action='store_true', help='Risolve la equazione per un forza esterna in esempio')
	parser.add_argument('--F3', action='store_true', help='Risolve la equazione per un forza esterna in esempio')

	return  parser.parse_args()


def main():

	# Parametri
	m = 0.2 	# [Kg]
	k = 2		# [N/m]
	C = 0.5		# [Ns/m]
	
	# Costanti equazione
	gamma   = C/(2*m)
	omega_0 = k/m 
	
	# Condizioni iniziali
	x_0 = 0		# [m]
	v_0 = 0		# [m/s]
	yinit = (x_0, v_0)
	
	# Vettori del tempo
	dt = 0.01
	time_vec = np.arange(0, 60, dt)
		
	# Ampiezza della forza esterna
	om_f = 1
	
	# Scelta della forza esterna tramite parser
	args = parser_arguments()
	
	if args.F2 == False and args.F3 == False:
	
		F = F1
	
	if args.F2 == True:
		
		F = F2
	
	if args.F3 == True:
	
		F = F3
		
	# Soluzione equazione differenziale
	osc_for = integrate.odeint(drdt_ar, yinit, time_vec, args=(gamma, omega_0, F, m, om_f))
	
	# Grafico della soluzione
	fig,ax = plt.subplots(3,1, figsize=(12,10), sharex=True)
	ax[0].plot(time_vec, F(omega_0, time_vec),  color='darkred')
	ax[1].plot(time_vec, osc_for[:,0],         color='cornflowerblue')
	ax[2].plot(time_vec, osc_for[:,1],         color='orange')
	ax[2].set_xlabel('time [s]')
	ax[0].set_ylabel('F    [N]')
	ax[1].set_ylabel('x    [m]')
	ax[2].set_ylabel('v    [m/s]')
	plt.show()
	
	A = []
	fmax = []

	# array per  valori parametro forza
	of = np.logspace(-1, 2, 100)

	# Ciclo soluzione in funzione del parametro della forza
	for oo in of: 
		osc_for = integrate.odeint(drdt_ar, yinit, time_vec, args=(gamma, omega_0, F, m, oo))
		A += [np.max(np.abs(osc_for[:,0]))]

		

	# Grafico Ampiezza vs parametro forza
	fig,ax = plt.subplots(figsize=(12,10))
	plt.plot(of, A, lw=2, color='royalblue')
	plt.xlabel(r'$par_F$',       fontsize=16)
	plt.ylabel(r'$A_{max}$ [m]', fontsize=16)
	plt.xscale('log')
	plt.ylim(0, max(A)*1.1)
	plt.show()

if __name__ == "__main__":

	main()
