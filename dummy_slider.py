# import pygame

# class Slider:
#     def __init__(self, x, y, width, min_val, max_val, current_val):
#         self.x = x
#         self.y = y
#         self.width = width
#         self.height = 20
#         self.min_val = min_val
#         self.max_val = max_val
#         self.current_val = current_val
#         self.rect = pygame.Rect(x, y, width, self.height)
#         self.knob_x = self.x + (self.width * ((self.current_val - self.min_val) / (self.max_val - self.min_val)))

#     def draw(self, screen):
#         # Draw the slider line
#         pygame.draw.line(screen, 'gray', (self.x, self.y + self.height // 2), 
#                          (self.x + self.width, self.y + self.height // 2), 4)

#         # Draw the knob
#         pygame.draw.circle(screen, 'white', (int(self.knob_x), self.y + self.height // 2), 10)

#     def handle_event(self, event):
#         if event.type == pygame.MOUSEBUTTONDOWN:
#             if pygame.Rect(self.knob_x - 10, self.y, 20, self.height).collidepoint(event.pos):
#                 self.dragging = True
#         elif event.type == pygame.MOUSEBUTTONUP:
#             self.dragging = False
#         elif event.type == pygame.MOUSEMOTION:
#             if getattr(self, 'dragging', False):
#                 # Update knob position
#                 self.knob_x = max(self.x, min(event.pos[0], self.x + self.width))
#                 # Update current value
#                 self.current_val = self.min_val + ((self.knob_x - self.x) / self.width) * (self.max_val - self.min_val)

#     def get_value(self):
#         return self.current_val
