import pygame
from AssetManager import AssetManager


class Block(pygame.sprite.Sprite):
    WIDTH = 30
    HEIGHT = 15

    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.type = color
        self.image = AssetManager.blocks[color]  # pygame.image.load("gfx/brick05.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dead = False

    def onCollide(self):
        return self.kill()

    def kill(self):
        self.dead = True
        return 100 + 10 * self.type