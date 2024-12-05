import pygame
import constants
class Tutorial:
    def __init__(self, font, screen):
        self.font = font
        self.screen = screen
        self.steps = {}
        self.completed_steps = set()

    def add_step(self, key, message, position):
         """Add a tutorial step identified by a key (e.g., 'movement', 'interaction')."""
         self.steps[key] = {"message": message, "position": position}

    def show_step(self, key):
        """Show the tutorial message for a specific key if it hasn't been completed."""
        if key not in self.completed_steps and key in self.steps:
            message = self.steps[key]["message"]
            position = self.steps[key]["position"]
            self.displayMessage(message, position)

    def complete_step(self, key):
        """Mark a tutorial step as completed."""
        self.completed_steps.add(key)

    def is_completed(self, key):
        return key in self.completed_steps
    def displayMessage(self, message, position):
        """Display the tutorial message on the screen."""
        text_surface = self.font.render(message, True, (255, 255, 255))
        self.screen.blit(text_surface, position)

    def reset(self):
        """Reset all tutorial steps (for debugging or game replay)."""
        self.completed_steps.clear()