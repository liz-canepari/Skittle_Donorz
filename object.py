import pygame
class Object(pygame.sprite.Sprite):

    def __init__(self,file_path, width, height, position = [0,0]):
        self.width = width
        self.height = height
        self.position = position
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = self.position[0]
        self.rect.y = self.position[1]
        self.mask = pygame.mask.from_surface(self.image)

    def set_position(self, x, y):
        self.position = [x, y]
    
    def draw(self, surface):
        surface.blit(self.image, self.position)
    
    def update(self, screen_scroll):
        self.position[0] += screen_scroll[0]
        self.position[1] += screen_scroll[1]

class ObjectCopy(Object):
    def __init__(self, object):
        self.width = object.width
        self.height = object.height
        self.position = object.position
        pygame.sprite.Sprite.__init__(self)
        self.image = object.image
        self.rect = object.rect
        self.mask = object.mask
