import pygame
import player
import constants

# class Tutorial():
#     def __init__(self, font):
#         self.font = font
#         self.message = None
#         self.showing = False

#     def show_message(self, message):
#         self.message = message
#         self.showing = True

#     def hide_message(self):
#         self.showing = False

#     def draw(self, screen):
#         if self.showing and self.message:
#             bubble_width = 400
#             bubble_height = 50
#             bubble_x = (constants.SCREEN_WIDTH - bubble_width) // 2
#             bubble_y = constants.SCREEN_HEIGHT - 100
#             pygame.draw.rect(screen, (255, 255, 255), (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
#             pygame.draw.rect(screen, (0, 0, 0), (bubble_x, bubble_y, bubble_width, bubble_height), 3, border_radius=10)
#             text_surface = self.font.render(self.message, True, (0, 0, 0))
#             screen.blit(text_surface, (bubble_x + 20, bubble_y + 10))

import pygame
import math

import pygame
import math

class TutorialManager:
    def __init__(self):
        self.messages = []  # List to hold all tutorial messages with positions and display status
        
        # Add all tutorial messages here, if you need to make a new message for the user, include the Position, Message, and Displayed. Thats it!
        self.messages.append({
            "position": (328, 212), 
            "message": "Press E to talk to the Mentor.", 
            "displayed": False
        })
        self.messages.append({
            "position": (150, 300), 
            "message": "Press E to examine the mysterious object.", 
            "displayed": False
        })
        # Add more tutorial messages as needed
    
    def display_proximity_message(self, player_position, threshold, screen, font):
        """Displays the tutorial message if the player is near an unseen message location."""
        for tutorial in self.messages:
            position = tutorial["position"]
            message = tutorial["message"]
            # Check distance only if the message hasn't been displayed
            if not tutorial["displayed"]:
                self.draw_message_bubble(screen, font, message)
                # distance = math.sqrt((player_position[0] - position[0]) ** 2 + (player_position[1] - position[1]) ** 2)
                # if distance < threshold:
                #     print('over here')
                #     self._draw_message_bubble(screen, font, message)
                #     tutorial["displayed"] = True  # Mark as displayed once shown
                tutorial["displayed"] = True

    def show_message(self, message):
        self.current_message = message 

    def draw_message_bubble(self, screen, font, message):
        """Draws the message bubble on the screen."""
        bubble_width = 200
        bubble_height = 40
        bubble_x = (screen.get_width() - bubble_width) // 2
        bubble_y = screen.get_height() - bubble_height - 50

        pygame.draw.rect(screen, (255, 255, 255), (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), (bubble_x, bubble_y, bubble_width, bubble_height), 3, border_radius=10)
        
        # Render and display the message text
        text_surface = font.render(message, True, (0, 0, 0))
        screen.blit(text_surface, (bubble_x + 10, bubble_y + 10))

    def reset_messages(self):
        """Resets the display status of all tutorial messages."""
        for position in self.displayed_messages:
            self.displayed_messages[position]["shown"] = False
