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


showgrid = True

# change this when we start adding multiple layers
title = "Control, then switch controllers via argparse"

#initialize pygame modules
pygame.init()
#is this redundant?
pygame.font.init()

FPSCLOCK = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)
hitsurf = font.render("Hit!!! Oops!!", 1, (255,255,255))

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(title)

def Quit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()
def PosInMap(pos):
    if pos[0] < 0 or pos[0] > WIDTH or pos[1] < 0 or pos[1] > HEIGHT:
        return False
    return True

def display(pos,showgrid=False):
    '''
    A test function for visualization features
    The intent is to test features that will become agent layers here 
    '''
    screen.fill( WHITE )
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
    if PosInMap(pos):
        pygame.draw.circle(screen,RED,pos,4)
    else:
        print("pos not in map")
    '''    
    pygame.draw.polygon(screen, RED, [pt, pt2, pos])
    pygame.draw.polygon(screen, GREY, [pt, pt2, pos],1)
    '''
    pygame.display.flip()

vx, vy = 5, 5
if __name__=='__main__':
    
    pos = [0,0]
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
        spritex, spritey = pos[0], pos[1]
        if keys_pressed[K_ESCAPE]:
            Quit()
        if keys_pressed[K_LEFT] or keys_pressed[K_a]:
            spritex -= vx
        if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
            spritex += vx
        if keys_pressed[K_UP] or keys_pressed[K_w]:
            spritey -= vy
        if keys_pressed[K_DOWN] or keys_pressed[K_s]:
            spritey += vy
        
        pos = [spritex,spritey]
         
        #it gets covered by the 2-D visibility
        
        # a is rectangle, b is circle for position
        b = display(pos,showgrid)
        print(pos)
        FPSCLOCK.tick(FPS)
