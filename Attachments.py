from constants import *
import pygame
from gamedata import Assets
from projectiles import Projectile

class Attachment(object):
    def __init__(self, parent=None):
        self.parts = []
        self.parent = parent

    def draw(self, screen, offset=(0, 0)):
        pass

    def use(self):
        pass


class AttachmentPart(object):
    def __init__(self, image, attachment_point=None):
        self.image = image
        dimensions = image.get_rect()
        self.width = dimensions.width
        self.height = dimensions.height
        self.attachment_point = attachment_point
        if self.attachment_point is None:
            self.attachment_point = (self.width, self.height - PADDLE_HEIGHT)

    def get_mirrored_version(self):
        mirrored_image = pygame.transform.flip(self.image, True, False)
        mirrored_point = (abs(self.width - self.attachment_point[0]), self.attachment_point[1])
        return AttachmentPart(mirrored_image, mirrored_point)


class LaserGunAttachment(Attachment):
    def __init__(self, parent=None):
        super(LaserGunAttachment, self).__init__(parent)
        self.parts = [AttachmentPart(Assets.lasergun_attachment)]
        self.parts.append(self.parts[0].get_mirrored_version())

    def draw(self, screen, offset=(0, 0)):
        if self.parent is not None:
            for i in xrange(0, len(self.parts)):
                screen.blit(self.parts[i].image, (self.parent.rect.x + self.parent.attachment_points[i][0] -
                                                  self.parts[i].attachment_point[0] + offset[0],
                                                  self.parent.rect.y + self.parent.attachment_points[i][1]
                                                  - self.parts[i].attachment_point[1] + offset[1]))

    def use(self, world=None):
        if world is not None:
            world.add_entity(Projectile(self.parent.rect.x + self.parent.attachment_points[0][0] -
                                        self.parts[0].attachment_point[0] - 3, self.parent.rect.y +
                                        self.parent.attachment_points[0][1] - self.parts[0].attachment_point[1],
                                        self.parent.owner))
            world.add_entity(Projectile(self.parent.rect.x + self.parent.attachment_points[1][0] -
                                        self.parts[1].attachment_point[0] + 3, self.parent.rect.y +
                                        self.parent.attachment_points[1][1] - self.parts[1].attachment_point[1],
                                        self.parent.owner))