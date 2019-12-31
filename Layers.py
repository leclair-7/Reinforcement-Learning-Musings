'''
Defines Layers / tables
Q(s,a)
V(s)
Pi(s)
'''

import numpy as np

from LayerUtils import *
from MagicNumbers import *

class Layer:
	def __init__(self, grid = np.array([]), name="", defaultColor = (0,0,0) ):
		self.grid = grid
		if not len(name):
			raise EmptyLayerName
		self.name = name
	def getColor(self):
		return self.defaultColor
	def setColor(self, color):
		self.defaultColor = color

if __name__=='__main__':
	
	# ------------- Layer class examples --------------
	# this should fail
	# l = Layer()

	#intended use is dict = { "layername": layerObj,... }
	# agent will do things on each layer
	Q_init = np.zeros((3,3))

	Qlayer = Layer(Q_init, "Q(s,a)")
	ValueLayer = Layer(np.array([1]), "V(s)")
	PolicyLayer = Layer(np.array([1]), "Pi(s)")
	# ------------- End of Layer class examples --------------

