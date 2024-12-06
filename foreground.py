import pygame
import constants
import csv
import object
from object import ObjectCopy
import json

class Foreground():

    def __init__(self):
        self.groups = {}
        self.top = {}

    '''LOAD
    Load in all objects from a CSV file
    *Room number: The number of the room to load in
    '''
    def load(self, room_number):
        self.groups.clear()
        self.top.clear()
        with open(f"rooms/{room_number}.json") as roomfile:
            contents = json.load(roomfile) #load json object
            items = contents["items"]
            for group in items["groups"]:
                if items["groups"][group]["type"] == "top":
                    self.add_group([], group, True)
                else:
                    self.add_group([], group, False)
                for item in items["groups"][group]:
                    if item != "type":
                        file_paths = items["groups"][group][item]["image_paths"]
                        name = items["groups"][group][item]["name"]
                        width = items["groups"][group][item]["width"]
                        height = items["groups"][group][item]["height"]
                        position = items["groups"][group][item]["position"]
                        file_paths_i = items["groups"][group][item]["file_paths_i"]
                        if file_paths_i == "":
                            file_paths_i = None
                        holding_item = items["groups"][group][item]["holding_item"]
                        if holding_item == "":
                            holding_item = False
                        else:
                            holding_item = True
                        item = items["groups"][group][item]["item"]
                        if item == "":
                            item = None
                        if items["groups"][group][item]["type"] == "push":
                            x = object.PushObject(file_paths, name, width, height, position, file_paths_i, holding_item, item)
                        else:
                            x = object.Object(file_paths, name, width, height, position, file_paths_i, holding_item, item)
                        self.add_to_group(x, group)
            for group in items["copy groups"]:
                file_paths = items["copy groups"][group]["item"]["image_paths"]
                name = items["copy groups"][group]["item"]["name"]
                width = items["copy groups"][group]["item"]["width"]
                height = items["copy groups"][group]["item"]["height"]
                position = items["copy groups"][group]["item"]["position"]
                file_paths_i = items["copy groups"][group]["item"]["file_paths_i"]
                if file_paths_i == "":
                    file_paths_i = None
                holding_item = items["copy groups"][group]["item"]["holding_item"]
                if holding_item == "":
                    holding_item = False
                else:
                    holding_item = True
                item = items["copy groups"][group]["item"]["item"]
                if item == "":
                    item = None
                x = object.Object(file_paths, name, width, height, position, file_paths_i, holding_item, item)
                data = items["copy groups"][group]["data_file"]
                if items["copy groups"][group]["type"] == "top":
                    self.add_copy_group(x, group, data, True)
                else:
                    self.add_copy_group(x, group, data, False)
            

            


            

    '''GET GROUP
    Retrieve a sprite group from the foreground
    *Name: Name of the group
    '''
    def get_group(self, name):
        return self.groups[name]
    
    '''GET GROUPS
    Retrieve all sprite groups in the foreground
    '''
    def get_groups(self):
        return self.groups
    
    '''GET TOP GROUPS
    Retrieve all sprite groups in the top level of the foreground
    '''
    def get_top_groups(self):
        return self.top
    '''
    ADD SINGLE OBJECT
    Add a single object to the map, in its own sprite group
    (if you want to add a single object to an already existing sprite group, use add_to_group)
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
    *Data: CSV file with multiple placements. Anywhere with a 1 will have a copy of the object placed there
    '''
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
            if name in self.groups.keys():
                self.groups[name].add(group)
            else:
                self.groups[name] = group   
        else: 
            if name in self.top.keys():
                self.top[name].add(group)
            else:
                self.top[name] = group

    '''
    ADD TO GROUP
    Add a single object to an already existing sprite group
    *Object: The object to add
    *Group name: The name of the group to add the object to
    '''
    def add_to_group(self, object, group_name, top=False):
        if not top:
            self.groups[group_name].add(object)
        else: self.top[group_name].add(object)

    '''
    ADD GROUP
    add new sprite group with already existing objects
    *Objects: The list of objects to add
    *Name: Name for the new object group, will be used as the key in the foreground dictionary of groups
    '''
    def add_group(self, objects, name, top=False):
        group = pygame.sprite.Group()
        for object in objects:
            group.add(object)
        if not top:
            self.groups[name] = group
        else: self.top[name] = group

    '''
    ADD EXISTING GROUP
    Add an already existing sprite group to the foreground dict for easy management
    '''
    def add_existing_group(self, group, name, top=False):
        if not top:
            self.groups[name] = group
        else: self.top[name] = group

                    
    '''
    DRAW
    put all ground level objects on the screen 
    (Should be called after world.draw, before player.draw)
    '''
    def draw(self, surface):
        for group in self.groups.values():
            for object in group:
                object.draw(surface)

    '''
    DRAW TOP
    put all top level objects on the screen
    (should be called after player.draw)
    '''
    def draw_top(self, surface):
        for group in self.top.values():
            for object in group:
                object.draw(surface)

    '''
    UPDATE
    Update position of all foreground objects
    *Screen_scroll: The position of the camera
    '''
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
    

    '''
    COLORIZE
    Switch all objects to colored images
    *Color: The color to add. None = all colors
    '''
    def colorize(self, color = None):
        for group in self.groups.values():
            for object in group:
                object.colorize(color)
        for group in self.top.values():
            for object in group:
                object.colorize(color)
    
    def decolorize(self):
        for group in self.groups.values():
            for object in group:
                object.decolorize()
        for group in self.top.values():
            for object in group:
                object.decolorize()