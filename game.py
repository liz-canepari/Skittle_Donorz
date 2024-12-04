import pygame
import csv
import constants
import player
import background
import npc
import tutorial
import button
import database
from inventory import Inventory
from world import World
from dialogue import DialogueManager
from foreground import Foreground
import button
from inputHandler import InputHandler
import object
#animation code from coding with russ tutorial
#https://www.youtube.com/watch?v=nXOVcOBqFwM&t=33s
 
pygame.init()
database.create_connection()
database.create_tables()

pygame_icon = pygame.image.load('images/cq_chamaleon.png')
pygame.display.set_icon(pygame_icon)

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Chroma Quest")
 
#define game variables
room_number = 1
exit_bool = False
screen_scroll = [0, 0]
clock = pygame.time.Clock()

# --------------------------------------------------------------------------Room/Tileset Code---------------------------------------------------------------------------
world = World()
colors = []
#load tilemap images
tile_list = []
#create empty tile list
world_data = []

#load in level data and create world
world.load_room(tile_list, world_data, room_number)

fg = Foreground()
bonzai = object.Object(["images/sprites/bonzai-fullcolor.png","images/sprites/bonzai-green.png"],"bonzai",59,85,[400,160])
teatable = object.Object(["images/sprites/tea-table.png"],"teatable",138,124,[80,180])
fg.add_group([bonzai, teatable], "furniture")

# --------------------------------------------------------------------------Player Code---------------------------------------------------------------------------
mc = player.Player(275, 350, 0, 0, "images/sprites/chameleon-sprite.png", 32, 32)

action = mc.get_action()
last_update = pygame.time.get_ticks()
last_update_npc = pygame.time.get_ticks()
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
npc_list = pygame.sprite.Group()
#initiate mentor sprite -- will later be moved to wherever we store room data
mentor = npc.Npc(name="Mentor", x=311, y=180, size=(24, 31), image_path="images/sprites/mentor-sprite.png", can_interact=True,
                dialogue=[
                    "Success...", "And Failure...", "Are Both Signs Of Progress.",
                    "My Student...", "My Spikes Have Become Dull,", "My Breath Weak,",
                    "And The Blood I Shed...", "Is No Longer Your Shield.", "I Love You...",
                    "But Never Come Back Home."
            ], dialogue_img="images/sprites/mentor-dialogue-img.png", animation_steps=[52])
npc_list.add(mentor)

# ---------------------------------------------------------------------------Inventory-------------------------------------------------------------------------------
# Variable to track if inventory is open or closed
inventory_open = False
selected = None
player_inventory = Inventory()
showing_notification = False #to check if screen needs to display notif from inventory
notification = None
notification_length = 2000
notification_start = 0
# --------------------------------------------------------------------------Tutorial Code---------------------------------------------------------------------------
font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 18)
tutorial_manager = tutorial.Tutorial(font, screen)
tutorial_manager.add_step("movement", "Move with WASD", (120, 10))
tutorial_manager.add_step("interaction", "Interact with NPCs with E", (100, 10))
# --------------------------------------------------------------------------Input Handler---------------------------------------------------------------------------
input_handler = InputHandler(mc, npc_list, tutorial_manager)
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


while run:
    #control FPS
    clock.tick(constants.FPS)

    #update background
    screen.fill((0, 0, 0))

    world.draw(screen)
    #world.draw_grid()
    fg.draw(screen) #draw bottom layer of foreground
    #world.draw_grid(screen)

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

    #check if exit collision
    if exit_bool:
        world.load_room(tile_list, world_data, room_number + 1)

    #event handler
    for event in pygame.event.get():

        # close the game
        if event.type == pygame.QUIT:
             run = False

        input_handler.handle_input(event)
        

# if npc had dialogue, print to the screen. the other stuff is for the text bubble at the bottom of the screen
    if inventory_open:
        player_inventory.draw()
    #inventory notification
    if showing_notification:
        player_inventory.notify(notification, screen)
        if pygame.time.get_ticks() - notification_start > notification_length:
            showing_notification = False
    
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

# update objects currently being used in the loops
    screen_scroll, exit_bool = mc.update(world.obstacle_tiles, world.exit_tiles, npc_list, collision_list,screen) #add collision_list eventually
    world.update(screen_scroll)
    fg.update(screen_scroll)
    for npc in npc_list:
        
        npc.update(screen_scroll)
    
    mc.draw(screen)
    
    pygame.display.update()
 
pygame.quit()
 