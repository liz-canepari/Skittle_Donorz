# There are two classes in this file. The "object class" (or items ex: box, apple, anythning you can pickup) and the "Character class" (actual NPC's). 
# The character classes inherits from NPC class. 
# As of right now 10/8/24, this file does not interact with the game.py file, this is just an outline file.
# maybe collsions

import pygame

class Object(pygame.sprite.Sprite):
    def __init__(self, skin, position, interact=False):

        pygame.sprite.Sprite.__init__(self)

        self.skin = skin  # Image file for the object or character
        self.position = position  # Position on the screen
        self.interact = interact # Boolean to track if interaction is possible
        self.rect = self.skin.get_rect()
        self.rect.center = self.position
        self.mask = pygame.mask.from_surface(self.skin)
   

    # Draw the object/character on the given surface
    def draw(self, surface):
        surface.blit(self.skin, self.position)

    def onInteract(self):
        if self.interact:
            print("You interacted with the object!")

class Character(Object):  # Inherit from your custom Object class
    def __init__(self, skin, position, interact=False, dialogue=""):

        pygame.sprite.Sprite.__init__(self)

        super().__init__(skin, position, interact) 
        self.rect = self.skin.get_rect()
        self.rect.center = self.position
        self.mask = pygame.mask.from_surface(self.skin)
        self.dialogue = dialogue
    
    def speak(self):
        if self.interact:
            print(f"NPC says: {self.dialogue}")


