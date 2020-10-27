import numpy as np

class Agent:
    '''
    eventually we want to give the control interface as a dictionary-esque to set a member
    '''
    def __init__(self,pos,movesmap):
        self.moves_map = movesmap
        self.pos = pos
        self.path = None
        self.moves = None
    def move(self,move):
        self.pos = self.pos + move
    def setPath(self,path,moves):
        self.path = path
        self.moves = moves
    def run_step(self):
        if self.moves:
            self.pos += self.moves.pop()
        
        # reset if the moves is the last element on the list
        if self.moves == None:
            self.path = None
        if isinstance(self.moves,list) and len(self.moves) == 0:
            self.path = None

            



