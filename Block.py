import pygame
from Entity import Entity


class Block(pygame.sprite.Sprite):
    WIDTH = 30
    HEIGHT = 15

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.x = x
        # self.y = y
        # self.width = 30
        # self.height = 15
        self.type = 0   # normal brick
        self.image = pygame.image.load("gfx/brick05.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dead = False

    # def think(self):
    #     pass

    def update(self):
        pass