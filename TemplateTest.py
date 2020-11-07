

import pygame
from pygame.locals import *
import random
from math import atan2
import math
import numpy as np
from copy import deepcopy
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

def load_image(path):
    'load an image from the data directory with per pixel alpha transparency.'
    return pygame.image.load(path).convert_alpha()

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self,pos):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = load_image("./SpaceShooterRedux/PNG/playerShip3_green.png")
        
        # required by pygame.sprite
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        self.mask = pygame.mask.from_surface(self.image)
        self.yaw =0 
        self.yaw_change = 5

        self.angle = 0
        self.oneDVel = 5
        self.velocity = [0,0]
        self.pos = pos

    def setVelocity(self,velocity):
        self.velocity = velocity
        
    def move(self,forwardOrBackward):
        '''
        self.pos  = [ round(self.pos[0] + self.velocity[0]), 
                      round(self.pos[1] + self.velocity[1]) 
                            ]
        if forwardOrBackward < 0:
            self.pos = [self.pos[0],self.pos[1]]
        '''
        self.pos  = [ 
                        round(self.pos[0] - forwardOrBackward * self.velocity[0]), 
                        round(self.pos[1] + forwardOrBackward * self.velocity[1]) 
                    ]
         
    def update(self):
        yawRadians = math.radians(self.yaw)
        self.velocity = [ 
                          self.oneDVel * math.sin(yawRadians),
                         -self.oneDVel * math.cos(yawRadians)
                        ]
        self.irotate()
    
    def irotate(self):
        self.image = pygame.transform.rotozoom(self.original_image, self.yaw, 1)
        self.rect = self.image.get_rect(center=self.pos)
    def rotate(self,angle):
        if angle > 0:
            self.yaw += self.yaw_change
        elif angle < 0:
            self.yaw -= self.yaw_change
        self.yaw = (self.yaw) % 360
        
def PosInMap(pos,gamemap):
    if pos[0] < 0 or pos [0] > gamemap[0] or pos[1] < 0 or pos[1] > gamemap[1]:
        return False
    return True
def HandleHmiMovementKeyPress(keys_pressed, ship):
    if keys_pressed[K_LEFT] or keys_pressed[K_a]:
        ship.rotate(-5)
    if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
        ship.rotate(5)
    if keys_pressed[K_UP] or keys_pressed[K_w]:
        ship.move(1)
    if keys_pressed[K_DOWN] or keys_pressed[K_s]:
        ship.move(-1)
done = False
pos = [screen_width//2,screen_height//2]
vx,vy = 5,5
ship = SpaceShip(pos)
sprites = pygame.sprite.RenderPlain(ship)
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If user clicked close
            done=True
        if event.type == KEYDOWN:
            if event.key == K_q:
                done = True
    keysPressed = pygame.key.get_pressed()
    HandleHmiMovementKeyPress(keysPressed, ship)
    #ship.setPos(pos)

    screen.fill(WHITE)
    pygame.draw.circle(screen,BLUE,pos,6)
    ship.update()
    sprites.draw(screen)
    print(ship.yaw)
    pygame.display.flip()
    clock.tick(20)

pygame.quit()




