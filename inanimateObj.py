# There are two classes in this file. The "object class" (or items ex: box, apple, anythning you can pickup) and the "Character class" (actual NPC's). 
# The character classes inherits from NPC class. 
# As of right now 10/8/24, this file does not interact with the game.py file, this is just an outline file.
# maybe collsions

class Object:
    def __init__(self, skin, position, interact=False):
        self.skin = skin  # Image file for the object or character
        self.position = position  # Position on the screen
        self.interact = interact  # Boolean to track if interaction is possible

    # Draw the object/character on the given surface
    def draw(self, surface):
        surface.blit(self.skin, self.position)

    #reposition the object by the screen_scroll 
    def update(self, screen_scroll):
        self.position[0] += screen_scroll[0]
        self.position[1] += screen_scroll[1]

    
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


