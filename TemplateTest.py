

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



def load_image(path):
    'load an image from the data directory with per pixel alpha transparency.'
    return pygame.image.load(path).convert_alpha()

class SpaceShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = load_image("./SpaceShooterRedux/PNG/playerShip3_green.png")
        self.image = self.original_image

        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        
        self.yaw = 0
        self.yaw_change = 5
    def setPos(self,pos):
        self.rect[0] = pos[0]
        self.rect[1] = pos[1]
    
    def update(self):
        self.image = pygame.transform.rotate(self.original_image,self.yaw)     
    def rotate(self,angle):
        if angle > 0:
            self.yaw += self.yaw_change
        elif angle < 0:
            self.yaw -= self.yaw_change
        self.yaw = self.yaw % 360


def PosInMap(pos,gamemap):
    if pos[0] < 0 or pos [0] > gamemap[0] or pos[1] < 0 or pos[1] > gamemap[1]:
        return False
    return True
def HandleHmiMovementKeyPress(keys_pressed, pos,ship):
    if keys_pressed[K_LEFT] or keys_pressed[K_a]:
        tentative_next_pos = [pos[0]-vx,pos[1]]
        if PosInMap(tentative_next_pos, GRID_DIMS):
            pos[0] -= vx
        ship.rotate(-5)
    if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
        tentative_next_pos = [pos[0]+vx,pos[1]]
        if PosInMap(tentative_next_pos, GRID_DIMS):
            pos[0] += vx
        ship.rotate(5)
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
ship = SpaceShip()
sprites = pygame.sprite.RenderPlain(ship)
while not done:
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If user clicked close
            done=True
        if event.type == KEYDOWN:
            if event.key == K_q:
                done = True
    keysPressed = pygame.key.get_pressed()
    HandleHmiMovementKeyPress(keysPressed, pos,ship)
    ship.setPos(pos)

    screen.fill(WHITE)
    pygame.draw.circle(screen,BLUE,pos,6)
    ship.update()
    sprites.draw(screen)
    pygame.display.flip()
    clock.tick(20)

pygame.quit()




