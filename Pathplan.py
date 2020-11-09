import numpy as np
import heapq as hq
from math import sqrt
import sys
'''
A-star implementation sources:
http://csis.pace.edu/~benjamin/teaching/cs627/webfiles/Astar.pdf
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
'''

def IsInMap(aGameMap, aPos):
   w,h = aGameMap.shape
   if aPos[0] < 0 or aPos[0] >= w or aPos[1] < 0 or aPos[1] >= h:
       return False
   return True

def IsMoveValid(aGameMap,aCurrPos, aMove):
   
   w,h = aGameMap.shape
   aMove = tuple(aMove)
   newPos = aCurrPos + aMove
   if not IsInMap(aGameMap,newPos):
       return False
   if aGameMap[newPos[0]][newPos[1]] == 99:
       return False
   return True 

class Node:
    def __init__(self,parent,position):
        self.parent = parent
        self.position = position
        self.move = None        
        self.g = 0
        self.f = 0
        self.h = 0
    def __eq__(self,other):
        return list(self.position) == list(other.position)
    def __str__(self):
        return "["+str(self.position[0]) + "," + str(self.position[1]) + "]"
def HDistance(aGameMap,aStartPt,aGoalPt):
    '''
    Heuristic Distance, Manhattan Distance
    '''
    return (aGoalPt[1] - aStartPt[1])**2 + (aGoalPt[0] - aStartPt[0])**2

def generateFrontier(aGameMap, aPos,moves):
    '''
    generates points around current point on the map
    '''
    frontier_add = []
    for i in moves:
        newmove = aPos.position + i
        if IsMoveValid(aGameMap, aPos.position, i):
            newLoc = Node(aPos,newmove)
            newLoc.move = i
            frontier_add.append(newLoc)
    return frontier_add

def generatePathToGoalPt(aGameMap,aStartPt,aGoalPt):
    '''
    return -1 if the goal point is impossible 
    '''
    if not IsInMap(aGameMap,aGoalPt):
        return -1
    
    moves = np.array(
            [
                [0,-1],
                [0,1],
                [-1,0],
                [1,0]
            ]
                )
    start = Node(None,aStartPt)
    start.g = start.h = start.f = 0
    start.move = np.array([0,0]) 
    goal = Node(None,aGoalPt)
    goal.g = goal.h = goal.f = 0

    open_list = [start]
    closed_list = []

    goalFound = False
    while len(open_list)>0:
        current_node = open_list[0]
        current_index = 0

        # can do this with a heapq probably
        for idx,item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = idx

        open_list.pop(current_index)
        closed_list.append(current_node)
        
        if current_node == goal:
            path = []
            moves = []
            current = current_node
            while current is not None:
                path.append(current.position)
                moves.append(current.move)
                current = current.parent
            print("not reversing moves so pop() executes on the agent path")
            return path[::-1],moves
        #print("aGameMap", aGameMap)
        #print("current_node", current_node)
        children = generateFrontier(aGameMap, current_node,moves)
        #for i in children:
        #    print(i.position)
        #sys.exit(0)
        for child in children:

            childClosedFlag = False
            for closed_child in closed_list:
                if child == closed_child:
                    childClosedFlag = True
            if childClosedFlag:
                continue
            
            child.g = current_node.g + 1
            child.h = HDistance(aGameMap, child.position,goal.position)
            child.f = child.g + child.h

            openNodeFlag = False
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    openNodeFlag = True
            if openNodeFlag:
                continue
            open_list.append(child)
    return -1,-1

if __name__=='__main__':
    moves = np.array(
            [
                [0,-1],
                [0,1],
                [-1,0],
                [1,0]
            ]
                )

    gamemap = np.ones((10,10))
    startpos = np.array([1,1])
    goalpos = np.array([8,8])

    gamemap[4:9,4]=99
    gamemap[4,4:8]=99

    astarpath,moves = generatePathToGoalPt(gamemap,startpos,goalpos)
    done_map = np.zeros_like(gamemap)
    
    if astarpath == -1:
        print("no path, check inputs")
    else:
        for i in astarpath:
            done_map[i[0]][i[1]] = 4
        print(done_map)


