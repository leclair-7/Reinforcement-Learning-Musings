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

#initialize pygame modules
pygame.init()
#is this redundant?
pygame.font.init()

FPSCLOCK = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)
hitsurf = font.render("Hit!!! Oops!!", 1, (255,255,255))

screen = pygame.display.set_mode(SIZE)
title = "Control, then switch controllers via argparse"
pygame.display.set_caption(title)

parser = argparse.ArgumentParser()
parser.add_argument("--showgrid",help="represent game map as a grid such as 4x4", action='store_true')
args = parser.parse_args()

showgrid = args.showgrid

'''
Change settings; set vars based on args
'''
vx, vy = 1, 1
pos = [0,0]
gamemap = np.zeros(GRID_DIMS)
costmap = np.zeros(GRID_DIMS)
horizontal_block_step = WIDTH // GRID_DIMS[0]
vertical_block_step = HEIGHT // GRID_DIMS[1]

if showgrid:
    horizontal_block_step = WIDTH // GRID_DIMS[0]
    vertical_block_step = HEIGHT // GRID_DIMS[1]
    #vx,vy = horizontal_block_step, vertical_block_step
    horiz_half_step, vert_half_step = int(horizontal_block_step * .5), int(vertical_block_step * .5)
else:
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

def display(pos,showgrid=False):
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
    if showgrid and PosInMap(pos):
        pospx = [horizontal_block_step * pos[0] + horiz_half_step,vertical_block_step * pos[1] + vert_half_step] 
        print(pospx)
        pygame.draw.circle(screen,RED,pospx,4)
    elif PosInMap(pos):
        pospx = pos
        pygame.draw.circle(screen,RED,pospx,4)
    else:
        print("pos not in map")
    '''    
    pygame.draw.polygon(screen, RED, [pt, pt2, pos])
    pygame.draw.polygon(screen, GREY, [pt, pt2, pos],1)
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
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                Quit()
            elif event.type == KEYDOWN:                
                if event.key == K_q:
                    Quit()
            elif event.type == KEYUP:
                velx, vely = 0,0
        keys_pressed = pygame.key.get_pressed()
        
        if keys_pressed[K_ESCAPE]:
            Quit()
        HandleHmiMovementKeyPress(keys_pressed, pos,showgrid)
                
        #it gets covered by the 2-D visibility
        
        # a is rectangle, b is circle for position
        b = display(pos,showgrid)
        #print(pos)
        FPSCLOCK.tick(FPS)
