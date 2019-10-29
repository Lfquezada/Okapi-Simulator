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
    			deltaX = self.xPos - x
    			deltaY = self.yPos - y
    			distance = abs(deltaX**2) + abs(deltaY**2)

    			if distance <= self.speed and self.speed <= 5:
    				
    				speedFactor = random.randint(1,100)
    				if speedFactor <= 50:
    					self.speed += 1

    				self.rFactor += random.randint(1,4)
    				self.weight += random.randint(2,5)
    				individualAte = True
    				return True
    			else:
    				individualAte = False
    	return individualAte

class Terrain:
	cycle = 0
	totalDeaths = 0
	individuals = []
	currentPopulation = []
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
			self.individuals.append(Okapi(initOkapiSpeed,initOkapiWeight,initReplicationFactor,initDeathFactor,randomX,randomY))

	def generateInitVegetation(self,vegetationAmount):
		for i in range(vegetationAmount):
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

	def update(self):
		self.cycle += 1
		self.currentPopulation.append(len(self.individuals))

		if self.cycle == 1:
			self.spawnFood()
		if self.cycle % 2 == 0:
			self.spawnFood()

		# random individual movement
		for individual in self.individuals:
			individual.move(terrain.width,terrain.height)

			# If food is near, the individual eats it
			individualAte = individual.eatNearFood(self.currentFood)

			if individualAte == False:
				probabilityFactor = random.randint(1,100)
				if probabilityFactor < 40:
					individual.deathFactor += 1

			# Chance to replicate depending on rFactor
			probabilityFactor = random.randint(1,1000)
			if probabilityFactor <= individual.rFactor: 
				# successful replication, spawns near
				self.individuals.append(Okapi(1,200,initReplicationFactor,initDeathFactor,individual.xPos,individual.yPos))

			# Chance of death depending on rFactor
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
	
	for individual in terrain.individuals:
		xs.append(individual.xPos)
		ys.append(individual.yPos)

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

	# Vegetation
	plt.scatter(terrain.vegetation['x'],terrain.vegetation['woodYs'],c='#47361E',marker='|',s=120)
	plt.scatter(terrain.vegetation['x'],terrain.vegetation['y'],c='#145A32',marker='^',s=120,linewidths=1,edgecolors='#1D8348')

	# Food
	plt.scatter(terrain.currentFood['x'],terrain.currentFood['y'],c='#27AE60',marker='d',s=5,linewidths=0.3,edgecolors='#00461D')


# Simulator  ---------------------------------------------------------------------
print("\n    O K A P I   S I M  1.0")
print("\n|| Building terrain...")
terrain = Terrain(200,200,20,75)
print("\n|| Terrain laid out...")
print("\n|| Stating simulation...")
animationCycle = FuncAnimation(plt.gcf(),animate,fargs=[terrain],interval=1)

print("\n|| Simulation running...")
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)

ax = plt.gca()
ax.set_facecolor('#229954')

fig = plt.gcf()
fig.canvas.set_window_title('OKAPI Simulator')

plt.show()

# Final Results ------------------------------------------------------------------

finalSpeeds = []
finalWeights = []
indexes = []

for i in terrain.individuals:
	finalSpeeds.append(i.speed)
	finalWeights.append(i.weight)

for i in range(0,terrain.cycle):
	indexes.append(i+1)

fig,axs = plt.subplots(2, constrained_layout=True)
axs[0].scatter(finalSpeeds,finalWeights,c='#C42B2B',marker='.',s=15)
axs[0].set_title('Speeds vs. Weights')
axs[0].set_xlabel('Speed (unit/cycle)')
axs[0].set_ylabel('Weight (kg)')
axs[0].set_facecolor('#3B3B3B')
fig.suptitle('Simulation Results',fontsize=12)
fig.canvas.set_window_title('OKAPI Simulator')

axs[1].plot(indexes,terrain.currentPopulation,c='#C42B2B')
axs[1].set_title('Cycle vs. Population')
axs[1].set_xlabel('Cycle')
axs[1].set_ylabel('Population')
axs[1].set_facecolor('#3B3B3B')

plt.show()

print("\n||| Simulation ended.\n")

