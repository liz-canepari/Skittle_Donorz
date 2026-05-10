import pygame
import constants
from slider import Slider  # Assuming you have a Slider class

# Initialize the volume slider
volume_slider = Slider(constants.SCREEN_WIDTH // 2 - 150, 200, 300, 0.0, 1.0, 0.5)  # Adjust the dimensions as needed

def draw_settings_menu(screen, font):
    # Draw semi-transparent overlay
    overlay = pygame.Surface((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((128, 128, 128, 150))
    screen.blit(overlay, (0, 0))

    # Render settings title
    title_text = font.render('Settings', True, 'black')
    title_rect = title_text.get_rect(center=(constants.SCREEN_WIDTH // 2, 50))
    screen.blit(title_text, title_rect)

    # Render volume label
    volume_text = font.render('Volume:', True, 'black')
    volume_label = volume_slider.x - volume_text.get_width() - 10
    volume_label_rect = volume_text.get_rect(topleft=(volume_label, 200))
    screen.blit(volume_text, volume_label_rect)

    # Draw the volume slider
    volume_slider.draw(screen)

    # Back to game button
    back_text = font.render('Press B to Return', True, 'black')
    back_rect = back_text.get_rect(center=(constants.SCREEN_WIDTH // 2, constants.SCREEN_HEIGHT - 50))
    screen.blit(back_text, back_rect)

def handle_settings_event(event):
    """Handle input for the settings menu."""
    global volume_slider
    volume_slider.handle_event(event)


def get_volume():
    """Return the current volume set by the slider."""
    return volume_slider.get_value()
