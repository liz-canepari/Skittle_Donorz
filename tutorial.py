import pygame
import constants
class Tutorial():
    def __init__(self, font):
        self.font = font
        self.message = None
        self.showing = False

    def show_message(self, message):
        self.message = message
        self.showing = True

    def hide_message(self):
        self.showing = False

    def draw(self, screen):
        if self.showing and self.message:
            bubble_width = 400
            bubble_height = 50
            bubble_x = (constants.SCREEN_WIDTH - bubble_width) // 2
            bubble_y = constants.SCREEN_HEIGHT - 100
            pygame.draw.rect(screen, (255, 255, 255), (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), (bubble_x, bubble_y, bubble_width, bubble_height), 3, border_radius=10)
            text_surface = self.font.render(self.message, True, (0, 0, 0))
            screen.blit(text_surface, (bubble_x + 20, bubble_y + 10))