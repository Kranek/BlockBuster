import pygame
from constants import *
from ImageManager import ImageManager

class Paddle(pygame.sprite.Sprite):
    WIDTH = 60
    HEIGHT = 15

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.vx = 0
        self.vy = 0
        self.width = 60
        self.height = 15
        self.speed = 10
        self.image = ImageManager.paddle  # pygame.image.load("gfx/paddle.png")
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # thinking too hard
    def update(self):
        if self.vx < 0 and self.rect.x - PLAYFIELD_PADDING[0] <= self.speed:
            self.rect.x = PLAYFIELD_PADDING[0] + 1
        elif self.vx > 0 and WINDOW_WIDTH - PLAYFIELD_PADDING[0] - self.width - self.rect.x <= self.speed:
            self.rect.x = WINDOW_WIDTH - PLAYFIELD_PADDING[0] - self.width - 1
        elif self.rect.x > PLAYFIELD_PADDING[0] and self.rect.x + self.width < WINDOW_WIDTH - PLAYFIELD_PADDING[0]:
            self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed

    # def update(self):
    #     pass