import pygame
from gamedata import Assets
from constants import *
from attachments import LaserGunAttachment

class Item(pygame.sprite.Sprite):
    WIDTH = 30
    HEIGHT = 30

    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 2
        self.image = Assets.item
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dead = False

    def update(self):
        if not self.dead:
            self.rect.y += self.speed
            if self.rect.y + Item.HEIGHT > LEVEL_HEIGHT:
                self.dead = True

    def draw(self, screen, offset=(0, 0)):
        screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))

    def on_collect(self, paddle):
        pass


class ItemLife(Item):
    def __init__(self, x, y):
        Item.__init__(self, x, y)
        self.image = Assets.itemLife

    def on_collect(self, paddle):
        paddle.owner.lives += 1


class ItemLaserGun(Item):
    def __init__(self, x, y):
        super(ItemLaserGun, self).__init__(x, y)
        self.image = Assets.itemLaserGun

    def on_collect(self, paddle):
        attach = True
        for attachment in paddle.attachments:
            if isinstance(attachment, LaserGunAttachment):
                attach = False
        if attach:
            paddle.attachments.append(LaserGunAttachment(paddle))


class ItemExpand(Item):
    def __init__(self, x, y):
        super(ItemExpand, self).__init__(x, y)
        self.image = Assets.itemExpand

    def on_collect(self, paddle):
        for i in xrange(0, len(PADDLE_WIDTHS)):
            if paddle.rect.width <= PADDLE_WIDTHS[i] and i < len(PADDLE_WIDTHS) - 1:
                paddle.change_size(PADDLE_WIDTHS[i+1])
                return


class ItemShrink(Item):
    def __init__(self, x, y):
        super(ItemShrink, self).__init__(x, y)
        self.image = Assets.itemShrink

    def on_collect(self, paddle):
        size = len(PADDLE_WIDTHS)
        for i in xrange(size-1, -1, -1):
            if paddle.rect.width >= PADDLE_WIDTHS[i] and i > 0:
                paddle.change_size(PADDLE_WIDTHS[i-1])
                return

class ItemPaddleNano(Item):
    def __init__(self, x, y):
        super(ItemPaddleNano, self).__init__(x, y)
        self.image = Assets.itemNano

    def on_collect(self, paddle):
        paddle.change_size(PADDLE_WIDTHS[0])
