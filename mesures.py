from simulation_graphics import main_noir
import matplotlib.pyplot as plt
from classes import coefT
c = coefT
nb_exp = 5

Vinf, Vsup = 75, 85
name = "mesures_camions_26%_25_50_25_"+str(Vinf)+"_"+str(Vsup)+".txt"
def launch():
	name = "mesures_camions_16%_25_50_25_"+str(Vinf)+"_"+str(Vsup)+".txt"
	fp = open(name, "w")
	fp.close()
	fp = open(name, "w")


	for j in range(nb_exp):
		T, X = main_noir(60, v_init_inf = Vinf, v_init_sup = Vsup)
		fp.write(str(T))
		fp.write("\n")
		fp.write(str(X))	
		fp.write("\n")
		print(c)
	return
	
#___________________________________________
#___________________________________________
def drawing():
	colors = ['b','g','r','c','m','y','k','w', 'r', 'r', 'b', 'c', 'b', 'c', 'c', 'c', 'c', 'c', 'c']
	fp = open("mesures_camions_25_50_25_75_85.txt", "r")
	i = 0
	for j in range(nb_exp-1): #parcours des mesures à coef fixé
		T = eval([e.strip() for e in fp.readline().splitlines()][0])
		X = eval([e.strip() for e in fp.readline().splitlines()][0])
		plt.plot(T, X, color = colors[i] )
	T = eval([e.strip() for e in fp.readline().splitlines()][0])
	X = eval([e.strip() for e in fp.readline().splitlines()][0])
	plt.plot(T, X, color = colors[i], label = "coef = "+str(i))
	fp.close()
	
	i= 1
	fp = open("mesures_camions_50%_25_50_25_75_85.txt", "r")
	for j in range(nb_exp-1): #parcours des mesures à coef fixé
		T = eval([e.strip() for e in fp.readline().splitlines()][0])
		X = eval([e.strip() for e in fp.readline().splitlines()][0])
		plt.plot(T, X, color = colors[i] )
	T = eval([e.strip() for e in fp.readline().splitlines()][0])
	X = eval([e.strip() for e in fp.readline().splitlines()][0])
	plt.plot(T, X, color = colors[i], label = "coef = "+str(i))
	fp.close()
	plt.xlabel("temps t en secondes")
	plt.ylabel("vitesse moyenne Vm(t)")
	plt.title("")
	plt.legend()


	# ~ # Afficher le graphique
	plt.show()
	
	return
	
# ~ launch()
# ~ drawing()

# ~ fp = open("mes"+str(1)+".txt", "r")
# ~ T = eval([e.strip() for e in fp.readline().splitlines()][0])
# ~ X = eval([e.strip() for e in fp.readline().splitlines()][0])
# ~ print(T)
# ~ print("\n et \n")
# ~ print(X)
# Ajouter des étiquettes et un titre

# ~ launch()
# ~ drawing()


# ~ import matplotlib.pyplot as plt
# ~ from mpl_toolkits import mplot3d
# ~ fig = plt.figure()
# ~ ax = plt.axes(projection='3d')
# ~ colors = ['b','g','r','c','m','y','k','c', 'r', 'mx', 'b', 'c', 'b', 'c', 'c', 'c', 'c', 'c', 'c']
# ~ L = [100, 90, 80, 70, 60, 50, 40, 30, 20, 10]
# ~ fp = open("mesures_camions_25_50_25_75_85.txt", "r")
# ~ i = 0
# ~ for j in range(9, 0, -1): #parcours des mesures à coef fixé
	# ~ T = eval([e.strip() for e in fp.readline().splitlines()][0])
	# ~ X = eval([e.strip() for e in fp.readline().splitlines()][0])
	# ~ ax.plot3D([t*4 for t in T], [L[j] for e in T],X , colors[j])
	# ~ print(55)
# ~ fp.close()





# ~ # Configurations des axes
# ~ ax.set_xlabel('temps t')
# ~ ax.set_ylabel('proportion de profils agressifs en %')
# ~ ax.set_zlabel('vitesse moyenne sur 10 simulations')

# ~ # Affichage du graphe en 3D
# ~ plt.show()

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
# ~ import matplotlib.pyplot as plt
# ~ from mpl_toolkits import mplot3d
fig = plt.figure()
ax = plt.axes(projection='3d')
# Données de la surface en 3D
L = [0, 10, 20, 30, 40, 50]
A = [0, 10, 20, 30, 40, 50]
p5 = [50 for i in range(6)]
z5 = [82.5, 81, 79, 78, 77.5, 77]
p4 = [40 for i in range(6)]
z4 = [82, 81, 82, 80, 79, 77.5]
p3 = [30 for i in range(6)]
z3 = [82, 83.5, 85 ,83, 80, 79]
p2 = [20 for i in range(6)]
z2 = [79, 81.5, 83,80, 81, 79.5]
p1 = [10 for i in range(6)]
z1 = [78, 79.5, 82.5, 79, 77, 76.5]
p0 = [0 for i in range(6)]
z0 = [79, 81, 80, 79, 77, 77]
     
ax.scatter3D(A, p0, z0, 'r')
ax.scatter3D(A, p1, z1, 'r')
ax.scatter3D(A, p2, z2, 'r')
ax.scatter3D(A, p3, z3, 'r')
ax.scatter3D(A, p4, z4, 'r')
ax.scatter3D(A, p5, z5, 'r')

ax.plot3D(A, p0, z0, 'r')
ax.plot3D(A, p1, z1, 'r')
ax.plot3D(A, p2, z2, 'r')
ax.plot3D(A, p3, z3, 'r')
ax.plot3D(A, p4, z4, 'r')
ax.plot3D(A, p5, z5, 'r')

ax.set_zlim(70, 85)





# Configurations des axes
ax.set_xlabel('proportion de profils prudents en %')
ax.set_ylabel('proportion de profils agressifs en %')
ax.set_zlabel('vitesse moyenne finale sur 50 simulations')


# Affichage de la surface en 3D
plt.show()



