import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
import sys, os 

class Hit:
	"""
	Classe che descrive il rilevatore suddiviso in 4 moduli ognuno con 5 sensori, 
	permette di definire gli hit del rilevati
	
	Attributi:
	mid : Id modulo
	sid : Id sensore
	time : Time Stamp rivelazione
	
	Metodi: 
	__init__ : Costruttore con gli attributi specificati sopra
	__lt__ : Comparatore less than
	__gt__ : Comparatore greater than
	__sub__ : Differenza tra due oggetti
	"""
	
	def __init__(self, mid, sid, time):
	
		self.mid = mid
		self.sid = sid 
		self.time = time
	
	def __eq__(self, other) :
	
        	return self.time == other.time

	def __lt__(self, other) :
	
		if self.time == other.time:
		
			return 10*self.mid+self.sid < 10*other.mid+other.sid
		else:
			return self.time < other.time

	def __gt__(self, other) :
		return self.time > other.time

	def __sub__(self, other) :
		return self.time - other.time
	
		
class Event:
	"""
	Classe che descrive un evento che è stato rilevato 
	
	Attributi:
	n_hit : Numero di hit
	t_0 : Time Stamp del primo Hit
	t_1 : Time Stamp dell'ultimo Hit
	dt : Durata temporale
	ar_hit : Array di tutti gli Hit
	
	Metodi:
	__init__ : Costruttore con gli attributi specificati sopra
	summary : Presenta gli eventi registrati
	"""
	
	def __init__(self, ar_hit):
	
		self.ar_hit = ar_hit
		self.n_hit = ar_hit.size
		self.t_0 = ar_hit[0].time
		self.t_1 = ar_hit[-1].time
		self.dt = self.t_1 - self.t_0
	
	def summary(self):
	
		print(f"Evento con {self.n_hit} hit, durata {self.dt:.2f} ns")
		
		
			
		
		 
		
		
		
		
		
		
		
