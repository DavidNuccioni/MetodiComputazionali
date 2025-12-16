import numpy as np
"""
Viene simulata l'interazione di una particella che entra nel rilevatore a gas MWPC rilasciando coppie elettrone-ione che vengono poi rilevate per via dell'azione di un campo elettrico. Per farlo vengono implementate le classi che descrivono il rilevatore e l'evento che si vuole osservare. Nella funzione principale verrà simulato l'uso dell'esperimento utilizzando le classi e riproducendo le distribuzioni interessate e le efficienze del rilevatore
"""

class MWPCev:
	"""
	Classe che descrive gli eventi di MWPC
	
	Parametri
	---------------------
	np		: Numero di coppie primarie
	Nd		: Numero di coppie rilevate
	pos		: Posizione delle coppie primarie
	dt		: Tempi di deriva
	"""

	def __init__(self, npp, Nd, pos, dt):
	
		self._np = Npp
		self._Nd = Nd
		self._pos = pos
		self._dt = dt
		
		if self._Nd > 0:
		
			self._dt_first = np.sort(self._dt)[0]
			self._dt_mean = np.mean(self._dt)
		
		else:
		
			self._dt_first = 0 
			self._dt_mean = 0 
			
			
	def get_dt_first(self):
	
		return self._dt_first
		
		
	def get_dt_mean(self): 
	
		return self._dt_mean
