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
        self.rows = 3
        self.col = 9
        self.items = [[None for _ in range(self.rows)] for _ in range(self.col)]
        self.box_size = 40
        self.x = 50
        self.y = 50
        self.border = 3

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
                    screen.blit(self.items[x][y][0].resize(self.box_size), rect)
                    # Display the item count
                    obj = font.render(str(self.items[x][y][1]), True, (0, 0, 0))
                    screen.blit(obj, (rect[0] + self.box_size // 2, rect[1] + self.box_size // 2))

    # Get the square that the mouse is over
    def Get_pos(self):
        mouse = pygame.mouse.get_pos()
        x = mouse[0] - self.x
        y = mouse[1] - self.y
        x = x // (self.box_size + self.border)
        y = y // (self.box_size + self.border)
        return (x, y)

    # Add an item/s
    def Add(self, item, xy):
        x, y = xy
        if self.items[x][y]:
            if self.items[x][y][0].id == item[0].id:
                self.items[x][y][1] += item[1]
            else:
                temp = self.items[x][y]
                self.items[x][y] = item
                return temp
        else:
            self.items[x][y] = item

    # Check whether the mouse is in the grid
    def In_grid(self, x, y):
        if 0 > x > self.col - 1:
            return False
        if 0 > y > self.rows - 1:
            return False
        return True

# Initialize player inventory
player_inventory = Inventory()



