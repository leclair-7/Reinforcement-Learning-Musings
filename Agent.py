import numpy as np

class Agent:
    '''
    eventually we want to give the control interface as a dictionary-esque to set a member
    '''
    def __init__(self,pos,movesmap,gamemap):
        self.moves_map = movesmap
        self.pos = pos
        self.path = None
        self.moves = None
        self.gamemap = gamemap
    
    def move(self,move):
        self.pos = self.pos + move
    
    def setPath(self,path,moves):
        self.path = path
        self.moves = moves
    
    def PosInMap(self,pos):
        if pos[0] < 0 or pos[0] >=len(self.gamemap[0]) or pos[1] < 0 or pos[1] >= len(self.gamemap[1]):
            return False
        return True

    def run_step(self):
        '''
        if the agent has a path, take the next step per frame
        this is called in the gameloop concept of the game run lifecycle
        '''
        if self.moves:
            nextstep = self.moves.pop()
            if self.PosInMap(self.pos+nextstep):
                self.pos += nextstep
        
        # reset if the moves is the last element on the list
        if self.moves == None:
            self.path = None
        if isinstance(self.moves,list) and len(self.moves) == 0:
            self.path = None

            



