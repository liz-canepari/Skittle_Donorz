import datetime
import pygame
import constants
import tutorial
from npc import get_npc_list
from datetime import datetime, timedelta
 
pygame.init()
 
# Screen setup
screen = pygame.display.set_mode((500, 500))
 
# Font setup
font = pygame.font.Font("fonts/Silkscreen-Regular.ttf", 24)
 
DIALOGUE_DELAY = 1
last_dialogue_time = datetime.now()
 
class DialogueManager:
    def __init__(self):
 
        # for every character create their dialogue here
        self.dialogue={
            "mentor": [
                "Success...", "And Failure...", "Are Both Signs Of Progress.",
                "My Student...", "My Spikes Have Become Dull,", "My Breath Weak,",
                "And The Blood I Shed...", "Is No Longer Your Shield.", "I Love You...",
                "But Never Come Back Home." ],
        }
        self.current_dialogue = None
        self.dialogue_index = 0
        self.showing_dialogue = False
 
    def display_bubble(self, text, img):
        """Display the dialogue bubble with the given text on screen."""
        bubble_width = constants.SCREEN_WIDTH-100
        bubble_height = 100
        bubble_x = 100
        bubble_y = constants.SCREEN_HEIGHT - bubble_height
        frame = pygame.image.load("images/dialogue-frame.png").convert_alpha()
        screen.blit(img, (0, bubble_y))
        pygame.draw.rect(screen, (212, 213, 186), (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
        screen.blit(frame, (bubble_x, bubble_y))
        #pygame.draw.rect(screen, (0, 0, 0), (bubble_x, bubble_y, bubble_width, bubble_height), 3, border_radius=10)
        text_surface = font.render(text, True, (55, 46, 46))
        screen.blit(text_surface, (bubble_x + 20, bubble_y + 30))
 
def process_npc_dialogue(npc, index):
    """Process and display the entire dialogue of the NPC if interaction is allowed."""
    # print(npc.dialogue)
    dialogue = npc.dialogue
    line = dialogue[index]
    print(line)
    # DialogueManager.display_bubble(line, line)
    return line
