import pygame
import csv
import constants
import player
import background
import npc
from npc import load_list
import tutorial
import button
import database
from inventory import Inventory
from world import World
from door import Door
from dialogue import DialogueManager
from foreground import Foreground
import button
from inputHandler import InputHandler
#animation code from coding with russ tutorial
#https://www.youtube.com/watch?v=nXOVcOBqFwM&t=33s


#TODO
# room transitions work, but the player spawns in slightly different places each time they change rooms. Why?
# - can i make every room start from the origin? maybe have it as a set reference point would help. 
# - figure out why the spawn point is always slightly off even though its a set number. What's changing it?
# the npc and inanimate objects base their position on the player, so need to figure out how to position them initially before the player enters
#

 
pygame.init()
database.create_connection()
database.create_tables()

pygame_icon = pygame.image.load('images/cq_chamaleon.png')
pygame.display.set_icon(pygame_icon)

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Chroma Quest")
 
#define game variables
room_number = 1
screen_scroll = [0, 0]
clock = pygame.time.Clock()

# --------------------------------------------------------------------------Room/Tileset Code---------------------------------------------------------------------------
world = World()
colors = []
#load tilemap images
tile_list = []
#create empty tile list
world_data = []
#create a list for doors
door_list = []
#variable to hold if a door has been walked through, and if so which door
current_door = None

#load in level data and create world
world.load_room(tile_list, world_data, door_list, room_number)

#door = Door(285, 350, 0, 0, 2)

fg = Foreground()
fg.load(room_number)

# --------------------------------------------------------------------------Player Code---------------------------------------------------------------------------
mc = player.Player(275, 350, 0, 0, "images/sprites/chameleon-sprite.png", 32, 32)

action = mc.get_action()
last_update = pygame.time.get_ticks()
last_update_npc = pygame.time.get_ticks()
last_update_fg = pygame.time.get_ticks()
FPS = 110
frame = mc.get_frame()
npc_frame = frame
#---------------------------------------------------------------------------NPC Code-------------------------------------------------------------------------------------------
# NPCs and their dialogue managers from the dialouge.py file
dialogue_index = -1 #need this
showing_dialogue = False # need this
speaker = None # need this
dialogue_start: 0 #will be used if mc speaks

# create group of all npc sprites
npc_list = load_list(room_number)

# ---------------------------------------------------------------------------Inventory-------------------------------------------------------------------------------
# Variable to track if inventory is open or closed
selected = None
player_inventory = Inventory()

# --------------------------------------------------------------------------Tutorial Code---------------------------------------------------------------------------
font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 18)
tutorial_manager = tutorial.Tutorial(font, screen)
tutorial_manager.add_step("movement", "Move with WASD", (120, 10))
tutorial_manager.add_step("interaction", "Interact with NPCs with E", (100, 10))
tutorial_manager.add_step("inventory", "Press I to open inventory", (100, 10))
# --------------------------------------------------------------------------Input Handler---------------------------------------------------------------------------
input_handler = InputHandler(mc, npc_list, tutorial_manager, player_inventory)
# --------------------------------------------------------------------------Main Game Code---------------------------------------------------------------------------

#create buttons
start_button = button.Button(constants.SCREEN_WIDTH // 2 - 300, constants.SCREEN_HEIGHT // 2 - 150, 'images/startbtn-sheet.png', 1)
exit_button = button.Button(constants.SCREEN_WIDTH // 2 + 50, constants.SCREEN_HEIGHT // 2 -150,'images/exitbtn-sheet.png', 1)
start_menu = background.Background('images/Chroma_Quest_Poster_Draft.jpg', 0, 0, constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT)

menu = True
while menu == True:
    #draw menu
    screen.fill((144, 201, 120))

    start_menu.draw(screen)
    #add buttons
    if start_button.draw(screen):
        menu = False
        run = True
    if exit_button.draw(screen):
        run = False
        menu = False

    #event handler
    for event in pygame.event.get():
        # close the game
        if event.type == pygame.QUIT:
            run = False
            menu = False

    pygame.display.update()

print(door_list)

while run:
    #control FPS
    clock.tick(constants.FPS)

    #update background
    screen.fill((0, 0, 0))

    world.draw(screen)
    #world.draw_grid(screen)

    for door in door_list:
        door.draw(screen)
    
    fg.draw(screen) #draw bottom layer of foreground
    

    if input_handler.should_show_movement_tutorial():
        tutorial_manager.show_step("movement")

    if input_handler.should_show_interaction_tutorial():
        tutorial_manager.show_step("interaction")

    #update player animations (currently only chameleon, but can add other animated sprites here)
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= FPS:
        mc.set_frame(frame + 1)
        frame = mc.get_frame()
        last_update = current_time
        if frame >= len(mc.get_animation()):
            mc.set_frame(0)
            frame = mc.get_frame()
     #npc animations
    for n in npc_list:
        current_time = pygame.time.get_ticks()
        if current_time - last_update_npc >= FPS:
            n.set_frame(n.get_frame() + 1)
            last_update_npc = current_time
            if n.get_frame() >= len(n.get_animation()):
                n.set_frame(0)
                npc_frame = n.get_frame()
    for group in fg.animated:
        for item in fg.animated[group]:
            current_time = pygame.time.get_ticks()
            if current_time - last_update_fg >= FPS:
                item.set_frame(item.get_frame() + 1)
                last_update_fg = current_time
                if item.get_frame() >= len(item.get_animation()):
                    item.set_frame(0)


    #draw NPCs
    for n in npc_list:
        n.draw(screen)

    #draw player
    mc.draw(screen)
    fg.draw_top(screen) #draw top layer of foreground

# threshold is number of pixels the user has to be in order to interact with the object.
    for npc in npc_list:
        if mc.player_is_near((npc.rect.center), threshold=80):
            npc.interact = True
        else:
            npc.interact = False


    #event handler
    for event in pygame.event.get():

        # close the game
        if event.type == pygame.QUIT:
             run = False

        input_handler.handle_input(event)
        

# if npc had dialogue, print to the screen. the other stuff is for the text bubble at the bottom of the screen
    input_handler.update_inventory(screen)
    
    current_dialogue = input_handler.get_current_dialogue()

    if current_dialogue:
        DialogueManager.display_bubble(DialogueManager, current_dialogue, input_handler.current_speaker.dialogue_img, input_handler.current_speaker.name)
        mc.stand_still()

    collision_list = [] #list of objects that the player is colliding with - not currently implemented
    for name in fg.groups:
        if name != "trunks": #trunks will be/is handled with obstacle tiles
            for sprite in fg.groups[name]:
                if mc.rect.colliderect(sprite.rect):
                    collision_list.append(sprite)
    for name in fg.animated:
        for sprite in fg.animated[name]:
            if mc.rect.colliderect(sprite.rect):
                collision_list.append(sprite)

# update objects currently being used in the loops
    screen_scroll, current_door = mc.update(world.obstacle_tiles, npc_list, collision_list, door_list, screen) #add collision_list eventually
    world.update(screen_scroll)
    for door in door_list:
        door.update(screen_scroll)
    fg.update(screen_scroll)
    for npc in npc_list:
        
        npc.update(screen_scroll)
    
    mc.draw(screen)

    if current_door != None:
        print(current_door.get_new_room_number())
        mc.set_position(current_door.get_new_x(), current_door.get_new_y())
        world.load_room(tile_list, world_data, door_list, current_door.get_new_room_number())
        fg.load(current_door.get_new_room_number())

        npc_list = load_list(current_door.get_new_room_number())
        current_door = None
        
    print(f"{mc.get_x()}, {mc.get_y()}")

    pygame.display.update()
 
pygame.quit()
 