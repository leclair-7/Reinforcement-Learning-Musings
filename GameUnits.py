import pygame
import math
from MagicNumbers import *

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
        
        self.velocity = 5
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



