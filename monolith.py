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

from math import sin, cos, sqrt, atan2, isclose, pi

FPS = 30

SIZE = (640,480)
# change this when we start adding multiple layers
title = "Test Scene"

#initialize pygame modules
pygame.init()
#is this redundant?
pygame.font.init()

FPSCLOCK = pygame.time.Clock()
font = pygame.font.SysFont('arial', 20)
hitsurf = font.render("Hit!!! Oops!!", 1, (255,255,255))

screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption(title)

# gets the image surface, RL things!
#ScreenImage = pygame.surfarray.array3d(pygame.display.get_surface())

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
class Point:
    def __init__(self, ax, ay, angle = 0, T1=0):
        self.x = ax
        self.y = ay
        self.T1 = T1
        self.angle = angle
    def __str__(self):
        return "Point: " + str(self.x) + " " + str(self.y)
class Ray:
    def __init__(self, a,b):
        #a is the reference position, b is mouse position
        self.a = Point(a[0], a[1])
        self.b = Point(b[0], b[1])
    def __str__(self):
        return "Point a: (" + str(self.a.x)+ ", " + str(self.a.y) + ") " + \
               "Point b: (" + str(self.b.x)+ ", " + str(self.b.y) + ") "
class LinePointAndAngle:
    def __init__(self, lp0, lp1):
        self.lp0 = lp0
        self.lp1 = lp1
        self.angle = atan2(lp1[1]-lp0[1], lp1[0] - lp1[0])
def getIntersection(ray, segment):
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
    if isclose( (s_dx*r_dy - s_dy*r_dx),0) or isclose(r_dx, 0):
        return None

    T2 = (r_dx*(s_py-r_py) + r_dy*(r_px-s_px))/(s_dx*r_dy - s_dy*r_dx)
    T1 = (s_px+s_dx*T2-r_px)/r_dx
    
    if T1<0:
        return None
    if T2 < 0 or T2 > 1:
        return None
    aPx, aPy = r_px+r_dx*T1,r_py+r_dy*T1
    angle = atan2( aPy - r_py, aPx - r_px)
    return Point(r_px+r_dx*T1,r_py+r_dy*T1,angle,T1)
def display(showgrid=False, pos=[0,0]):
    '''
    A test function for visualization features
    The intent is to test features that will become agent layers here 
    '''
    screen.fill( WHITE )
    
    # rp - reference position
    rp = np.array(SIZE)//2
    
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
    segments = []
    #draw all line segments for the shapes/polygons
    for i in range(len(mapPolyLineSeg)):
        line = None
        if i %4 == 3:
            line = pygame.draw.line(screen, GREY,mapPolyLineSeg[i], mapPolyLineSeg[i-3] ,1)
            segments.append(Ray(mapPolyLineSeg[i], mapPolyLineSeg[i-3]))
        else:
            line = pygame.draw.line(screen, GREY,mapPolyLineSeg[i], mapPolyLineSeg[i+1] ,1 )
            segments.append(Ray(mapPolyLineSeg[i], mapPolyLineSeg[i+1]))
    pos = pygame.mouse.get_pos()
    b = pygame.draw.circle(screen, BLUE, pos, 4)

    MPosToCornerRays = []
    uniquePoints = []
    for segment in segments:
        for seg in [segment.a, segment.b]:
            MPosToCornerRays.append( Ray(pos, (seg.x, seg.y) ) )
            uniquePoints.append( (seg.x, seg.y) )
    # project this to either closest edge or to the edge of the screen
    uniquePoints = list(set(uniquePoints))
    uniqueAngles = []
    for pt in uniquePoints:
        angle = atan2( pt[1] - pos[1], pt[0] - pos[0])
        uniqueAngles.extend( (angle - 0.00001, angle, angle + 0.00001) )

    LinePoints = []
    for ray in MPosToCornerRays:
        closestIntersect = None
        for segment in segments:
            intersect =  getIntersection(ray, segment)
            if not intersect:    
                continue
            if (not closestIntersect or intersect.T1 < closestIntersect.T1):
                closestIntersect = intersect
        if closestIntersect:
            LinePoints.append([ pos ,(int(closestIntersect.x), int(closestIntersect.y))])
        else:
            LinePoints.append([ pos , (ray.b.x, ray.b.y) ])
    for lp in LinePoints:
        pygame.draw.line(screen, GREEN, lp[0], lp[1], 1)     
    
    pygame.display.flip()
    return b

vx, vy = 5, 5
aPrev, bPrev = None, None
if __name__=='__main__':
    # rather than complex event management, we'll use this
    # until we need a dedicated event manager, then we'll despair
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
        b = display(pos=pos)
        

        FPSCLOCK.tick(FPS)
