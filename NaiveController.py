
import random 

class NaiveController:
	def __init__(self, actions = None):
		self.actions = actions
	def GetNextAction(self):
		return random.choice(self.actions)
