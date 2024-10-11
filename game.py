import pygame
import player
import background
from inanimateObj import Character
#animation code from coding with russ tutorial
#https://www.youtube.com/watch?v=nXOVcOBqFwM&t=33s
 
pygame.init()
 
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sprite")
 
bg = background.Background("images/scenes/room.png", 0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)
 
player = player.Player(400, 250, 0, 0, "images/sprites/chameleon-sprite.png")
 
action = player.get_action()
last_update = pygame.time.get_ticks()
animation_cooldown = 110
frame = player.get_frame()

# box = Object(box_image, [100, 150], interact=True)


# This is the mentor's code. load the image, then pass the params. we draw mentor in code below.
npc_image = pygame.image.load("images/sprites/mentor.png").convert_alpha()
npc = Character(npc_image, [350, 245], interact=True, dialogue="Hello there!")
 
 
run = True
while run:
    #update background
    screen.fill((0, 0, 0))
    bg.draw(screen)
 
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
    npc.draw(screen)
    player.draw(screen)
    #event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.set_action(1)
                action = player.get_action()
                player.set_frame(0)
                frame = player.get_frame()
                player.move_left()
            if event.key == pygame.K_d:
                player.set_action(2)
                action = player.get_action()
                player.set_frame(0)
                frame = player.get_frame()
                player.move_right()
            if event.key == pygame.K_w:
                player.set_action(4)
                action = player.get_action()
                player.set_frame(0)
                frame = player.get_frame()
                player.move_up()
            if event.key == pygame.K_s:
                player.set_action(3)
                action = player.get_action()
                player.set_frame(0)
                frame = player.get_frame()
                player.move_down()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.set_action(0)
                action = player.get_action()
                player.set_frame(0)
                frame = player.get_frame()
            if event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_a:
                player.set_action(0)
                action = player.get_action()
                player.set_frame(0)
                frame = player.get_frame()
            player.stand_still()
    player.update()

    # event interaction like the characters

    pygame.display.update()
 
pygame.quit()
 