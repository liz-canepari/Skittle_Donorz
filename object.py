import pygame
import constants
class Object(pygame.sprite.Sprite):

    def __init__(self,file_paths, name, width, height, position = [0,0],file_paths_i = None, holding_item = False, item = None):
        self.name = name
        if file_paths_i: #will be a list of the different interaction images
            self.interact_imgs = file_paths_i
            self.interact_index = 1
            self.interactable = True
            self.holding_item = holding_item
        else: self.interactable = False
        if holding_item:
            self.item = item
            self.open = False
        self.width = width
        self.height = height
        pygame.sprite.Sprite.__init__(self)
        self.color_image = pygame.image.load(file_paths[1]).convert_alpha()
        self.gray_image = pygame.image.load(file_paths[0]).convert_alpha()
        self.image = pygame.transform.scale(self.gray_image, (width, height))
        self.rect = pygame.Rect(position[0], position[1], width-10, height - 10)
        self.mask = pygame.mask.from_surface(self.image)
        self.position = position
        self.used = False

    def colorize(self):
        self.image = pygame.transform.scale(self.color_image, (self.width, self.height))
    def get_image(self):
        return self.image
    
    def get_name(self):
        return self.name
    
    def is_used(self):
        return self.used
    
    def is_holding_item(self):
        return self.holding_item
    
    def is_open(self):
        return self.open
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
    

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
    
    def update(self, screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

    def interact(self):
        if self.interact_index == 1:
            self.og_image = self.image
        self.image = pygame.image.load(self.interact_imgs[self.interact_index]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.interact_index += 1
        if self.interact_index >= len(self.interact_imgs):
            self.interact_index = 1
            self.used = True
        
    def in_inventory(self):
        self.image = pygame.image.load(self.interact_imgs[0]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))



class ObjectCopy(Object):
    def __init__(self, object):
        if object.interactable:
            self.interact_imgs = object.interact_imgs
            self.interactable = True
        else: self.interactable = False
        self.width = object.width
        self.height = object.height
        pygame.sprite.Sprite.__init__(self)
        self.color_image = object.color_image
        self.gray_image = object.gray_image
        self.image = object.image
        position = object.position
        self.rect = pygame.rect.Rect(object.rect.x, object.rect.y, object.width, object.height)
        self.mask = object.mask