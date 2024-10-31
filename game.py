import pygame
import csv
import constants
import player
import background
import npc
from tutorial import TutorialManager
from npc import get_npc_list
from inventory import player_inventory
from world import World
from dialogue import DialogueManager, check_npc_interaction, process_npc_dialogue


#animation code from coding with russ tutorial
#https://www.youtube.com/watch?v=nXOVcOBqFwM&t=33s
 
pygame.init()
 
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Skittle Game")
 
#define game variables
level = 1

# --------------------------------------------------------------------------Room/Tileset Code---------------------------------------------------------------------------
#load tilemap images
tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"images/tiles/mentor_hut_tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILESIZE, constants.TILESIZE))
    tile_list.append(tile_image)

#create empty tile list
world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)
#load in level data and create world
with open("levels/mentors_hut_data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter = ",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)


world = World()
world.process_data(world_data, tile_list)

def draw_grid():
    for x in range(30):
        pygame.draw.line(screen, constants.WHITE, (x * constants.TILESIZE, 0), (x * constants.TILESIZE, constants.SCREEN_HEIGHT))
        pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILESIZE), (constants.SCREEN_WIDTH, x * constants.TILESIZE))

# --------------------------------------------------------------------------Player Code---------------------------------------------------------------------------

player = player.Player(400, 250, 0, 0, "images/sprites/chameleon-sprite.png")
 
action = player.get_action()
last_update = pygame.time.get_ticks()
animation_cooldown = 110
frame = player.get_frame()

#---------------------------------------------------------------------------NPC Code-------------------------------------------------------------------------------------------
# NPCs and their dialogue managers from the dialouge.py file
dialogue_manager = DialogueManager()
font = pygame.font.Font(None, 36)
# Track dialogue state
current_npc = None
current_dialogue = None
current_dialogue_manager = None
showing_dialogue = False
dialogue_manager_ref = {'current': None} 
npc_list = get_npc_list()   
# ---------------------------------------------------------------------------Inventory-------------------------------------------------------------------------------
# Variable to track if inventory is open or closed
inventory_open = False
selected = None 
# --------------------------------------------------------------------------Tutorial Code---------------------------------------------------------------------------
tutorial_manager = TutorialManager()
npc_interaction_shown = False
# tutorial = Tutorial(font)
# tutorial.show_message("Use WASD to move")
# --------------------------------------------------------------------------Main Game Code---------------------------------------------------------------------------
run = True
while run:
    #update background
    screen.fill((0, 0, 0))
    # world.draw(screen)
    #draw_grid()
    screen.fill((0, 0, 0))
    world.draw(screen)

    for npc in npc_list:
        npc.draw(screen)
        if player.player_is_near(npc.position):
            tutorial_manager.display_proximity_message(player.position, 40, screen, font)

    player.draw(screen)

    # tutorial_manager.display_proximity_message()

 
    #update animations (currently only chameleon, but can add other animated sprites here)
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        player.set_frame(frame + 1)
        frame = player.get_frame()
        last_update = current_time
        if frame >= len(player.get_animation()):
            player.set_frame(0)
            frame = player.get_frame()

    interacting_npc = check_npc_interaction(player, npc_list, dialogue_manager)

    #event handler
    for event in pygame.event.get():
        # close the game
        if event.type == pygame.QUIT:
            run = False
        process_npc_dialogue(event, dialogue_manager, interacting_npc)

        # take keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.move_left()
                action = player.get_action()
                frame = player.get_frame()
            if event.key == pygame.K_d:
                player.move_right()
                action = player.get_action()
                frame = player.get_frame()
            if event.key == pygame.K_w:
                player.move_up()
                action = player.get_action()
                frame = player.get_frame()
            if event.key == pygame.K_s:
                player.move_down()
                action = player.get_action()
                frame = player.get_frame()







            if event.key == pygame.K_e:
                if not dialogue_manager.showing_dialogue:
                    current_npc = check_npc_interaction(player, npc_list, dialogue_manager)
                    if current_npc:
                        # Load NPC's dialogue and activate dialogue
                        dialogue_manager.load_dialogue(current_npc.dialogue)
                        dialogue_active = True
                    # If dialogue is active, process the next line
                    if dialogue_active:
                        line = process_npc_dialogue(event, dialogue_manager, current_npc)
                        if line:
                            # Display the current line of dialogue
                            dialogue_manager.display_bubble(line)
                        else:
                            # End of dialogue, deactivate
                            dialogue_active = False






        #Logic for if key is releasedw
        if event.type == pygame.KEYUP:
            pressed = pygame.key.get_pressed()
            if event.key == pygame.K_a:
                player.stand_still()
                if pressed[pygame.K_w]:
                    player.move_up()
                elif pressed[pygame.K_s]:
                    player.move_down()
                elif pressed[pygame.K_d]:
                    player.move_right()
            if event.key == pygame.K_d:
                player.stand_still()
                if pressed[pygame.K_w]:
                    player.move_up()
                elif pressed[pygame.K_s]:
                    player.move_down()
                elif pressed[pygame.K_a]:
                    player.move_left()
            if event.key == pygame.K_w:
                player.stand_still()
                if pressed[pygame.K_a]:
                    player.move_left()
                elif pressed[pygame.K_d]:
                    player.move_right()
                elif pressed[pygame.K_s]:
                    player.move_down()
            if event.key == pygame.K_s:
                player.stand_still()
                if pressed[pygame.K_a]:
                    player.move_left()
                elif pressed[pygame.K_d]:
                    player.move_right()
                elif pressed[pygame.K_w]:
                    player.move_up()
            if event.key == pygame.K_i:
                inventory_open = not inventory_open

    if dialogue_manager.showing_dialogue and dialogue_manager.has_more_dialogues():
        line = dialogue_manager.next_line()  # Fetch the current dialogue line
        dialogue_manager.display_bubble(line)

    if inventory_open:
        player_inventory.draw()

    # Update player logic
    player.update()
    pygame.display.update()