"""
This file contains projectile
"""
from pygame.mask import from_surface
from pygame.sprite import Sprite
from gamedata import Assets

class Projectile(Sprite):
    """
    Projectile is an object spawned by the Paddle weapon Attachments
    """
    def __init__(self, x, y, owner=None):
        """
        Init with owner to give him points for each destroyed block
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :param owner: Player-class object
        :return:
        """
        Sprite.__init__(self)
        self.vx = 0
        self.vy = -8
        self.image = Assets.projectile_laser
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = from_surface(self.image)
        self.owner = owner
        self.dead = False

    def update(self):
        """
        Method called each frame, to update the state of entity (if it's not dead already)
        :return:
        """
        if not self.dead:
            self.rect.y += self.vy
            if self.rect.y <= 0:
                self.dead = True

    def draw(self, screen, offset=(0, 0)):
        """
        Method called each frame to (re)draw the object
        :param screen: PyGame surface to draw the object on
        :param offset: Needed if you want to draw at different position than default (0, 0)
        :return:
        """
        if not self.dead:
            screen.blit(self.image, (self.rect.x + offset[0], self.rect.y + offset[1]))

    def on_collide(self, obj=None):
        """
        Action to be performed on obj-projectile collision
        :param obj: Object with which the projectile collided, used to get the point-worth from
        :return:
        """
        if not self.dead:
            # temp = obj.on_collide()
            # if self.owner is not None:
            #     self.owner.score += temp
            _ = obj
            self.dead = True

    # def check_collision(self):
    #     pass
