

import pygame
from pygame.locals import *
import random
 
# Define some colors
BLACK    = (   0,   0,   0)  
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)  

from MagicNumbers import *
pygame.init()
 
# Set the height and width of the screen
screen_width = 700 
screen_height = 400 
GRID_DIMS = (screen_width,screen_height)
screen = pygame.display.set_mode([screen_width, screen_height])
clock = pygame.time.Clock()

def PosInMap(pos,gamemap):
    if pos[0] < 0 or pos [0] > gamemap[0] or pos[1] < 0 or pos[1] > gamemap[1]:
        return False
    return True
def HandleHmiMovementKeyPress(keys_pressed, pos):
    if keys_pressed[K_LEFT] or keys_pressed[K_a]:
        tentative_next_pos = [pos[0]-vx,pos[1]]
        if PosInMap(tentative_next_pos, GRID_DIMS):
            pos[0] -= vx
    if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
        tentative_next_pos = [pos[0]+vx,pos[1]]
        if PosInMap(tentative_next_pos, GRID_DIMS):
            pos[0] += vx
    if keys_pressed[K_UP] or keys_pressed[K_w]:
        tentative_next_pos = [pos[0],pos[1]-vy]
        if PosInMap(tentative_next_pos, GRID_DIMS):
            pos[1] -= vy
    if keys_pressed[K_DOWN] or keys_pressed[K_s]:
        tentative_next_pos = [pos[0],pos[1]+vy]
        if PosInMap(tentative_next_pos, GRID_DIMS):
            pos[1] += vy


done = False
pos = [screen_width//2,screen_height//2]
vx,vy = 5,5
while not done:
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If user clicked close
            done=True
    
    keysPressed = pygame.key.get_pressed()
    HandleHmiMovementKeyPress(keysPressed, pos)
    
    screen.fill(BLACK)
    pygame.draw.circle(screen,BLUE,pos,6)

    pygame.display.flip()
    clock.tick(20)

pygame.quit()




