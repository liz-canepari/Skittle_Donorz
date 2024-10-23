# There are two classes in this file. The "object class" (or items ex: box, apple, anythning you can pickup) and the "Character class" (actual NPC's). 
# The character classes inherits from NPC class. 
# As of right now 10/8/24, this file does not interact with the game.py file, this is just an outline file.
# maybe collsions

import pygame


class Object:
    def __init__(self, skin, position, interact=False, item_name = None):
        self.skin = skin  # Image file for the object or character
        self.position = position  # Position on the screen
        self.interact = interact  # Boolean to track if interaction is possible
        self.item_name = item_name

    # Draw the object/character on the given surface
    def draw(self, surface):
        surface.blit(self.skin, self.position)

    def onInteract(self):
        if self.interact:
            print("You interacted with the object!")

class Character(Object):  # Inherit from your custom Object class
    def __init__(self, skin, position, interact=False, dialogue=""):
        super().__init__(skin, position, interact) 
        self.dialogue = dialogue
    
    def speak(self):
        if self.interact:
            print(f"NPC says: {self.dialogue}")



red_item_skin = pygame.image.load("images/sprites/apple.png")
# green_item_skin = pygame.image.load("images/items/green_item.png")
# yellow_item_skin = pygame.image.load("images/items/yellow_item.png")
# blue_item_skin = pygame.image.load("images/items/blue_item.png")

# Creating Object instances for each item
red_item = Object(red_item_skin, (100, 100), False, "Red Circle")
# green_item = Object(green_item_skin, (150, 100), False, "Green Circle")
# yellow_item = Object(yellow_item_skin, (200, 100), False, "Yellow Circle")
# blue_item = Object(blue_item_skin, (250, 100), False, "Blue Circle")