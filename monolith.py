
'''
A Pygame based renderer
takes in a numpy array and scales the screen display
'''
'''
class Balloon(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initializer
        self.image, self.rect = pygame.image.load("balloon.png")
        self.mask = pygame.mask.from_surface(self.image)
b1 = Balloon()
b2 = Balloon()

if pygame.sprite.spritecollide(b1, b2, False, pygame.sprite.collide_mask):
    print("sprites have collided!")
'''

import pygame, sys
from pygame.locals import *
from MagicNumbers import *
import numpy as np
import pygame.sprite

FPS = 60


SIZE = (640,480)
grid = np.zeros(SIZE)

# change this when we start adding multiple layers
title = "Scene"

#initialize pygame modules
pygame.init()
#is this redundant?
pygame.font.init()

FPSCLOCK = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)
hitsurf = font.render("Hit!!! Oops!!", 1, (255,255,255))

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(title)

# gets the iamge surface, RL things!
#ScreenImage = pygame.surfarray.array3d(pygame.display.get_surface())
pos = np.array( [ 100, 100 ])

# for masks
last_bx, last_by = 0,0

aas = False
def Quit():
    pygame.display.quit()
    pygame.quit()
    sys.exit()
def rectStartFinish(px, py, width, height):
    # for now, we'll return same side long edge
    h = [0,0,0,0]
    if height >= width:
        h = [px, py, px, py + height]
    else:
        h = [px, py, px + width, py]
    return h

def pointsToRectEdge(pos,edge1, edge2, testpoint ):

    '''
    2 Things we need for this:
        - angle from the pos to edge value to color the coords to it
        - line from pos to edge
            a. we'll loop from minx, miny to maxx, maxy

    # stupid line thing:
    posx, posy ------- ex, ey
    suppose
    0,4 -- 4,0
    y-y1 = m(x-x1)

    y = -1/4x + 4

    y-4= m(x-0)
    m = (y2-y1)/x2-x1
    y = mx - mx1 + y1
    y = -1/4x + 0 + 4 

    1 >= -1/4 * 1 + 4 (which is False)
    '''

    #edge1 is bottom, edge2 is the top
    assert( edge1[1] < edge2[1])
    x,y = pos
    e1x,e1y = edge1
    e2x,e2y = edge2
    mPosToE1 = (e1y-y)/(e1x-x)
    mPosToE2 = (e2y-y)/(e2x-x)
    m1, b1 = mPosToE1, (mPosToE1 * x + y)
    m2, b2 = mPosToE2, (mPosToE2 * x + y)

    assert( len(testpoint) == 2)
    tx, ty = testpoint

    lowerTest = ty >= mPosToE1 * tx + b1
    upperTest = ty <= mPosToE2 * tx + b2
    # should be >= segment 1 and should be <= segment 2

    return lowerTest and upperTest

def display(showgrid=False, pos=[0,0]):
    # Resolve screen size with grid size
    # May want boxes based on the smaller dimension 
    # start centerpoint, decide based on showgrid
    screen.fill( WHITE )
    pos = (pos[0], pos[1])
    
    # proves we can write pixels for viewshed on the 
    # game surface
    global aas
    if not aas:
        aas = True
        #print(dir(screen))

    q,w,e,r = [400, 100, 25, 250]
    a11,b11,c11,d11 = rectStartFinish(q,w,e,r)
    rect_init_coords = [400, 100, 25, 250]
    a = pygame.draw.rect(screen, BLACK, rect_init_coords)

    # ToDo put an angled rectangle here (and make a function to do so)
    # maybe startpoint, thickness, angle, put in the rectangles array
    #
    # a = pygame.draw.polygon(screen, BLACK, (()  ) )

    #very fragile, make robust for y == y case (for example)
    top = [a11,b11]
    bottom = [c11,d11]
    pygame.draw.polygon(screen, LIGHTGREEN, (pos, top, bottom) )
    pygame.draw.line(screen, YELLOW, pos, top, 3)
    pygame.draw.line(screen, YELLOW, pos, bottom, 3)


    b = pygame.draw.circle(screen, BLUE, pos, 25)
    if a.colliderect(b):
        print("Denver we have a collision")
    pygame.display.flip()
    return a, b

vx, vy = 5, 5
aPrev, bPrev = None, None
if __name__=='__main__':
    # rather than complex event management, we'll use this
    # until we need a dedicated event manager
    while True:
        for event in pygame.event.get():
            #self.eventHandle(event)
            if event.type == QUIT:
                Quit()
            elif event.type == KEYDOWN:                
                if event.key == K_q:
                    Quit()
            elif event.type == KEYUP:
                velx, vely = 0,0
        keys_pressed = pygame.key.get_pressed()
        spritex, spritey = pos[0], pos[1]
        if keys_pressed[K_LEFT] or keys_pressed[K_a]:
            spritex -= 5
        if keys_pressed[K_RIGHT] or keys_pressed[K_d]:
            spritex += 5
        if keys_pressed[K_UP] or keys_pressed[K_w]:
            spritey -= 5
        if keys_pressed[K_DOWN] or keys_pressed[K_s]:
            spritey += 5
        pos[0] = spritex
        pos[1] = spritey

        # a is rectangle, b is circle for position
        a, b = display(pos=pos)
        aPrev, bPrev = a, b

        FPSCLOCK.tick(FPS)
