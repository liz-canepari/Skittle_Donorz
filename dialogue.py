# dialogue.py
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
font = pygame.font.Font(None, 36)

# 
DIALOGUE_DELAY = 1
last_dialogue_time = datetime.now()

class DialogueManager:
    def __init__(self):
        self.current_dialogue = None
        self.dialogue_index = 0
        self.showing_dialogue = False

    def next_line(self):
        """Return the next line of dialogue or end if complete."""
        if self.current_dialogue and self.dialogue_index < len(self.current_dialogue):
            line = self.current_dialogue[self.dialogue_index]
            self.dialogue_index += 1
            return line
        else:
            # Dialogue ended
            self.showing_dialogue = False
            self.current_dialogue = None
            self.dialogue_index = 0
            return None

    def has_more_dialogues(self):
        """Check if there are more dialogues left."""
        return self.current_dialogue and self.dialogue_index < len(self.current_dialogue)

    def display_bubble(self, text):
        """Display the dialogue bubble with the given text on screen."""
        if self.showing_dialogue:
            bubble_width = constants.SCREEN_WIDTH
            bubble_height = 100
            bubble_x = 0
            bubble_y = constants.SCREEN_HEIGHT - bubble_height
            pygame.draw.rect(screen, (255, 255, 255), (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), (bubble_x, bubble_y, bubble_width, bubble_height), 3, border_radius=10)
            text_surface = font.render(text, True, (0, 0, 0))
            screen.blit(text_surface, (bubble_x + 20, bubble_y + 30))

def check_npc_interaction(player, npc_list, dialogue_manager):
    """Check if the player is near any NPC and show interaction prompt."""
    for npc in npc_list:
        if player.rect.colliderect(npc.rect):
            dialogue_manager.display_bubble(f"Press E to interact with {npc.name}")
            return npc

def process_npc_dialogue(dialogue_manager, npc, can_interact):
    """Process the dialogue for the current NPC interaction."""
    print(dialogue_manager)
    print(npc)
    print(npc.can_interact)
    print(npc.dialogue)
    if can_interact:
        # Check if there are more lines to display
        if npc.dialogue and dialogue_manager.dialogue_index < len(npc.dialogue):
            # Get the next line of dialogue
            line = npc.dialogue[dialogue_manager.dialogue_index]
            dialogue_manager.display_bubble(line)  # Display the dialogue bubble with the line
            dialogue_manager.dialogue_index += 1  # Move to the next line
        else:
            # If no more dialogue, hide the dialogue
            dialogue_manager.showing_dialogue = False
            dialogue_manager.current_dialogue = None
            dialogue_manager.dialogue_index = 0
