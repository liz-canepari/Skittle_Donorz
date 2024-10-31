import pygame
class Object(pygame.sprite.Sprite):

    def __init__(self,file_path, width, height):
        self.width = width
        self.height = height
        self.position = [0, 0]
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