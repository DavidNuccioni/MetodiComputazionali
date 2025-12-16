import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import time
import es3_mwpc, es3_ev
"""
Viene simulata l'interazione di una particella che entra nel rilevatore a gas MWPC rilasciando coppie elettrone-ione che vengono poi rilevate per via dell'azione di un campo elettrico. Per farlo vengono implementate le classi che descrivono il rilevatore e l'evento che si vuole osservare. Nella funzione principale verrà simulato l'uso dell'esperimento utilizzando le classi e riproducendo le distribuzioni interessate e le efficienze del rilevatore
"""

def run():

	for i in tqdm(range(1000)):
	
		npc, nr, pos, dt = camera.sim_event
		
		camera_ev = np.append(camera_ev, es3_mwpc.MWPC(npc, len(drift_t), pos, drift_dt))
		
	positions = np.empty(0)
	primaries = np.empty(0)
	detections = np.empty(0)
	dt_first = np.empty(0)
	dt_mean = np.empty(0)
	
	for ce in camera_ev:
	
		positions = np.append(positions, ce._pos)
		primaries = np.append(primaries, ce._Np_mean)
		detections = np.append(detections, ce._Nr) 
		dt_first = np.append(dt_first, ce._dt_first)
		dt_mean = np.append(dt_mean, ce._dt_mean)
	
	mask = primaries == 0 
	eff = detections / primaries
	
	plt.hist(positions, bins=20, range=(-0.5, 0.5))
	plt.xlabel('Primary Position [cm]')
	plt.ylabel('entries / bin ')
	plt.show()

	plt.hist(primaries, bins=15, range=(0,15))
	plt.xlabel('Priamrie pairs')
	plt.ylabel('entries / bin ')
	plt.show()

	plt.hist(detections, bins=15, range=(0,15))
	plt.xlabel('Detected electrons')
	plt.ylabel('entries / bin ')
	plt.show()

	plt.hist(primaries,  bins=15, range=(0,15),            label='Primary')
	plt.hist(detections, bins=15, range=(0,15), alpha=0.6, label='Detected')
	plt.xlabel('Charges')
	plt.ylabel('entries / bin ')
	plt.legend()
	plt.show()

	plt.hist(np.log10(dt_mean),  range=(-12, -6), bins=48, alpha=1, label='mean')
	plt.hist(np.log10(dt_first), range=(-12, -6), bins=48, alpha=0.6, label='first')
	plt.xlabel(r'log($t$)')
	plt.ylabel('entries / bin ')
	plt.legend()
	plt.show()

	plt.hist(eff*100, bins=50)
	plt.xlabel(r'$\varepsilon$ (%)')
	plt.ylabel('entries / bin ')
	plt.legend()
	plt.show()
	
	detected_tracks = np.count_nonzero(eff)
	tracks_eff = detected_tracks/len(camera_ev)
	tracks_effe = np.sqrt(tracks_eff * (1-tracks_eff) / len(camera_ev))
	
	print('Eff = {:.2f} +- {:.2f}'.format(tracks_eff*100, tracks_effe*100))
	
	
if __name__=='__main__':

	camera = es3_mwpc.MWPC(Su=1e-4, Sf=5e-5, Nr=1e4)
	camera_ev = es3_ev.MWPCev = np.empty(0)

	run()
