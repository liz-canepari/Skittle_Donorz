# Adds pygame library to the program
import pygame

# Starts up pygame
pygame.init()

# Creates variables for screen width/height and sets the game screen to that size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Creates rectangle for player to control
player = pygame.Rect((300, 250, 50, 50))

# Loop for the actual game
run = True
while run:

    screen.fill((0, 0, 0))

    pygame.draw.rect(screen, (255, 0, 0), player)

    # Waits for player input, moves the player's rectangle when appropriate button is pressed (uses WASD keys)
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:     # Move left using A
        player.move_ip(-1, 0)
    if key[pygame.K_d] == True:     # Move right using D
        player.move_ip(1, 0)
    if key[pygame.K_w] == True:     # Move up using W
        player.move_ip(0, -1)
    if key[pygame.K_s] == True:     # Move down using S
        player.move_ip(0, 1)

    # ends main game loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
