# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 19:32:13 2022

@author: Sean
"""
import math
import pygame
import scipy

pygame.init()
# Set window caption
pygame.display.set_caption('Solar Simulator')
# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1200
# Create the screen object
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
zoom = 1
# Setup the clock for a decent framerate
clock = pygame.time.Clock()
FPS = 60
G = 6.67 * 10 ** - 11
AU = 1.50* 10 ** 11 #used to scale distance in force calcs
DISTANCE_SCALE = AU / 100
TIME_STEP = (1 / FPS) * 5 * 10 **6
RGB_COLOURS = {"WHITE": (255, 255, 255), "RED": (255, 0, 0) , "BLUE": (0, 0, 255), "ORANGE": (255, 153, 0), "GREY": (102, 102, 153), "GREEN": (102, 153, 153)}
PLANET_FONT = pygame.font.SysFont("cambriamath", 20)

#extension: update with current/historical planet starting positions
#https://ssd.jpl.nasa.gov/horizons/app.html#/
#https://ssd-api.jpl.nasa.gov/doc/horizons.html

class Planet(object):
    def __init__(self, name, m, r, colour, pos, vel, accel = [0 , 0]):
        self.name = name
        self.mass = m
        self.radius = r
        self.colour = colour 
        self.x_pos = pos[0] * DISTANCE_SCALE
        self.y_pos = pos[1] * DISTANCE_SCALE
        self.x_vel = vel[0] 
        self.y_vel = vel[1] 
        self.x_accel = accel[0] 
        self.y_accel = accel[1] 
        self.x_scaled = self.x_pos
        self.y_scaled = self.y_pos
        self.radius_scaled = self.radius
        
    def get_planet_name(self):
        return self.name
    
    def get_mass(self):
        return self.mass
    
    def get_pos(self):
        return [self.x_pos, self.y_pos]
        
    def update_pos(self):
        #s = vt - 1/2 at^2
        self.x_pos += (self.x_vel * TIME_STEP) - 0.5 * self.x_accel * (TIME_STEP) ** 2 
        self.y_pos += (self.y_vel * TIME_STEP) - 0.5 * self.y_accel * (TIME_STEP) ** 2 
        
    def update_vel(self):
        #v = u + at
        self.x_vel += self.x_accel * TIME_STEP
        self.y_vel += self.y_accel * TIME_STEP
        self.update_pos()
        
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
        magnitude = G * mass_other * self.mass / (r_distance ** 2)
        x_force = unit_vector[0] * magnitude
        y_force = unit_vector[1] * magnitude
        force = [x_force, y_force]     
        return force 

    def set_scale_zoom_distances(self):
        self.x_scaled = int((self.x_pos / DISTANCE_SCALE - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2)
        self.y_scaled = int((self.y_pos / DISTANCE_SCALE - SCREEN_HEIGHT / 2) * zoom + SCREEN_WIDTH / 2)
        self.radius_scaled = int(self.radius * zoom)

    def get_scaled_pos(self):
        return[self.x_scaled, self.y_scaled]
    
    def draw_planet(self): 
        self.set_scale_zoom_distances()
        #draw path
        for i, point in enumerate(path_points[self]):
            #only draw point outside of planet radius
            planet_point_distance = self.calc_distance([point[0] * DISTANCE_SCALE, point[1] * DISTANCE_SCALE])
            if planet_point_distance > (self.radius_scaled * DISTANCE_SCALE):
                pygame.draw.circle(screen, self.colour, (point[0], point[1]), 1)

        path_points[self].append([self.x_scaled, self.y_scaled])
        # Draw planet
        pygame.draw.circle(screen, self.colour, (self.x_scaled, self.y_scaled), self.radius_scaled)
    def draw_planet_text(self):
            scaled_x = int((self.x_pos / DISTANCE_SCALE - SCREEN_WIDTH / 2) * zoom + SCREEN_WIDTH / 2)
            scaled_y = int((self.y_pos / DISTANCE_SCALE - SCREEN_HEIGHT / 2) * zoom + SCREEN_WIDTH / 2)
            scaled_radius = int(self.radius * zoom)
            text = PLANET_FONT.render(self.get_planet_name(), False, RGB_COLOURS["WHITE"])
            screen.blit(text, (scaled_x - 18, scaled_y - scaled_radius - 26))

def set_zoom(scroll_increment, previous_zoom):
    if (previous_zoom < 0.2) & (scroll_increment == -1):
        zoom = previous_zoom
    else:    
        zoom = previous_zoom + scroll_increment / 10
    return zoom

#REALISTIC MASSESS/Orbital veloicties
Mercury = Planet("Mecury", 3.3 * 10 ** 23, 4, RGB_COLOURS["GREY"], [38 + SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2] , [0, 4.7 * 10 ** 4])
Venus = Planet("Venus", 4.9 * 10 ** 24, 8, RGB_COLOURS["WHITE"], [72 + SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2] , [0 , 3.5 * 10 ** 4])
Earth = Planet("Earth", 6 * 10 ** 24, 8, RGB_COLOURS["BLUE"], [100 + SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2] , [0 , 3 * 10 ** 4])
Mars = Planet("Mars", 6.4 * 10 ** 23, 4, RGB_COLOURS["RED"], [152 + SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2] , [0 , 2.4 * 10 ** 4])
Jupiter = Planet("Jupiter", 1.9 * 10 ** 27, 12, RGB_COLOURS["GREEN"], [520 + SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2] , [0 , 1.3 * 10 ** 4])
Sun = Planet("Sun", 2 * 10 ** 30, 15, RGB_COLOURS["ORANGE"], [SCREEN_WIDTH / 2, SCREEN_HEIGHT/ 2] , [0, 0])
planet_list = [Mercury, Venus, Earth, Mars, Jupiter, Sun]
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
        elif event.type == pygame.MOUSEWHEEL:
            zoom = set_zoom(scroll_increment=event.y, previous_zoom=zoom)    
    for Planet_i in planet_list:
        force = [0, 0]
        for Planet_j in planet_list:
            #sum up forces on planet_i and update accelaration
            if Planet_i != Planet_j:
                x_force, y_force = Planet_i.calc_force(Planet_j.get_pos(), Planet_j.get_mass())
                force[0] += x_force
                force[1] += y_force   
        accel = [force[0] / Planet_i.get_mass(), force[1] / Planet_i.get_mass()]

        Planet_i.update_accel(accel)
        Planet_i.draw_planet()
        Mouse_x, Mouse_y = pygame.mouse.get_pos()
        if ((Planet_i.get_scaled_pos()[0] - 10 <= Mouse_x <= Planet_i.get_scaled_pos()[0] + 10) and (Planet_i.get_scaled_pos()[1] - 10  <= Mouse_y <= Planet_i.get_scaled_pos()[1] + 10)):
            Planet_i.draw_planet_text()  
    pygame.display.update()
pygame.quit()
