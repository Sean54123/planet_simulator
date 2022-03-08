# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 19:32:13 2022

@author: Sean
"""
import math
import pygame
import scipy

pygame.init()

# Simple pygame program

# Define constants for the screen width and height
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

# Setup the clock for a decent framerate
clock = pygame.time.Clock()
FPS = 6000
G = 6.67 * 10 ** - 11


#See here for example of how to organise:
#https://github.com/techwithtim/Pygame-Car-Racer/blob/main/tutorial1-code/main.py
#planet class, update position based on current velocity
#First get single planet working in a circle
#https://research.wdss.io/planetary-motion/#Moving-to-3D
path_points = []


class Planet(object):
    def __init__(self, m, r, pos, vel, accel = [0 , 0]):
        self.mass = m
        self.radius = r
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.x_vel = vel[0]
        self.y_vel = vel[1]
        self.x_accel = accel[0]
        self.y_accel = accel[1]
        
        
    def get_mass(self):
        return (self.mass)
    
    def get_pos(self):
        return ([self.x_pos, self.y_pos])
        
    def update_pos(self):
        self.x_pos += (self.x_vel * 1 / FPS) - 0.5 * self.x_accel * (1 / FPS) ** 2  # need to add accel
        self.y_pos += (self.y_vel * 1 / FPS) - 0.5 * self.y_accel * (1 / FPS) ** 2 
        
    def update_vel(self):
        self.x_vel += self.x_accel * 1 / FPS
        self.y_vel += self.y_accel * 1 / FPS
        self.update_pos()
        print("vx , vy = ", [self.x_vel , self.y_vel])
        
    def update_accel(self, accel):
        self.x_accel = accel[0]
        self.y_accel = accel[1]
        self.update_vel()
        
        
    def draw(self): 
        for point in path_points:
            pygame.draw.circle(screen, (0, 255, 0), (point[0], point[1]), 1)
        path_points.append([self.x_pos, self.y_pos])
        
        pygame.draw.circle(screen, (0, 0, 255), (self.x_pos, self.y_pos), self.radius)
        
       # pygame.draw.circle(screen, (255, 0, 0), (SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2), 15)
        
        
    def calc_force(self, pos_other, mass_other):
        
        r_distance = ((self.x_pos - pos_other[0])** 2 + (self.y_pos - pos_other[1])** 2) ** 0.5
        
        magnitude = G * mass_other * self.mass / (r_distance ** 2)# 1/r^2 for now
        
        unit_vector = [((pos_other[0] - self.x_pos) / r_distance), ((pos_other[1] - self.y_pos) / r_distance)]
        
        x_force = unit_vector[0] * magnitude
        y_force = unit_vector[1] * magnitude
        force = [x_force, y_force]
        
        return force    


Earth = Planet(9 * 10 ** 15, 10, [200, 225] , [-0.5, 520])
Moon = Planet(8.3 * 10 ** 13, 6, [195, 225] , [0, 700])
Sun = Planet(1 * 10 ** 18, 15, [SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2] , [0, 0])

planet_list = [Earth, Moon, Sun]


theta = 0
# Run until the user asks to quit
running = True
while running:
    clock.tick(FPS)

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background black
    screen.fill((0, 0, 0))

    # Draw a solid blue circle in the center
    #pygame.draw.circle(screen, (0, 0, 255), (SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2), 75)
    #theta += 2 * math.pi / 60
    #Earth.update_vel([100 * math.cos(theta), 100 * math.sin(theta)])
    
    for Planet_i in planet_list:
        force = [0, 0]
        for Planet_j in planet_list:
            if Planet_i != Planet_j:
                
                force[0] += Planet_i.calc_force(Planet_j.get_pos(), Planet_j.get_mass())[0]
                force[1] += Planet_i.calc_force(Planet_j.get_pos(), Planet_j.get_mass())[1] # dumb, find better way
    
        print("force =" , force)
        accel = [force[0] / Planet_i.get_mass(), force[1] / Planet_i.get_mass()]
        Planet_i.update_accel(accel)
    
        Planet_i.update_pos()
        Planet_i.draw()

        pygame.display.update()
# Done! Time to quit.
pygame.quit()