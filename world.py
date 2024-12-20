import pygame
import constants
from door import Door
import csv
import json

class World():

    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []


    def load_room(self, tile_list, world_data, door_list, room_number):
        tile_list.clear()
        world_data.clear()
        door_list.clear()
        self.map_tiles.clear()
        self.obstacle_tiles.clear()

        with open(f"rooms/{room_number}.json", "r") as roomfile:
            data = json.load(roomfile)
            # load the tiles from the given file address
            tile_list = self.load_tilemap_images(tile_list, data["tile_types"], data["tileset_address"])
            world_data = self.world_fill_defaults(world_data, data["rows"], data["columns"])
            world_data = self.load_csv_level(world_data, data["level_address"])
            self.process_tile_data(world_data, tile_list, data["obstacles_start"], data["obstacles_end"])

            # read the list of door data and make a list of doors
            print(data["doors_data"])
            door_list = self.process_door_data(door_list, data["doors_data"])


    def process_tile_data(self, data, tile_list, obstacle_start, obstacle_end):
        self.level_length = len(data)
        
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile][0]
                image_rect = image.get_rect()
                image_x = x * constants.TILESIZE
                image_y = y * constants.TILESIZE
                image_rect.x = image_x
                image_rect.y = image_y
                color_image = tile_list[tile][1]
                gray_image = tile_list[tile][2]
                green_image = tile_list[tile][3]
                #image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y, color_image, gray_image, green_image]

                #add image data to main tiles list
                if tile >= 0:
                    self.map_tiles.append(tile_data)
                if obstacle_start <= tile <= obstacle_end:
                    self.obstacle_tiles.append(tile_data)


    def process_door_data(self, door_list, data_list):

        print(data_list)
        for door in data_list:
            
            """
            door[0] is x position
            door[1] is y position
            door[2] is x reposition (for the next room)
            door[3] is y reposition (for the next room)
            door[4] is the room number for the next room
            """
            new_door = Door(door[0], door[1], door[2], door[3], door[4])
            door_list.append(new_door)

        

    def update(self, screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0]
            tile[3] += screen_scroll[1]
            tile[1].center = (tile[2], tile[3])


    def draw(self, surface):
        for tile in self.map_tiles:
            surface.blit(tile[0], tile[1])


    def draw_grid(self, screen):
        for x in range(30):
            pygame.draw.line(screen, constants.WHITE, (x * constants.TILESIZE, 0), (x * constants.TILESIZE, constants.SCREEN_HEIGHT))
            pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILESIZE), (constants.SCREEN_WIDTH, x * constants.TILESIZE))


    def load_tilemap_images(self, tile_list, tile_types, tileset_address):
        for x in range(tile_types):
            color_image = pygame.image.load(f"{tileset_address}/color/{x}.png").convert_alpha()
            gray_image = pygame.transform.grayscale(color_image)
            green_image = pygame.image.load(f"{tileset_address}/green/{x}.png").convert_alpha()
            tile_image = pygame.transform.scale(gray_image, (constants.TILESIZE, constants.TILESIZE))
            tile_list.append([tile_image, color_image, gray_image, green_image])
        return tile_list


    def world_fill_defaults(self, world_data, rows, cols):
        for row in range(rows):
            r = [-1] * cols
            world_data.append(r)
        return world_data
    

    def load_csv_level(self, world_data, level_address):
        with open(f"{level_address}", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter = ",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
        return world_data
    

    '''
    COLORIZE
    Switch all tile images to the colorized version
    '''
    def colorize(self, colors = None):
        if colors:
            if "green" in colors:
                for tile in self.map_tiles:
                    tile[0] = pygame.transform.scale(tile[6], (constants.TILESIZE, constants.TILESIZE))
                for tile in self.obstacle_tiles:
                    tile[0] = pygame.transform.scale(tile[6], (constants.TILESIZE, constants.TILESIZE))
            elif "yellow" in colors and "red" in colors:
                for tile in self.map_tiles:
                    tile[0] = pygame.transform.scale(tile[4], (constants.TILESIZE, constants.TILESIZE))
                for tile in self.obstacle_tiles:
                    tile[0] = pygame.transform.scale(tile[4], (constants.TILESIZE, constants.TILESIZE))
        else:
            return

    def decolorize(self):
        for tile in self.map_tiles:
            tile[0] = pygame.transform.scale(tile[5], (constants.TILESIZE, constants.TILESIZE))
        for tile in self.obstacle_tiles:
            tile[0] = pygame.transform.scale(tile[5], (constants.TILESIZE, constants.TILESIZE))
        for tile in self.exit_tiles:
            tile[0] = pygame.transform.scale(tile[5], (constants.TILESIZE, constants.TILESIZE))