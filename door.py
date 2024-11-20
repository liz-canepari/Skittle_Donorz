import pygame
import constants

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
        self.rect[2] += screen_scroll[0]
        self.rect[3] += screen_scroll[1]


    """
    Function to draw the doors onto the screen
    """
    def draw(self, screen):
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 0)

    

    """
    Function that will take player from room A to room B
    """
    def enter():
        pass


    
