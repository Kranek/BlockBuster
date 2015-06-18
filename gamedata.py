"""
This file contains Assets used in the game
"""
import pygame


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
        Assets.gameIcon = pygame.image.load('gfx/game_icon.png')
        Assets.background = pygame.image.load('gfx/background.png')
        Assets.border = pygame.image.load('gfx/border.png')
        Assets.paddles.append(pygame.image.load("gfx/paddle_b.png"))
        Assets.paddles.append(pygame.image.load("gfx/paddle_r.png"))
        Assets.ball = pygame.image.load("gfx/ball.png")

        for i in xrange(1, 7):
            Assets.blocks.append(pygame.image.load("gfx/block" + str(i) + ".png"))

        Assets.blockI = pygame.image.load("gfx/blockI.png")

        for i in xrange(0, 3):
            Assets.blocksM.append(pygame.image.load("gfx/blockM" + str(1+(i*2)) + "_v2.png"))

        Assets.blockE = pygame.image.load("gfx/blockE.png")

        Assets.item = pygame.image.load("gfx/item.png")
        Assets.itemLife = pygame.image.load("gfx/itemLife.png")
        Assets.itemLaserGun = pygame.image.load("gfx/itemLaserGun.png")
        Assets.itemExpand = pygame.image.load("gfx/itemExpand.png")
        Assets.itemShrink = pygame.image.load("gfx/itemShrink.png")
        Assets.itemNano = pygame.image.load("gfx/itemNano.png")

        Assets.explosion = pygame.image.load("gfx/explosion.png")
        Assets.editor_cursor_block = pygame.image.load("gfx/editor_cursor_block.png")

        Assets.lasergun_attachment = pygame.image.load("gfx/lasergun_attachment.png")
        Assets.projectile_laser = pygame.image.load("gfx/projectile_laser.png")

        Assets.font = pygame.font.Font("fonts/Xolonium-Regular.otf", 12)
        Assets.menu_font = pygame.font.Font("fonts/Xolonium-Regular.otf", 32)
        Assets.title_font = pygame.font.Font("fonts/Xolonium-Regular.otf", 72)

    def dummy(self):
        """
        I hate PyLint
        :return:
        """
        pass
