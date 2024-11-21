import pygame
import spritesheet
#button class
class Button():
	def __init__(self,x, y, image, scale):
		sprite_sheet = image
		width = image.get_width()/2
		height = image.get_height()
		self.unpressed = spritesheet.SpriteSheet(sprite_sheet).get_image(0, width, height)
		self.pressed = spritesheet.SpriteSheet(sprite_sheet).get_image(1, width, height)
		self.image = self.unpressed
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			self.image = self.pressed
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True
		else: 
			self.image = self.unpressed

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action