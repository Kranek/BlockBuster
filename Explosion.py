from pygame import Rect, sprite
from gamedata import Assets


class Explosion(sprite.Sprite):
    # WIDTH = 70
    # HEIGHT = 70
    # STATE_NUM = 6
    WIDTH = 64
    HEIGHT = 64
    STATE_NUM = 34

    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Assets.explosion
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.dead = False
        self.state = 0
        self.counter = 0

    def update(self):
        # self.counter += 1
        # if self.counter > 2:
        #     self.state += 1
        #     self.counter = 0
        self.state += 1
        if self.state + 1 >= Explosion.STATE_NUM:
            self.dead = True

    def draw(self, screen, offset=(0, 0)):
        screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]),
                    Rect(self.WIDTH * self.state, 0, self.WIDTH, self.HEIGHT))
