"""
1- Legga il file ExoplanetsPars_2025.csv e crei il DataFrame pandas corrispondente;
suggerimento: usare l'opzione comment='#'
2- Stampi il nome delle colonne del DataFrame;
3- Stampi un estratto del contenuto del DataFrame;
4- Produca un grafico con assi logaritmici della massa del pianeta in funzione del periodo orbitale;
suggerimento: usare pyplot.scatter;
5- Produca un grafico con assi logaritmici della grandezza R²max/m* in funzione del periodo orbitale;
 Rmax=Orbit Semi-Major Axis
 m*=Stellar Mass
6- Produca un grafico con assi logaritmici della massa del pianeta in funzione del periodo orbitale distinguendo gli esopianeti per metodo di scoperta (Transit o Radial Velocity) con la corrispondente legenda (gli altri tipi di esopianeti non vanno considerate nel grafico);
suggerimento: usare .loc per la serezione dei valori nel DataFrame;
suggerimento: usare l'opzione alpha per la trasparenza;
7- Produca l'istogramma sovrapposto della massa del pianeta distinguendo gli esopianeti per metodo di scoperta (Transit o Radial Velocity) con la corrispondente legenda con la relativa legenda;
suggerimento: usare pyplot.hist definendo lo stesso numero di bin e lo stesso intervallo per l'asse x;
suggerimento: scegliere intervallo e numero di bin da utilizzare per avere tutto uguale
suggerimento: usare l'opzione alpha per la trasparenza;
8- Produca un grafico analogo al precedente per il logaritmo in base 10 della massa del pianeta.
(OPZIONALE)
9- Combinare: il grafico del punto 2.6 mostrando direttamente il logaritmo in base 10 dei valori invece di usare la scala logaritmica per gli assi, l'istogramma dei punti 2.8 e un istogramma simile a quello del punto 2.8 ma per il periodo orbitale. Combinare in un'unica immagine e salvare il risultato in un file png e in un file pdf.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Punto 1
df = pd.read_csv('dati_es2.csv', comment = '#')

# Punto 2 
"""
print(df.columns)
"""
# Punto 3
"""
print(df.head)
"""
# Punto 4 
"""
plt.scatter( df['pl_orbper'], df['st_mass'], color='royalblue', s=20)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Period (Days)')
plt.ylabel('Planet Mass (solar masses)')
plt.title('Grafico Punto 4')
plt.show()
"""

# Punto 5 
"""
as_x = pow(df['pl_orbsmax'],2)/df['st_mass']
plt.scatter( as_x, df['pl_orbper'], color='orange', s=20)
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Period (Days)')
plt.ylabel('R²/m (m²/days)')
plt.title('Grafico Punto 5')
plt.show()
"""

# Punto 6
"""
fig, ax = plt.subplots(figsize=(12,6))
plt.scatter(df.loc[df['discoverymethod']=='Transit', 'pl_orbper'],
df.loc[df['discoverymethod']=='Transit', 'pl_bmassj'], alpha=0.3, label='Transit')
plt.scatter(df.loc[df['discoverymethod']=='Radial Velocity', 'pl_orbper'],
df.loc[df['discoverymethod']=='Radial Velocity', 'pl_bmassj'], alpha=0.3, label='Radial Velocity')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('Period (Days)', fontsize=16)
plt.ylabel('Planet Mass m', fontsize=16)
plt.legend(fontsize=14)
plt.title('Grafico Punto 6')
plt.savefig('Graf1_Es2_Punto6.pdf')
plt.savefig('Graf2_Es2_Punto6.png')
plt.show()
"""

# Punto 7-8 (La differenza è che c'è np.log10 che non viene messo nel punto 7 e viene brutto)
"""
fig, ax = plt.subplots(figsize=(12,6))
plt.hist(np.log10(df.loc[df['discoverymethod']=='Transit', 'pl_bmassj']),
bins=50, range=(-4, 4), color='limegreen',  alpha=0.5, orientation='vertical', label='Transit')
plt.hist(np.log10(df.loc[df['discoverymethod']=='Radial Velocity', 'pl_bmassj']),
bins=50, range=(-4, 4), color='darkorange',  alpha=0.5, orientation='vertical', label='Radial Velocity')

plt.xlabel('Mass of Planets', fontsize=14)
plt.ylabel('Number of Planets', fontsize=14)
plt.legend(fontsize=16)
plt.title('Grafico Punto 7')
plt.show()
"""

# Punto 9 (Copiato dalle soluzioni)
fig = plt.figure(figsize=(12,11))

# creo griglia 2x2 per subplot con asse X in comune per le colonne e asse Y inb comune per le righe 
gs = fig.add_gridspec(2, 2, hspace=0, wspace=0)
ax = gs.subplots( sharex='col', sharey='row')

ax[1,0].scatter( np.log10(df.loc[df['discoverymethod']=='Transit',         'pl_orbper']),
                 np.log10(df.loc[df['discoverymethod']=='Transit',         'pl_bmassj']), color='limegreen',  alpha=0.3, label='Transit')
ax[1,0].scatter( np.log10(df.loc[df['discoverymethod']=='Radial Velocity', 'pl_orbper']),
                 np.log10(df.loc[df['discoverymethod']=='Radial Velocity', 'pl_bmassj']), color='darkorange', alpha=0.3, label='Radial Velocity')

ax[1,0].tick_params(axis='both', which='major', labelsize=14)
ax[1,0].set_xlabel('log(Period [days])',         fontsize=16)
ax[1,0].set_ylabel(r'log(Planet Mass [$m_J$])',  fontsize=16)
ax[1,0].legend(fontsize=16)


# Istogramma Periodo
ax[0,0].hist( np.log10(df.loc[df['discoverymethod']=='Transit', 'pl_orbper']),
              bins=50, range=(-2, 5), color='limegreen',  alpha=0.5, label='Transit')

ax[0,0].hist( np.log10(df.loc[df['discoverymethod']=='Radial Velocity', 'pl_orbper']),
              bins=50, range=(-2, 5), color='darkorange',  alpha=0.5, label='Radial Velocity')
ax[0,0].tick_params(axis='both', which='major', labelsize=14)
ax[0,0].set_ylabel(r'Number of planets',        fontsize=16)
ax[0,0].legend(fontsize=16)


# Istogramma Massa pianeta
ax[1,1].hist( np.log10(df.loc[df['discoverymethod']=='Transit', 'pl_bmassj']),
              bins=50, range=(-4, 4), color='limegreen',  alpha=0.5, orientation='horizontal', label='Transit')

ax[1,1].hist( np.log10(df.loc[df['discoverymethod']=='Radial Velocity', 'pl_bmassj']),
              bins=50, range=(-4, 4), color='darkorange',  alpha=0.5, orientation='horizontal', label='Radial Velocity')

ax[1,1].tick_params(axis='both', which='major', labelsize=14)
ax[1,1].set_xlabel( 'Number of planets',        fontsize=16)
ax[1,1].legend(fontsize=16)

# Rimuovo assi per riquadro non necessario
ax[0,1].axis('off')

plt.savefig('Graf1_Es2_Punto9.pdf')
plt.savefig('Graf2_Es2_Punto9.png')
plt.show()




