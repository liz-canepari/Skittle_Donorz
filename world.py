import pygame
import constants
import csv

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []

    def process_data(self, data, tile_list):
        self.level_length = len(data)
        #iterate through each value in level data file
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x * constants.TILESIZE
                image_y = y * constants.TILESIZE
                image_rect.x = image_x
                image_rect.y = image_y
                #image_rect.center = (image_x, image_y)
                tile_data = [image, image_rect, image_x, image_y]

                #add image data to main tiles list
                if tile >= 0:
                    self.map_tiles.append(tile_data)
                if 1 <= tile <= 11:
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

    def load_tilemap_images(self, tile_list):
        for x in range(constants.TILE_TYPES):
            tile_image = pygame.image.load(f"images/tiles/mentor_hut_tiles/{x}.png").convert_alpha()
            tile_image = pygame.transform.scale(tile_image, (constants.TILESIZE, constants.TILESIZE))
            tile_list.append(tile_image)
        return tile_list

    def world_fill_defaults(self, world_data):
        for row in range(constants.ROWS):
            r = [-1] * constants.COLS
            world_data.append(r)
        return world_data
    
    def load_csv_level(self, world_data):
        with open("levels/mentors_hut_data.csv", newline="") as csvfile:
            reader = csv.reader(csvfile, delimiter = ",")
            for x, row in enumerate(reader):
                for y, tile in enumerate(row):
                    world_data[x][y] = int(tile)
        return world_data