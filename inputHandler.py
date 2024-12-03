import pygame

class InputHandler:
    def __init__(self, player, npc_list, tutorial_manager):
        self.player = player
        self.npc_list = npc_list
        self.tutorial_manager = tutorial_manager
        self.showing_dialogue = False
        self.dialogue_index = -1
        self.current_speaker = None
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_a:  
                self.player.move_left()  
            elif event.key == pygame.K_d:  
                self.player.move_right()  
            elif event.key == pygame.K_w:  
                self.player.move_up()  
            elif event.key == pygame.K_s:  
                self.player.move_down()  
            elif event.key == pygame.K_e:  
                self.handle_npc_interaction()  
            elif event.key == pygame.K_i:  
            # Handle inventory toggle
                pass  
    
        elif event.type == pygame.KEYUP:   
            pressed = pygame.key.get_pressed()  
            if event.key in (pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s):   
                if not any((pressed[pygame.K_a], pressed[pygame.K_d], pressed[pygame.K_w], pressed[pygame.K_s])):  
                    self.player.stand_still()   
                elif pressed[pygame.K_a]:   
                    self.player.move_left()   
                elif pressed[pygame.K_d]:   
                    self.player.move_right()   
                elif pressed[pygame.K_w]:   
                    self.player.move_up()
                elif pressed[pygame.K_s]:   
                    self.player.move_down()

    def handle_movement(self, key):
        if key == pygame.K_a:
            self.player.move_left()  
        elif key == pygame.K_d:  
            self.player.move_right() 
        elif key == pygame.K_w:  
            self.player.move_up()  
        elif key == pygame.K_s:  
            self.player.move_down() 

                    

    def handle_npc_interaction(self):
        if self.showing_dialogue:
            self.process_dialogue()
        else:
            for npc in self.npc_list:
                if self.player.player_is_near(npc.rect.center):
                    self.current_speaker = npc
                    self.showing_dialogue = True
                    self.dialogue_index = 0
                    self.tutorial_manager.complete_step("interaction")
                    break

    def process_dialogue(self):
        if self.current_speaker:
            self.dialogue_index += 1
            if self.dialogue_index >= len(self.current_speaker.dialogue):
                self.showing_dialogue = False
                self.dialogue_index = -1
                self.current_speaker = None

    def get_current_dialogue(self):
        if self.showing_dialogue and self.current_speaker:
            return self.current_speaker.dialogue[self.dialogue_index]
        return None
    
    def should_show_movement_tutorial(self):
        return not self.tutorial_manager.is_completed("movement")
    
    def should_show_interaction_tutorial(self):
        if not self.tutorial_manager.is_completed("interaction"):
            for npc in self.npc_list:
                if self.player.player_is_near(npc.rect.center, threshold=80):
                    return True
        return False
    