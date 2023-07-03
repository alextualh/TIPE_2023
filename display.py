import pygame
from pygame.locals import *
from classes import coefT, Road,Driver,Car,Cell
# ~ HEIGHT,WIDTH = 830,1530
# ~ WINDOW = pygame.display.set_mode((WIDTH, HEIGHT)) #Setting WINDOW
# ~ pygame.display.set_caption('Traffic SIM') #Window Name
#______________________________________________________________________________ 
def displayCalculs(road:Road, dim:tuple):
	HEIGHT, WIDTH = dim
	taille = road.taille
	
	if taille < 1000 :
		taillePort = round( taille / 5 )
	if 1000 <= taille <= 5000 and len(road.voies)<=3  :
		taillePort = round( taille / 10 )
	if 1000 <= taille <= 5000 and len(road.voies)>3  :
		taillePort = round( taille / 5 )
	if taille > 5000 and len(road.voies)<=2  :
		taillePort = round( taille / 10 )
	if taille > 5000 and len(road.voies)>2 :
		taillePort = round( taille / 5 )
	nbPortions = round( taille / taillePort ) 
	gap = 15
	if len(road.voies) == 1:
		gap = 50
	roadTness = round( (HEIGHT-((nbPortions-1)*gap)) / nbPortions ) # largeur route (ie tte les voies)
	tness = round ( roadTness/len(road.voies) )
	
	
	rep : tuple = (taillePort, nbPortions, gap, roadTness, tness) 
	return rep
#______________________________________________________________________________ drawRoad

def drawRoad(road, WINDOW, dim : tuple):
	HEIGHT, WIDTH = dim
	ROADCOLOR = (80, 80, 80) #gris
	WHITE = (35, 35, 35) #définition du blanc (gris sombre)
	taille = road.taille
	
	taillePort, nbPortions, gap, roadTness, tness = displayCalculs(road, dim)
	
	yDraw = 5				
	for j in range(nbPortions):
		# DESSINE PAR PORTIONS
		pygame.draw.rect(WINDOW, ROADCOLOR, (0,yDraw,WIDTH,roadTness)) #Drawing the road, thickness 0 = filled, 0 pos en x
#______________________________________________________________________________ 
		#dessin des lignes de sécurité blanches
		x=0
		sideLen = 30 #longueur dans le sens de la route des bandes
		sideWid = 1 #largeur des bandes en pixel
		while x < WIDTH: #boucle qui fait avancer la zone de dessin en x (horizontalement)
			pygame.draw.rect(WINDOW, WHITE, (x,yDraw+5, sideLen,sideWid))#en haut
			pygame.draw.rect(WINDOW, WHITE, (x,yDraw + roadTness - 5 - sideWid, sideLen,sideWid))#en bas
			i=0
			while i<(len(road.voies)-1): #boucle qui dessine chaque étage de bande blanche en un même x
				y = yDraw+(tness*(i+1))-(sideWid//2)
				pygame.draw.rect(WINDOW, WHITE,(x, y, sideLen, sideWid))#au milieu, entre les voies
				i += 1
			x+=2*sideLen
		#met à jour yDraw, on dessine la portion suivante au prochain tour de boucle avec cette nouvelle position
		yDraw += roadTness + gap 



#______________________________________________________________________________ 
#______________________________________________________________________________ drawCell

def drawCell(road, WINDOW, dim : tuple): #dessine chaque véhicule
	#CONSTANTES 
	HEIGHT,WIDTH = dim #taille de la fenêtre
	taille = road.taille
	
	taillePort, nbPortions, gap, roadTness, tness = displayCalculs(road, dim)
  
	portion = taillePort #en mètre
	coef = round(WIDTH/portion)
	for i in range(len(road.voies)):
		cell = road.voies[i]
		head = road.voies[i]
					
		while cell.next != head and cell.next != None:
			x = cell.content.x
			indPort = (x // portion)
			yDraw = ((tness//2) - round((tness*0.7)/2)) + 5 + indPort*(gap+roadTness)      + tness*i
			# -round(..)/2 car on va en haut du véhicule de largeur round(..), +20 car décalage initial, 2 terme pr la portion, init à 20, 3e pr la voir dans la portion1
			xPort = x - portion*indPort
			xDraw = round(xPort * coef)
			pygame.draw.rect(WINDOW,cell.content.car.color,(xDraw, yDraw, coef*cell.content.car.longueur, round(tness*0.7))) # le dernier nbre donne la largeur du véhicule, 80% de la largeur de la voie
			
			if road.display_vitesses == 1 :
				font = pygame.font.SysFont(None, cell.content.car.longueur*5)
				img = font.render(str(round(cell.content.v*3.6/coefT, 2))+' km/h', True, (255, 255, 255))
				rect = img.get_rect()
				rect.center = (xDraw+(coef*(cell.content.car.longueur))//2, yDraw+(round(tness*0.7))//2)
				WINDOW.blit(img, rect)
			if road.display_vitesses == 2 :
				font = pygame.font.SysFont(None, cell.content.car.longueur*5)
				img = font.render(str(cell.content.etat_nc)+' '+str(cell.content.etat_c), True, (255, 255, 255))
				rect = img.get_rect()
				rect.center = (xDraw+(coef*(cell.content.car.longueur))//2, yDraw+(round(tness*0.7))//2)
				WINDOW.blit(img, rect)
			
			cell = cell.next
		
		if cell.content != None:
			x = cell.content.x
			indPort = (x // portion)
			yDraw = ((tness//2) - round((tness*0.7)/2)) + 5 + indPort*(gap+roadTness)      + tness*i
			# -round(..)/2 car on va en haut du véhicule de largeur round(..), +20 car décalage initial, 2 terme pr la portion, init à 20, 3e pr la voir dans la portion1
			xPort = x - portion*indPort
			xDraw = round(xPort * coef)
			pygame.draw.rect(WINDOW,cell.content.car.color,(xDraw, yDraw, coef*cell.content.car.longueur, round(tness*0.7))) # le dernier nbre donne la largeur du véhicule, 80% de la largeur de la voie
			
			if road.display_vitesses == 1 :
				font = pygame.font.SysFont(None, cell.content.car.longueur*5)
				img = font.render(str(round(cell.content.v*3.6/coefT, 2))+' km/h', True, (255, 255, 255))
				rect = img.get_rect()
				rect.center = (xDraw+(coef*(cell.content.car.longueur))//2, yDraw+(round(tness*0.7))//2)
				WINDOW.blit(img, rect)
			if road.display_vitesses == 2 :
				font = pygame.font.SysFont(None, cell.content.car.longueur*5)
				img = font.render(str(cell.content.etat_nc)+' '+str(cell.content.etat_c), True, (255, 255, 255))
				rect = img.get_rect()
				rect.center = (xDraw+(coef*(cell.content.car.longueur))//2, yDraw+(round(tness*0.7))//2)
				WINDOW.blit(img, rect)


    

	


