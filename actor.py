import pygame
from helpers import *

class Actor(pygame.sprite.Sprite):
    def __init__(self, image, initial_position, initial_orientation):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = initial_position
        self._angle = initial_orientation
        self._loaded_image = self.image

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)