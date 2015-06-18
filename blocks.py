"""
This file contains block variants used in the BlockBuster
"""
import pygame
from gamedata import Assets


class Block(pygame.sprite.Sprite):
    """
    Basic block type
    """
    WIDTH = 30
    HEIGHT = 15

    def __init__(self, x, y, color):
        """
        Initialize with coordinates and block "color" for regular blocks
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :param color: block color number (0-5)
        :return:
        """
        pygame.sprite.Sprite.__init__(self)
        self.type = color
        self.image = Assets.blocks[color]  # pygame.image.load("gfx/brick05.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dead = False

    def on_collide(self):
        """
        Default action when the ball collides with block
        :return:
        """
        return self.kill()

    def kill(self):
        """
        Default action when the block dies (set dead true and return points)
        :return: Amount of points the block is worth
        """
        self.dead = True
        return 100 + 10 * self.type

    def draw(self, screen, offset=(0, 0)):
        """
        Method called each frame to (re)draw the object
        :param screen: PyGame surface to draw the object on
        :param offset: Needed if you want to draw at different position than default (0, 0)
        :return:
        """
        screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))


class BlockExplosive(Block):
    """
    Explosive Block, kills its neighbours on hit
    """
    def __init__(self, x, y):
        """
        Init only with position, does not take the color argument
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :return:
        """
        Block.__init__(self, x, y, 0)
        self.image = Assets.blockE

    def kill(self):
        """
        Kill action of the Explosive Block (does not return points)
        :return:
        """
        self.dead = True
        return False


class BlockIndestructible(Block):
    """
    Indestructible Block
    """
    def __init__(self, x, y):
        """
        Init only with position, does not take the color argument
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :return:
        """
        Block.__init__(self, x, y, 0)
        self.image = Assets.blockI

    def kill(self):
        """
        Don't you die on me!
        :return:
        """
        return False


class BlockMultiHit(Block):
    """
    MultiHit Block
    """
    def __init__(self, x, y):
        """
        Init only with position, does not take the color argument
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :return:
        """
        Block.__init__(self, x, y, 2)
        self.image = Assets.blocksM[2]

    def on_collide(self):
        """
        Hitting the block decreases its integrity
        :return:
        """
        if self.type <= 0:  # FIXME: Change variable not to use type as integrity counter
            return self.kill()
        else:
            self.type -= 1
            self.image = Assets.blocksM[self.type]
            return False

    def kill(self):
        """
        Kill action of the MultiHit block (kill and return 400 points)
        :return: Amount of points the four blocks would be worth (since it requires 4 hits)
        """
        self.dead = True
        return 400
