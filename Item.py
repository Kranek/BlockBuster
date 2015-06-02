import pygame
from ImageManager import ImageManager
from constants import *

class Item(pygame.sprite.Sprite):
    WIDTH = 30
    HEIGHT = 30

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 3
        self.image = ImageManager.item
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dead = False

    def update(self):
        if not self.dead:
            self.rect.y += self.speed
            if self.rect.y + Item.HEIGHT > WINDOW_HEIGHT:
                self.dead = True
