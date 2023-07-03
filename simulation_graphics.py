import win32gui,win32api,win32con
import time
from random import randint
from doubleChainedList import DCList
from classes import coefT, Road,Driver,Car,Cell,Traffic
import os
import pygame
from pygame.locals import *
from display import displayCalculs, drawRoad, drawCell 
import matplotlib.pyplot as plt
from math import sqrt
from random import uniform




def main():
	#_________________________________CARACTERISTIQUES FENETRE PYGAME
	HEIGHT,WIDTH = 840,1530
	dim = (HEIGHT, WIDTH)
	BACKGROUND = (50,50,50) #couleur du fond
	WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) #Setting WINDOW
	pygame.display.set_caption(  'Traffic SIM') #Window Name
	WINDOW.fill(BACKGROUND)
	pygame.init()
	#_________________________________
	run = True
	road = Road('test_road.txt') #objet route
	traffic = Traffic(road)
	timestamp = time.time()
	CLOCK = pygame.time.Clock()
	drawRoad(road, WINDOW, dim)
	
	taillePort, nbPortions, gap, roadTness, tness = displayCalculs(road, dim)
	traffic.generateCells(170,110, 120,14)

	cell = None
	date_debut_simulation = time.time()
	T=[]
	VT = []
	DT = []
	MAX = []
	MIN = []
	L0, L10, L20, L30, L40, L50 = [], [], [], [], [], []
	
	v_ideal = 115
	
	while run and time.time() < date_debut_simulation+100:
		dt = time.time()-timestamp
		timestamp = time.time()
		dt = dt*coefT
		
		
		if road.date_debut_mesure_VM + road.duree_mesure_VM*dt < time.time() : #au 1er tour de boucle tq on a dépasser le temps dure*dt depuis la dernière mesure, on mesure
			road.mesure_vitesses = True
			road.list_vitesses = []
			road.date_debut_mesures_VM = time.time()
	#__UPDATE___________________
		road.update(dt)
	#__UPDATE___________________
	
		# ~ if win32api.GetKeyState(0x1B) < 0:	run = False #échap met fin a la boucle while sans fermer la fenêtre
		
		#_________________________________AFFICHAGE
		CLOCK.tick(60)
		drawRoad(road, WINDOW, dim)
		drawCell(road, WINDOW, dim)
		
		#_________________________________MESURES
		if road.mesure_vitesses == True and road.list_vitesses != []:
			date =time.time()-date_debut_simulation
			road.mesure_vitesses = False
			SOM = sum(road.list_vitesses)
			LEN = len(road.list_vitesses)
			mes = (SOM/LEN)*3.6
			
			# ~ SOMD = sum(road.list_distances)
			# ~ LEND = len(road.list_distances)
			# ~ mesd = (SOMD/LEND)
			nb_0 = 0
			nb_10 = 0
			nb_20 = 0
			nb_30 = 0
			nb_40 = 0
			nb_50 = 0
			for v in road.list_vitesses:
				if v/coefT < (v_ideal - 100)/3.6 :
					nb_50 += 1
				elif v/coefT < (v_ideal - 80)/3.6:
					nb_40 += 1
				elif v/coefT < (v_ideal - 60)/3.6 :
					nb_30 += 1
				elif v/coefT < (v_ideal - 40)/3.6 :
					nb_20 += 1
				elif v/coefT < (v_ideal - 20)/3.6 :
					nb_10 += 1
				else : 
					nb_0 += 1
			road.list_vitesses = []
					
				
			L0.append(nb_0)
			L10.append(nb_10)
			L20.append(nb_20)
			L30.append(nb_30)
			L40.append(nb_40)
			L50.append(nb_50)
			# ~ mi_ecart_type = (sqrt(sum([v**2 for v in road.list_vitesses])/ LEN)*3.6)/2
			# ~ mini =  mes - mi_ecart_type
			# ~ maxi = mes + mi_ecart_type
			# ~ print("Vitesse moyenne = "+str( mes ) +" à "+str(date)+" secondes du lancement" )
			# ~ MAX.append(maxi)
			# ~ MIN.append(mini)
			
			T.append(date*15)
			VT.append(mes/coefT)
		#_________________________________MESURES
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
			  run = False
			if event.type == pygame.MOUSEBUTTONDOWN: #dynamic cell spawner
				
				a,b = pygame.mouse.get_pos()
				indPort = (b-5)//(roadTness+gap)
				v = ((b-5)-indPort*(roadTness+gap))//tness
				if v >= len(road.voies) :
					v = v//4
				x = (a/WIDTH)*taillePort + indPort*taillePort
				cell = traffic.spawnCell(x, v, "_aggressif")
			
		pressed = pygame.key.get_pressed()
		if pressed[pygame.K_ESCAPE]:    
			run = False

		if pressed[pygame.K_RIGHT]:   
			cell.v += 1
			# ~ cell.driver.vitesse_voulue += 1
		if pressed[pygame.K_LEFT]:    
			cell.v -= 4
			# ~ cell.driver.vitesse_voulue -= 1
		if pressed[pygame.K_DOWN]:
			cell.change = 1
		if pressed[pygame.K_UP]:
			cell.change = 0
		# ~ if pressed[pygame.K_a]:
			# ~ cell.change = 2
		pygame.display.update()
		#_________________________________FIN AFFICHAGE
	print("execution terminee --> temps simulé = "+str((time.time()-date_debut_simulation)*coefT) + "\ntemps réel écoulé = "+str(time.time()-date_debut_simulation))
	print("nombre d'accidents : "+str(len(road.list_accidents)))
	fig, (g1, g2) = plt.subplots(1, 2)
	g1.plot(T, VT)
	g2.plot(T,L0  , label="-0" )
	g2.plot(T,L10 , label="[-20, 0]")
	g2.plot(T,L20 , label="[-40, -20]")
	g2.plot(T,L30 , label="[-60, -40]")
	g2.plot(T,L40 , label="[-80, -60]")
	g2.plot(T,L50 , label="[-100, -80]")
		#plt.fill_between(T, MIN, MAX, color='lightblue', alpha=0.5, label='Intervalle de dispertion')
	g1.set_xlabel("temps t")
	g1.set_ylabel("vitesse moyenne Vm(t)")
	g1.set_title("vitesse moyenne de l'ensemble du traffic\nau cours du temps")
	g2.set_xlabel("temps t")
	g2.set_ylabel("nombre de véhicules")
	g2.set_title("nombre de véhicules par tranche de\ndifférence à la vitesse idéale selon le temps")
	g2.legend()
	# Ajuster l'espacement entre les graphiques
	plt.tight_layout()
	# Afficher le graphique
	plt.show()
	return 
	
def main_no_diplay(duree, v_ideal = 115, v_init_inf = 75, v_init_sup = 85):
	run = True
	road = Road('test_road.txt') #objet route
	traffic = Traffic(road)
	timestamp = time.time()
	CLOCK = pygame.time.Clock()
	# ~ drawRoad(road, WINDOW, dim)
	
	# ~ taillePort, nbPortions, gap, roadTness, tness = displayCalculs(road, dim)
	nb_cell = 80
	distance_minimale = 10
	traffic.generateCells(170,110, 120,14)
	cell = None
	date_debut_simulation = time.time()
	T=[]
	VT = []
	DT = []
	L0, L10, L20, L30, L40, L50 = [], [], [], [], [], []
	
	print("coefficient temporel = "+str(coefT))
	
	while time.time() - date_debut_simulation < duree:
		dt = time.time()-timestamp
		timestamp = time.time()
		dt = dt*coefT
		
		
		if road.date_debut_mesure_VM + road.duree_mesure_VM*dt < time.time() : #au 1er tour de boucle tq on a dépasser le temps dure*dt depuis la dernière mesure, on mesure
			road.mesure_vitesses = True
			road.list_vitesses = []
			road.date_debut_mesures_VM = time.time()
		#__UPDATE___________________
		road.update(dt)
		#__UPDATE___________________
		
		CLOCK.tick(60)
		#_________________________________MESURES
		if road.mesure_vitesses == True and road.list_vitesses != []:
			date =time.time()-date_debut_simulation
			road.mesure_vitesses = False
			SOM = sum(road.list_vitesses)
			LEN = len(road.list_vitesses)
			mes = (SOM/LEN)*3.6
			
			# ~ SOMD = sum(road.list_distances)
			# ~ LEND = len(road.list_distances)
			# ~ mesd = (SOMD/LEND)
			nb_0 = 0
			nb_10 = 0
			nb_20 = 0
			nb_30 = 0
			nb_40 = 0
			nb_50 = 0
			for v in road.list_vitesses:
				if v/coefT < (v_ideal - 100)/3.6 :
					nb_50 += 1
				elif v/coefT < (v_ideal - 80)/3.6:
					nb_40 += 1
				elif v/coefT < (v_ideal - 60)/3.6 :
					nb_30 += 1
				elif v/coefT < (v_ideal - 40)/3.6 :
					nb_20 += 1
				elif v/coefT < (v_ideal - 20)/3.6 :
					nb_10 += 1
				else : 
					nb_0 += 1
			road.list_vitesses = []
					
				
			L0.append(nb_0)
			L10.append(nb_10)
			L20.append(nb_20)
			L30.append(nb_30)
			L40.append(nb_40)
			L50.append(nb_50)
			
			
			
			# ~ mi_ecart_type = (sqrt(sum([v**2 for v in road.list_vitesses])/ LEN)*3.6)/2
			# ~ mini =  mes - mi_ecart_type
			# ~ maxi = mes + mi_ecart_type
			# ~ print("Vitesse moyenne = "+str( mes ) +" à "+str(date)+" secondes du lancement" )
			# ~ MAX.append(maxi)
			# ~ MIN.append(mini)
			
			T.append(date*10)
			VT.append(mes/coefT)
		#_________________________________MESURES
			
		##############################################FIN BOUCLE
	print("execution terminee --> compte rendu :\n temps simulé = "+str((time.time()-date_debut_simulation)*coefT) + "\ntemps réel écoulé = " + str(time.time()-date_debut_simulation))
	print("nombre d'accidents : "+str(len(road.list_accidents)))
	print("nombre de véhicules injecté = "+str(nb_cell) + "\nà une vitesse initiale comprise entre "+str(v_init_inf)+" et "+str(v_init_sup)+" km/h")
	fig, (g1, g2) = plt.subplots(1, 2)
	g1.plot(T, VT)
	g2.plot(T,L0  , label="-0" )
	g2.plot(T,L10 , label="[-20, 0]")
	g2.plot(T,L20 , label="[-40, -20]")
	g2.plot(T,L30 , label="[-60, -40]")
	g2.plot(T,L40 , label="[-80, -60]")
	g2.plot(T,L50 , label="[-100, -80]")
		#plt.fill_between(T, MIN, MAX, color='lightblue', alpha=0.5, label='Intervalle de dispertion')
	g1.set_xlabel("temps t")
	g1.set_ylabel("vitesse moyenne Vm(t)")
	g1.set_title("vitesse moyenne de l'ensemble du traffic\nau cours du temps")
	g2.set_xlabel("temps t")
	g2.set_ylabel("nombre de véhicules")
	g2.set_title("nombre de véhicules par tranche de\ndifférence à la vitesse idéale selon le temps")
	g2.legend()
	# Ajuster l'espacement entre les graphiques
	plt.tight_layout()
	# Afficher le graphique
	plt.show()
	return 

def main_noir(duree, v_ideal = 115, v_init_inf = 110, v_init_sup = 125):
	run = True
	road = Road('test_road.txt') #objet route
	traffic = Traffic(road)
	timestamp = time.time()
	# ~ CLOCK = pygame.time.Clock()
	# ~ drawRoad(road, WINDOW, dim)
	
	# ~ taillePort, nbPortions, gap, roadTness, tness = displayCalculs(road, dim)
	nb_cell = 80
	distance_minimale = 10
	traffic.generateCells(170, v_init_inf,v_init_sup, 7)
	cell = None
	date_debut_simulation = time.time()
	T=[]
	VT = []
	L0, L10, L20, L30, L40, L50 = [], [], [], [], [], []
	
	print("coefficient temporel = "+str(coefT))
	
	while time.time() - date_debut_simulation < duree:
		dt = time.time()-timestamp
		timestamp = time.time()
		dt = dt*coefT
		
		
		if road.date_debut_mesure_VM + road.duree_mesure_VM*dt < time.time() : #au 1er tour de boucle tq on a dépasser le temps dure*dt depuis la dernière mesure, on mesure
			road.mesure_vitesses = True
			road.list_vitesses = []
			road.date_debut_mesures_VM = time.time()
		#__UPDATE___________________
		road.update(dt)
		#__UPDATE___________________
		
		# ~ CLOCK.tick(60)
		#_________________________________MESURES
		if road.mesure_vitesses == True and road.list_vitesses != []:
			date =time.time()-date_debut_simulation
			road.mesure_vitesses = False
			SOM = sum(road.list_vitesses)
			LEN = len(road.list_vitesses)
			mes = (SOM/LEN)*3.6
			
			# ~ SOMD = sum(road.list_distances)
			# ~ LEND = len(road.list_distances)
			# ~ mesd = (SOMD/LEND)
			# ~ nb_0 = 0
			# ~ nb_10 = 0
			# ~ nb_20 = 0
			# ~ nb_30 = 0
			# ~ nb_40 = 0
			# ~ nb_50 = 0
			# ~ for v in road.list_vitesses:
				# ~ if v < v_ideal - 100 :
					# ~ nb_50 += 1
				# ~ elif v < v_ideal - 80 :
					# ~ nb_40 += 1
				# ~ elif v < v_ideal - 60 :
					# ~ nb_30 += 1
				# ~ elif v < v_ideal - 40 :
					# ~ nb_20 += 1
				# ~ elif v < v_ideal - 20 :
					# ~ nb_10 += 1
				# ~ else : 
					# ~ nb_0 += 1
					
				
			# ~ L0.append(nb_0)
			# ~ L10.append(nb_10)
			# ~ L20.append(nb_20)
			# ~ L30.append(nb_30)
			# ~ L40.append(nb_40)
			# ~ L50.append(nb_50)
			
			
			
			# ~ mi_ecart_type = (sqrt(sum([v**2 for v in road.list_vitesses])/ LEN)*3.6)/2
			# ~ mini =  mes - mi_ecart_type
			# ~ maxi = mes + mi_ecart_type
			# ~ print("Vitesse moyenne = "+str( mes ) +" à "+str(date)+" secondes du lancement" )
			# ~ MAX.append(maxi)
			# ~ MIN.append(mini)
			
			T.append(date*10)
			VT.append(mes)
		#_________________________________MESURES
			
		##############################################FIN BOUCLE
	print("execution terminee --> compte rendu :\n temps simulé = "+str((time.time()-date_debut_simulation)*8) + "\ntemps réel écoulé = "+str(time.time()-date_debut_simulation))
	print("nombre d'accidents : "+str(len(road.list_accidents)))
	print("nombre de véhicules injecté = "+str(nb_cell) + "\nà une vitesse initiale comprise entre "+str(v_init_inf)+" et "+str(v_init_sup)+" km/h")
	i = int(0.90*len(T))
	return 	(sum(VT[i:])/len(VT[i:]))*3.6 #, L0, L10, L20, L30, L40, L50 

if __name__ == '__main__':
	# ~ print(main_no_diplay(10))
	main()


















