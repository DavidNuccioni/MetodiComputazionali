# L'esercizio richiede creare una lista con i giorni della settimana per tutto il mese di 
# ottobre 2025. Creare poi un dizionario che li metta in relazione con il giorno

list_g1 = ['lun', 'mar', 'mer', 'gio', 'ven', 'sab', 'dom']
list_g = list_g1*5
list_o = []

for i in range(31):
	list_o.append(list_g[i+2])
	
print('Il mese di ottobre è composto dai seguenti giorni:\n', list_o)

# Creo un dizionario che mette in relazione il giorno della settimana con il numero del mese
# L'utente potrà chiedere il giorno della settimana al numero richiesto del mese

ott_dict = {i+1: list_o[i] for i in range(len(list_o))}

print(ott_dict)

gg_str = input('Scegli il numero del giorno che vuoi conoscere ')
gg = int(gg_str)
print('Il giorno', gg, 'è un:', ott_dict[gg])







