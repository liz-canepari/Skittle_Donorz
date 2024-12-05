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
        self.original_image = self.animation_list[0][0]
        self.image = self.original_image
        self.rect = pygame.Rect(x, y, 60, 60)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = [velocity_x, velocity_y]
        self.facing_right = False

#-----------------------------------------------getters---------------------------------------
    def get_frame(self):
        return self.current_frame
    
    def get_action(self):
        return self.current_action
    
    def get_animation(self):
        return self.animation_list[self.current_action]
    
    def get_animation_frame(self):
        frame = self.animation_list[self.current_action][self.current_frame]  
        if self.facing_right:  
            return pygame.transform.flip(frame, True, False)  
        return frame
        
    
    def get_x(self):        
        return self.rect.centerx
    
    def get_y(self):
        return self.rect.centery
#-----------------------------------------------setters---------------------------------------
    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.position = [x, y]
    
    def set_frame(self, frame):
        self.current_frame=frame

    def set_action(self, action):
        self.current_action=action

    
    def set_velocity_x(self, x, y):
        self.velocity = [x, y]

    def set_speed(self, num):
        self.SPEED = num

    #Updates position of the player using velocity
    def update(self, obstacle_tiles, npc_list, collision_list, door_list, screen, debug = False):

        current_door = None

        #check for collision with map in x direction
        if self.velocity[0] > 0:
            for obstacle in obstacle_tiles:
                if obstacle[1].colliderect(pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.rect.width, self.rect.height)):
                    self.velocity[0] = 0
                    break
            for npc in npc_list:
                if npc.rect.colliderect(pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.rect.width, self.rect.height)):
                    self.velocity[0] = 0
                    break
                if npc.rect.colliderect(pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.rect.width, self.rect.height)):
                    self.velocity[0] = 0
                    break
            for door in door_list:
                if door.rect.colliderect(pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.rect.width, self.rect.height)):
                    current_door = door

        elif self.velocity[0] < 0:
            for obstacle in obstacle_tiles:
                if obstacle[1].colliderect(pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.rect.width, self.rect.height)):
                    self.velocity[0] = 0
                    break
            for npc in npc_list:
                if npc.rect.colliderect(pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.rect.width, self.rect.height)):
                    self.velocity[0] = 0
                    break
            for door in door_list:
                if door.rect.colliderect(pygame.Rect(self.rect.x + self.velocity[0], self.rect.y, self.rect.width, self.rect.height)):
                    current_door = door
                    break

        #check for collision with map in y direction
        if self.velocity[1] > 0:
            for obstacle in obstacle_tiles:
                if obstacle[1].colliderect(pygame.Rect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height)):
                    self.velocity[1] = 0
                    break
            for npc in npc_list:
                if npc.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height)):
                    self.velocity[1] = 0
                    break
            for door in door_list:
                if door.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height)):
                    current_door = door
                    break
        elif self.velocity[1] < 0:
            for obstacle in obstacle_tiles:
                if obstacle[1].colliderect(pygame.Rect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height)):
                    self.velocity[1] = 0
                    break
            for npc in npc_list:
                if npc.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height)):
                    self.velocity[1] = 0
                    break
            for door in door_list:
                if door.rect.colliderect(pygame.Rect(self.rect.x, self.rect.y + self.velocity[1], self.rect.width, self.rect.height)):
                    current_door = door
                    break

        #update player position
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


        #update animation
        self.image = self.get_animation_frame()
        self.mask = pygame.mask.from_surface(self.image)

                         
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

        if debug:
            for obstacle in obstacle_tiles:
                pygame.draw.rect(screen, (255, 0, 0), obstacle[1], 2)
            for npc in npc_list:
                pygame.draw.rect(screen, (255, 0, 0), npc.rect, 2)

            pygame.draw.rect(screen, (0, 255, 0), self.rect, 2)
        
        return screen_scroll, current_door

        
    #put character on screen
    def draw(self, surface):
        #draw rect for development purposes
        # rect_img = pygame.surface.Surface(self.rect.size)
        # rect_img.fill((0, 0, 255))
        # surface.blit(rect_img, (self.rect.x, self.rect.y))
        current_frame = self.get_animation_frame()
        current_frame.set_colorkey((0, 0, 0))
       
        surface.blit(current_frame, (self.rect.x, self.rect.y))
            

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

