import pygame
import spritesheet

class Player():
    #Animation code from Coding with Russ tutorial
    #https://www.youtube.com/watch?v=nXOVcOBqFwM&t=33s
    animation_list = []
    animation_steps = []
    current_frame = 0
    current_action = 0
    position = [0, 0]
    velocity = [0, 0]
    SPEED = .15
    
    def __init__(self, x, y, velocity_x, velocity_y, image_path):
        sprite_sheet_image = pygame.image.load(image_path).convert_alpha()
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)

        frame_0 = sprite_sheet.get_image(0, 0, 32)
        animation_list = []
        animation_steps = [3, 4, 4, 4, 4]
        step_counter = 0

        for animation in animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(sprite_sheet.get_image(step_counter, 32, 32, 2))
                step_counter += 1
            animation_list.append(temp_img_list)
        
        self.animation_list = animation_list
        self.animation_steps = animation_steps
        self.image = self.animation_list[0][0]
        self.velocity = [velocity_x, velocity_y]
        self.position = [x, y]
    def set_frame(self, frame):
        self.current_frame=frame
    def set_action(self, action):
        self.current_action=action
    def get_frame(self):
        return self.current_frame
    
    def get_action(self):
        return self.current_action
    
    def get_animation(self):
        return self.animation_list[self.current_action]
    
    def get_animation_frame(self):
        return self.animation_list[self.current_action][self.current_frame]
    
    def get_x(self):
        return self.position[0]
    
    def get_y(self):
        return self.position[1]
    
    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
    def draw(self, surface):
        surface.blit(self.get_animation_frame(), self.position)

    def move_left(self):
        self.velocity[0] = -(self.SPEED)
    
    def move_right(self):
        self.velocity[0] = (self.SPEED)
    
    def move_up(self):
        self.velocity[1] = -(self.SPEED)
    
    def move_down(self):
        self.velocity[1] = (self.SPEED)
    
    def stand_still(self):
        self.velocity[0] = 0
        self.velocity[1] = 0

    def set_velocity_x(self, x, y):
        
        self.velocity = [x, y]
    
    # Calculate the distance between the player and the object. -Porter
    def player_is_near(self, obj_position, threshold=40):
        player_x = self.get_x()
        player_y = self.get_y()
        
        distance_x = abs(player_x - obj_position[0])
        distance_y = abs(player_y - obj_position[1])
        
        return distance_x < threshold and distance_y < threshold

