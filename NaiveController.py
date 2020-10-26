
import random 

class RandomController:
	def __init__(self, actions = None):
            self.actions = actions
            self.actionTranslator = None
	def GetNextAction(self):
            if self.actionTranslator:
                return random.choice(self.actionTranslator.values())
            return random.choice(self.actions)
