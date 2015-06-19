"""
This file contains Assets used in the game
"""
from pygame import image, font


class Assets(object):
    """
    This class contains assets used in the game (as a static fields), and a method to load them once
    """
    def __init__(self):
        """
        Dummy
        :return:
        """
        pass

    gameIcon = None
    background = None
    border = None
    paddles = []
    ball = None
    blocks = []
    blockI = None
    blocksM = []
    blockE = None
    item = None
    itemLife = None
    itemLaserGun = None
    itemShrink = None
    itemNano = None
    explosion = None
    font = None
    menu_font = None
    title_font = None
    editor_cursor_block = None
    lasergun_attachment = None
    projectile_laser = None

    @staticmethod
    def load_images():
        """
        Loads images (hopefully once)
        :return:
        """
        Assets.gameIcon = image.load('gfx/game_icon.png')
        Assets.background = image.load('gfx/background.png')
        Assets.border = image.load('gfx/border.png')
        Assets.paddles.append(image.load("gfx/paddle_b.png"))
        Assets.paddles.append(image.load("gfx/paddle_r.png"))
        Assets.ball = image.load("gfx/ball.png")

        for i in xrange(1, 7):
            Assets.blocks.append(image.load("gfx/block" + str(i) + ".png"))

        Assets.blockI = image.load("gfx/blockI.png")

        for i in xrange(0, 3):
            Assets.blocksM.append(image.load("gfx/blockM" + str(1+(i*2)) + "_v2.png"))

        Assets.blockE = image.load("gfx/blockE.png")

        Assets.item = image.load("gfx/item.png")
        Assets.itemLife = image.load("gfx/itemLife.png")
        Assets.itemLaserGun = image.load("gfx/itemLaserGun.png")
        Assets.itemExpand = image.load("gfx/itemExpand.png")
        Assets.itemShrink = image.load("gfx/itemShrink.png")
        Assets.itemNano = image.load("gfx/itemNano.png")

        Assets.explosion = image.load("gfx/explosion.png")
        Assets.editor_cursor_block = image.load("gfx/editor_cursor_block.png")

        Assets.lasergun_attachment = image.load("gfx/lasergun_attachment.png")
        Assets.projectile_laser = image.load("gfx/projectile_laser.png")

        Assets.font = font.Font("fonts/Xolonium-Regular.otf", 12)
        Assets.menu_font = font.Font("fonts/Xolonium-Regular.otf", 32)
        Assets.title_font = font.Font("fonts/Xolonium-Regular.otf", 72)

    def dummy(self):
        """
        I hate PyLint
        :return:
        """
        pass
