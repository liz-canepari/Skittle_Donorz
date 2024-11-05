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
 
    def get_x(self):
        return self.position[0]
   
    def get_y(self):
        return self.position[1]
    
    def update(self, screen_scroll):
        self.position[0] += screen_scroll[0]
        self.position[1] += screen_scroll[1]
 
def get_npc_list():
    return [
            Npc(name="Mentor", position=[328, 212], size=(64, 64), skin="images/sprites/mentor.png", can_interact=True,
                dialogue=[
                    "Success...", "And Failure...", "Are Both Signs Of Progress.",
                    "My Student...", "My Spikes Have Become Dull,", "My Breath Weak,",
                    "And The Blood I Shed...", "Is No Longer Your Shield.", "I Love You...",
                    "But Never Come Back Home."
            ]),
        # Add more NPCs here...
    ] # Draw the NPC image on the screen at its position