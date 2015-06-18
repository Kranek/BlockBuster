"""
This file contains an explosion effect class, used in the game.
"""
from pygame import Rect, sprite
from gamedata import Assets


class Explosion(sprite.Sprite):
    """
    The explosion effect appears on explosive block hit. When the explosion ends, the object is
    marked as dead(and ready to recycle if needed)
    """
    # WIDTH = 70
    # HEIGHT = 70
    # STATE_NUM = 6
    WIDTH = 64
    HEIGHT = 64
    STATE_NUM = 34
    # """Constants used in the class"""

    def __init__(self, x, y):
        """
        Initialize it with spawn position
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :return:
        """
        sprite.Sprite.__init__(self)
        self.image = Assets.explosion
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dead = False
        self.state = 0
        self.counter = 0

    def update(self):
        """
        Method called each frame, to update the state of entity (if it's not dead already)
        :return:
        """
        # self.counter += 1
        # if self.counter > 2:
        #     self.state += 1
        #     self.counter = 0
        self.state += 1
        if self.state + 1 >= Explosion.STATE_NUM:
            self.dead = True

    def draw(self, screen, offset=(0, 0)):
        """
        Method called each frame to (re)draw the object
        :param screen: PyGame surface to draw the object on
        :param offset: Needed if you want to draw at different position than default (0, 0)
        :return:
        """
        screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]),
                    Rect(self.WIDTH * self.state, 0, self.WIDTH, self.HEIGHT))
