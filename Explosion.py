import pygame
from AssetManager import AssetManager


class Explosion(pygame.sprite.Sprite):
    # WIDTH = 70
    # HEIGHT = 70
    # STATE_NUM = 6
    WIDTH = 64
    HEIGHT = 64
    STATE_NUM = 34

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = AssetManager.explosion
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dead = False
        self.state = 0
        self.counter = 0

    def update(self):
        # self.counter += 1
        # if self.counter > 2:
        #     self.state += 1
        #     self.counter = 0
        self.state += 1
        if self.state + 1 >= Explosion.STATE_NUM:
            self.dead = True
