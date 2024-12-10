import pygame

class InputHandler:
    def __init__(self, player, npc_list, tutorial_manager, player_inventory, foreground, world):
        self.world = world
        self.fg = foreground
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
        self.colors = []
    
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
                for npc in self.npc_list:
                    if self.mc.player_is_near(npc.rect.center):
                        self.handle_npc_interaction()  
                for group in self.fg.get_groups().values():
                    for item in group:
                        if self.mc.player_is_near(item.rect.center) and item.interactable:
                            self.handle_item_interaction(item)

            elif event.key == pygame.K_i:
                self.toggle_inventory()
            
        
        
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
        self.tutorial_manager.complete_step("interaction")
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

    def handle_item_interaction(self, item):
        i = item.interact_index
        if i == 1:
            if item.holding_item and item.used:
                item.interact_index = 2
            item.interact()
            if item.holding_item and not item.open:

                item.open = True
        if i == 2:
            item.interact()
            if item.holding_item and item.open and not item.used:
                item.item.in_inventory()
                if "skittle" in item.item.name:
                    if "green" in item.item.name:
                        self.colors.append("green")
                    if "red" in item.item.name:
                        self.colors.append("red")
                    if "yellow" in item.item.name:
                        self.colors.append("yellow")
                self.inventory.add_item(item.item)
            item.used = True
        if i == 3:
            item.interact()

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

    def show_notification(self, message):
        self.showing_notification = True
        self.notification = message
        self.notification_start = pygame.time.get_ticks()

    def update_inventory(self, screen):  
      if self.inventory_open:  
        self.inventory.draw()  
      if self.showing_notification:  
        self.inventory.notify(self.notification, screen)  
        if pygame.time.get_ticks() - self.notification_start > self.notification_length:  
           self.showing_notification = False 