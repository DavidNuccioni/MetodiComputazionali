# Creare un programma che calcoli l'età in base a una data immessa dall'utente

from datetime import datetime, timedelta
datenow = datetime.now()

mydate_str = input('Inserisci la tua data di nascita: ')
mydate = datetime.strptime(mydate_str, "%d-%m-%Y %H:%M:%S")

timediff = datenow - mydate

giorni = timediff.days
anni = giorni // 365
mesi = (giorni % 365) // 30
giorni_restanti = (giorni % 365) % 30
ore = timediff.seconds // 3600
minuti = (timediff.seconds % 3600) // 60
secondi = timediff.seconds % 60

Anni = 'Anni'
Mesi = 'Mesi'
Giorni = 'Giorni'
Ore = 'Ore'
Minuti = 'Minuti'
Secondi = 'Secondi' 

fine = 'Hai trascorso:\n{:<10s}{:02d}\n{:<10s}{:02d}\n{:<10s}{:02d}\n{:<10s}{:02d}\n{:<10s}{:02d}\n{:<10s}{:02d}'.format(Anni, anni, Mesi, mesi,Giorni, giorni_restanti, Ore, ore, Minuti, minuti, Secondi, secondi)
print(fine)

tots = timediff.total_seconds()
tts = int(tots)
print('Sei sopravvisuto per un totale di: ', tts, 'secondi, complimenti!')
