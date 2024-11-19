import pygame
import spritesheet
 
class Npc(pygame.sprite.Sprite):

    animation_list = [] #will hold all animation frames
    animation_steps = [] #used to set up animation frames for each action--number coordinates with number of frames in each animation
    current_frame = 0 #current animation frame for character display
    current_action = 0 
    def __init__(self, name, x, y, size, image_path, can_interact, dialogue, dialogue_img): 
        pygame.sprite.Sprite.__init__(self)
        sprite_sheet_image = pygame.image.load(image_path).convert_alpha()
        #create spritesheet object
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

                #load animation frames
        frame_0 = sprite_sheet.get_image(0, 0, size[0])
        animation_list = []
        animation_steps = [26]
        step_counter = 0

        for animation in animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(sprite_sheet.get_image(step_counter, 32, 32, 2))
                step_counter += 1
            animation_list.append(temp_img_list)
        
        self.animation_list = animation_list
        self.animation_steps = animation_steps
        self.name = name
        self.size = size
        self.skin = self.animation_list[0][0]
        self.dialogue_img = pygame.image.load(dialogue_img).convert_alpha() if dialogue_img else None
        self.can_interact = can_interact
        self.dialogue = dialogue
        self.rect = pygame.Rect(x, y, 64, 64)
 
    def get_frame(self):
        return self.current_frame
    
    def get_action(self):
        return self.current_action
    
    def get_animation(self):
        return self.animation_list[self.current_action]
    
    def get_animation_frame(self):
        return self.animation_list[self.current_action][self.current_frame]
    
    def set_frame(self, frame):
        self.current_frame=frame

    def set_action(self, action):
        self.current_action=action
    
    def interact(self):
        if self.can_interact:
            return self.dialogue
       
    def draw(self, screen):
        screen.blit(self.get_animation_frame(), (self.rect.x, self.rect.y))
 
    def get_x(self):
        return self.rect.x
   
    def get_y(self):
        return self.rect.y
    
    def update(self, screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        self.skin = self.get_animation_frame()
 
