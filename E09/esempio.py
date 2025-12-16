import numpy as np
import pandas as pd
from scipy import constants, fft
import matplotlib.pyplot as plt
"""
Monthly averages of the daily sunspot number with error estimates as posted at the WDC-SILSO, Royal Observatory of Belgium, Brussels downloaded from https://www.sidc.be/SILSO/datafiles
"""

# Lettura dei dati
dfsun = pd.read_csv('DATI_E09/SN_m_tot_V2.0.csv', sep=';')


# Grafico dati macchie solari
plt.subplots(figsize=(11,7))
plt.plot(dfsun['year_fraction'], dfsun['sunspots'], color='gold')
plt.xlabel('Data')
plt.ylabel('Numero Macchie Solari')
plt.show()


# Zoom su uno dei massimi
plt.subplots(figsize=(11,7))
plt.plot(dfsun['year_fraction'], dfsun['sunspots'], color='gold')
plt.xlabel('Data')
plt.ylabel('Numero Macchie Solari')
plt.xlim(2009,2026)
plt.show()


# real FFT 
csun = fft.rfft(dfsun['sunspots'].values)   


# Grafico spettro di potenza 
plt.plot(np.absolute(csun[:csun.size//2])**2, 'o', markersize=4)
plt.xlabel('Indice')
plt.ylabel(r'$|c_k|^2$')
plt.xscale('log')
plt.yscale('log')
plt.show()


# Esprimo la differenza temporale fra le misure in frazione di anni (1 mese=1/12 anno)
sundt = 1/12

# Recupero frequenze
snyquist = 0.5

# Frequenze per rfft (real fft) 
sunf = snyquist*fft.rfftfreq(csun.size, d=sundt) 


# Grafico spetto di potenza in funzione delle frequenze
plt.plot(sunf[:int(csun.size/2)], np.absolute(csun[:int(csun.size/2)])**2, 'o', markersize=4)
plt.xlabel('Frequenza [1/yr]')
plt.ylabel(r'$|c_k|^2$')
plt.xscale('log')
plt.yscale('log')
plt.show()


# Grafico spettro di potenza in funzione del periodo (1/freq)
plt.plot(1/sunf[1:int(csun.size/2)], np.absolute(csun[1:int(csun.size/2)])**2, 'o', markersize=4)
plt.xlabel('Periodo [yr]')
plt.ylabel(r'$|c_k|^2$')
plt.xscale('log')
plt.yscale('log')
plt.show()


# Zoom spettro di potenza in funzione del periodo
plt.plot(1/sunf[1:csun.size//2], np.absolute(csun[1:csun.size//2])**2, 'o-', markersize=4)
plt.xlabel('Periodo [yr]')
plt.ylabel(r'$|c_k|^2$')
#plt.xscale('log')
#plt.yscale('log')
plt.xlim(5, 15)
plt.show()


# Applico maschera per filtrare frequenze meno imporatanti sulla base del PS
fftmask1 = np.absolute(csun)**2< 2e7
fftmask2 = np.absolute(csun)**2< 1e7

# Deep copy di csun1
filtered_csun1 = csun.copy()
filtered_csun1[fftmask1] = 0

# Deep copy di csun2
filtered_csun2 = csun.copy()
filtered_csun2[fftmask2] = 0


# Trasformata FFT inversa con coefficienti filtrati 
filtered_sun1 = fft.irfft(filtered_csun1, n=len(dfsun['sunspots']))
filtered_sun2 = fft.irfft(filtered_csun2, n=len(dfsun['sunspots']))
#filtered_sun1 = fft.ifft(filtered_csun1.astype(float))  
#filtered_sun2 = fft.ifft(filtered_csun2.astype(float))

print(len(dfsun['sunspots']), csun.size, filtered_sun1.size)


# Grafico dati originali e filtrati
plt.subplots(figsize=(11,7))
plt.plot(dfsun['year_fraction'], dfsun['sunspots'], color='gold',      label='Dati Originali')
plt.plot(dfsun['year_fraction'], filtered_sun2,     color='limegreen', label='Filtro $P>1\cdot 10^7$')
plt.plot(dfsun['year_fraction'], filtered_sun1,     color='magenta',   label='Filtro $P>2\cdot 10^7$')
plt.legend(fontsize=13)
plt.xlabel('Data')
plt.ylabel('Macchie Solari')
plt.show()


# Zooom grafico dati originali e filtrati
plt.subplots(figsize=(11,7))
plt.plot(dfsun['year_fraction'], dfsun['sunspots'], color='gold',      label='Dati Originali')
plt.plot(dfsun['year_fraction'], filtered_sun2,     color='limegreen', label='Filtro $P>1\cdot 10^7$')
plt.plot(dfsun['year_fraction'], filtered_sun1,     color='magenta',   label='Filtro $P>2\cdot 10^7$')
plt.legend(fontsize=14)
plt.xlabel('Data')
plt.ylabel('Macchie Solari')
plt.xlim(1995, 2020)
plt.show()
