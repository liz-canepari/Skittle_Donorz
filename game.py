import pygame
import csv
import constants
import player
import background
import inanimateObj
from tutorial import Tutorial
from world import World
from dialouge import setup_npc_data 
import object
from foreground import Foreground

#animation code from coding with russ tutorial
#https://www.youtube.com/watch?v=nXOVcOBqFwM&t=33s
 
pygame.init()

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Skittle Game")
 
#define game variables
level = 1
screen_scroll = [0, 0]

# --------------------------------------------------------------------------Room/Tileset Code---------------------------------------------------------------------------
#load tilemap images
tile_list = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"images/tiles/forest/background-tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILESIZE, constants.TILESIZE))
    tile_list.append(tile_image)

#create empty tile list
world_data = []
for row in range(constants.ROWS):
    r = [-1] * constants.COLS
    world_data.append(r)
#load in level data and create world
with open("levels/forest/forest-floor-data.csv", newline="") as csvfile:
    reader = csv.reader(csvfile, delimiter = ",")
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)


world = World()
world.process_data(world_data, tile_list)

tree = object.Object("images/tiles/forest/tree.png", 180, 180)
fg = Foreground()
fg.add_single_object(tree, "trees","levels/forest/forest-trees.data.csv")


def draw_grid():
    
    for x in range(30):
        pygame.draw.line(screen, constants.WHITE, (x * constants.TILESIZE, 0), (x * constants.TILESIZE, constants.SCREEN_HEIGHT))
        pygame.draw.line(screen, constants.WHITE, (0, x * constants.TILESIZE), (constants.SCREEN_WIDTH, x * constants.TILESIZE))

# --------------------------------------------------------------------------Player Code---------------------------------------------------------------------------
mc = player.Player(400, 250, 0, 0, "images/sprites/chameleon-sprite.png", 32, 32)

action = mc.get_action()
last_update = pygame.time.get_ticks()
FPS = 110
frame = mc.get_frame()

#---------------------------------------------------------------------------NPC Code-------------------------------------------------------------------------------------------
# NPCs and their dialogue managers from the dialouge.py file
npc_data = setup_npc_data()
dialogue_font = pygame.font.Font("fonts\Silkscreen-Regular.ttf", 24)
screen_font = pygame.font.Font("fonts\PressStart2P-Regular.ttf", 18)

# create npc sprite group for collision testing
npc_group = pygame.sprite.GroupSingle()
npc_group.add(npc_data[0]['npc'])

# Track dialogue state
current_dialogue = ""
current_dialogue_img = None
current_dialogue_manager = None
showing_dialogue = False

# --------------------------------------------------------------------------Tutorial Code---------------------------------------------------------------------------
tutorial = Tutorial(screen_font, screen)
tutorial.add_step("movement", "Move with WASD", (120, 10))
tutorial.add_step("interaction", "Interact with NPCs with E", (100, 10))
show_movement_tutorial = True
# --------------------------------------------------------------------------Main Game Code---------------------------------------------------------------------------

run = True
while run:
    #update background
    screen.fill((0, 0, 0))

    world.draw(screen)
    #draw_grid()
    #draw_grid()
 
    #update animations (currently only chameleon, but can add other animated sprites here)
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= FPS:
        mc.set_frame(frame + 1)
        frame = mc.get_frame()
        last_update = current_time
        if frame >= len(mc.get_animation()):
            mc.set_frame(0)
            frame = mc.get_frame()
 

    #show frame image
    # box.draw(screen)
    for npc_entry in npc_data:
        npc_entry['npc'].draw(screen)

    #draw player
    mc.draw(screen)

# threshold is number of pixels the user has to be in order to interact with the object.
    for npc_entry in npc_data:
        npc = npc_entry['npc']
        if mc.player_is_near(npc.position, threshold=40):
            npc.interact = True
            tutorial.show_step("interaction")
        else:
            npc.interact = False

    #event handler
    for event in pygame.event.get():
        # close the game
        if event.type == pygame.QUIT:
            run = False
        # take keyboard presses
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_a:
                mc.move_left()
                action = mc.get_action()
                frame = mc.get_frame()
                show_movement_tutorial = False
            if event.key == pygame.K_d:
                mc.move_right()
                show_movement_tutorial = False
                action = mc.get_action()
                frame = mc.get_frame()
            if event.key == pygame.K_w:
                mc.move_up()
                show_movement_tutorial = False
                action = mc.get_action()
                frame = mc.get_frame()
            if event.key == pygame.K_s:
                mc.move_down()
                show_movement_tutorial = False
                action = mc.get_action()
                frame = mc.get_frame()

# NPC dialogue manager logic 
            if event.key == pygame.K_e:
                tutorial.complete_step("interaction")
                for npc_entry in npc_data:
                    if npc_entry['npc'].interact:
                        dialogue_manager = npc_entry['dialogue_manager']
                        if dialogue_manager.has_more_dialogues():
                            current_dialogue = dialogue_manager.next_line()
                            current_dialogue_manager = dialogue_manager
                            showing_dialogue = True
                        else:
                            showing_dialogue = False
        #Logic for if key is released
        if event.type == pygame.KEYUP:
            pressed = pygame.key.get_pressed()
            if event.key == pygame.K_a:
                mc.stand_still()
                if pressed[pygame.K_w]:
                    mc.move_up()
                elif pressed[pygame.K_s]:
                    mc.move_down()
                elif pressed[pygame.K_d]:
                    mc.move_right()
            if event.key == pygame.K_d:
                mc.stand_still()
                if pressed[pygame.K_w]:
                    mc.move_up()
                elif pressed[pygame.K_s]:
                    mc.move_down()
                elif pressed[pygame.K_a]:
                    mc.move_left()
            if event.key == pygame.K_w:
                mc.stand_still()
                if pressed[pygame.K_a]:
                    mc.move_left()
                elif pressed[pygame.K_d]:
                    mc.move_right()
                elif pressed[pygame.K_s]:
                    mc.move_down()
            if event.key == pygame.K_s:
                mc.stand_still()
                if pressed[pygame.K_a]:
                    mc.move_left()
                elif pressed[pygame.K_d]:
                    mc.move_right()
                elif pressed[pygame.K_w]:
                    mc.move_up()

# if npc had dialogue, print to the screen. the other stuff is for the text bubble at the bottom of the screen
    if showing_dialogue:
        current_dialogue_img = pygame.image.load("images\sprites\mentor-dialogue-img.png").convert_alpha()
        dialogue_frame = pygame.image.load("images/dialogue-frame.png").convert_alpha()
        dialogue_frame.set_colorkey((0, 0, 0))
        bubble_width = constants.SCREEN_WIDTH - 100
        bubble_height = 100
        bubble_x = 100
        bubble_y = constants.SCREEN_HEIGHT - bubble_height
        screen.blit(current_dialogue_img, (0, bubble_y))
        pygame.draw.rect(screen, (214, 210, 185), (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
        screen.blit(dialogue_frame, (bubble_x, bubble_y))
        #pygame.draw.rect(screen, (0, 0, 0), (bubble_x, bubble_y, bubble_width, bubble_height), 3, border_radius=10)
        text_surface = dialogue_font.render(current_dialogue, True, (41, 25, 21))
        screen.blit(text_surface, (bubble_x + 20, bubble_y + 30))

# Draw tutorial if not finished
    tutorial.draw(screen)
    if show_movement_tutorial:
        tutorial.show_step("movement")
# update objects currently being used in the loops
    screen_scroll = player.update()
    world.update(screen_scroll)
    for npc in npc_data:
        npc['npc'].update(screen_scroll)

    mc.update()
    pygame.display.update()
 
pygame.quit()
 