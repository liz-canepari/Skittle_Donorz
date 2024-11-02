import pygame
import constants
import csv
import copy

class Foreground():

    def __init__(self):
        self.groups = {}

    def get_group(self, name):
        return self.groups[name]
    
    '''
    ADD SINGLE OBJECT
    Add a single object to the map, in its own sprite group
    *Object: The object to add
    *Name: Name for the new object group, will be used as the key in the foreground dictionary of groups
    *Data:
    If given a data sheet with multiple placements, will place the same object in multiple locations
    (the same as in exact same reference just in different places.)
    If no data is given, the object will keep what ever position it was given when initiated
    '''
    def add_single_object(self, object, name, data=None):
        #init list for placement info
        if data == None:
            group = pygame.sprite.GroupSingle()
            group.add(object)
        else:
            placement_data = []
            group = pygame.sprite.Group()
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
            #place object in each location
            for x, row in enumerate(placement_data):
                for y, tile in enumerate(row):
                    if tile == 1:
                        object.set_position(x * constants.TILESIZE, y * constants.TILESIZE)
                        group.add(object)
        self.groups[name] = group

    '''
    ADD COPY GROUP
    Function takes one object and makes a group of copies of it
    *Object: The object that will be copied
    *Name: Name for the new object group, will be used as the key in the foreground dictionary of groups
    *Data: CSV file with multiple placements. Anywhere with a 1 will have a copy of the object placed there'''
    def add_copy_group(self, object, name, data,):

        placement_data = []
        group = pygame.sprite.Group()

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
                    if tile == 1:
                        object_copy = copy.deepcopy(object)
                        object_copy.set_position(x * constants.TILESIZE, y * constants.TILESIZE)
                        group.add(object_copy)

        self.groups[name] = group   

    def add_to_group(self, object, group_name):
        self.groups[group_name].add(object)

    '''
    ADD GROUP
    Add an already existing sprite group to the foreground dict for easy management'''
    def add_group(self, name, group):
        self.groups[name] = group

                    

    def draw(self, surface):
        for group in self.groups.values():
            pygame.sprite.Group.draw(group, surface)

    '''
    CHECK ALL COLLIDE
    Check if a sprite collides with any objects in all of the existing groups
    *Sprite: The sprite to check for collisions
    *Kill: Whether or not to kill the sprite if it collides with main sprite
    RETURNS: List of collided objects
    '''
    def check_all_collide(self, sprite, kill=False):
        collisions = []
        for group in self.groups.values():
            check = pygame.sprite.spritecollide(sprite, group, kill)
            if check:
                for c in check:
                    collisions.append(c)
        return collisions

    '''
    CHECK COLLIDE
    Check if a sprite collides with any objects in a specific group
    *Sprite: The sprite to check for collisions
    *Group name: The name of the group to check for collisions
    *Kill: Whether or not to kill the sprite if it collides with main sprite
    RETURNS: List of collided objects
    '''
    def check_collide(self, sprite, group_name, kill=False):
        return pygame.sprite.spritecollide(sprite, self.groups[group_name], kill)