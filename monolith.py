
'''
A Pygame based renderer
takes in a numpy array and scales the screen display

2D visibility calculation is thanks to:
https://ncase.me/sight-and-light/

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

from math import sin, cos, sqrt, atan2, isclose, pi

FPS = 30


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

idx = 0

class Point:
    def __init__(self, ax, ay, T1=0):
        self.x = ax
        self.y = ay
        self.T1 = T1
class Ray:
    def __init__(self, a,b):
        #a is the reference position, b is mouse position
        self.a = Point(a[0], a[1])
        self.b = Point(b[0], b[1])


def getIntersection(ray, segment):
    point = None

    r_px = ray.a.x 
    r_py = ray.a.y
    r_dx = ray.b.x - ray.a.x
    r_dy = ray.b.y - ray.a.y
    
    s_px = segment.a.x
    s_py = segment.a.y
    s_dx = segment.b.x - segment.a.x
    s_dy = segment.b.y - segment.a.y

    r_mag = sqrt(r_dx * r_dx + r_dy * r_dy)
    s_mag = sqrt(s_dx * s_dx + s_dy * s_dy)

    if (r_dx/r_mag==s_dx/s_mag and r_dy/s_mag==s_dy/s_mag):
        return None
    T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)
    T1 = (s_px+s_dx*T2-r_px)/r_dx
    
    if T1<0:
        return None
    if T2 < 0 or T2 > 1:
        return None
    return Point(r_px+r_dx*T1,r_py+r_dy*T1,T1)



    return point
def display(showgrid=False, pos=[0,0]):
    # Resolve screen size with grid size
    # May want boxes based on the smaller dimension 
    # start centerpoint, decide based on showgrid
    screen.fill( WHITE )
    
    #used to keep collision frame count
    global idx
    
    q,w,e,r = [400, 100, 25, 250]
    a11,b11,c11,d11 = rectStartFinish(q,w,e,r)
    rect_init_coords = [400, 100, 25, 250]
    a = pygame.draw.rect(screen, GREY, rect_init_coords)
    
    #getting mouse 
    # rp - reference position
    rp = np.array(SIZE)//2
    reference_point = pygame.draw.circle(screen, RED, rp, 5)
    
    #2D Visibility calculation tests
    w,h = SIZE
    mapPolyLineSeg = ( (int(w*4/20), int(h*2/11)),
                     (int(w*3/20), int(h*5/11)),
                     (int(w*5/20), int(h*7/11)),
                     (int(w*6/20), int(h*1/11)),
                     (int(w*7/20), int(h*6/11)),
                     (int(w*9/20), int(h*7/11)),
                     (int(w*12/20), int(h*10/11)),
                     (int(w*6/20), int(h*9/11)) 
                    )
    lines_arr = []
    shapeSegPts = []
    segments = []
    for i in range(len(mapPolyLineSeg)):
        line, lineSeg = None, None 
        if i %4 == 3:
            lineSeg = [mapPolyLineSeg[i],  mapPolyLineSeg[i-3] ]
            line = pygame.draw.line(screen, GREY,mapPolyLineSeg[i], mapPolyLineSeg[i-3] ,1)
            segments.append(Ray(mapPolyLineSeg[i], mapPolyLineSeg[i-3]))
        else:
            lineSeg = [mapPolyLineSeg[i],  mapPolyLineSeg[i+1] ]
            line = pygame.draw.line(screen, GREY,mapPolyLineSeg[i], mapPolyLineSeg[i+1] ,1 )
            segments.append(Ray(mapPolyLineSeg[i], mapPolyLineSeg[i+1]))
        lines_arr.append(line)
        shapeSegPts.append(lineSeg)

    # 1 get ray x,y 
    pos = pygame.mouse.get_pos()
    b = pygame.draw.circle(screen, BLUE, pos, 4)

    ray = Ray(rp, pos)
    # rp - reference map position

    closestIntersect = None
    for segment in segments:
        intersect =  getIntersection(ray, segment)
        if not intersect:    
            continue
        if (not closestIntersect or intersect.T1 < closestIntersect.T1):
            closestIntersect = intersect

    if closestIntersect:
        pygame.draw.line(screen, GREEN, rp, (int(closestIntersect.x), int(closestIntersect.y)), 1 )
    else:
        pygame.draw.line(screen, GREEN, rp, pos, 1 )
        

    # theta is between mouse pos and the reference position
    '''
    theta = atan2( (pos[1] - r_py), (pos[0] - r_px) )
    r_dx = cos(theta)
    r_dy = sin(theta)
    T1 =  sqrt( (pos[0] - r_px)**2 + (pos[1] - r_py)**2)
    '''
    '''
    angle_deg = theta * 180/pi
    print("Angle in deg: ", angle_deg)
    #print(pos )
    # 2 loop through all segment points, get segment x,y
    anX, anY = rp
    dot = [r_px + r_dx * T1, r_py + r_dy * T1]
    lowestT1 = T1
    for i in shapeSegPts:
        dst, src = i[0], i[1]
        s_px, s_py = src
        beta = atan2( (dst[1]-src[1]),(dst[0]-src[0]) )
        s_dx = cos(beta)
        s_dy = sin(beta)

        # check for parallel lines, placeholder
        if False:
            pass
        # otherwise, we have an intersection
        else:
            T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)
            T1 = (s_px+s_dx*T2-r_px)/r_dx
            #print(T1, T2)
            if T1 < 0:
                continue
            if (T2 < 0 or T2 > 1):
                continue
            #Intersection
            idx += 1
            print("Intersection found!!!", idx)
            #lowestT1 = min(T1, lowe cstT1)
            if abs(T1) < abs(lowestT1):
                lowestT1 = T1
    dot = [r_px + r_dx * lowestT1, r_py + r_dy * lowestT1]
    dot = [min(SIZE[0], dot[0]), min(SIZE[1], dot[1])]
    dot = list(map(int, dot))
    '''
    #pygame.draw.line(screen, GREEN, rp, dot, 1 )

    #solve for T1, T2

    rect_store = [a]     
    #pygame.draw.line(screen, BLUE, pos, rp, 3)
    '''
    for game_wall in rect_store:
        if b.colliderect(game_wall):
            idx += 1
            print("Denver we have a collision", idx)
    '''
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
