import pygame
import csv
import constants
import player
<<<<<<< HEAD
from dialogue import setup_npc_data
from dialogue import DialogueManager
=======
import background
from world import World
from dialouge import setup_npc_data 
>>>>>>> 24ff85ac1710a2df188f2a19b88e96c7602353f0

#animation code from coding with russ tutorial
#https://www.youtube.com/watch?v=nXOVcOBqFwM&t=33s
 
pygame.init()
 
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Sprite")
 
bg = background.Background("images/scenes/room.png", 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)

#define game variables
level = 1

# --------------------------------------------------------------------------Room/Tileset Code---------------------------------------------------------------------------
#load tilemap images
tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"images/tiles/test_tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILESIZE, constants.TILESIZE))
    tile_list.append(tile_image)

#create empty tile list
world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)
#load in level data and create world
with open("levels/test_level_1.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter = ",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            print(f"{x}, {y}")
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
npc_data = setup_npc_data()
font = pygame.font.Font(None, 36)

# Track dialogue state
current_dialogue = ""
current_dialogue_manager = None
showing_dialogue = False
 
# --------------------------------------------------------------------------Main Game Code---------------------------------------------------------------------------

run = True
while run:
    #update background
    screen.fill((0, 0, 0))
    bg.draw(screen)

    world.draw(screen)
    draw_grid()
 
    #update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= animation_cooldown:
        player.set_frame(frame + 1)
        frame = player.get_frame()
        last_update = current_time
        if frame >= len(player.get_animation()):
            player.set_frame(0)
            frame = player.get_frame()
 

    #show frame image
    # box.draw(screen)
    for npc_entry in npc_data:
        npc_entry['npc'].draw(screen)
    player.draw(screen)


# threshold is number of pixels the user has to be in order to interact with the object.
    for npc_entry in npc_data:
        npc = npc_entry['npc']
        if player.player_is_near(npc.position, threshold=40):
            npc.interact = True
        else:
            npc.interact = False


<<<<<<< HEAD
    # Event handler
=======

    #event handler
>>>>>>> 24ff85ac1710a2df188f2a19b88e96c7602353f0
    for event in pygame.event.get():
        # close the game
        if event.type == pygame.QUIT:
            run = False
        # take keyboard presses
        if event.type == pygame.KEYDOWN:
            if not showing_dialogue:  # Allow movement only if not showing dialogue
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


            if event.key == pygame.K_e:  # Interact with NPC or advance dialogue
                if showing_dialogue:
                    # If already showing dialogue, advance to the next line or end dialogue
                    if current_dialogue_manager.has_more_dialogues():
                        current_dialogue = current_dialogue_manager.next_line()
                    else:
                        # End of dialogue, reset states
                        showing_dialogue = False
                        current_dialogue = ""  # Clear dialogue once finished
                        current_dialogue_manager = None  # Clear current dialogue manager
                else:
                    # Interact with NPC to start dialogue
                    for npc_entry in npc_data:
                        npc = npc_entry['npc']
                        if npc.interact:  # Check if NPC is interactable (near the player)
                            dialogue_manager = npc_entry['dialogue_manager']
                            if dialogue_manager.has_more_dialogues():
                                current_dialogue = dialogue_manager.next_line()
                                current_dialogue_manager = dialogue_manager
                                showing_dialogue = True
                            else:
                                # Reset the dialogue manager to allow repeated conversation
                                dialogue_manager.reset_dialogue()
                                showing_dialogue = False

                    
        if event.type == pygame.KEYUP:
            if not showing_dialogue:
                player.stand_still()

        # Handle continuous movement by checking keys directly
        keys = pygame.key.get_pressed()
        if not showing_dialogue:  # Prevent movement while showing dialogue
            if keys[pygame.K_a]:
                player.move_left()
                action = player.get_action()
                frame = player.get_frame()
            elif keys[pygame.K_d]:
                player.move_right()
                action = player.get_action()
                frame = player.get_frame()
            elif keys[pygame.K_w]:
                player.move_up()
                action = player.get_action()
                frame = player.get_frame()
            elif keys[pygame.K_s]:
                player.move_down()
                action = player.get_action()
                frame = player.get_frame()
    

# if npc had dialouge, print to the screen. the other stuff is for the text bubble at the bottom of the screen
    if showing_dialogue:
        bubble_width = constants.SCREEN_WIDTH 
        bubble_height = 100
        bubble_x = 0
        bubble_y = constants.SCREEN_HEIGHT - bubble_height
        pygame.draw.rect(screen, (255, 255, 255), (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
        pygame.draw.rect(screen, (0, 0, 0), (bubble_x, bubble_y, bubble_width, bubble_height), 3, border_radius=10)
        text_surface = font.render(current_dialogue, True, (0, 0, 0))
        screen.blit(text_surface, (bubble_x + 20, bubble_y + 30))

    player.update()
    pygame.display.update()
 
pygame.quit()
 