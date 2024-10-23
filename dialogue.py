# Porter Brien
import pygame

from inanimateObj import Character


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


# Function to set up NPCs and their dialogues
def setup_npc_data():
    npc_data = []

    # Mentor NPC
    mentor_image = pygame.image.load("images/sprites/mentor.png").convert_alpha()
    mentor_image = pygame.transform.scale(mentor_image, (64, 64))
    mentor = Character(mentor_image, [350, 245], interact=True, dialogue="Hello there!")

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
