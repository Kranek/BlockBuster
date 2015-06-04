import pygame


class AssetManager():
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
    explosion = None
    font = None
    menu_font = None
    title_font = None
    editor_cursor_block = None

    @staticmethod
    def loadImages():
        AssetManager.gameIcon = pygame.image.load('gfx/game_icon.png')
        AssetManager.background = pygame.image.load('gfx/background.png')
        AssetManager.border = pygame.image.load('gfx/border.png')
        AssetManager.paddles.append(pygame.image.load("gfx/paddle_b.png"))
        AssetManager.paddles.append(pygame.image.load("gfx/paddle_r.png"))
        AssetManager.ball = pygame.image.load("gfx/ball.png")

        for i in xrange(1, 7):
            AssetManager.blocks.append(pygame.image.load("gfx/block" + str(i) + ".png"))

        AssetManager.blockI = pygame.image.load("gfx/blockI.png")

        for i in xrange(0, 3):
            AssetManager.blocksM.append(pygame.image.load("gfx/blockM" + str(1+(i*2)) + "_v2.png"))

        AssetManager.blockE = pygame.image.load("gfx/blockE.png")

        AssetManager.item = pygame.image.load("gfx/item.png")
        AssetManager.itemLife = pygame.image.load("gfx/itemLife.png")

        AssetManager.explosion = pygame.image.load("gfx/explosion.png")
        AssetManager.editor_cursor_block = pygame.image.load("gfx/editor_cursor_block.png")

        AssetManager.font = pygame.font.Font("fonts/Xolonium-Regular.otf", 12)
        AssetManager.menu_font = pygame.font.Font("fonts/Xolonium-Regular.otf", 32)
        AssetManager.title_font = pygame.font.Font("fonts/Xolonium-Regular.otf", 72)
