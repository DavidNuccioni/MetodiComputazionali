#L'esercizio richiede di calcolare la somma di un valore in input dato dall'utente

"""
Per controllare che le variabili inserite siano effettivamente interi si potrebbe
utilizzare il .isdigit che controlla se una stringa contiene solo numeri naturali
Per esempio si potrebbe riscrivere il codice dopo la prima riga come:
"""
stop = False
while not stop:
	nn = input('Immettere un numero naturale: ')
	if nn.isdigit() and int(nn) > 0:
		nnf = int(nn)
		somma = 0
		for i in range(nnf+1):
			somma = somma + i
		strg = 'La somma dei numeri fino a {:d} è {:d}'.format(nnf,somma)
		print(strg)
		stop = True		
	else:
		print('Errore, devi inserire un numero naturale maggiore di zero')
		while True: #ciclo infinito finchè non si esce con break			
			nd = input('Vuoi riprovare? (Scrivi si o no): ')
			if nd == 'no':
				stop = True
				break
			elif nd == 'si':
				print('Ricominciamo allora')
				break
			else:
				print('Devi inserire o si o no')
"""
In questo codice si controlla il tutto tramite variabile bool lo script che viene inizializzato se l'utente mette un numero corretto entra nel codice che somma ed esce dopo aver stampato la somma, altirmenti entra in un ciclo while infinito dove gli viene chiesto se vuole riprovare, se risponde no si interrompe il ciclo while e tramite accensione bool si esce anche dal while iniziale e termina tutto altrimenti se vuole riprovare si interrompe solo il ciclo while e si ritorna all'inizio, se la stringa non è ne si ne no gli viene chiesto di rimmettere la stringa corretta 
"""	
