import pygame


class ImageManager():
    blocks = []

    @staticmethod
    def loadImages():
        ImageManager.gameIcon = pygame.image.load('gfx/game_icon.png')
        ImageManager.background = pygame.image.load('gfx/background.png')
        ImageManager.border = pygame.image.load('gfx/border.png')
        ImageManager.paddle = pygame.image.load("gfx/paddle_b.png")
        ImageManager.ball = pygame.image.load("gfx/ball.png")

        for i in xrange(1, 7):
            ImageManager.blocks.append(pygame.image.load("gfx/block" + str(i) + ".png"))
            # # ImageManager.blocks.append(pygame.image.load("gfx/blockM" + str(i) + ".png"))
            # # ImageManager.blocks.append(pygame.image.load("gfx/blockM" + str(i) + "_v2.png"))
            # ImageManager.blocks.append(pygame.image.load("gfx/blockI.png"))

        ImageManager.blockI = pygame.image.load("gfx/blockI.png")

        ImageManager.item = pygame.image.load("gfx/item.png")
        ImageManager.itemLife = pygame.image.load("gfx/itemLife.png")