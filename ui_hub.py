# this is going to be a different screen for the user, it will be an overlay with all the important buttons on it.
import pygame

class UIHub:
    def __init__(self):
        self.elements = []

    def add_element(self, element):
        """Add a UI element (e.g., a button or slider) to the hub."""
        self.elements.append(element)

    def draw(self, screen):
        """Draw all UI elements."""
        for element in self.elements:
            element.draw(screen)

    def handle_events(self, event):
        """Handle events for all UI elements."""
        for element in self.elements:
            element.handle_event(event)
