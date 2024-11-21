import pygame
import csv
import constants
import player
import background
import npc
import tutorial
from inventory import Inventory
from world import World
from dialogue import DialogueManager
from foreground import Foreground
import button

#animation code from coding with russ tutorial
#https://www.youtube.com/watch?v=nXOVcOBqFwM&t=33s
 
pygame.init()

pygame_icon = pygame.image.load('images/sprites/mentor.png')
pygame.display.set_icon(pygame_icon)

screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
pygame.display.set_caption("Skittle Game")
 
#define game variables
room_number = 1
exit_bool = False
screen_scroll = [0, 0]
clock = pygame.time.Clock()

# --------------------------------------------------------------------------Room/Tileset Code---------------------------------------------------------------------------
world = World()
#load tilemap images
tile_list = []
#create empty tile list
world_data = []

#load in level data and create world
world.load_room(tile_list, world_data, room_number)

fg = Foreground()
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
mentor = npc.Npc(name="Mentor", x=305, y=180, size=(32, 32), image_path="images/sprites/mentor-sprite.png", can_interact=True,
                dialogue=[
                    "Success...", "And Failure...", "Are Both Signs Of Progress.",
                    "My Student...", "My Spikes Have Become Dull,", "My Breath Weak,",
                    "And The Blood I Shed...", "Is No Longer Your Shield.", "I Love You...",
                    "But Never Come Back Home."
            ], dialogue_img="images/sprites/mentor-dialogue-img.png", animation_steps=[42])
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
show_movement_tutorial = True
# --------------------------------------------------------------------------Main Game Code---------------------------------------------------------------------------

#create buttons
start_img = pygame.image.load('images/start_btn.png').convert_alpha()
exit_img = pygame.image.load('images/exit_btn.png').convert_alpha()

start_button = button.Button(constants.SCREEN_WIDTH // 2 - 130, constants.SCREEN_HEIGHT // 2 - 150, start_img, 1)
exit_button = button.Button(constants.SCREEN_WIDTH // 2 - 110, constants.SCREEN_HEIGHT // 2 + 50, exit_img, 1)

menu = True
while menu == True:
    #draw menu
    screen.fill((144, 201, 120))
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
            tutorial_manager.show_step("interaction")
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
        # take keyboard presses
        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_a:
                mc.move_left()
                action = mc.get_action()
                frame = mc.get_frame()
                show_movement_tutorial = False
                mc.facing_right = False
            if event.key == pygame.K_d:
                mc.move_right()
                show_movement_tutorial = False
                action = mc.get_action()
                frame = mc.get_frame()
                mc.facing_right = False
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
                for npc in npc_list:
                    if mc.player_is_near(npc.rect.center):
                        speaker = npc
                        showing_dialogue = True
                        dialogue_index += 1
                        if dialogue_index > len(npc.dialogue)-1:
                            showing_dialogue = False
                            dialogue_index = -1

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
                mc.facing_right = True
                if pressed[pygame.K_w]:
                    mc.move_up()
                elif pressed[pygame.K_s]:
                    mc.move_down()
                elif pressed[pygame.K_a]:
                    mc.move_left()
                    mc.facing_right = False
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
            if event.key == pygame.K_i:
                inventory_open = not inventory_open

# if npc had dialogue, print to the screen. the other stuff is for the text bubble at the bottom of the screen
    if inventory_open:
        player_inventory.draw()
    #inventory notification
    if showing_notification:
        player_inventory.notify(notification, screen)
        if pygame.time.get_ticks() - notification_start > notification_length:
            showing_notification = False

# Draw tutorial if not finished
    if show_movement_tutorial:
        tutorial_manager.show_step("movement")

    if showing_dialogue:
        DialogueManager.display_bubble(DialogueManager, speaker.dialogue[dialogue_index], speaker.dialogue_img, speaker.name)
        mc.stand_still()

    collision_list = [] #list of objects that the player is colliding with - not currently implemented
    # for name in fg.groups:
    #     if name != "trunks": #trunks will be/is handled with obstacle tiles
    #         for sprite in fg.groups[name]:
    #             if mc.rect.colliderect(sprite.rect):
    #                 collision_list.append(sprite)

# update objects currently being used in the loops
    screen_scroll, exit_bool = mc.update(world.obstacle_tiles, world.exit_tiles, npc_list) #add collision_list eventually
    world.update(screen_scroll)
    fg.update(screen_scroll)
    for npc in npc_list:
        
        npc.update(screen_scroll)
    
    pygame.display.update()
 
pygame.quit()
 