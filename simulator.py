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

    	# terrein restrictions
    	if self.xPos < 0:
    		self.xPos = 1
    	if self.xPos > xMax:
    		self.xPos = xMax-1

    	if self.yPos < 0:
    		self.yPos = 1
    	if self.yPos > yMax:
    		self.yPos = yMax-1


class Terrein:

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
			individual.move(terrein.width,terrein.height)

	def printData(self):
		print('Dimensions X:{} Y:{}\n'.format(self.width,self.height))
		for individual in self.individuals:
			print('ID:{} \tX:{} \tY:{} \trFactor:{} \tData:{}'.format(individual.id,individual.xPos,individual.yPos,individual.rFactor,individual))

def animate(frame,terrein):
	terrein.update()
	xs = []
	ys = []
	terreinXs = [-3,terrein.width+3,terrein.width+3,-3,-3]
	terreinYs = [-3,-3,terrein.height+3,terrein.height+3,-3]
	
	for individual in terrein.individuals:
		xs.append(individual.xPos)
		ys.append(individual.yPos)

	plt.cla()
	plt.plot(terreinXs,terreinYs,color='#252525')
	plt.scatter(xs,ys,color='#FF7700')


# Simulator  ---------------------------------------------------------------------
print("\n    O K A P I   S I M  1.0")
print("\n|| Building terrein...")
terrein = Terrein(200,200,20)
print("\n|| Terrein laid out...")
print("\n|| Stating simulation...")
animationCycle = FuncAnimation(plt.gcf(),animate,fargs=[terrein],interval=100)

print("\n|| Simulation running...")
plt.tight_layout()
plt.gca().axes.get_xaxis().set_visible(False)
plt.gca().axes.get_yaxis().set_visible(False)

ax = plt.gca()
ax.set_facecolor('#252525')

plt.show()

print("\n||| Simulation ended.\n")

