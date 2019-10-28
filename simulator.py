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
initReplicationFactor = 3
initDeathFactor = 1
initOkapiSpeed = 2
initOkapiSize = 100

class Okapi:

    def __init__(self,speed,size,rFactor,deathFactor,xPos,yPos):
    	# Creation genotypes are assigned
    	self.speed = speed
    	self.size = size
    	self.rFactor = rFactor
    	self.deathFactor = deathFactor
    	self.xPos = xPos
    	self.yPos = yPos

    def move(self,xMax,yMax):
    	moveX = random.randint(-1*self.speed,self.speed)
    	moveY = random.randint(-1*self.speed,self.speed)
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
	cycle = 0
	totalDeaths = 0
	individuals = []
	initFood = {'x':[],'y':[]}
	currentFood = {'x':[],'y':[]}
	vegetation = {'x':[],'y':[],'woodYs':[]}

	def __init__(self,height,width,populationAmount,vegetationAmount):
		self.height = height
		self.width = width
		self.vegetationAmount = vegetationAmount
		self.generateInitPopulation(populationAmount)
		self.generateInitVegetation(vegetationAmount)
		self.spawnInitFood()

	def generateInitPopulation(self,amount):
		for i in  range(amount):
			randomX = random.randint(0,self.width)
			randomY = random.randint(0,self.height)
			self.individuals.append(Okapi(initOkapiSpeed,initOkapiSize,initReplicationFactor,initDeathFactor,randomX,randomY))

	def generateInitVegetation(self,vegetationAmount):
		for i in range(vegetationAmount):
			randomX = random.randint(0,self.width)
			randomY = random.randint(0,self.height)
			self.vegetation['x'].append(randomX)
			self.vegetation['y'].append(randomY)
			self.vegetation['woodYs'].append(randomY-4)

	def spawnInitFood(self):
		for i in  range(self.vegetationAmount):
			xPos = self.vegetation['x'][i] - random.randint(1,2)
			yPos = self.vegetation['y'][i] -4
			self.initFood['x'].append(xPos)
			self.initFood['y'].append(yPos)

			xPos = self.vegetation['x'][i] + random.randint(1,2)
			yPos = self.vegetation['y'][i] -4
			self.initFood['x'].append(xPos)
			self.initFood['y'].append(yPos)

	def spawnFood(self):
		self.currentFood = self.initFood

	def update(self):
		self.cycle += 1
		self.spawnFood()

		# random individual movement
		for individual in self.individuals:
			individual.move(terrain.width,terrain.height)

			# Chance to replicate depending on rFactor
			probabilityFactor = random.randint(1,1000)
			if probabilityFactor <= individual.rFactor: 
				# successful replication, spawns near
				self.individuals.append(Okapi(initOkapiSpeed,initOkapiSize,initReplicationFactor,initDeathFactor,individual.xPos,individual.yPos))

			# Chance of death depending on rFactor
			probabilityFactor = random.randint(1,750)
			if probabilityFactor <= individual.deathFactor: 
				# death
				self.individuals.remove(individual)
				self.totalDeaths += 1

		# TODO: individual finds food: rFactor += 2
		# doesnt find food: rFactor -= 1


	def printData(self):
		print('Dimensions X:{} Y:{}\n'.format(self.width,self.height))
		for individual in self.individuals:
			print('ID:{} \tX:{} \tY:{} \trFactor:{} \tData:{}'.format(individual.id,individual.xPos,individual.yPos,individual.rFactor,individual))

def animate(frame,terrain):
	spacer = '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'
	terrain.update()
	xs = []
	ys = []
	terrainXs = [-3,terrain.width+3,terrain.width+3,-3,-3]
	terrainYs = [-3,-3,terrain.height+3,terrain.height+3,-3]
	
	for individual in terrain.individuals:
		xs.append(individual.xPos)
		ys.append(individual.yPos)

	plt.cla()
	plt.title('{}Cycle: {}\n[ Alive: {} ][ Deaths: {} ]'.format(
		spacer,
		terrain.cycle,
		len(terrain.individuals),
		terrain.totalDeaths),
	fontsize=10,
	loc='left')

	# Anchor points for terrain visual
	plt.plot(terrainXs,terrainYs,color='#229954')

	# Animals
	plt.scatter(xs,ys,c='#352510',marker='1',s=75)

	# Vegetation
	plt.scatter(terrain.vegetation['x'],terrain.vegetation['woodYs'],c='#47361E',marker='|',s=120)
	plt.scatter(terrain.vegetation['x'],terrain.vegetation['y'],c='#145A32',marker='^',s=120,linewidths=1,edgecolors='#1D8348')

	# Food
	plt.scatter(terrain.currentFood['x'],terrain.currentFood['y'],c='#27AE60',marker='d',s=5,linewidths=0.3,edgecolors='#00461D')

	#print('{}[ Generation: {} ]\n[ Alive: {} ]\n[ Deaths: {} ]'.format(spacer,terrain.generation,len(terrain.individuals),terrain.totalDeaths))


# Simulator  ---------------------------------------------------------------------
print("\n    O K A P I   S I M  1.0")
print("\n|| Building terrain...")
terrain = Terrain(200,200,20,75)
print("\n|| Terrain laid out...")
print("\n|| Stating simulation...")
animationCycle = FuncAnimation(plt.gcf(),animate,fargs=[terrain],interval=10)

print("\n|| Simulation running...")
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)

ax = plt.gca()
ax.set_facecolor('#229954')

fig = plt.gcf()
fig.canvas.set_window_title('OKAPI Simulator')

plt.show()

print("\n||| Simulation ended.\n")

