import pygame
import constants
import world

class Door():
    
    def __init__(self, door_x, door_y, reposition_x, reposition_y, new_room_number):
       self.reposition_x = reposition_x
       self.reposition_y = reposition_y
       self.new_room_number = new_room_number
       self.rect = pygame.Rect(door_x, door_y, constants.TILESIZE, constants.TILESIZE)


    """
    Function to move the doors along with the player's movement, need to connect to screen scroll function
    """
    def update(self, screen_scroll):
        self.rect[0] += screen_scroll[0]
        self.rect[1] += screen_scroll[1]


    """
    Function to draw the doors onto the screen
    """
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 0)

    
    """
    Getter function for the new coordinates and room number
    """
    def get_new_room_number(self):
        return self.new_room_number
    
    def get_new_x(self):
        return self.reposition_x

    def get_new_y(self):
        return self.reposition_y


    
