import numpy as np
import matplotlib.pyplot as plt 
"""
1- Produrre uno script python che: nell'intervallo x=[0;10] permetta di generare un distribuzione di probabilità secondo la legge: f(x)= 3x²/1000 utilizzando sia il metodo Hit or Miss che il metodo della cumulativa.
2- Rappresentare un esempio delle distibuzioni ottenute in un grafico.
"""

def func(x):
    """
    funzione 3x²/1000
    """ 
    f = 3 * x**2 / 1000
    
    return f 
    
def X_cum(N):
	"""
    funzione per generare una distribuzione random di valori x, metodo della cumulativa
    """
	
	cum = np.random.random(N)
    
	x_cum = (1000 * cum)**(1/3)

	return x_cum
    

def X_hm(x_f, N):
    """
    funzione per generare una distribuzione random di valori x, metodo hit or miss
    """
    
    y_hm = np.random.random(N)
    mask = y_hm <= func(x_f)
    
    x_h = x_f[mask]
    
    return x_h
    
    
def prob_dist():

	# Valori x per grafico della funzione teorica
	x_graf = np.linspace(x_min, x_max, N)
	
	# Valori x per grafico metodo Hit or Miss
	x_hm = X_hm(x_graf, N)
	
	# Valori x per grafico metodo Cumulativa
	x_cum = X_cum(N)
	
	# Grafico con i due metodi a confronto con la curva teorica
	nbins = 50	
	plt.figure()
	plt.hist(x_hm, nbins, density=True, alpha=0.6, label="Hit-or-Miss")
	plt.hist(x_cum, nbins, density=True, alpha=0.6, label="Cumulativa")
	plt.plot(x_graf, func(x_graf), label="f(x) teorica")
	plt.xlabel("x")
	plt.ylabel("Densità di probabilità")
	plt.legend()
	plt.show()


if __name__=='__main__':

	# Valori inziali 
	N = 10000
	x_min = 0.0
	x_max = 10.0
	
	prob_dist()
    
