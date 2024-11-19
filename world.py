import pygame
import constants
import csv

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []


    def load_room(self, tile_list, world_data, room_number):
        tile_list.clear()
        world_data.clear()

        with open(f"rooms/{room_number}.csv", newline="") as roomfile:
            reader = csv.DictReader(roomfile)
            data = {row['key']: row['value'] for row in reader} # creates a key-value dictionary

            # load the tiles from the given file address
            tile_list = self.load_tilemap_images(tile_list, int(data["tile_types"]), data["tileset_address"])
            world_data = self.world_fill_defaults(world_data, int(data["rows"]), int(data["columns"]))
            world_data = self.load_csv_level(world_data, data["level_address"])
            self.process_data(world_data, tile_list)


    def process_data(self, data, tile_list):
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
                #image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y, color_image]

                #add image data to main tiles list
                if tile >= 0:
                    self.map_tiles.append(tile_data)
                if 0 <= tile <= 11:
                    self.obstacle_tiles.append(tile_data)

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
            gray_image = pygame.image.load(f"{tileset_address}/{x}.png").convert_alpha() #currently don't have different gray vs colored images for mentors hut so they are the same
            color_image = pygame.image.load(f"{tileset_address}/{x}.png").convert_alpha()
            tile_image = pygame.transform.scale(gray_image, (constants.TILESIZE, constants.TILESIZE))
            tile_list.append([tile_image, color_image])
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
    def colorize(self):
        for tile in self.map_tiles:
            tile[0] = pygame.transform.scale(tile[4], (constants.TILESIZE, constants.TILESIZE))
        for tile in self.obstacle_tiles:
            tile[0] = pygame.transform.scale(tile[4], (constants.TILESIZE, constants.TILESIZE))