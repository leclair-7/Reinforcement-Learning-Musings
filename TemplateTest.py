

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
        
class Bullet(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self,angle):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([4, 10]).convert_alpha()
        self.original_image = self.image
        self.image.fill(BLACK)
 
        self.rect = self.image.get_rect()
        
        self.velocity = 3
        self.yaw = angle + 90
        self.mask = pygame.mask.from_surface(self.image)
    def update(self):
        """ Move the bullet. """
        yawRad = math.radians(self.yaw)
        self.rect.y -= int(self.velocity * math.sin(yawRad))
        self.rect.x += int(self.velocity * math.cos(yawRad))
        
        self.rotate_rect()
    
    def rotate_rect(self):
        self.image = pygame.transform.rotozoom(self.original_image, self.yaw-90,1)
        self.rect =  self.image.get_rect(center = self.rect.center)

class Block(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self, color):
        # Call the parent class (Sprite) constructor
        super().__init__()

        self.image = pygame.Surface([20, 15]).convert_alpha()
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)



def PosInMap(pos,gamemap):
    if pos[0] < 0 or pos [0] > gamemap[0] or pos[1] < 0 or pos[1] > gamemap[1]:
        return False
    return True
def HandleHmiMovementKeyPress(keys_pressed, ship):
    if keys_pressed[K_LEFT] or keys_pressed[K_a]:
        ship.rotate(5)
    if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
        ship.rotate(-5)
    if keys_pressed[K_UP] or keys_pressed[K_w]:
        ship.move(1)
    if keys_pressed[K_DOWN] or keys_pressed[K_s]:
        ship.move(-1)



# --- Sprite lists
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
 
# List of each block in the game
block_list = pygame.sprite.Group()
 
# List of each bullet
bullet_list = pygame.sprite.Group()

pos = [screen_width//2,int(.8*(screen_height)) ]
player = SpaceShip(pos)
all_sprites_list.add(player)


for i in range(50):
    # This represents a block
    block = Block(BLUE)

    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(350)

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If user clicked close
            done=True
        elif event.type == KEYDOWN:
            if event.key == K_q:
                done = True
        elif event.type == MOUSEBUTTONDOWN:
            bullet=Bullet(player.yaw)
            bullet.rect.x = player.rect.centerx
            bullet.rect.y = player.rect.centery
            all_sprites_list.add(bullet)
            bullet_list.add(bullet)
    keysPressed = pygame.key.get_pressed()
    HandleHmiMovementKeyPress(keysPressed, player)

    
    all_sprites_list.update() 
    
    for bullet in bullet_list:
        block_hit_list = pygame.sprite.spritecollide(bullet,block_list,True,pygame.sprite.collide_mask)
        for block in block_hit_list:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)

        if bullet.rect.y < -10:
            bullet_list.remove(bullet)
            all_sprites_list.remove(bullet)
    
    
    #clear screen
    screen.fill(WHITE)

    all_sprites_list.draw(screen)
    
    #update the screen 
    pygame.display.flip()
    clock.tick(20)

pygame.quit()




