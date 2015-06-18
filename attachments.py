"""
This file contains Paddle Attachments and their parts
"""
from constants import PADDLE_HEIGHT
import pygame
from gamedata import Assets
from projectiles import Projectile


class Attachment(object):
    """
    Basic attachment, don't spawn it directly. Used as a base of the other attachments
    """

    def __init__(self, parent=None):
        """
        Init with Paddle as a parent, so that the attachment can use its docking points
        to position itself
        :param parent: Paddle to attach the thing to...
        :return:
        """
        self.parts = []
        self.parent = parent

    def draw(self, screen, offset=(0, 0)):
        """
        Method called each frame to (re)draw the object. OVERRIDE IT!
        :param screen: PyGame surface to draw the object on
        :param offset: Needed if you want to draw at different position than default (0, 0)
        :return:
        """
        raise NotImplementedError("You are doing it wrong...")

    def use(self, world=None):
        """
        Method called by the Paddle to use the attachment. OVERRIDE IT!
        :param world: Supplied only to retain interface compatibility
        :return:
        """
        raise NotImplementedError("You are doing it wrong...")


class AttachmentPart(object):
    """
    Singular part of the attachment set. Holds position, image and allows to get mirrored part.
    Doesn't know how to draw itself (acts primarily as a image/coord container)
    """

    def __init__(self, image, attachment_point=None):
        """
        Init with the Attachment image, and point of attachment to the Paddle.
        Start from the left part and then generate the right one using get_mirrored_version()
        if possible.
        :param image: Attachment image
        :param attachment_point: Docking point of the AttachmentPart, will be connected to the
        attachment point of the Paddle
        :return:
        """
        self.image = image
        dimensions = image.get_rect()
        self.width = dimensions.width
        self.height = dimensions.height
        self.attachment_point = attachment_point
        if self.attachment_point is None:
            self.attachment_point = (self.width, self.height - PADDLE_HEIGHT)

    def get_mirrored_version(self):
        """
        Utility method to get the part with mirrored image and attachment points
        :return: Mirrored AttachmentPart object
        """
        mirrored_image = pygame.transform.flip(self.image, True, False)
        mirrored_point = (abs(self.width - self.attachment_point[0]), self.attachment_point[1])
        return AttachmentPart(mirrored_image, mirrored_point)

    def set_dimensions(self, dimensions):
        """
        Utility method to set width/height from tuple (mainly to silence the PyLint)
        :return:
        """
        assert isinstance(dimensions, tuple)
        self.width, self.height = dimensions


class LaserGunAttachment(Attachment):
    """
    Laser gun attachment. Shoots laser projectiles.
    """

    def __init__(self, parent=None):
        """
        Init with Paddle as a parent, so that the attachment can use its docking points
        to position itself
        :param parent: Paddle to attach the thing to...
        :return:
        """
        super(LaserGunAttachment, self).__init__(parent)
        self.parts = [AttachmentPart(Assets.lasergun_attachment)]
        self.parts.append(self.parts[0].get_mirrored_version())

    def draw(self, screen, offset=(0, 0)):
        """
        Method called each frame to (re)draw the object
        :param screen: PyGame surface to draw the object on
        :param offset: Needed if you want to draw at different position than default (0, 0)
        :return:
        """
        if self.parent is not None:
            for i in xrange(0, len(self.parts)):
                screen.blit(self.parts[i].image,
                            (self.parent.rect.x + self.parent.attachment_points[i][0] -
                             self.parts[i].attachment_point[0] + offset[0],
                             self.parent.rect.y + self.parent.attachment_points[i][1] -
                             self.parts[i].attachment_point[1] + offset[1]))

    def use(self, world=None):
        """
        Method called by the Paddle to use the attachment.
        :param world: The play-field into which the attachment spawns the projectile.
        :return:
        """
        if world is not None:
            world.add_entity(
                Projectile(self.parent.rect.x + self.parent.attachment_points[0][0] -
                           self.parts[0].attachment_point[0] + 3, self.parent.rect.y +
                           self.parent.attachment_points[0][1] - self.parts[0].attachment_point[1],
                           self.parent.owner))
            world.add_entity(
                Projectile(self.parent.rect.x + self.parent.attachment_points[1][0] -
                           self.parts[1].attachment_point[0] + 3, self.parent.rect.y +
                           self.parent.attachment_points[1][1] - self.parts[1].attachment_point[1],
                           self.parent.owner))
