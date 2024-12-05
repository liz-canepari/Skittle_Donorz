import pygame

class InputHandler:
    def __init__(self, player, npc_list, tutorial_manager, player_inventory, save_function, load_function):
        self.mc = player
        self.npc_list = npc_list
        self.tutorial_manager = tutorial_manager
        self.showing_dialogue = False
        self.dialogue_index = -1
        self.current_speaker = None
        self.inventory = player_inventory
        self.inventory_open = False
        self.showing_notification = False
        self.notification = None
        self.notification_length = 2000
        self.notification_start = 0
        self.show_inventory_tutorial = False
        self.save_game = save_function
        self.load_game = load_function
    
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN: 
            self.mc.facing_right = False 
            self.tutorial_manager.complete_step("movement")
            if event.key == pygame.K_a:
                self.mc.move_left()
            elif event.key == pygame.K_d:
                self.mc.move_right()
            elif event.key == pygame.K_w:
                self.mc.move_up()
            elif event.key == pygame.K_s:
                self.mc.move_down()
            elif event.key == pygame.K_e:  
                self.handle_npc_interaction()  
            elif event.key == pygame.K_i:
                self.toggle_inventory()
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.save_game()
            elif event.key == pygame.K_l and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.load_game()
            
        
        
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
                self.inventory.open = not self.inventory.open

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
    
    def toggle_inventory(self):
        self.inventory_open = not self.inventory_open
        if self.inventory_open:
            self.tutorial_manager.complete_step("inventory")
        

    def show_notification(self, message):
        self.showing_notification = True
        self.notification = message
        self.notification_start = pygame.time.get_ticks()
        self.show_inventory_tutorial = True

    def update_inventory(self, screen):  
        if self.inventory_open:  
            self.inventory.draw()  
        if self.showing_notification:  
            self.inventory.notify(self.notification, screen)  
            if pygame.time.get_ticks() - self.notification_start > self.notification_length:  
                self.showing_notification = False 
        if self.show_inventory_tutorial and not self.inventory_open:
            self.tutorial_manager.show_step("inventory")

    def should_show_inventory_tutorial(self):
        return self.show_inventory_tutorial and not self.inventory_open