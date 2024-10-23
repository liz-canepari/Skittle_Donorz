import pygame

pygame.init()

# Set up display
screen = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Inventory System")

# font (taken from our game.py file)
font = pygame.font.Font(None, 36)

# These are the images that get shown as items, different color circles for each item
items = [pygame.Surface((50, 50), pygame.SRCALPHA) for x in range(4)]
pygame.draw.circle(items[0], (255, 0, 0), (25, 25), 25)  # Red circle
pygame.draw.circle(items[1], (0, 255, 0), (25, 25), 25)  # Green circle
pygame.draw.circle(items[2], (255, 255, 0), (25, 25), 25)  # Yellow circle
pygame.draw.circle(items[3], (0, 0, 255), (25, 25), 25)  # Blue circle


# The inventory system
class Inventory:
    def __init__(self):
        self.rows = 1  # Single row for simplicity
        self.col = 4  # Four columns for four items
        self.items = [[None for _ in range(self.rows)] for _ in range(self.col)]
        self.box_size = 50
        self.x = 50
        self.y = 400  # Place the inventory bar lower on the screen
        self.border = 5

    # Draw everything
    def draw(self):
        # Draw background for inventory
        pygame.draw.rect(screen, (100, 100, 100),
                         (self.x, self.y, (self.box_size + self.border) * self.col + self.border,
                          (self.box_size + self.border) * self.rows + self.border))
        # Draw individual inventory slots
        for x in range(self.col):
            for y in range(self.rows):
                rect = (self.x + (self.box_size + self.border) * x + self.border,
                        self.y + (self.box_size + self.border) * y + self.border, self.box_size, self.box_size)
                pygame.draw.rect(screen, (180, 180, 180), rect)
                if self.items[x][y]:
                    # Draw the item image in the slot
                    screen.blit(self.items[x][y][0], (rect[0], rect[1]))
                    # Display the item count
                    obj = font.render(str(self.items[x][y][1]), True, (0, 0, 0))
                    screen.blit(obj, (rect[0] + self.box_size // 2, rect[1] + self.box_size // 2))

    # Add an item to a specific slot based on keypress (e.g., 1 for slot 0, 2 for slot 1, etc.)
    def add_item(self, item, slot):
        if 0 <= slot < self.col:
            if self.items[slot][0]:  # If the slot already has an item
                self.items[slot][1] += item[1]  # Add the item count
            else:
                self.items[slot] = item  # Place the item in the slot