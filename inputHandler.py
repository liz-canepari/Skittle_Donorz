import pygame

class InputHandler:
    def __init__(self, player, npc_list):
        self.player = player
        self.npc_list = npc_list
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_a:
                self.player.move_left()
                action = self.player.get_action()
                frame = self.player.get_frame()
                show_movement_tutorial = False
                self.player.facing_right = False  
            elif event.key == pygame.K_d:  
                self.player.move_right()
                show_movement_tutorial = False
                action = self.player.get_action()
                frame = self.player.get_frame()
                self.player.facing_right = False  
            elif event.key == pygame.K_w:  
                self.player.move_up()
                show_movement_tutorial = False
                action = self.player.get_action()
                frame = self.player.get_frame()  
            elif event.key == pygame.K_s:  
                self.player.move_down()
                show_movement_tutorial = False
                action = self.player.get_action()
                frame = self.player.get_frame()  
            elif event.key == pygame.K_e:
                for npc in self.npc_list:
                        if self.player.player_is_near(npc.rect.center):
                            speaker = npc
                            showing_dialogue = True
                            dialogue_index += 1
                            if dialogue_index > len(npc.dialogue)-1:
                                showing_dialogue = False
                                dialogue_index = -1  
            elif event.key == pygame.K_i:  
            # Handle inventory toggle  
                pass  
    
        elif event.type == pygame.KEYUP:  
            pressed = pygame.key.get_pressed()
            if event.key == pygame.K_a:
                self.player.stand_still()
                if pressed[pygame.K_w]:
                    self.player.move_up()
                elif pressed[pygame.K_s]:
                    self.player.move_down()
                elif pressed[pygame.K_d]:
                    self.player.move_right()
            elif event.key == pygame.K_d:
                self.player.stand_still()
                self.player.facing_right = True
                if pressed[pygame.K_w]:
                    self.player.move_up()
                elif pressed[pygame.K_s]:
                    self.player.move_down()
                elif pressed[pygame.K_a]:
                    self.player.move_left()
                    self.player.facing_right = False
            elif event.key == pygame.K_w:
                self.player.stand_still()
                if pressed[pygame.K_a]:
                    self.player.move_left()
                elif pressed[pygame.K_d]:
                    self.player.move_right()
                elif pressed[pygame.K_s]:
                    self.player.move_down()
            elif event.key == pygame.K_s:
                self.player.stand_still()
                if pressed[pygame.K_a]:
                    self.player.move_left()
                elif pressed[pygame.K_d]:
                    self.player.move_right()
                elif pressed[pygame.K_w]:
                    self.player.move_up()
            elif event.key == pygame.K_i:
                
                pass