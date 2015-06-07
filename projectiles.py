import pygame
from gamedata import Assets

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, owner=None):
        self.vx = 0
        self.vy = -5
        self.image = Assets.projectile_laser
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.owner = owner
        self.dead = False

    def update(self):
        if not self.dead:
            self.rect.y += self.vy
            if self.rect.y <= 0:
                self.dead = True

    def draw(self, screen, offset=(0, 0)):
        if not self.dead:
            screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))

    def on_collide(self, obj=None):
        if not self.dead:
            # temp = obj.on_collide()
            # if self.owner is not None:
            #     self.owner.score += temp
            self.dead = True

    # def check_collision(self):
    #     pass