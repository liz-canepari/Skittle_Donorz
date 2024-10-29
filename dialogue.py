# Porter Brien
import pygame
import constants
from inanimateObj import Character

pygame.init()

screen = pygame.display.set_mode((500, 500))
# font (taken from our game.py file)
font = pygame.font.Font(None, 36)


class DialogueManager:
    def __init__(self, character_name, dialogues):
        """
        Initialize the dialogue manager with a character's name and a list of dialogues.
        """
        self.character_name = character_name
        self.dialogues = dialogues  # A list of dialogue strings
        self.current_index = 0      # Tracks the current dialogue

    def next_line(self):
        """
        Return the next line of dialogue and move to the next one.
        """
        if self.current_index < len(self.dialogues):
            dialogue = self.dialogues[self.current_index]
            self.current_index += 1
            return f"{self.character_name}: {dialogue}"
        else:
            return f"{self.character_name}: No more dialogues."

    def reset_dialogue(self):
        """
        Reset the dialogue back to the start.
        """
        self.current_index = 0

    def has_more_dialogues(self):
        """
        Check if there are more dialogues to show.
        """
        return self.current_index < len(self.dialogues)
    
    def display_bubble(current_dialogue):
        bubble_width = constants.SCREEN_WIDTH
        bubble_height = 100
        bubble_x = 0
        bubble_y = constants.SCREEN_HEIGHT - bubble_height
        pygame.draw.rect(screen, (255, 255, 255), (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), (bubble_x, bubble_y, bubble_width, bubble_height), 3, border_radius=10)
        text_surface = font.render(current_dialogue, True, (0, 0, 0))
        screen.blit(text_surface, (bubble_x + 20, bubble_y + 30))
    
    def process_npc_dialogue_interaction(event, npc_data, tutorial, dialogue_manager_ref):
        for npc_entry in npc_data:
            if npc_entry['npc'].interact:
                dialogue_manager = npc_entry['dialogue_manager']
                
                if dialogue_manager.has_more_dialogues():
                    current_dialogue = dialogue_manager.next_line()
                    dialogue_manager_ref['current'] = dialogue_manager  # Update the reference to track the ongoing dialogue
                    tutorial.hide_message()  # Hide tutorial message on interaction start
                    return current_dialogue, True
                else:
                    # End of dialogue: clear dialogue reference and bubble
                    dialogue_manager_ref['current'] = None
                    return None, False  # Signals to clear the dialogue bubble


# dialogue.py
def check_npc_interaction(player, npc_data, tutorial, threshold=40):
    # Checks proximity of the player to NPCs and manages interaction prompts.
    # Parameters:
    # - player: The player instance
    # - npc_data: List of NPC data containing NPC instances and positions
    # - tutorial: Tutorial or UI element to show messages
    # - threshold: Distance threshold for interaction
    npc_interaction_shown = False

    for npc_entry in npc_data:
        npc = npc_entry['npc']
        if player.player_is_near(npc.position, threshold=threshold):
            npc.interact = True
            if not npc_interaction_shown:
                tutorial.show_message("Press E to interact")
                npc_interaction_shown = True
        else:
            npc.interact = False



# Function to set up NPCs and their dialogues
def setup_npc_data():
    npc_data = []

    # Mentor NPC
    mentor_image = pygame.image.load("images/sprites/mentor.png").convert_alpha()
    mentor_image = pygame.transform.scale(mentor_image, (64, 64))
    mentor = Character(mentor_image, [328, 212], interact=True, dialogue="Hello there!")

    mentor_dialogues = DialogueManager("Mentor", [
        "Success...",
        "And Failure...",
        "Are Both Signs Of Progress.",
        "My Student...",
        "My Spikes Have Become Dull,",
        "My Breath Weak,",
        "And The Blood I Shed...",
        "Is No Longer Your Shield.",
        "I Love You...",
        "But Never Come Back Home."
    ])
    
    npc_data.append({'npc': mentor, 'dialogue_manager': mentor_dialogues})

    # Add more NPCs here if needed
    # Example:
    # villager_image = pygame.image.load("images/sprites/villager.png").convert_alpha()
    # villager_image = pygame.transform.scale(villager_image, (64, 64))
    # villager = Character(villager_image, [150, 300], interact=True)
    # villager_dialogues = DialogueManager("Villager", ["Good day!", "It's sunny today!"])
    # npc_data.append({'npc': villager, 'dialogue_manager': villager_dialogues})

    return npc_data
