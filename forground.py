import pygame
import constants
import csv

class Forground():

    def __init__(self):
        self.objects = []
    
    def add_object(self, data, object):
        #init list for placement info
        placement_data = []
        #create empty tile list
        for row in range(constants.ROWS):
            r = [-1] * constants.COLS
            placement_data.append(r)
        #load in level data
        with open(data, newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter = ",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    print(f"{x}, {y}")
                    placement_data[x][y] = int(tile)
        
        self.objects.append([placement_data, object])


    def draw(self, surface):
        for obj in self.objects:
            for y, row in enumerate(obj[0]):
                for x, tile in enumerate(row):
                    if tile >= 0:
                        new_x = x * constants.TILESIZE - constants.TILESIZE
                        new_y = y * constants.TILESIZE - obj[1].height + constants.TILESIZE
                        obj[1].set_position(new_x, new_y)
                        obj[1].draw(surface)