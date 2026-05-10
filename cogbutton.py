import pygame


class CogButton:

    def __init__(self, image_path, scale, curr_angle, position):
        self.original_image = pygame.image.load(image_path)
        self.angle = curr_angle
        self.base_size = (int(self.original_image.get_width() * scale), int(self.original_image.get_height() * scale))
        self.rect = pygame.Rect(position[0], position[1], self.base_size[0], self.base_size[1])
        self.rect.topleft = position
        self.clicked = False

    def draw(self, surface):
        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
	
        if self.rect.collidepoint(pos):
            self.angle += 1
            draw_size = (int(self.base_size[0] * 1.05), int(self.base_size[1] * 1.05))
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        else:
            self.angle = 0
            draw_size = self.base_size

        # draw button
        rotated = pygame.transform.rotate(self.original_image, self.angle)
        scaled = pygame.transform.scale(rotated, draw_size)
        new_rect = scaled.get_rect(center=self.rect.center)
        surface.blit(scaled, new_rect)
        return action