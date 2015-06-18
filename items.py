"""
This file contains pickup items, that (mostly) fall from the destroyed blocks
"""
from pygame.sprite import Sprite
from gamedata import Assets
from constants import LEVEL_HEIGHT, PADDLE_WIDTHS
from attachments import LaserGunAttachment

class Item(Sprite):
    """
    Basic item. OVERRIDE IT!
    """
    WIDTH = 30
    HEIGHT = 30

    def __init__(self, x, y):
        """
        Initialize it with spawn position
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :return:
        """
        Sprite.__init__(self)
        self.speed = 2
        self.image = Assets.item
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dead = False

    def update(self):
        """
        Method called each frame, to update the state of object (if it's not dead already)
        :return:
        """
        if not self.dead:
            self.rect.y += self.speed
            if self.rect.y + Item.HEIGHT > LEVEL_HEIGHT:
                self.dead = True

    def draw(self, screen, offset=(0, 0)):
        """
        Method called each frame to (re)draw the object
        :param screen: PyGame surface to draw the object on
        :param offset: Needed if you want to draw at different position than default (0, 0)
        :return:
        """
        screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))

    def on_collect(self, paddle):
        """
        Method called on collision with the Paddle. OVERRIDE IT (unless you want to create
        a dummy item)
        :param paddle: Paddle with which the item collided
        :return:
        """
        pass


class ItemLife(Item):
    """
    Extra Life Item. Adds extra life to the player who owns the Paddle (duh)
    """
    def __init__(self, x, y):
        """
        Initialize it with spawn position
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :return:
        """
        Item.__init__(self, x, y)
        self.image = Assets.itemLife

    def on_collect(self, paddle):
        """
        Method called on collision with the Paddle.
        :param paddle: Paddle with which the item collided
        :return:
        """
        paddle.owner.add_lives(1)


class ItemLaserGun(Item):
    """
    LaserGun Item. Attaches the LaserGun Attachment
    """
    def __init__(self, x, y):
        """
        Initialize it with spawn position
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :return:
        """
        Item.__init__(self, x, y)
        # super(ItemLaserGun, self).__init__(x, y)
        self.image = Assets.itemLaserGun

    def on_collect(self, paddle):
        """
        Method called on collision with the Paddle.
        :param paddle: Paddle with which the item collided
        :return:
        """
        attach = True
        for attachment in paddle.attachments:
            if isinstance(attachment, LaserGunAttachment):
                attach = False
        if attach:
            paddle.attachments.append(LaserGunAttachment(paddle))


class ItemExpand(Item):
    """
    Expand Paddle Item. Expands the Paddle using the predefined widths
    """
    def __init__(self, x, y):
        """
        Initialize it with spawn position
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :return:
        """
        Item.__init__(self, x, y)
        # super(ItemExpand, self).__init__(x, y)
        self.image = Assets.itemExpand

    def on_collect(self, paddle):
        """
        Method called on collision with the Paddle
        :param paddle: Paddle with which the item collided
        :return:
        """
        for i in xrange(0, len(PADDLE_WIDTHS)):
            if paddle.rect.width <= PADDLE_WIDTHS[i] and i < len(PADDLE_WIDTHS) - 1:
                paddle.change_size(PADDLE_WIDTHS[i+1])
                return


class ItemShrink(Item):
    """
    Shrink Paddle Item. Shrinks the Paddle using the predefined widths
    """
    def __init__(self, x, y):
        """
        Initialize it with spawn position
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :return:
        """
        Item.__init__(self, x, y)
        # super(ItemShrink, self).__init__(x, y)
        self.image = Assets.itemShrink

    def on_collect(self, paddle):
        """
        Method called on collision with the Paddle
        :param paddle: Paddle with which the item collided
        :return:
        """
        size = len(PADDLE_WIDTHS)
        for i in xrange(size-1, -1, -1):
            if paddle.rect.width >= PADDLE_WIDTHS[i] and i > 0:
                paddle.change_size(PADDLE_WIDTHS[i-1])
                return


class ItemPaddleNano(Item):
    """
    Nano Paddle Item. Shrinks the paddle to the minimum permitted width
    """
    def __init__(self, x, y):
        """
        Initialize it with spawn position
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :return:
        """
        Item.__init__(self, x, y)
        # super(ItemPaddleNano, self).__init__(x, y)
        self.image = Assets.itemNano

    def on_collect(self, paddle):
        """
        Method called on collision with the Paddle
        :param paddle: Paddle with which the item collided
        :return:
        """
        paddle.change_size(PADDLE_WIDTHS[0])
