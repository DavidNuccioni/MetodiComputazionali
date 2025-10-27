"""
1- legga il file kplr010666592-2011240104155_slc.csv e crei il DataFrame pandas corrispondente;
2- Stampi il nome delle colonne del DataFrame;
3- Produca un grafico del flusso in funzione del tempo
suggerimento: usare pyplot.plot;
4- Produca un grafico del flusso in funzione del tempo coi punti del grafico demarcati da un simbolo (no linea);
suggerimento: usare pyplot.plot con opzione 'o' o equivalente;
5- Produca un grafico del flusso in funzione del tempo con barre di errore e salvi il risultato in un file png e/o pdf;
suggerimento: usare pyplot.errorbar;
6- Produca un grafico simile al precedente selezionando un intervallo temporale attorno ad uno dei minimi;
suggerimento: usare .loc per la serezione dei valori nel DataFrame;
7- Produca un grafico come per il punto 5 ma con la selezione del punto 6 mostrata come riquadro.
suggerimento: utilizzare inset_axes
(OPZIONALE)
8- Riprendendo i dati dell' Esercizio 1, determinare il periodo orbitale 
T e mostrare tutti i transiti in un unico grafico con tempo compreso fra -T/2 e T/2.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Punto 1
df = pd.read_csv('dati_es1.csv')

# Punto 2
"""
print(df.columns)
"""

# Punto 3
"""
plt.plot(df['TIME'], df['PDCSAP_FLUX'], color='blue')
plt.xlabel('Time (BjD-2454833)')
plt.ylabel('Flux (e¯/s)')
plt.title('Grafico Punto 3')
plt.show()
"""

# Punto 4
"""
plt.plot(df['TIME'], df['PDCSAP_FLUX'], 'o', markersize=3, color='blue')
plt.xlabel('Time (BjD-2454833)')
plt.ylabel('Flux (e¯/s)')
plt.title('Grafico Punto 4')
plt.show()
"""

# Punto 5 
"""
plt.errorbar(df['TIME'], df['PDCSAP_FLUX'], yerr=df['PDCSAP_FLUX_ERR'], markersize=3, fmt='o')
plt.xlabel('Time (BjD-2454833)')
plt.ylabel('Flux (e¯/s)')
plt.title('Grafico Punto 5')
plt.show()
plt.savefig('Graf_Es1_Punto5.pdf')
"""

# Punto 6
"""
df_min = df.loc[(df['TIME'] < 944.2) & (df['TIME'] > 943.1)]
plt.errorbar(df_min['TIME'] , df_min['PDCSAP_FLUX'], yerr=df_min['PDCSAP_FLUX_ERR'], markersize=3, fmt='o')
plt.xlabel('Time (BjD-2454833)')
plt.ylabel('Flux (e¯/s)')
plt.title('Grafico Punto 5')
plt.show()
plt.savefig('Graf_Es1_Punto6.pdf')
"""

# Punto 7
"""
df_min = df.loc[(df['TIME'] < 944.2) & (df['TIME'] > 943.1)]
fig, ax = plt.subplots(figsize=(12,10))
ax.errorbar(df['TIME'], df['PDCSAP_FLUX'], yerr=df['PDCSAP_FLUX_ERR'], markersize=3, fmt='o')
ax.set_xlabel('Time (BjD-2454833)')
ax.set_ylabel('Flux (e¯/s)')
ax.set_title('Grafico Punto 7')
ins_ax = ax.inset_axes([0.68, 0.84, 0.2,0.13]) 
ins_ax.errorbar(df_min['TIME'] , df_min['PDCSAP_FLUX'], yerr=df_min['PDCSAP_FLUX_ERR'], markersize=3, fmt='o')
plt.show()
plt.savefig('Graf_Es1_Punto7.pdf')
"""

# Punto 8 

# Il prof in questa parte fa uno scan su 5 range di periodo intorno a quello osservato visivamente per trovare quello migliore: in questo caso il terzo con T=2.2040

t_0 = 941.52
t_1 = 943.73
"""
T = t_1 - t_0
print('Il periodo osservato è:', T) 
tt = np.linspace(2.2020, 2.2080, 5)

fig, ax = plt.subplots(5,1, figsize=(12,12))
for t, ai in zip(tt, ax):

    folded_time = (((df['TIME'].values - t_0-t/2)*1e6).astype(int)%int(t*1e6) )/1e6 -t/2

    ## grafico Flusso vs. Tempo con folding
    ai.errorbar(folded_time, df['PDCSAP_FLUX'], yerr=df['PDCSAP_FLUX_ERR'], fmt='.', color='cornflowerblue' )
    ai.set_xlabel('Folded Time [d]', fontsize=14)
    ai.set_ylabel(r'Flux ($e^-/s$)',      fontsize=14)
    ai.set_xlim(-0.5,0.5)

plt.show()
"""
# Qui il periodo identificato viene usato per creare dunque il folding su un solo grafico
T = 2.2040
folded_time = ( (((df['TIME'].values - t_0-T/2)*1e6).astype(int)%int(T*1e6) )/1e6 )/T -0.5
df['FOLDED_TIME'] = folded_time
fig, ax = plt.subplots(figsize=(12,6))
plt.errorbar(df['FOLDED_TIME'], df['PDCSAP_FLUX'], yerr=df['PDCSAP_FLUX_ERR'], fmt='.', color='cornflowerblue' )
plt.xlabel('Folded Time [1/T]', fontsize=14)
plt.ylabel(r'Flux ($e^-/s$)',      fontsize=14)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.savefig('Kepler_fold.pdf')
plt.savefig('Kepler_fold.png')
plt.show()
