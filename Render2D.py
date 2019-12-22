'''
A Pygame based renderer
takes in a numpy array and scales the screen display
'''

import pygame, sys
from pygame.locals import *
from MagicNumbers import *
import numpy as np
FPS = 30

class Render:
	def __init__(self, layer, showgrid=False, screendims=(640,480), caption="RL Renderer"):
		self.grid = layer.grid
		self.agent_pos = [3,0]
		self.grid[0][0] = 1
		# change this when we start adding multiple layers
		self.title = layer.name
		self.showgrid = showgrid

		#initialize pygame modules
		pygame.init()
		#is this redundant?
		pygame.font.init()

		self.FPSCLOCK = pygame.time.Clock()
		self.font = pygame.font.SysFont('arial', 20)
		self.size = screendims

		self.screen = pygame.display.set_mode(self.size)
		pygame.display.set_caption(self.title)

		self.isinstanceRunning = True
		self.pixelcord = [0,0]
		# gets the iamge surface, RL things!
		#ScreenImage = pygame.surfarray.array3d(pygame.display.get_surface())

	def display(self):
		self.screen.fill( WHITE )
		# Resolve screen size with grid size
		# May want boxes based on the smaller dimension 

		width, height = self.size
		numRow, numCol = self.grid.shape
		rowHeight = height // numRow
		colWidth = width // numCol
		# draw horizontal row lines
		for yCoord in range(0,height, rowHeight):
			pygame.draw.line(self.screen, BLACK, (0,yCoord),(width, yCoord))
		# draw verticle column lines
		for xCoord in range(0, width, colWidth):
			pygame.draw.line(self.screen, BLACK, (xCoord,0), (xCoord,height))

		#calculate center point to draw player
		centerPt = [colWidth * self.agent_pos[1] + colWidth//2,rowHeight * self.agent_pos[0] + rowHeight//2]
		self.pixelcord = centerPt
		pygame.draw.circle(self.screen, BLUE, centerPt, 25)
		pygame.display.flip()

	def HandleEvent(self):
		# rather than complex event management, we'll use this
		# until we need a dedicated event manager
		for event in pygame.event.get():
			if event.type == QUIT:
				self.Quit()
			elif event.type == KEYDOWN:
				if event.key in (K_w, K_UP):
					if self.agent_pos[0] - 1 < 0:
						print("pressed up, did nothing")
					else:
						self.agent_pos[0] -= 1 
				if event.key in (K_a, K_DOWN):
					if self.agent_pos[0] +1 >= self.grid.shape[0]:
						print("pressed down, did nothing")
					else:
						self.agent_pos[0] += 1
				if event.key in (K_s, K_LEFT):
					if self.agent_pos[1] - 1 < 0:
						print("pressed left, did nothing")
					else:
						self.agent_pos[1] -= 1
				if event.key in (K_d, K_RIGHT):
					#print(self.agent_pos, self.grid.shape[0])
					if self.agent_pos[1] +1 >= self.grid.shape[1]:
						print("pressed right, did nothing")
					else:
						self.agent_pos[1] += 1
				if event.key == K_q:
					self.Quit()
				self.grid = np.zeros(self.grid.shape)
				self.grid[self.agent_pos[0]][self.agent_pos[1]] = 1
				print(self.grid)
				print( self.agent_pos, self.grid.shape, self.pixelcord )
				
		self.FPSCLOCK.tick(60)
		self.display()
	# --- Below are class functions in descending order of perceived utility or use frequency
	def getRunning(self):
		return self.isinstanceRunning
	def Quit(self):
		self.isinstanceRunning = False
		pygame.display.quit()
		pygame.quit()
		sys.exit()
	def setTitle(self, newTitle):
		self.title = newTitle
		pygame.display.set_caption(self.title)