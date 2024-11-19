import pygame
import spritesheet
import constants
import math

class Player(pygame.sprite.Sprite):
    #Animation code from Coding with Russ tutorial
    #https://www.youtube.com/watch?v=nXOVcOBqFwM&t=33s

    animation_list = [] #will hold all animation frames
    animation_steps = [] #used to set up animation frames for each action--number coordinates with number of frames in each animation
    current_frame = 0 #current animation frame for character display
    current_action = 0 
    position = [0, 0] #coordinates of character on screen
    velocity = [0, 0] #controls how quickly character moves and in what direction 
    SPEED = 5 #controls how quickly character moves --- used in when changing velocity
    
    def __init__(self, x, y, velocity_x, velocity_y, image_path, image_width, image_height):

        pygame.sprite.Sprite.__init__(self)
        #load sprite sheet
        sprite_sheet_image = pygame.image.load(image_path).convert_alpha()
        #create spritesheet object
        sprite_sheet = spritesheet.SpriteSheet(sprite_sheet_image)
       
        #load animation frames
        frame_0 = sprite_sheet.get_image(0, 0, image_width)
        animation_list = []
        animation_steps = [3, 4, 4, 4, 4]
        step_counter = 0

        for animation in animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(sprite_sheet.get_image(step_counter, image_width, image_height, 2))
                step_counter += 1
            animation_list.append(temp_img_list)
        
        self.animation_list = animation_list
        self.animation_steps = animation_steps
        self.image = self.animation_list[0][0]
        self.rect = pygame.Rect(x, y, 60, 60)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = [velocity_x, velocity_y]
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
        return self.rect.centerx
    
    def get_y(self):
        return self.rect.centery
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
    def update(self, obstacle_tiles, exit_tiles, npc_list):

        exit_bool = False

        #check for collision with map in x direction
        self.rect.centerx += self.velocity[0]
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                if self.velocity[0] > 0:
                    self.rect.right = obstacle[1].left
                if self.velocity[0] < 0:
                    self.rect.left = obstacle[1].right

        #check for collision with map in y direction
        self.rect.centery += self.velocity[1]
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                if self.velocity[1] > 0:
                    self.rect.bottom = obstacle[1].top
                if self.velocity[1] < 0:
                    self.rect.top = obstacle[1].bottom

        #check for collision with exit tile
        for exit in exit_tiles:
            if exit[1].colliderect(self.rect):
                #ensure player is close to the center of the exit tile
                exit_dist = math.sqrt(((self.rect.centerx - exit[1].centerx) ** 2) + ((self.rect.centery - exit[1].centery) ** 2))
                if exit_dist < 20: 
                    exit_bool = True

        # ------------------- NPC COLLISION -----------------------------------------
        # self.rect.centerx += self.velocity[0]
        #check for collision with map in x direction
        for npc in npc_list:
            if npc.rect.colliderect(self.rect):
                if self.velocity[0] > 0:
                    self.rect.right = npc.rect.left
                if self.velocity[0] < 0:
                    self.rect.left = npc.rect.right

        #check for collision with map in y direction
        # self.rect.centery += self.velocity[1]
        for npc in npc_list:
            if npc.rect.colliderect(self.rect):
                if self.velocity[1] > 0:
                    self.rect.bottom = npc.rect.top
                if self.velocity[1] < 0:
                    self.rect.top = npc.rect.bottom

        self.image = self.get_animation_frame()
        self.mask = pygame.mask.from_surface(self.image)
        
        for obstacle in obstacle_tiles:
            if obstacle[1].colliderect(self.rect):
                if self.velocity[0] > 0:
                    self.rect.right = obstacle[1].left
                if self.velocity[0] < 0:
                    self.rect.left = obstacle[1].right

                         
        screen_scroll = [0, 0]

        #Moves the camera left and right 
        if self.rect.right > (constants.SCREEN_WIDTH - constants.SCROLL_THRESH):
            screen_scroll[0] = (constants.SCREEN_WIDTH - constants.SCROLL_THRESH) - self.rect.right
            self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESH
        if self.rect.left < constants.SCROLL_THRESH:
            screen_scroll[0] = constants.SCROLL_THRESH - self.rect.left
            self.rect.left = constants.SCROLL_THRESH

        #Moves the camera up and down
        if self.rect.top > (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH):
            screen_scroll[1] = (constants.SCREEN_HEIGHT - constants.SCROLL_THRESH) - self.rect.top
            self.rect.top = constants.SCREEN_HEIGHT - constants.SCROLL_THRESH
        if self.rect.bottom < constants.SCROLL_THRESH:
            screen_scroll[1] = constants.SCROLL_THRESH - self.rect.bottom
            self.rect.bottom = constants.SCROLL_THRESH
        
        return screen_scroll, exit_bool

        
    #put character on screen
    def draw(self, surface):
        #draw rect for development purposes
        # rect_img = pygame.surface.Surface(self.rect.size)
        # rect_img.fill((0, 0, 255))
        # surface.blit(rect_img, (self.rect.x, self.rect.y))

        
        #draw character
        surface.blit(self.get_animation_frame(), (self.rect.x, self.rect.y))

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
    def player_is_near(self, obj_position, threshold=80):
        player_x = self.get_x()
        player_y = self.get_y()
        
        distance_x = abs(player_x - obj_position[0])
        distance_y = abs(player_y - obj_position[1])
        
        return distance_x < threshold and distance_y < threshold

