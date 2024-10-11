import pygame

class Background(pygame.sprite.Sprite):
    image = None
    x = 0
    y = 0

    def __init__(self, image_path, x, y, width, height):
        bg_image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(bg_image, (width, height))
        self.x = x
        self.y = y

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))