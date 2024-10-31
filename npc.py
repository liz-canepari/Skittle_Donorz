# There are two classes in this file. The "object class" (or items ex: box, apple, anythning you can pickup) and the "Character class" (actual NPC's). 
# The character classes inherits from NPC class. 
# As of right now 10/8/24, this file does not interact with the game.py file, this is just an outline file.
# maybe collsions
import pygame

class Npc:
    def __init__(self, name, position, size, skin, can_interact, dialogue):
        self.name = name
        self.position = position
        self.size = size
        self.skin = pygame.image.load(skin).convert_alpha()
        self.skin = pygame.transform.scale(self.skin, self.size)
        self.can_interact = can_interact
        self.dialogue = dialogue
        self.rect = self.skin.get_rect(topleft=self.position)

    def interact(self):
        if self.can_interact:
            return self.dialogue
        
    def draw(self, screen):
        screen.blit(self.skin, self.rect)

def get_npc_list():
    return [
        Npc(name="Mentor", position=(328, 212), size=(64, 64), skin="images/sprites/mentor.png", can_interact=True,
            dialogue=[
                "Success...", "And Failure...", "Are Both Signs Of Progress.",
                "My Student...", "My Spikes Have Become Dull,", "My Breath Weak,",
                "And The Blood I Shed...", "Is No Longer Your Shield.", "I Love You...",
                "But Never Come Back Home."
            ]),
        # Add more NPCs here...
    ] # Draw the NPC image on the screen at its position


# create an NPC! here is the EX:

# Npc(name="Mentor", position=(328, 212), skin="images/sprites/mentor.png", can_interact=True,
#    dialogue=[
        # "Success...", "And Failure...", "Are Both Signs Of Progress.",
        # "My Student...", "My Spikes Have Become Dull,", "My Breath Weak,",
        # "And The Blood I Shed...", "Is No Longer Your Shield.", "I Love You...",
        # "But Never Come Back Home."
    # ]),

# then add it to the npc_list() below
# def get_npc_list():
#     return [
#             Npc(name="Mentor", position=(328, 212), size=(64, 64), skin="images/sprites/mentor.png", can_interact=True,
#                 dialogue=[
#                     "Success...", "And Failure...", "Are Both Signs Of Progress.",
#                     "My Student...", "My Spikes Have Become Dull,", "My Breath Weak,",
#                     "And The Blood I Shed...", "Is No Longer Your Shield.", "I Love You...",
#                     "But Never Come Back Home."
#                 ]),

#                 # add more npc down here. This is just a list that can be passed into main.
# ]







# green_item_skin = pygame.image.load("images/items/green_item.png")
# yellow_item_skin = pygame.image.load("images/items/yellow_item.png")
# blue_item_skin = pygame.image.load("images/items/blue_item.png")

# Creating Object instances for each item
# red_item = Object(red_item_skin, (100, 100), False, "Red Circle")
# green_item = Object(green_item_skin, (150, 100), False, "Green Circle")
# yellow_item = Object(yellow_item_skin, (200, 100), False, "Yellow Circle")
# blue_item = Object(blue_item_skin, (250, 100), False, "Blue Circle")