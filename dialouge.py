# Porter Brien

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
