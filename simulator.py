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

# Constants
initRFactor = 0.3

class Okapi:

    def __init__(self,id,rFactor,xPos,yPos):
        self.id = id
        self.rFactor = rFactor
        self.xPos = xPos
        self.yPos = yPos


class Terrein:

	individuals = []

	def __init__(self,height,width,amount):
		self.height = height
		self.width = width
		self.generateInitPopulation(amount)

	def generateInitPopulation(self,amount):
		for id in  range(amount):
			randomX = random.randint(0,self.width+1)
			randomY = random.randint(0,self.height+1)
			self.individuals.append(Okapi(id+1,initRFactor,randomX,randomY))

	def printData(self):
		print('Dimensions X:{} Y:{}\n'.format(self.width,self.height))
		for individual in self.individuals:
			print('ID:{} \tX:{} \tY:{} \trFactor:{} \tData:{}'.format(individual.id,individual.xPos,individual.yPos,individual.rFactor,individual))


# Simulator
terrein = Terrein(400,400,50)
terrein.printData()





