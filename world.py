import pygame
import constants

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []

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

    '''
    COLORIZE
    Switch all tile images to the colorized version
    '''
    def colorize(self):
        for tile in self.map_tiles:
            tile[0] = pygame.transform.scale(tile[4], (constants.TILESIZE, constants.TILESIZE))
        for tile in self.obstacle_tiles:
            tile[0] = pygame.transform.scale(tile[4], (constants.TILESIZE, constants.TILESIZE))