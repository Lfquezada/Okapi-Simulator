'''
Universidad del Valle de Guatemala
Proyecto de Biologia General
Simulador de Okapi
'''

# Modulos a usar
import random
import argparse
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from scipy import stats

# Random seed
random.seed(5)

# Initial Values
initReplicationFactor = 4 # 4/1000
initDeathFactor = 1 # 1/1000
initOkapiSpeed = 2 # units per cyle
initOkapiWeight = 250 # standard init weight for medium okapis


class Okapi:

	# Creation traits are assigned
    def __init__(self,speed,weight,rFactor,deathFactor,xPos,yPos):
    	self.speed = speed
    	self.weight = weight
    	self.rFactor = rFactor
    	self.deathFactor = deathFactor
    	self.xPos = xPos
    	self.yPos = yPos

    # Okapi movement is random in all directions depending on its speed
    def move(self,xMax,yMax):
    	moveX = random.randint(-1*self.speed,self.speed)
    	moveY = random.randint(-1*self.speed,self.speed)
    	self.xPos += moveX
    	self.yPos += moveY

    	# terrain restrictions to prevent okapis from moving outside of bounds
    	if self.xPos < 0:
    		self.xPos = 1
    	if self.xPos > xMax:
    		self.xPos = xMax-1

    	if self.yPos < 0:
    		self.yPos = 1
    	if self.yPos > yMax:
    		self.yPos = yMax-1

    # Okapi checks on their range (depending on its speed) for near food
    def eatNearFood(self,food):

    	for x in food['x']:
    		for y in food['y']:
    			# ranges
    			xRange = range(self.xPos-self.speed,self.xPos+self.speed+1)
    			yRange = range(self.yPos-self.speed,self.yPos+self.speed+1)

    			# if food is near the okapi eats
    			if (x in xRange and y in yRange):
    				if self.speed < 6: # 6 speed limit (because Okapis real max speed is 60km/h)
    					speedFactor = random.randint(1,100) # to make speed not so easy to obtain thus more diversity
    					if speedFactor <= 35:
    						self.speed += 1

    					self.rFactor += random.randint(1,2) # eating increases chances of reproduction
    					self.weight += random.randint(2,4) # eating also increases weight
    					return (x,y)

    	# if no food was found near the okapi does not eat that cycle
    	# therefore deathchances increase
    	probabilityFactor = random.randint(1,100)
    	if probabilityFactor <= 10: # 10%
    		self.deathFactor += 1
    	return (-1,-1)


class Leopard:

	# Creation traits are assigned
    def __init__(self,speed,xPos,yPos):
    	# Creation genotypes are assigned
    	self.speed = speed
    	self.xPos = xPos
    	self.yPos = yPos

    # Leopard movement is pseudo-random in all directions depending on its speed
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


class Hunter:
	isAvailableToHunt = True
	lastHuntCycle = 0

	# Creation traits are assigned
	def __init__(self,gunRange,xPos,yPos):
		self.gunRange = gunRange
		self.xPos = xPos
		self.yPos = yPos

	# Hunter movement is random in all directions
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
	cycle = 0
	totalDeaths = 0
	totalBirths = 0
	individuals = []
	predators = []
	hunters = []
	currentPopulation = []
	initFood = {'x':[],'y':[]}
	currentFood = {'x':[],'y':[]}
	vegetation = {'x':[],'y':[],'woodYs':[]}

	# Terrain is given a size and the amount of okapis, trees, predators and hunters to start the simulation
	def __init__(self,height,width,populationAmount,vegetationAmount,predatorsAmount,huntersAmount, endCycle):
		self.height = height
		self.width = width
		self.huntersAmount = huntersAmount
		self.vegetationAmount = vegetationAmount
		self.predatorsAmount = predatorsAmount
		self.endCycle = endCycle
		self.generateInitPopulation(populationAmount)
		self.generateInitVegetation()
		self.spawnInitFood()
		self.spawnPredators()
		self.spawnHunters()

	# Spawns the requested amount of okapis in random spots around the terrain
	def generateInitPopulation(self,amount):
		for i in  range(amount):
			randomX = random.randint(0,self.width)
			randomY = random.randint(0,self.height)
			self.individuals.append(Okapi(initOkapiSpeed,initOkapiWeight,initReplicationFactor,initDeathFactor,randomX,randomY))

	# Spawns the requested amount of trees in random spots around the terrain
	def generateInitVegetation(self):
		for i in range(self.vegetationAmount):
			randomX = random.randint(0,self.width)
			randomY = random.randint(0,self.height)
			self.vegetation['x'].append(randomX)
			self.vegetation['y'].append(randomY)
			self.vegetation['woodYs'].append(randomY-4)

	# Spawns food sources in the trees hanging from the tree
	def spawnInitFood(self):
		for i in  range(self.vegetationAmount):
			xPos = self.vegetation['x'][i] + random.randint(-2,2)
			yPos = self.vegetation['y'][i] - 4
			self.initFood['x'].append(xPos)
			self.initFood['y'].append(yPos)

	# Refills food sources
	def spawnFood(self):
		self.currentFood = self.initFood

	# Spawns the requested amount of leopards in random spots around the terrain
	def spawnPredators(self):
		for i in range(self.predatorsAmount):
			randomX = random.randint(0,self.width)
			randomY = random.randint(0,self.height)
			self.predators.append(Leopard(random.randint(8,10),randomX,randomY))

	# Spawns the requested amount of hunters in random spots around the terrain
	def spawnHunters(self):
		for i in range(self.huntersAmount):
			randomX = random.randint(0,self.width)
			randomY = random.randint(0,self.height)
			self.hunters.append(Hunter(random.randint(15,20),randomX,randomY))

	# Terrain Cycle: 
	def update(self):
		self.cycle += 1 # cycle count
		self.currentPopulation.append(len(self.individuals)) # to keep track of population size over time

		if self.cycle == 1:
			self.spawnFood()
		if self.cycle % 2 == 0:
			self.spawnFood() # Food refills every 2 cycles

		# Leopards (if any) move
		for leopard in self.predators:
			leopard.move(terrain.width,terrain.height)

		# Hunters (if any) move
		for hunter in self.hunters:
			hunter.move(terrain.width,terrain.height)

			# After a hunters kills an okapi, it takes 4 cycles to reset (cooldown)
			if self.cycle - hunter.lastHuntCycle == 4:
				hunter.isAvailableToHunt = True

		# Okapis move, reproduce and can be hunted
		for individual in self.individuals:
			individual.move(terrain.width,terrain.height)

			# If food is near, the okapi eats it
			foodX,foodY = individual.eatNearFood(self.currentFood)

			# Death chances increase by excess weight
			if individual.weight in range(250,300):
				individual.deathFactor += random.randint(0,1)
			if individual.weight in range(300,325):
				individual.deathFactor += 1
			if individual.weight in range(325,350):
				individual.deathFactor += 2
			if individual.weight in range(350,400):
				individual.deathFactor += 10
			if individual.weight >= 400:
				individual.deathFactor += 50

			individualKilled = False

			# Check if a hunter is able to shoot (hunt every 3 cycles) an Okapi if it is in the gun range
			if self.huntersAmount != 0:
				for hunter in self.hunters:
					if hunter.isAvailableToHunt:
						huntXRange = range(hunter.xPos-hunter.gunRange,hunter.xPos+hunter.gunRange+1)
						huntYRange = range(hunter.yPos-hunter.gunRange,hunter.yPos+hunter.gunRange+1)

						if (individual.xPos in huntXRange and individual.yPos in huntYRange):
							# death by a hunter
							if individual in self.individuals:
								self.individuals.remove(individual)
							self.totalDeaths += 1 # to keep track of deaths
							individualKilled = True
							hunter.lastHuntCycle = self.cycle
							hunter.isAvailableToHunt = False

			# Check if a leopard is near enough to eat an okapi
			if self.predatorsAmount != 0:
				if not individualKilled:
					for leopard in self.predators:
						# Leopard eating range depends on its speed
						leopardXRange = range(leopard.xPos-leopard.speed,leopard.xPos+leopard.speed+1)
						leopardYRange = range(leopard.yPos-leopard.speed,leopard.yPos+leopard.speed+1)

						if (individual.xPos in leopardXRange and individual.yPos in leopardYRange):
							# death by leopard
							if individualKilled == False:
								self.individuals.remove(individual)
								self.totalDeaths += 1 # to keep track of deaths
								individualKilled = True
								leopard.xPos = individual.xPos
								leopard.yPos = individual.yPos

			# Chance of death depending on deathFactor (natural cause) if not killed by a predator
			if not individualKilled:
				probabilityFactor = random.randint(1,1000)
				if probabilityFactor <= individual.deathFactor: 
					# death by natural chances (influenced by excess weight or not enough food)
					self.individuals.remove(individual)
					individualKilled = True
					self.totalDeaths += 1

			if not individualKilled:
				# Chance for reproduction depending on rFactor
				probabilityFactor = random.randint(1,1000)
				if probabilityFactor <= individual.rFactor: 
					# successful reproduction, child spawns near
					self.individuals.append(Okapi(1,200,initReplicationFactor,initDeathFactor,individual.xPos,individual.yPos))
					self.totalBirths += 1


# Useful function to print the main statistics for a data set
def printStats(data):
	print('MAX:\t{}'.format(max(data)))
	print('MIN:\t{}'.format(min(data)))
	print('MEAN:\t{}'.format(np.mean(data)))
	print('MEDIAN:\t{}'.format(np.median(data)))
	print('MODE:\t{}'.format(stats.mode(data)[0][0]))
	print('STD:\t{}'.format(np.std(data)))

# Global function that plots and draws all the data in a plane (GUI)
def animate(frame,terrain):
	global animationCycle, allSpeeds, allWeights
	cycleSpeeds = []
	cycleWeights = []
	
	# Arrays to plot data
	xs = []
	ys = []
	leopardXs = []
	leopardYs = []
	huntersXs = []
	huntersYs = []
	huntersHeads = []
	huntersArms = []

	# Anchor points to zoom out the graph
	terrainXs = [-5,terrain.width+5,terrain.width+5,-5,-5] 
	terrainYs = [-5,-5,terrain.height+5,terrain.height+5,-5]
	
	for individual in terrain.individuals:
		xs.append(individual.xPos)
		ys.append(individual.yPos)
		cycleSpeeds.append(individual.speed)
		cycleWeights.append(individual.weight)
	allSpeeds.append(cycleSpeeds)
	allWeights.append(cycleWeights)

	for leopard in terrain.predators:
		leopardXs.append(leopard.xPos)
		leopardYs.append(leopard.yPos)

	for hunter in terrain.hunters:
		huntersXs.append(hunter.xPos)
		huntersYs.append(hunter.yPos)
		huntersHeads.append(hunter.yPos+5)
		huntersArms.append(hunter.yPos+2)

	# clear previous graphed data and update the title display
	plt.cla()
	plt.title('Cycle: {}\n[ Alive: {} ] [ Births: {} ] [ Deaths: {} ]'.format(
		terrain.cycle,
		len(terrain.individuals),
		terrain.totalBirths,
		terrain.totalDeaths),
	fontsize=10,
	loc='left')

	# Anchor points for terrain visual
	plt.plot(terrainXs,terrainYs,color='#000000',alpha=0.0)

	# Animals
	plt.scatter(xs,ys,c='#352510',marker='1',s=75)

	# Predators
	plt.scatter(leopardXs,leopardYs,c='#bf891d',marker='v',s=70,alpha=0.9,linewidths=0.2,edgecolors='#bf891d')

	# Hunters
	plt.scatter(huntersXs,huntersYs,c='#05336e',marker='2',s=60,alpha=0.8)
	plt.scatter(huntersXs,huntersHeads,c='#05336e',marker='.',s=50,alpha=0.8)
	plt.scatter(huntersXs,huntersArms,c='#05336e',marker='_',s=30,alpha=0.8)

	# Vegetation
	plt.scatter(terrain.vegetation['x'],terrain.vegetation['woodYs'],c='#47361E',marker='|',s=120)
	plt.scatter(terrain.vegetation['x'],terrain.vegetation['y'],c='#145A32',marker='^',s=120,linewidths=1,edgecolors='#1D8348')

	# Food
	plt.scatter(terrain.currentFood['x'],terrain.currentFood['y'],c='#27AE60',marker='d',s=5,linewidths=0.3,edgecolors='#00461D')

	terrain.update() # all information of the simulation updates

	if terrain.cycle == terrain.endCycle:
		animationCycle.event_source.stop()
		plt.close()

# Global function that draws the final results animated (GUI)
def animateFinal(i):
	global finalAnimationCycle, allSpeeds, allWeights, allPopulations, indexes, cont, fig, axs, ax1Anchors, ax2Anchors, color

	# clear previous graphed data and update the title display
	axs[0].cla()
	axs[1].cla()

	# Traits evolution graph
	axs[0].set_title('Speeds vs. Weights')
	axs[0].set_xlabel('Speed (unit/cycle)')
	axs[0].set_ylabel('Weight (kg)')

	# Population over time graph
	axs[1].set_title('Cycle vs. Population')
	axs[1].set_xlabel('Cycle')
	axs[1].set_ylabel('Population')

	# Plot anchor points
	axs[0].scatter(ax1Anchors['x'],ax1Anchors['y'],c='#000000',alpha=0.0)
	axs[1].scatter(ax2Anchors['x'],ax2Anchors['y'],c='#000000',alpha=0.0)

	# Plot the data
	axs[0].scatter(allSpeeds[cont],allWeights[cont],c=color,marker='.',s=100,alpha=0.2)
	axs[1].fill_between(indexes[0:cont+1],allPopulations[0:cont+1],0,color=color,alpha=0.5)

	if cont == (len(allSpeeds)-1):
		finalAnimationCycle.event_source.stop()
	else:
		cont += 1


# Simulator  ---------------------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('okapis',help='Number of Okapis to spawn.')
parser.add_argument('trees',help='Number of trees to spawn.')
parser.add_argument('predators',help='Number of predators to spawn.')
parser.add_argument('hunters',help='Number of hunters to spawn.')
parser.add_argument('endCycle',help='Number cycles to simulate.')
args = parser.parse_args()

print("\n    O K A P I   S I M  1.0")
print("\n|| Building terrain...")
terrain = Terrain(200,200,int(args.okapis),int(args.trees),int(args.predators),int(args.hunters),int(args.endCycle))
print("\n|| Terrain laid out...")
allSpeeds = []
allWeights = []
print("\n|| Stating simulation...")

#plt.style.use('fivethirtyeight')

# Simulation starts until stopped
animationCycle = FuncAnimation(plt.gcf(),animate,fargs=[terrain],interval=1,cache_frame_data=False)

print("\n|| Simulation running...")

# GUI customization
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)
ax = plt.gca()
ax.set_facecolor('#229954')
fig = plt.gcf()
fig.canvas.set_window_title('OKAPI Simulator')

plt.show()
print("\n|| Simulation ended.")

# Final Results ------------------------------------------------------------------

# To display the trais from the final population
indexes = []
allPopulations = terrain.currentPopulation

for i in range(0,terrain.cycle):
	indexes.append(i+1)

plt.style.use('dark_background')
fig,axs = plt.subplots(2, constrained_layout=True)

fig.suptitle('Simulation Results\n[Input] Okapis: {}    Trees: {}    Predators: {}    Hunters: {}'.format(args.okapis,args.trees,args.predators,args.hunters),fontsize=12)
fig.canvas.set_window_title('OKAPI Simulator')

# Anchor points to help the display of the plots
ax1Anchors = {
'x':[0,6,0,6],
'y':[0,0,400,400]
}

ax2Anchors = {
'x':[0,max(indexes),0,max(indexes)],
'y':[0,0,max(allPopulations),max(allPopulations)]
}

cont = 0
# Color mapping for final plots
if len(terrain.individuals) == 0:
	color = '#ff201c' # if extinct sets a red color on final results plots
if len(terrain.individuals) in range(1,int(args.okapis)):
	color = '#ffe600' # final population less than init population, sets a yellow warning color on final results plots
if len(terrain.individuals) >= int(args.okapis):
	color = '#3AFF00' # final population greater than init population, sets a green color
	
finalAnimationCycle = FuncAnimation(plt.gcf(),animateFinal,interval=1,cache_frame_data=False)

print("\n|| Final Stats:")
finalSpeeds = []
finalWeights = []

for okapi in terrain.individuals:
	finalSpeeds.append(okapi.speed)
	finalWeights.append(okapi.weight)

if len(terrain.individuals) != 0:
	print('__________________________________________________\n\t    Final Speeds')
	printStats(finalSpeeds)
	print('\n__________________________________________________\n\t    Final Weights')
	printStats(finalWeights)
else:
	print('\n\t Species EXTINCT')

print('\n__________________________________________________\n\t    Population Stats')
print(' ALIVE:   {}\n DEATHS:  {}\n BIRTHS:  {}'.format(len(terrain.individuals),terrain.totalDeaths,terrain.totalBirths))
print('__________________________________________________\n')

print("\n|| Showing final results via plot animation...")
plt.show()
print("\n|| Closed.")

print("\n|| OKAPISIM terminated.\n\n")

