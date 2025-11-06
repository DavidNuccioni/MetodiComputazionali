""" 
Creare il file python somme.py in cui vanno definite due funzioni:
1- Una funzione che restituisca la somma dei primi n numeri naturali, con n da passare tramite un argomento;
2- Una funzione che restituisca la somma delle radici dei primi n numeri naturali, con n da passare tramite un argomento.
3- Una funzione che restituisca la somma e il prodotto dei primi n numeri naturali, con n da passare tramite un argomento;
4- Una funzione che restituisca la serie di potenze con n da passare tramite un argomento e alpha da passare come argomento opzionale con valore di default pari a 1.
5- Creare uno script python che importi il modulo somme appena creato e ne utilizzi le funzioni
"""

import numpy as np
import sys,os

# Punto 1 

def somma(n):
	"""
	Calcola la somma di n numeri interi
	
	Parameters
	----------
	
	n : Rappresenta l'intero massimo su cui viene calcolata la somma
	
	Return
	----------
	
	sum : Somma dei primi n numeri interi
	"""
	
	nn = np.arange(1, n+1)
	sum_n = np.sum(nn)
	return sum_n
	
def somma_sqrt(n):
	"""
	Calcola la somma delle radice di n numeri interi
	
	Parameters
	----------
	
	n : Rappresenta l'intero massimo su cui viene calcolata la somma
	
	Return
	----------
	
	sum_sq : Somma delle radici dei primi n numeri interi
	"""
	
	nn = np.arange(1, n+1)
	nn_sq = np.sqrt(nn)
	sum_sq = nn_sq.sum()
	return sum_sq
	
def som_pro(n):
	"""
	Calcola la somma e il prodotto di n numeri interi
	
	Parameters
	----------
	
	n : Rappresenta l'intero massimo su cui viene calcolata la somma e il prodotto
	
	Return
	----------
	
	sum : Somma dei primi n numeri interi
	pro : Prodotto dei primi n numeri interi
	"""
	
	nn = np.arange(1, n+1)
	sum_nn = np.sum(nn)
	pro_nn = np.prod(nn)
	return sum_nn, pro_nn
	
def som_pow(n, alpha = 1):
	"""
	Calcola la serie di potenze di n numeri interi con indice alpha
	
	Parameters
	----------
	
	n : Rappresenta l'intero massimo su cui viene calcolata la somma e il prodotto
	
	Return
	----------
	
	ser_pow : Rappresenta il risultato della serie di potenza
	"""
	
	nn = np.arange(1, n+1)
	n_pow = np.power(nn, alpha)
	ser_pow = n_pow.sum()
	return ser_pow
	

	
	

	
	
