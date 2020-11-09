import pygame
from pygame.locals import *
import random
from math import atan2
import math
import numpy as np
from copy import deepcopy

from MagicNumbers import *
from GameUnits import *
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
def HandleHmiMovementKeyPress(keys_pressed, aSprite):
    if keys_pressed[K_LEFT] or keys_pressed[K_a]:
        aSprite.rotate(5)
    if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
        aSprite.rotate(-5)
    if keys_pressed[K_UP] or keys_pressed[K_w]:
        aSprite.move(1)
    if keys_pressed[K_DOWN] or keys_pressed[K_s]:
        aSprite.move(-1)

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

