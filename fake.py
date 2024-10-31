import pygame
import csv
import constants
import player
import background
import tutorial
import npc
from inventory import player_inventory
from world import World
from dialogue import DialogueManager, check_npc_interaction, process_npc_dialogue

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Skittle Game")

# Define game variables
level = 1

# Load tilemap images
tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"images/tiles/mentor_hut_tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILESIZE, constants.TILESIZE))
    tile_list.append(tile_image)

# Create empty tile list
world_data = [[-1] * constants.COLS for _ in range(constants.ROWS)]

# Load in level data and create world
with open("levels/mentors_hut_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter=",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
world.process_data(world_data, tile_list)

def draw_grid():
    for x in range(30):
        pygame.draw.line(screen, constants.WHITE, (x * constants.TILESIZE, 0), (x * constants.TILESIZE, constants.SCREEN_HEIGHT))
        pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILESIZE), (constants.SCREEN_WIDTH, x * constants.TILESIZE))

# Initialize Player
game_player = player.Player(400, 250, 0, 0, "images/sprites/chameleon-sprite.png")

# NPC Code
font = pygame.font.Font(None, 36)
the_npc_list = npc.initialize_npc_list()  # Initialize NPCs using a function
# Track dialogue state
current_dialogue = None
showing_dialogue = False
dialogue_manager_ref = {'current': None}

# Inventory
inventory_open = False

# Tutorial Code
npc_interaction_shown = False

# Main Game Loop
run = True
while run:
    # Update background
    screen.fill((0, 0, 0))
    world.draw(screen)
    # draw_grid()

    # Update animations
    current_time = pygame.time.get_ticks()
    if current_time - game_player.last_update >= game_player.animation_cooldown:
        game_player.update_animation()
    
    # Draw NPCs and Player
    for npc in the_npc_list:
        npc.draw(screen)
    game_player.draw(screen)

    # Check for NPC interactions
    check_npc_interaction(game_player, the_npc_list, tutorial)

    # Event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                game_player.move_left()
                tutorial.hide_message()
            if event.key == pygame.K_d:
                game_player.move_right()
                tutorial.hide_message()
            if event.key == pygame.K_w:
                game_player.move_up()
                tutorial.hide_message()
            if event.key == pygame.K_s:
                game_player.move_down()
                tutorial.hide_message()
            if event.key == pygame.K_e:
                # Trigger dialogue interaction
                result = process_npc_dialogue(event, the_npc_list, tutorial, {'current': None})
                if result:
                    current_dialogue, showing_dialogue = result
                    tutorial.hide_message()

        # Logic for key releases
        if event.type == pygame.KEYUP:
            game_player.handle_key_release(event)

        if event.key == pygame.K_i:
            inventory_open = not inventory_open

    if showing_dialogue and current_dialogue:
        DialogueManager.display_bubble(current_dialogue)

    if inventory_open:
        player_inventory.draw()

    # Draw tutorial
    tutorial.draw(screen)

    # Update player logic
    game_player.update()
    pygame.display.update()


# Example of game loop: test for collision with rect.
# def game_loop(screen, player_rect):
#     npcs = npc_list()  # Get the list of NPCs
#     for npc in npcs:
#         npc.draw(screen)  # Draw NPCs
#         if npc.rect.colliderect(player_rect):  # Check for collision with the player
#             print(f"{npc.name} is colliding with the player!")