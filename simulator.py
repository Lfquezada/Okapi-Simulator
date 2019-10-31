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
import argparse
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
initReplicationFactor = 4
initDeathFactor = 1
initOkapiSpeed = 2
initOkapiWeight = 250

class Okapi:

    def __init__(self,speed,weight,rFactor,deathFactor,xPos,yPos):
    	# Creation genotypes are assigned
    	self.speed = speed
    	self.weight = weight
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

    def eatNearFood(self,food):

    	for x in food['x']:
    		for y in food['y']:

    			xRange = range(self.xPos-self.speed,self.xPos+self.speed+1)
    			yRange = range(self.yPos-self.speed,self.yPos+self.speed+1)

    			if (x in xRange and y in yRange):
    				if self.speed < 5:
    					speedFactor = random.randint(1,100)
    					if speedFactor <= 25:
    						self.speed += 1

    					self.rFactor += random.randint(1,2)
    					self.weight += random.randint(2,4)
    					return (x,y)
    	probabilityFactor = random.randint(1,100)
    	if probabilityFactor <= 25:
    		self.deathFactor += 1
    	return (-1,-1)


class Leopard:

    def __init__(self,speed,xPos,yPos):
    	# Creation genotypes are assigned
    	self.speed = speed
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
	predators = []
	currentPopulation = []
	initFood = {'x':[],'y':[]}
	currentFood = {'x':[],'y':[]}
	vegetation = {'x':[],'y':[],'woodYs':[]}

	def __init__(self,height,width,populationAmount,vegetationAmount,predatorsAmount):
		self.height = height
		self.width = width
		self.vegetationAmount = vegetationAmount
		self.predatorsAmount = predatorsAmount
		self.generateInitPopulation(populationAmount)
		self.generateInitVegetation()
		self.spawnInitFood()
		self.spawnPredators()

	def generateInitPopulation(self,amount):
		for i in  range(amount):
			randomX = random.randint(0,self.width)
			randomY = random.randint(0,self.height)
			self.individuals.append(Okapi(initOkapiSpeed,initOkapiWeight,initReplicationFactor,initDeathFactor,randomX,randomY))

	def generateInitVegetation(self):
		for i in range(self.vegetationAmount):
			randomX = random.randint(0,self.width)
			randomY = random.randint(0,self.height)
			self.vegetation['x'].append(randomX)
			self.vegetation['y'].append(randomY)
			self.vegetation['woodYs'].append(randomY-4)

	def spawnInitFood(self):
		for i in  range(self.vegetationAmount):
			xPos = self.vegetation['x'][i] + random.randint(-2,2)
			yPos = self.vegetation['y'][i] - 4
			self.initFood['x'].append(xPos)
			self.initFood['y'].append(yPos)
			'''
			xPos = self.vegetation['x'][i] + random.randint(1,2)
			yPos = self.vegetation['y'][i] - 4
			self.initFood['x'].append(xPos)
			self.initFood['y'].append(yPos)
			'''

	def spawnFood(self):
		self.currentFood = self.initFood

	def spawnPredators(self):
		for i in range(self.predatorsAmount):
			randomX = random.randint(0,self.width)
			randomY = random.randint(0,self.height)
			self.predators.append(Leopard(random.randint(8,10),randomX,randomY))


	def update(self):
		self.cycle += 1
		self.currentPopulation.append(len(self.individuals))

		if self.cycle == 1:
			self.spawnFood()
		if self.cycle % 2 == 0:
			self.spawnFood()

		for leopard in self.predators:
			leopard.move(terrain.width,terrain.height)

		# random individual movement
		for individual in self.individuals:
			individual.move(terrain.width,terrain.height)

			# If food is near, the individual eats it
			foodX,foodY = individual.eatNearFood(self.currentFood)

			# Chance to replicate depending on rFactor
			probabilityFactor = random.randint(1,1000)
			if probabilityFactor <= individual.rFactor: 
				# successful replication, spawns near
				self.individuals.append(Okapi(1,200,initReplicationFactor,initDeathFactor,individual.xPos,individual.yPos))

			# Death chances increase by excess weight
			if individual.weight in range(250,300):
				individual.deathFactor += 1
			if individual.weight in range(300,325):
				individual.deathFactor += 2
			if individual.weight in range(325,350):
				individual.deathFactor += 10
			if individual.weight >= 350:
				individual.deathFactor += 50

			individualKilled = False
			for leopard in self.predators:
				leopardXRange = range(leopard.xPos-leopard.speed,leopard.xPos+leopard.speed+1)
				leopardYRange = range(leopard.yPos-leopard.speed,leopard.yPos+leopard.speed+1)

				if (individual.xPos in leopardXRange and individual.yPos in leopardYRange):
					# death by leopard
					self.individuals.remove(individual)
					self.totalDeaths += 1
					individualKilled = True
					leopard.xPos = individual.xPos
					leopard.yPos = individual.yPos

			# Chance of death depending on deathFactor if not killed by a predator
			if not individualKilled:
				probabilityFactor = random.randint(1,1000)
				if probabilityFactor <= individual.deathFactor: 
					# death
					self.individuals.remove(individual)
					self.totalDeaths += 1

	def printData(self):
		print('Dimensions X:{} Y:{}\n'.format(self.width,self.height))
		for individual in self.individuals:
			print('ID:{} \tX:{} \tY:{} \trFactor:{} \tData:{}'.format(individual.id,individual.xPos,individual.yPos,individual.rFactor,individual))

def animate(frame,terrain):
	terrain.update()
	xs = []
	ys = []
	terrainXs = [-5,terrain.width+5,terrain.width+5,-5,-5]
	terrainYs = [-5,-5,terrain.height+5,terrain.height+5,-5]
	leopardXs = []
	leopardYs = []
	
	for individual in terrain.individuals:
		xs.append(individual.xPos)
		ys.append(individual.yPos)

	for leopard in terrain.predators:
		leopardXs.append(leopard.xPos)
		leopardYs.append(leopard.yPos)

	plt.cla()
	plt.title('Cycle: {}\n[ Alive: {} ][ Deaths: {} ]'.format(
		terrain.cycle,
		len(terrain.individuals),
		terrain.totalDeaths),
	fontsize=10,
	loc='left')

	# Anchor points for terrain visual
	plt.plot(terrainXs,terrainYs,color='#229954')

	# Animals
	plt.scatter(xs,ys,c='#352510',marker='1',s=75)

	# Predators
	plt.scatter(leopardXs,leopardYs,c='#bf891d',marker='v',s=70,alpha=0.9,linewidths=0.2,edgecolors='#ab7a1a')

	# Vegetation
	plt.scatter(terrain.vegetation['x'],terrain.vegetation['woodYs'],c='#47361E',marker='|',s=120)
	plt.scatter(terrain.vegetation['x'],terrain.vegetation['y'],c='#145A32',marker='^',s=120,linewidths=1,edgecolors='#1D8348')

	# Food
	plt.scatter(terrain.currentFood['x'],terrain.currentFood['y'],c='#27AE60',marker='d',s=5,linewidths=0.3,edgecolors='#00461D')


# Simulator  ---------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('okapis',help='Number of Okapis to spawn.')
parser.add_argument('trees',help='Number of trees to spawn.')
parser.add_argument('predators',help='Number of predators to spawn.')
parser.add_argument('hunters',help='Number of hunters to spawn')
args = parser.parse_args()

print("\n    O K A P I   S I M  1.0")
print("\n|| Building terrain...")
terrain = Terrain(200,200,int(args.okapis),int(args.trees),int(args.predators))
print("\n|| Terrain laid out...")
print("\n|| Stating simulation...")

#plt.style.use('dark_background')
animationCycle = FuncAnimation(plt.gcf(),animate,fargs=[terrain],interval=1)

print("\n|| Simulation running...")
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)

ax = plt.gca()
ax.set_facecolor('#229954')

fig = plt.gcf()
fig.canvas.set_window_title('OKAPI Simulator')

plt.show()
print("\n|| Simulation ended.")

# Final Results ------------------------------------------------------------------

finalSpeeds = []
finalWeights = []
indexes = []

for i in terrain.individuals:
	finalSpeeds.append(i.speed)
	finalWeights.append(i.weight)

for i in range(0,terrain.cycle):
	indexes.append(i+1)

plt.style.use('dark_background')

fig,axs = plt.subplots(2, constrained_layout=True)
axs[0].set_title('Speeds vs. Weights')
axs[0].set_xlabel('Speed (unit/cycle)')
axs[0].set_ylabel('Weight (kg)')
axs[0].set_facecolor('#000000')
fig.suptitle('Simulation Results',fontsize=12)
fig.canvas.set_window_title('OKAPI Simulator')

axs[1].set_title('Cycle vs. Population')
axs[1].set_xlabel('Cycle')
axs[1].set_ylabel('Population')
axs[1].set_facecolor('#000000')

axs[0].scatter(finalSpeeds,finalWeights,c='#3AFF00',marker='.',s=100,alpha=0.5)
axs[1].fill_between(indexes,terrain.currentPopulation,0,color='#3AFF00',alpha=0.5)

plt.show()
print("\n|| Showing final results...\n")

