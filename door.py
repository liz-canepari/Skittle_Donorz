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
        self.rect[0] += screen_scroll[0]
        self.rect[1] += screen_scroll[1]


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

        #issue: is there a way to do things with the tiles and not just straight coordinates? 
        #I'd like to be able to just take the coordinates from the tile where the door is supposed to be
        #Something I can do in the world file...?

    
