import pygame
 
class Npc:
    def __init__(self, name, x, y, size, skin, can_interact, dialogue, dialogue_img): 
        self.name = name
        self.size = size
        self.skin = pygame.image.load(skin).convert_alpha()
        self.skin = pygame.transform.scale(self.skin, self.size)
        self.dialogue_img = pygame.image.load(dialogue_img).convert_alpha() if dialogue_img else None
        self.can_interact = can_interact
        self.dialogue = dialogue
        self.rect = pygame.Rect(x, y, 64, 64)
 
    def interact(self):
        if self.can_interact:
            return self.dialogue
       
    def draw(self, screen):
        screen.blit(self.skin, self.rect)
 
    def get_x(self):
        return self.rect.x
   
    def get_y(self):
        return self.rect.y
    
    def update(self, screen_scroll):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
 
def get_npc_list():
    return [
            Npc(name="Mentor", x=305, y=180, size=(64, 64), skin="images/sprites/mentor.png", can_interact=True,
                dialogue=[
                    "Success...", "And Failure...", "Are Both Signs Of Progress.",
                    "My Student...", "My Spikes Have Become Dull,", "My Breath Weak,",
                    "And The Blood I Shed...", "Is No Longer Your Shield.", "I Love You...",
                    "But Never Come Back Home."
            ], dialogue_img="images/sprites/mentor-dialogue-img.png"),
        # Add more NPCs here...
    ] # Draw the NPC image on the screen at its position