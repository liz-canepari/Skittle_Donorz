import pygame
import constants
import csv
from object import ObjectCopy

class Foreground():

    def __init__(self):
        self.groups = {}
        self.top = {}

    def get_group(self, name):
        return self.groups[name]
    
    def get_groups(self):
        return self.groups
    
    '''
    ADD SINGLE OBJECT
    Add a single object to the map, in its own sprite group
    *Object: The object to add
    *Name: Name for the new object group, will be used as the key in the foreground dictionary of groups
    '''
    def add_single_object(self, object, name, top=False):
        group = pygame.sprite.GroupSingle()
        group.add(object)
    
        if not top:
            self.groups[name] = group
        else: self.top[name] = group

    '''
    ADD COPY GROUP
    Function takes one object and makes a group of copies of it
    *Object: The object that will be copied
    *Name: Name for the new object group, will be used as the key in the foreground dictionary of groups
    *Data: CSV file with multiple placements. Anywhere with a 1 will have a copy of the object placed there'''
    def add_copy_group(self, object, name, data, top=False):

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
                    if placement_data[x][y] == 0:
                        new_object = ObjectCopy(object)
                        if top:
                            new_object.set_position(y * constants.TILESIZE - (object.width/2) + object.position[0], x * constants.TILESIZE - object.height + object.position[1])
                        else:
                            new_object.set_position(y * constants.TILESIZE - (object.width/2), x * constants.TILESIZE - object.height)
                        group.add(new_object)
        if not top:
            self.groups[name] = group   
        else: self.top[name] = group

    def add_to_group(self, object, group_name, top=False):
        if not top:
            self.groups[group_name].add(object)
        else: self.top[group_name].add(object)

    '''
    ADD GROUP
    Add an already existing sprite group to the foreground dict for easy management'''
    def add_group(self, name, group, top=False):
        if not top:
            self.groups[name] = group
        else: self.top[name] = group

                    

    def draw(self, surface):
        for group in self.groups.values():
            for object in group:
                object.draw(surface)

    def draw_top(self, surface):
        for group in self.top.values():
            for object in group:
                object.draw(surface)

    def update(self, screen_scroll):
        for group in self.groups.values():
            for object in group:
                object.update(screen_scroll)

        for group in self.top.values():
            for object in group:
                object.update(screen_scroll)

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
        collisions = pygame.sprite.spritecollide(sprite, self.groups[group_name], kill)
        return collisions