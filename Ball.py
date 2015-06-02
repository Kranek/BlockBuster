import pygame
from constants import *
from ImageManager import ImageManager

class Ball(pygame.sprite.Sprite):
    RADIUS = 8

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.vx = 0
        self.vy = 0
        self.RADIUS = Ball.RADIUS
        self.speed = 5
        self.image = ImageManager.ball  # pygame.image.load("gfx/ball.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.docked = True
        self.dead = False

    # def think(self):
    #     pass

    def update(self):
        if self.rect.y < PLAYFIELD_PADDING[1]:
            self.vy = -self.vy
        if self.rect.x < PLAYFIELD_PADDING[1] or self.rect.x + self.RADIUS * 2 > WINDOW_WIDTH - PLAYFIELD_PADDING[0]:
            self.vx = -self.vx

        if self.rect.y + self.RADIUS * 2 > WINDOW_HEIGHT:
            self.vx = 0
            self.vy = 0

        self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed

    def onCollide(self, collNum):
        if collNum[0] == 4 and collNum[1] == 0 and collNum[2] == 0:  # topLeft
            self.vx = 1
            self.vy = 1
        elif collNum[0] == 2 and collNum[2] == 0:  # topMid...
            self.vy = 1
            if collNum[1] == 8:  # ...with midLeft
                self.vx = 1
            elif collNum[1] == 1:  # ...with midRight
                self.vx = -1

        elif collNum[0] == 1 and collNum[1] == 0 and collNum[2] == 0:  # topRight
            self.vx = -1
            self.vy = 1
        elif collNum[0] == 6:  # topLeft and topMid...
            if collNum[1] == 0:  # only what above
                self.vy = 1
            elif collNum[2] == 4:  # ...with midLeft
                self.vx = 1
                self.vy = 1
        elif collNum[0] == 3:  # topMid and topRight...
            if collNum[1] == 0:  # only what above
                self.vy = 1
            elif collNum[1] == 1:  # with midRight
                self.vx = -1
                self.vy = 1

        elif collNum[0] == 0 and collNum[1] == 0 and collNum[2] == 4:  # bottomLeft
            self.vx = 1
            self.vy = -1
        elif collNum[0] == 0 and collNum[1] == 0 and collNum[2] == 2:  # bottomMid
            self.vy = -1
            if collNum[1] == 8:  # ...with midLeft
                self.vx = 1
            elif collNum[1] == 1:  # ...with midRight
                self.vx = -1

        elif collNum[0] == 0 and collNum[1] == 0 and collNum[2] == 1:  # bottomRight
            self.vx = -1
            self.vy = -1
        elif collNum[2] == 6:  # bottomLeft and bottomMid...
            if collNum[1] == 0:  # only what above
                self.vy = -1
            elif collNum[1] == 4:  # ...with midLeft
                self.vx = 1
                self.vy = -1
        elif collNum[2] == 3:  # bottomMid and bottomRight...
            if collNum[1] == 0:  # only what above
                self.vy = -1
            elif collNum[1] == 1:  # with midRight
                self.vx = -1
                self.vy = -1

        elif collNum[0] == 0 and collNum[1] == 4 and collNum[2] == 0:  # leftMid
            self.vx = 1
        elif collNum[0] == 4 and collNum[1] == 4 and collNum[2] == 0:  # leftTop and leftMid
            self.vx = 1
        elif collNum[0] == 0 and collNum[1] == 4 and collNum[2] == 4:  # leftMid and leftBottom
            self.vx = 1

        elif collNum[0] == 0 and collNum[1] == 1 and collNum[2] == 0:  # rightMid
            self.vx = -1
        elif collNum[0] == 1 and collNum[1] == 1 and collNum[2] == 0:  # rightTop and rightMid
            self.vx = -1
        elif collNum[0] == 0 and collNum[1] == 1 and collNum[2] == 1:  # rightMid and rightBottom
            self.vx = -1