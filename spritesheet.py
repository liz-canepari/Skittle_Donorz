import pygame
#from coding with russ tutorial https://www.youtube.com/watch?v=nXOVcOBqFwM&t=33s
class SpriteSheet():
    def __init__(self, image):
        self.sheet = image

#Extract image from sprite sheet given a frame number, width of sprite, height of sprite, scale factor, and background color to turn transparent
    def get_image(self, frame, width, height, scale=1, color=(0,0,0)):
        image = pygame.Surface((width, height)).convert_alpha()
        image.blit(self.sheet, (0, 0), ((frame * width), 0, width, height))
        image = pygame.transform.scale(image, (width * scale, height * scale))
        image.set_colorkey(color)
        return image