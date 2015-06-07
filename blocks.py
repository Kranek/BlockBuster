import pygame
from gamedata import Assets


class Block(pygame.sprite.Sprite):
    WIDTH = 30
    HEIGHT = 15

    def __init__(self, x, y, color):
        pygame.sprite.Sprite.__init__(self)
        self.type = color
        self.image = Assets.blocks[color]  # pygame.image.load("gfx/brick05.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dead = False

    def on_collide(self):
        return self.kill()

    def kill(self):
        self.dead = True
        return 100 + 10 * self.type

    def draw(self, screen, offset=(0, 0)):
        screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))


class BlockExplosive(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y, 0)
        self.image = Assets.blockE

    def kill(self):
        self.dead = True
        return False


class BlockIndestructible(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y, 0)
        self.image = Assets.blockI

    def on_collide(self):
        return self.kill()

    def kill(self):
        return False


class BlockMultiHit(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y, 2)
        self.image = Assets.blocksM[2]

    def on_collide(self):
        if self.type <= 0:
            return self.kill()
        else:
            self.type -= 1
            self.image = Assets.blocksM[self.type]
            return False

    def kill(self):
        self.dead = True
        return 400
