import pygame
class Object(pygame.sprite.Sprite):

    def __init__(self,file_path, width, height, position = [0,0]):
        self.width = width
        self.height = height
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(position[0], position[1], width-10, height - 10)
        self.mask = pygame.mask.from_surface(self.image)

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
    
    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self, screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

class ObjectCopy(Object):
    def __init__(self, object):
        self.width = object.width
        self.height = object.height
        pygame.sprite.Sprite.__init__(self)
        self.image = object.image
        self.rect = pygame.rect.Rect(object.rect.x, object.rect.y, object.width, object.height)
        self.mask = object.mask