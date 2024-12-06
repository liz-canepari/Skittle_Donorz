import pygame
import constants
import spritesheet
class Object(pygame.sprite.Sprite):

    def __init__(self,file_paths, name, width, height, position = [0,0],file_paths_i = None, holding_item = False, item = None):
        
        self.name = name #name of the object, will be used for certain interactions and for inventory
        #if file_paths_i is present, means object is interactable (i stands for interaction)
        if file_paths_i: #list of the different interaction images
            self.interact_imgs = file_paths_i
            self.interact_index = 1
            self.interactable = True
            self.holding_item = holding_item
        else: self.interactable = False

        if holding_item:
            self.item = item #item must be initiated before the container object
            self.open = False

        self.width = width
        self.height = height
        pygame.sprite.Sprite.__init__(self)

        #gray image is initial image, colorize methode changes image to color image
        if len(file_paths) == 1:
            self.color_image = pygame.image.load(file_paths[0]).convert_alpha()
            self.gray_image = pygame.transform.grayscale(self.color_image)
            self.image = pygame.transform.scale(self.gray_image, (width, height))
            self.green_image = self.gray_image
            self.yellow_image = self.gray_image
            self.red_image = self.gray_image
        elif len(file_paths) == 2:
            for path in file_paths:
                if "color" in path:    
                    self.color_image = pygame.image.load(file_paths[1]).convert_alpha()
                if "green" in path:
                    self.green_image = pygame.image.load(file_paths[1]).convert_alpha()
            self.gray_image = pygame.transform.grayscale(pygame.image.load(file_paths[0]).convert_alpha())
            self.yellow_image = self.gray_image
            self.red_image = self.gray_image
            self.image = pygame.transform.scale(self.gray_image, (width, height))
        self.rect = pygame.Rect(position[0], position[1], width-10, height - 10)
        self.mask = pygame.mask.from_surface(self.image)
        self.position = position #idk just incase we still want it later??
        self.used = False #initially set to False, will be set to True when object is "used"

    '''COLORIZE
    changes the current image to color_image
    '''
    def colorize(self, colors = None):
        if colors:
            if "green" in colors:
                self.image = pygame.transform.scale(self.green_image, (self.width, self.height))
            elif "yellow" in colors and "red" in colors:
                self.image = pygame.transform.scale(self.color_image, (self.width, self.height))
        else:
            self.image = pygame.transform.scale(self.color_image, (self.width, self.height))

    def decolorize(self):
        self.image = pygame.transform.scale(self.gray_image, (self.width, self.height))
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
    
    '''UPDATE
    updates the position of the object
    *Screen_scroll is the amount the screen has scrolled/camera position'''
    def update(self, screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

    '''INTERACT
    changes the current image to the next interaction image'''
    def interact(self):
        if self.interact_index == 1:
            self.og_image = self.image
        self.image = pygame.image.load(self.interact_imgs[self.interact_index]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.interact_index += 1
        if self.interact_index >= len(self.interact_imgs):
            self.interact_index = 1
            self.used = True
    
    '''IN INVENTORY
    changes current image to the first interaction image
    changes size of image to fit in inventory slot
    '''
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
        self.position = object.position
        self.rect = pygame.rect.Rect(object.rect.x, object.rect.y, object.width, object.height)
        self.mask = object.mask

class PushObject(Object):
    def __init__(self, file_paths, name, width, height, position = [0,0], place = [0,0]):
        super().__init__(file_paths, name, width, height, position)
        self.inplace = False
        self.place = place

    def push(self, direction, speed):
        if not self.inplace:
            if direction == "up":
                self.rect.y -= 1 * speed
            elif direction == "down":
                self.rect.y += 1 * speed
            elif direction == "left":
                self.rect.x -= 1 * speed
            elif direction == "right":
                self.rect.x += 1 * speed
    
    def check_place(self):
        if self.rect.x in range(self.place[0] - 5, self.place[0] + 48) and self.rect.y in range(self.place[1] - 5, self.place[1] + 48):
            self.inplace = True

    def update(self, screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        self.place[0] += screen_scroll[0]
        self.place[1] += screen_scroll[1]

class AnimatedObject(Object):
    
    animation_list = [] #will hold all animation frames
    animation_steps = [] #used to set up animation frames for each action--number coordinates with number of frames in each animation
    current_frame = 0 #current animation frame for character display
    current_action = 0 
    def __init__(self, file_path, name, width, height, position = [0,0], animation_steps = [], scale=constants.SCALE):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.position = position
        sprite_sheet_image = pygame.image.load(file_path).convert_alpha()
        #create spritesheet object
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

                #load animation frames
        animation_list = [] #will hold all animation frames
        self.animation_steps = animation_steps  #used to set up animation frames for each action--number coordinates with number of frames in each animation

        for i in range(0, animation_steps[0]):
            animation_list.append(sprite_sheet.get_image(i, width, height, scale))
        self.color_animation_list = animation_list
        self.gray_animation_list = []
        for frame in self.color_animation_list:
            self.gray_animation_list.append(pygame.transform.grayscale(frame))
        for frame in self.gray_animation_list:
            frame.set_colorkey((0,0,0))

        self.animation_list = self.gray_animation_list

        if (len(self.animation_list) > 1):
            self.image = self.animation_list[0]
        else: self.image = sprite_sheet.get_image(0, width, height, 1)
        self.rect = pygame.rect.Rect(position[0], position[1], width, height)

    def get_frame(self):
        return self.current_frame
    
    def get_action(self):
        return self.current_action
    
    def get_animation(self):
        return self.animation_list
    
    def get_animation_frame(self):
        return self.animation_list[self.current_frame]
    
    def set_frame(self, frame):
        self.current_frame=frame

    def set_action(self, action):
        self.current_action=action
    
    def draw(self, screen):
        screen.blit(self.get_animation_frame(), (self.rect.x, self.rect.y))

    def update(self, screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        self.image = self.get_animation_frame()
    
    def colorize(self, colors = None):
        if "green" in colors:
            self.animation_list = self.gray_animation_list
        if "yellow" in colors and "red" in colors:
            self.animation_list = self.color_animation_list
        else:
            self.animation_list = self.color_animation_list