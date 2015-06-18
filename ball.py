"""
This file contains ball (and later, it might also contain other variants of it)
"""
from constants import LEVEL_WIDTH, LEVEL_HEIGHT, PLAYFIELD_PADDING
from gamedata import Assets
import pygame

class Ball(pygame.sprite.Sprite):
    """
    Basic ball. Bounces off the bricks on hit and damages them.
    """
    RADIUS = 8

    def __init__(self, x, y):
        """
        Init ball with the spawn position
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :return:
        """
        pygame.sprite.Sprite.__init__(self)
        self.vx = 0
        self.vy = 0
        self.radius = Ball.RADIUS
        self.speed = 5
        self.image = Assets.ball  # pygame.image.load("gfx/ball.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.docked = True
        self.dead = False

    def draw(self, screen, offset=(0, 0)):
        """
        Method called each frame to (re)draw the object
        :param screen: PyGame surface to draw the object on
        :param offset: Needed if you want to draw at different position than default (0, 0)
        :return:
        """
        screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))

    def update(self):
        """
        Method called each frame, to update the state of the ball
        :return:
        """
        if self.rect.y < PLAYFIELD_PADDING[1]:
            self.vy = -self.vy
        if self.rect.x < PLAYFIELD_PADDING[1] or \
           self.rect.x + self.radius * 2 > LEVEL_WIDTH - PLAYFIELD_PADDING[0]:
            self.vx = -self.vx

        if self.rect.y + self.radius * 2 > LEVEL_HEIGHT:
            self.vx = 0
            self.vy = 0

        self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed

    def on_collide(self, coll_num):
        """
        Mirrors the ball vector components appropriately, with way too many branches.
        Refactor/upgrade required!
        :param coll_num: A complex one: each row of 3x3 block area near the ball is converted
        into a decimal representation of the binary representation of its occupancy, eg.
        [[1,1,0], [1,0,0], [0,0,0]] will be [6, 4, 0] and it will mean that the top-left,
        top-center and center-left blocks exist near the ball's current location
        :return:
        """
        if coll_num[0] == 4 and coll_num[1] == 0 and coll_num[2] == 0:  # topLeft
            self.vx = 1
            self.vy = 1
        elif coll_num[0] == 2 and coll_num[2] == 0:  # topMid...
            self.vy = 1
            if coll_num[1] == 4:  # ...with midLeft
                self.vx = 1
            elif coll_num[1] == 1:  # ...with midRight
                self.vx = -1

        elif coll_num[0] == 1 and coll_num[1] == 0 and coll_num[2] == 0:  # topRight
            self.vx = -1
            self.vy = 1
        elif coll_num[0] == 6:  # topLeft and topMid...
            if coll_num[1] == 0:  # only what above
                self.vy = 1
            elif coll_num[1] == 4:  # ...with midLeft
                self.vx = 1
                self.vy = 1
        elif coll_num[0] == 3:  # topMid and topRight...
            if coll_num[1] == 0:  # only what above
                self.vy = 1
            elif coll_num[1] == 1:  # with midRight
                self.vx = -1
                self.vy = 1

        elif coll_num[0] == 0 and coll_num[1] == 0 and coll_num[2] == 4:  # bottomLeft
            self.vx = 1
            self.vy = -1
        elif coll_num[0] == 0 and coll_num[1] == 0 and coll_num[2] == 2:  # bottomMid
            self.vy = -1
            if coll_num[1] == 4:  # ...with midLeft
                self.vx = 1
            elif coll_num[1] == 1:  # ...with midRight
                self.vx = -1

        elif coll_num[0] == 0 and coll_num[1] == 0 and coll_num[2] == 1:  # bottomRight
            self.vx = -1
            self.vy = -1
        elif coll_num[2] == 6:  # bottomLeft and bottomMid...
            if coll_num[1] == 0:  # only what above
                self.vy = -1
            elif coll_num[1] == 4:  # ...with midLeft
                self.vx = 1
                self.vy = -1
        elif coll_num[2] == 3:  # bottomMid and bottomRight...
            if coll_num[1] == 0:  # only what above
                self.vy = -1
            elif coll_num[1] == 1:  # with midRight
                self.vx = -1
                self.vy = -1

        elif coll_num[0] == 0 and coll_num[1] == 4 and coll_num[2] == 0:  # leftMid
            self.vx = 1
        elif coll_num[0] == 4 and coll_num[1] == 4 and coll_num[2] == 0:  # leftTop and leftMid
            self.vx = 1
        elif coll_num[0] == 0 and coll_num[1] == 4 and coll_num[2] == 4:  # leftMid and leftBottom
            self.vx = 1

        elif coll_num[0] == 0 and coll_num[1] == 1 and coll_num[2] == 0:  # rightMid
            self.vx = -1
        elif coll_num[0] == 1 and coll_num[1] == 1 and coll_num[2] == 0:  # rightTop and rightMid
            self.vx = -1
        elif coll_num[0] == 0 and coll_num[1] == 1 and coll_num[2] == 1:  # rightMid and rightBottom
            self.vx = -1
