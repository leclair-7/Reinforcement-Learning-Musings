'''
A Pygame based testing for new features of the game
takes in a numpy array and scales the screen display

2D visibility calculation is thanks to:
https://ncase.me/sight-and-light/
'''

import pygame, sys
from pygame.locals import *
from MagicNumbers import *
import numpy as np
import pygame.sprite
import argparse
from math import sin, cos, sqrt, atan2, isclose, pi
import sys
import Agent as agent

import pathplan as plan

parser = argparse.ArgumentParser()
parser.add_argument("--showgrid",help="represent game map as a grid such as 4x4", action='store_true')
args = parser.parse_args()

showgrid = args.showgrid

'''
Change settings; set vars based on args
'''
gamemap = np.ones(GRID_DIMS)
costmap = np.zeros(GRID_DIMS)
horizontal_block_step = WIDTH // GRID_DIMS[0]
vertical_block_step = HEIGHT // GRID_DIMS[1]

W = 0 
S = 1
G = 2
F = 3

TileColor = { W : BLUE,
              S : SANDYYELLOW,
              G : GRASSGREEN,
              F : FORESTGREEN
             }

TILESIZE = 40
tilemap = np.random.random( GRID_DIMS )
colorChoice = [W,S,G,F,W]
multiplier_prob = 1 / len(colorChoice)
for i,v in enumerate(colorChoice):
    tilemap= np.where( (tilemap< ( multiplier_prob * (i+1))), colorChoice[i],tilemap)
#print(tilemap)

#initialize pygame modules
pygame.init()
pygame.font.init()

FPSCLOCK = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)
hitsurf = font.render("Hit!!! Oops!!", 1, (255,255,255))


button = pygame.Rect(int(.1*WIDTH),int(.8*HEIGHT),200,50)

screen = None
if showgrid:
    screen = pygame.display.set_mode(SIZE)
else:
    WIDTH = GRID_DIMS[0]*TILESIZE  
    HEIGHT = GRID_DIMS[1]*TILESIZE  
    screen = pygame.display.set_mode((WIDTH,HEIGHT))
title = "Control, then switch controllers via argparse"
pygame.display.set_caption(title)


if showgrid:
    horizontal_block_step = WIDTH // GRID_DIMS[0]
    vertical_block_step = HEIGHT // GRID_DIMS[1]
    #vx,vy = horizontal_block_step, vertical_block_step
    horiz_half_step, vert_half_step = int(horizontal_block_step * .5), int(vertical_block_step * .5)
elif not showgrid:
    print("not showgrid")
    horizontal_block_step = (GRID_DIMS[0] * TILESIZE) // GRID_DIMS[0]
    vertical_block_step = (GRID_DIMS[1] * TILESIZE) // GRID_DIMS[1]
    #vx,vy = horizontal_block_step, vertical_block_step
    horiz_half_step, vert_half_step = int(horizontal_block_step * .5), int(vertical_block_step * .5)
else:
    # keeping a simple debug setting
    vx,vy = 5,5
def Quit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()
def PosInMap(pos,showgrid=False,grid_dims=None):
    if showgrid:
        if pos[0] < 0 or pos[0] >= grid_dims[0] or pos[1] < 0 or pos[1] >= grid_dims[1]:
            return False
    elif pos[0] < 0 or pos[0] > WIDTH or pos[1] < 0 or pos[1] > HEIGHT:
        return False
    return True

def display(robot,showgrid=False):
    '''
    A test function for visualization features
    The intent is to test features that will become agent layers here 
    '''
    screen.fill( WHITE )

    # if we passed show grid on initialization
    #GRID_DIMS
    if showgrid and GRID_DIMS[0] > 0 and GRID_DIMS[1] > 0:
        # rows
        idx_multiplier = HEIGHT//GRID_DIMS[0]
        pygame.draw.line(screen, BLUE, [0,0],[WIDTH,0], 4)
        for i in range(GRID_DIMS[0]):
            startpt = [0,i * idx_multiplier]
            endpt = [WIDTH,i * idx_multiplier]
            pygame.draw.line(screen, BLUE, startpt,endpt, 1)
        pygame.draw.line(screen, BLUE, [0,HEIGHT],[WIDTH,HEIGHT], 4)
        # columns
        idx_multiplier = WIDTH // GRID_DIMS[1]
        pygame.draw.line(screen, BLUE, [0,0],[0,HEIGHT], 4)
        for i in range(1,GRID_DIMS[1]):
            startpt = [i * idx_multiplier,0]
            endpt = [i * idx_multiplier,HEIGHT]
            pygame.draw.line(screen, BLUE, startpt,endpt, 1)
        pygame.draw.line(screen, BLUE, [WIDTH,0],[WIDTH,HEIGHT], 4)
    else:
        #color tiles
        for row in range(GRID_DIMS[0]):
            for col in range(GRID_DIMS[1]):
                pygame.draw.rect(screen,TileColor[tilemap[row][col]], (col*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE) )
    
    if robot.path != None:
        for rbox in robot.path:
            pygame.draw.rect(screen,LIGHTBLUE,(rbox[0] *TILESIZE,rbox[1]*TILESIZE,TILESIZE,TILESIZE))

    goalptpx = [horizontal_block_step * goalpt[0] + horiz_half_step, vertical_block_step * goalpt[1] + vert_half_step]
    #print(goalptpx)
    pygame.draw.circle(screen,BLACK,goalptpx,6)
     
    #print(horizontal_block_step, vertical_block_step,pos)
    if PosInMap(robot.pos):
        pospx = [horizontal_block_step * robot.pos[0] + horiz_half_step,vertical_block_step * robot.pos[1] + vert_half_step] 
        pygame.draw.circle(screen,RED,pospx,4)
    else:
        print("pos not in map")
    
    pygame.draw.rect(screen, [255, 0, 0], button)
    
    font = pygame.font.Font(None, 25)
    
    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf = font.render("Select Layer", True, BLACK)
    textRect = textSurf.get_rect()
    textRect.center = ( (int(.1*WIDTH)+(200//2)), (int(.8*HEIGHT)+(50//2)) )
    screen.blit(textSurf, textRect)
    '''
    text = font.render("You win!", True, BLACK)
    text_rect = text.get_rect(center=(int(.1*WIDTH) + 150//2 ,int(.8*HEIGHT) + 50//2 ))
    text_rect.center = (
    screen.blit(text, text_rect)
    '''
    pygame.display.flip()

def HandleHmiMovementKeyPress(keys_pressed, pos,showgrid):
    if keys_pressed[K_LEFT] or keys_pressed[K_a]:
        tentative_next_pos = [pos[0]-vx,pos[1]]
        if PosInMap(tentative_next_pos,showgrid, GRID_DIMS):
            pos[0] -= vx
    if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
        tentative_next_pos = [pos[0]+vx,pos[1]]
        if PosInMap(tentative_next_pos,showgrid, GRID_DIMS):
            pos[0] += vx
    if keys_pressed[K_UP] or keys_pressed[K_w]:
        tentative_next_pos = [pos[0],pos[1]-vy]
        if PosInMap(tentative_next_pos,showgrid, GRID_DIMS):
            pos[1] -= vy
    if keys_pressed[K_DOWN] or keys_pressed[K_s]:
        tentative_next_pos = [pos[0],pos[1]+vy]
        if PosInMap(tentative_next_pos,showgrid, GRID_DIMS):
            pos[1] += vy

if __name__=='__main__':
   
    #default velocity, more often than not it's number of graph fields per key press
    vx, vy = 1, 1
    robot = agent.Agent(np.array([0,0]),{})
    goalpt = np.array([8,4])
    checkpath,moves = plan.generatePathToGoalPt(gamemap,robot.pos,goalpt)
    robot.setPath(checkpath,moves)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                Quit()
            elif event.type == KEYDOWN:                
                if event.key == K_q:
                    Quit()
            elif event.type == MOUSEBUTTONDOWN:
                mousepos = event.pos
                if button.collidepoint(mousepos):
                    print("collided")
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[K_ESCAPE]:
            Quit()
        
        robot.run_step() 
        HandleHmiMovementKeyPress(keys_pressed, robot.pos,showgrid)
                
        #it gets covered by the 2-D visibility
        # a is rectangle, b is circle for position
        b = display(robot,showgrid)
        #print(pos)
        FPSCLOCK.tick(FPS)
