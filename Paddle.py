"""
This file contains Paddle class
"""
from pygame import transform, SRCALPHA, mask, Surface
from pygame.sprite import Sprite
from pygame.locals import Rect
from constants import PLAYFIELD_PADDING, LEVEL_WIDTH
from gamedata import Assets
# from attachments import LaserGunAttachment


class Paddle(Sprite):
    """
    Paddle class. Player can control it. Attachments can be attached to it.
    """
    WIDTH = 60
    HEIGHT = 15

    def __init__(self, x, y, paddle_color, parent=None, owner=None):
        """
        Initialize it with spawn position
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :param paddle_color:
        :param parent: ?
        :param owner: ?
        :return:
        """
        Sprite.__init__(self)
        self.vx = 0
        self.vy = 0
        self.speed = 10
        self.image = Assets.paddles[paddle_color]  # pygame.image.load("gfx/paddle.png")
        self.mask = mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.attachment_points = [(8, 0), (self.rect.width-8, 0)]
        self.attachments = []
        # self.attachments = [LaserGunAttachment(self)]
        self.parent = parent
        self.owner = owner

    # thinking too hard
    def update(self):
        """
        Method called each frame, to update the state of the Paddle
        :return:
        """
        if self.vx < 0 and self.rect.x - PLAYFIELD_PADDING[0] <= self.speed:
            self.rect.x = PLAYFIELD_PADDING[0] + 1
        elif self.vx > 0 and LEVEL_WIDTH - PLAYFIELD_PADDING[0] - \
                self.rect.width - self.rect.x <= self.speed:
            self.rect.x = LEVEL_WIDTH - PLAYFIELD_PADDING[0] - self.rect.width - 1
        elif self.rect.x > PLAYFIELD_PADDING[0] and self.rect.x + \
                self.rect.width < LEVEL_WIDTH - PLAYFIELD_PADDING[0]:
            self.rect.x += self.vx * self.speed
        self.rect.y += self.vy * self.speed

    # noinspection PyUnusedLocal
    def draw(self, screen, offset=(0, 0)):
        """
        Method called each frame to (re)draw the object
        :param screen: PyGame surface to draw the object on
        :param offset: Needed if you want to draw at different position than default (0, 0)
        :return:
        """
        screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))
        for attachment in self.attachments:
            attachment.draw(screen)

    def change_size(self, new_width):
        """
        Function used to change the size of the palette. Rebuilds image from source and
        generates new collision Rect
        :param new_width: new Paddle width in pixels (min. 22px)
        :return:
        """
        new_width = max(new_width, 22)  # 22 = (border(8) + colorbar(3))*2
        paddle_mid = Surface((38, 15))  # (2*paddle.rect.width, paddle.rect.height))
        # paddle_mid.blit(self.image, (0, 0), Rect(11, 0, 38, 15))
        paddle_mid.blit(Assets.paddles[0], (0, 0), Rect(11, 0, 38, 15))
        paddle_mid = transform.scale(paddle_mid, (new_width-22, self.rect.height))
        new_paddle = Surface((new_width, self.rect.height), SRCALPHA)  # blank surface
        # new_paddle.fill(pygame.Color(0, 0, 0, 0), new_paddle.get_rect())
        new_paddle.blit(paddle_mid, (11, 0))
        new_paddle.blit(Assets.paddles[0], (0, 0), Rect(0, 0, 11, 15))
        new_paddle.blit(Assets.paddles[0], (new_width - 11, 0),
                        Rect(Assets.paddles[0].get_rect().width - 11, 0, 11, 15))
        paddle_new_x = self.rect.x + self.rect.width/2 - new_paddle.get_rect().width/2
        self.rect = Rect(paddle_new_x, self.rect.y, new_paddle.get_rect().width,
                         new_paddle.get_rect().height)
        self.mask = mask.from_surface(new_paddle)
        self.image = new_paddle
        self.attachment_points[1] = (self.rect.width-8, 0)
        # self.paddle.attachment_points[1] =

    def use_attachment(self):
        """
        Use the available attachment(s)
        :return:
        """
        for attachment in self.attachments:
            attachment.use(self.parent)
