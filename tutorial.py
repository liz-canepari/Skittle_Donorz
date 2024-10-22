import pygame

class Tutorial:
    def __init__(self, screen_width, screen_height, font):
        self.steps = {
            "movement": "Use WASD to move",
            "interaction": "Press E to talk to friends",
        }

        self.active_step = None
        self.font = font
        self.finished = False
        self.screen_width = screen_width
        self.screen_height = screen_height
        
    def show_movement_instruction(self):
        """Show the movement instruction."""
        self.active_step = "movement"
        print(f"Movement instruction shown: {self.steps[self.active_step]}")

    def show_interaction_instruction(self):
        """Show the interaction instruction."""
        self.active_step = "interaction"
        

    def hide_tutorial(self):
        """Hide the tutorial step."""
        self.active_step = None

    def is_active(self):
        """Check if a tutorial step is currently active."""
        print(f"Active step: {self.active_step}")
        return self.active_step is not None

    def draw(self, screen):
        """Render the current active tutorial step on the screen."""
        if self.active_step:
            print(f"Drawing tutorial: {self.steps[self.active_step]}")
            tutorial_text = self.steps[self.active_step]
            bubble_width = self.screen_width
            bubble_height = 100
            bubble_x = 0
            bubble_y = self.screen_height - bubble_height
            pygame.draw.rect(screen, (255, 255, 255), (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), (bubble_x, bubble_y, bubble_width, bubble_height), 3, border_radius=10)
            text_surface = self.font.render(tutorial_text, True, (0, 0, 0))
            screen.blit(text_surface, (bubble_x + 20, bubble_y + 30))