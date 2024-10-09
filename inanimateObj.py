# There are two classes in this file. The "NPC class" (or items) and the "Character class" (actual NPC's). 
# The character classes inherits from NPC class. 
# As of right now 10/8/24, this file does not interact with the game.py file, this is just an outline file.
# maybe collsions

class NPC:
    def item(self, skin, position, interact ):
        # image.png hopefully
        self.skin = skin

        # tuple??? we just talked and said tuple was bad (try list)
        # position on screen (x and y)
        self.position = position

        # press E to interact
        # this will be the True or false value
        self.interact = interact

        ...

        def draw(self, surface):
            surface.blit(self.skin, self.position)
            # surface.blit(self.skin, self.position): blit is a method in pygame that draws one surface (in this case, the NPC’s skin) onto another surface (in this case, the surface where it will appear).

        # find out the the True or false value, then print the dialouge (this is like "you found the apple!").
        # call this function like "NPC1.onInteract()"
        def onInteract(self):
            if self.interact:
                print("You interacted with an NPC!")


class Character(NPC):
    def __init__(self, skin, position, interact, dialogue):
        super().__init__(skin, position, interact)
        self.dialogue = dialogue
    
    def speak(self):
        if self.interact:
            print(f"NPC says: {self.dialogue}")

    # Create Characters down here >>>>


