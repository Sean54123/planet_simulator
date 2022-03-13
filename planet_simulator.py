# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 19:32:13 2022

@author: Sean
"""
import math
import pygame
import scipy

pygame.init()

# Define constants for the screen width and height
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1000

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Setup the clock for a decent framerate
clock = pygame.time.Clock()
FPS = 60
G = 6.67 * 10 ** - 11
AU = 1.50* 10 ** 11 #used to scale distance in force calcs
DISTANCE_SCALE = AU / 100
TIME_STEP = (1 / FPS) * 5 * 10 **6
RGB_COLOURS = {"WHITE": (255, 255, 255), "RED": (255, 0, 0) , "BLUE": (0, 0, 255)}

#See here for example of how to organise:
#https://github.com/techwithtim/Pygame-Car-Racer/blob/main/tutorial1-code/main.py
#planet class, update position based on current velocity
#First get single planet working in a circle
#https://research.wdss.io/planetary-motion/#Moving-to-3D
path_points = []

class Planet(object):
    def __init__(self, m, r, colour, pos, vel, accel = [0 , 0]):
        self.mass = m
        self.radius = r
        self.colour = colour 
        self.x_pos = pos[0] * DISTANCE_SCALE
        self.y_pos = pos[1] * DISTANCE_SCALE
        self.x_vel = vel[0] 
        self.y_vel = vel[1] 
        self.x_accel = accel[0] 
        self.y_accel = accel[1] 
          
    def get_mass(self):
        return (self.mass)
    
    def get_pos(self):
        return ([self.x_pos, self.y_pos])
        
    def update_pos(self):
        #s = vt - 1/2 at^2
        self.x_pos += (self.x_vel * TIME_STEP) - 0.5 * self.x_accel * (TIME_STEP) ** 2 
        self.y_pos += (self.y_vel * TIME_STEP) - 0.5 * self.y_accel * (TIME_STEP) ** 2 
        print("sx , sy = ", [self.x_pos , self.y_pos])
        
    def update_vel(self):
        #v = u + at
        self.x_vel += self.x_accel * TIME_STEP
        self.y_vel += self.y_accel * TIME_STEP
        self.update_pos()
        print("vx , vy = ", [self.x_vel , self.y_vel])
        
    def update_accel(self, accel):
        self.x_accel = accel[0]
        self.y_accel = accel[1]
        self.update_vel()
 
    def calc_distance(self, pos_other):
        distance = ((self.x_pos - pos_other[0])** 2 + (self.y_pos - pos_other[1])** 2) ** 0.5
        return distance
        
    def calc_force(self, pos_other, mass_other):
        r_distance = self.calc_distance(pos_other)
        unit_vector = [((pos_other[0] - self.x_pos) / r_distance), ((pos_other[1] - self.y_pos) / r_distance)]
        
        magnitude = G * mass_other * self.mass / (r_distance ** 2)# 1/r^2 for now
        
        x_force = unit_vector[0] * magnitude
        y_force = unit_vector[1] * magnitude
        force = [x_force, y_force]     
        return force    
    
    def draw(self): 
        #draw path
        for i, point in enumerate(path_points[self]):
            #only draw point outside of planet radius
            planet_point_distance = self.calc_distance([point[0] * DISTANCE_SCALE, point[1] * DISTANCE_SCALE])
            if planet_point_distance > (self.radius * DISTANCE_SCALE):
                pygame.draw.circle(screen, self.colour, (point[0], point[1]), 1)

        path_points[self].append([self.x_pos / DISTANCE_SCALE, self.y_pos / DISTANCE_SCALE])
        #draw planet
        pygame.draw.circle(screen, self.colour, (self.x_pos / DISTANCE_SCALE, self.y_pos / DISTANCE_SCALE), self.radius)

Earth = Planet(6 * 10 ** 24, 10, RGB_COLOURS["BLUE"], [100 + SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2] , [-5 * 10 ** 3 , 2 * 10 ** 4])
Moon = Planet(7 * 10 ** 22, 6, RGB_COLOURS["WHITE"], [120 + SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2] , [-5.1 * 10 ** 3 , 2.1 * 10 ** 4])
Sun = Planet(2 * 10 ** 30, 15, RGB_COLOURS["RED"], [SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2] , [0, 0])
planet_list = [Earth, Moon, Sun]

#initialising dict to plot orbit path
path_points = {}
for planet in planet_list:
    path_points[planet] = []
    
# Run until the user asks to quit
running = True
while running:
    clock.tick(FPS)
    # Fill the background black
    screen.fill((0, 0, 0))

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for Planet_i in planet_list:
        force = [0, 0]
        for Planet_j in planet_list:
            if Planet_i != Planet_j:
                
                force[0] += Planet_i.calc_force(Planet_j.get_pos(), Planet_j.get_mass())[0]
                force[1] += Planet_i.calc_force(Planet_j.get_pos(), Planet_j.get_mass())[1] # dumb, find better way
    
        print("force =" , force)
        accel = [force[0] / Planet_i.get_mass(), force[1] / Planet_i.get_mass()]
        Planet_i.update_accel(accel)
        Planet_i.draw()
    pygame.display.update()
pygame.quit()
