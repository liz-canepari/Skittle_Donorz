import pygame
import spritesheet

class Player():
    #Animation code from Coding with Russ tutorial
    #https://www.youtube.com/watch?v=nXOVcOBqFwM&t=33s

    animation_list = [] #will hold all animation frames
    animation_steps = [] #used to set up animation frames for each action--number coordinates with number of frames in each animation
    current_frame = 0 #current animation frame for character display
    current_action = 0 
    position = [0, 0] #coordinates of character on screen
    velocity = [0, 0] #controls how quickly character moves and in what direction 
    SPEED = .25 #controls how quickly character moves --- used in when changing velocity
    
    def __init__(self, x, y, velocity_x, velocity_y, image_path):

        #load sprite sheet
        sprite_sheet_image = pygame.image.load(image_path).convert_alpha()
        #create spritesheet object
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
       
        #load animation frames
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
#-----------------------------------------------getters---------------------------------------
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
#-----------------------------------------------setters---------------------------------------
    def set_frame(self, frame):
        self.current_frame=frame

    def set_action(self, action):
        self.current_action=action

    
    def set_velocity_x(self, x, y):
        self.velocity = [x, y]

    def set_speed(self, num):
        self.SPEED = num

    #Updates position of the player using velocity
    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

        self.clamp_position(screen_width=600, screen_height=600)

    def clamp_position(self, screen_width, screen_height):
        # Assuming the player's image width and height are 32x32 pixels
        self.position[0] = max(0, min(self.position[0], screen_width - 32))
        self.position[1] = max(0, min(self.position[1], screen_height - 32))

        
    #put character on screen
    def draw(self, surface):
        surface.blit(self.get_animation_frame(), self.position)

#---------------------------------------------------------movement functions----------------------------------
    def move_left(self):
        # change velocity x value
        self.velocity[0] = -(self.SPEED)
        #set animation to left facing walking animation
        self.set_action(1)
        self.set_frame(0)
    
    def move_right(self):
        #change velocity x value
        self.velocity[0] = (self.SPEED)
        #set animation to right facing walking animation
        self.set_action(2)
        self.set_frame(0)
    
    def move_up(self):
        #change velocity y value
        self.velocity[1] = -(self.SPEED)
        #set animation to backwards facing walking animation
        self.set_action(4)
        self.set_frame(0)
    
    def move_down(self):
        #change velocity y value
        self.velocity[1] = (self.SPEED)
        #set to move forward facing walking animation
        self.set_action(3)
        self.set_frame(0)
    
    #Character goes back to idle and stops moving
    def stand_still(self):
        #change velocity
        self.velocity[0] = 0
        self.velocity[1] = 0
        #set to idle animation
        self.set_action(0)
        self.set_frame(0)
    
    # Calculate the distance between the player and the object. -Porter
    def player_is_near(self, obj_position, threshold=40):
        player_x = self.get_x()
        player_y = self.get_y()
        
        distance_x = abs(player_x - obj_position[0])
        distance_y = abs(player_y - obj_position[1])
        
        return distance_x < threshold and distance_y < threshold

