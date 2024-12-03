import pygame

class InputHandler:
    def __init__(self, player, npc_list, tutorial_manager):
        self.mc = player
        self.npc_list = npc_list
        self.tutorial_manager = tutorial_manager
        self.showing_dialogue = False
        self.dialogue_index = -1
        self.current_speaker = None
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN: 
            self.mc.facing_right = False 
            self.tutorial_manager.complete_step("movement")
            if event.key == pygame.K_a:
                self.mc.move_left()
            if event.key == pygame.K_d:
                self.mc.move_right()
            if event.key == pygame.K_w:
                self.mc.move_up()
            if event.key == pygame.K_s:
                self.mc.move_down()
        
        
        elif event.type == pygame.KEYUP:  
            self.mc.facing_right = False 
            pressed = pygame.key.get_pressed()
            if event.key == pygame.K_a:
                self.mc.stand_still()
                if pressed[pygame.K_w]:
                    self.mc.move_up()
                elif pressed[pygame.K_s]:
                    self.mc.move_down()
                elif pressed[pygame.K_d]:
                    self.mc.move_right()
            if event.key == pygame.K_d:
                self.mc.stand_still()
                self.mc.facing_right = True
                if pressed[pygame.K_w]:
                    self.mc.move_up()
                elif pressed[pygame.K_s]:
                    self.mc.move_down()
                elif pressed[pygame.K_a]:
                    self.mc.move_left()
                    self.mc.facing_right = False
            if event.key == pygame.K_w:
                self.mc.stand_still()
                if pressed[pygame.K_a]:
                    self.mc.move_left()
                elif pressed[pygame.K_d]:
                    self.mc.move_right()
                elif pressed[pygame.K_s]:
                    self.mc.move_down()
            if event.key == pygame.K_s:
                self.mc.stand_still()
                if pressed[pygame.K_a]:
                    self.mc.move_left()
                elif pressed[pygame.K_d]:
                    self.mc.move_right()
                elif pressed[pygame.K_w]:
                    self.mc.move_up()
            if event.key == pygame.K_i:
                inventory_open = not inventory_open

    def handle_movement(self, key):
        if key == pygame.K_a:
            self.mc.move_left()  
        elif key == pygame.K_d:  
            self.mc.move_right() 
        elif key == pygame.K_w:  
            self.mc.move_up()  
        elif key == pygame.K_s:  
            self.mc.move_down() 

                    

    def handle_npc_interaction(self):
        if self.showing_dialogue:
            self.process_dialogue()
        else:
            for npc in self.npc_list:
                if self.mc.player_is_near(npc.rect.center):
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
                if self.mc.player_is_near(npc.rect.center, threshold=80):
                    return True
        return False
    