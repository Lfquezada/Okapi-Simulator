'''
Universidad del Valle de Guatemala
Proyecto de Biologia General
Simulador de Okapi

Integrantes: 
- Luis Quezada
- Jennifer Sandoval
- Esteban del Valle
- Andrea Paniagua
'''

import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
initRFactor = 0.3

class Okapi:

    def __init__(self,id,rFactor,xPos,yPos):
        self.id = id
        self.rFactor = rFactor
        self.xPos = xPos
        self.yPos = yPos

    def move(self,xMax,yMax):
    	moveX = random.randint(-2,2)
    	moveY = random.randint(-2,2)
    	self.xPos += moveX
    	self.yPos += moveY

    	# terrain restrictions
    	if self.xPos < 0:
    		self.xPos = 1
    	if self.xPos > xMax:
    		self.xPos = xMax-1

    	if self.yPos < 0:
    		self.yPos = 1
    	if self.yPos > yMax:
    		self.yPos = yMax-1


class Terrain:

	individuals = []

	def __init__(self,height,width,amount):
		self.height = height
		self.width = width
		self.generateInitPopulation(amount)

	def generateInitPopulation(self,amount):
		for id in  range(amount):
			randomX = random.randint(0,self.width)
			randomY = random.randint(0,self.height)
			self.individuals.append(Okapi(id+1,initRFactor,randomX,randomY))

	def update(self):
		# random individual movement
		for individual in self.individuals:
			individual.move(terrain.width,terrain.height)

	def printData(self):
		print('Dimensions X:{} Y:{}\n'.format(self.width,self.height))
		for individual in self.individuals:
			print('ID:{} \tX:{} \tY:{} \trFactor:{} \tData:{}'.format(individual.id,individual.xPos,individual.yPos,individual.rFactor,individual))

def animate(frame,terrain):
	terrain.update()
	xs = []
	ys = []
	terrainXs = [-3,terrain.width+3,terrain.width+3,-3,-3]
	terrainYs = [-3,-3,terrain.height+3,terrain.height+3,-3]
	
	for individual in terrain.individuals:
		xs.append(individual.xPos)
		ys.append(individual.yPos)

	plt.cla()
	plt.plot(terrainXs,terrainYs,color='#252525')
	plt.scatter(xs,ys,color='#FF7700')

	print('[ Alive: {} ]\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'.format(len(terrain.individuals)))
	#print('[ Deaths: {} ]\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'.format(len(terrain.individuals)))


# Simulator  ---------------------------------------------------------------------
print("\n    O K A P I   S I M  1.0")
print("\n|| Building terrain...")
terrain = Terrain(200,200,20)
print("\n|| Terrain laid out...")
print("\n|| Stating simulation...")
animationCycle = FuncAnimation(plt.gcf(),animate,fargs=[terrain],interval=100)

print("\n|| Simulation running...")
plt.tight_layout()
plt.title("OKAPI Simulator", fontsize=22)
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)

ax = plt.gca()
ax.set_facecolor('#252525')

fig = plt.gcf()
fig.canvas.set_window_title('OKAPI Simulator')


plt.show()

print("\n||| Simulation ended.\n")

