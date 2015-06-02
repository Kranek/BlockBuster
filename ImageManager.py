import pygame


class ImageManager():

    @staticmethod
    def loadImages():
        ImageManager.gameIcon = pygame.image.load('gfx/game_icon.png')
        ImageManager.background = pygame.image.load('gfx/background.png')
        ImageManager.border = pygame.image.load('gfx/border.png')
        ImageManager.paddle = pygame.image.load("gfx/paddle_b.png")
        ImageManager.ball = pygame.image.load("gfx/ball.png")
        ImageManager.block05 = pygame.image.load("gfx/brick05.png")
        ImageManager.item = pygame.image.load("gfx/item.png")
        ImageManager.itemLife = pygame.image.load("gfx/itemLife.png")