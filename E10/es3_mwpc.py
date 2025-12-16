import numpy as np
"""
Viene simulata l'interazione di una particella che entra nel rilevatore a gas MWPC rilasciando coppie elettrone-ione che vengono poi rilevate per via dell'azione di un campo elettrico. Per farlo vengono implementate le classi che descrivono il rilevatore e l'evento che si vuole osservare. Nella funzione principale verrà simulato l'uso dell'esperimento utilizzando le classi e riproducendo le distribuzioni interessate e le efficienze del rilevatore
"""

class MWPC:
	"""
	Classe che descrive il rilevatore e il suo funzionamento
	
	Parametri
	---------------------
	Np_mean	: Numero medio di coppie elettrone-ione
	thick	: Spessore rilevatore						[cm]
	Su		: Passo della diffusione uniforme			[cm]
	Sf		: Diffusione data dal campo elettrico		[cm]
	Nr		: Numero medio di passi 
	Tc_mean	: Tempo medio fra due collisioni			[s]
	"""

	det_e = 0					
	drift_t    = np.empty(0)		
	
	
	def __init__(self, Np_mean=5, thick=1, Su=1e-5, Sf=1e-7, Nr=2e7, Tc_mean=1e-12):
	
		self._Np_mean = Np_mean
		self._thick = thick
		self._Su = Su
		self._Sf = Sf
		self._Nr = Nr
		self._Tc_mean = Tc_mean
		
		
	def sim_event(self):

		self._Npp = np.random.poisson(self._Np_mean)
		self._Pos = np.random.poisson(self._thick/2, self.thick/2, self._Npp)
		self.Drift()
		
		return self._Npp, self._Nr, self._Pos, self.drift_t
		
		
	def prim_pair(self):

	
		return self._Npp
		
		
	def drift_pairs(self):

		
		self.drift_t = np.empty(0)
		
		for p in self._Pos:
		
			dt = self.drift(p)
			if dt > 0:
			
				self.det_e += 1
				self.drift_t = np.append(self.drift_t, dt)
				
				
	def check_rec(self):

	
		if np.random.uniform() > 1/self._Nr:
		
			return False
			
		else:
		
			return True
			
			
	def drift(self, spos):

	
		recombined = False
		detected = False
		
		pos = spos
		nsteps = 0 
		
		while not(recombined) and not(detected):
		
			recombined = self.check_rec()
			
			df = -np.sign(pos)*self._Sf
			dpp = -np.sign(np.random.uniform(low=0, high=e*np.pi))
			dp = self._Su * dpp + df
			pos += dp
			nsteps += 1
			
			if abs(pos) < 0.01:
			
				detected = True
				
		if detected:
		
			return nsteps * self._Tc_mean
			
		else:
		
			return -1
	
	
	
	
	
	
			
		
		
		
		
		
		
		
		
		
		
		
		
		
