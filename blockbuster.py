import sys
import os
import pygame
from pygame.locals import *

from Block import Block
from LevelLoader import LevelLoader
from ImageManager import ImageManager
from Paddle import Paddle
from Ball import Ball
from Player import Player
from gameclock import GameClock
from constants import *

pygame.init()
# pygame.display.init()
ImageManager.loadImages()
game_icon = ImageManager.gameIcon  # pygame.image.load('gfx/game_icon.png')
pygame.display.set_caption('BlockBuster')
pygame.display.set_icon(game_icon)
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))



# TODO: wrap graphics into an object
background = ImageManager.background  # pygame.image.load('gfx/background.png')
border = ImageManager.border  # pygame.image.load('gfx/border.png')

#
screen = pygame.display.get_surface()
pygame.display.flip()

prevInputX = 0


def input(events):
    global prevInputX
    for event in events:
        if event.type == QUIT:
            sys.exit(0)
        elif event.type == KEYDOWN:
            if event.key == K_LEFT:
                if paddle.vx != 0:
                    prevInputX = 1
                paddle.vx = -1

            elif event.key == K_RIGHT:
                if paddle.vx != 0:
                    prevInputX = -1
                paddle.vx = 1

        elif event.type == KEYUP:
            if event.key == K_LEFT:
                if prevInputX < 0:
                    prevInputX = 0
                elif prevInputX > 0:
                    paddle.vx = 1
                    prevInputX = 0
                else:
                    paddle.vx = 0

            elif event.key == K_RIGHT:
                if prevInputX > 0:
                    prevInputX = 0
                elif prevInputX < 0:
                    paddle.vx = -1
                    prevInputX = 0
                else:
                    paddle.vx = 0

            elif event.key == K_UP:
                if ball.docked:
                    ball.docked = False
                    ball.vx = 1
                    ball.vy = -1
        # else:
        #     print event


def loadLevel(newLevelNumber):
    global level, level_number, blocks, blockCount
    level = LevelLoader.load(LEVELDIR + str(newLevelNumber).zfill(2) + ".lvl")
    level_number = newLevelNumber
    blocks = []
    blockCount = 0
    for y in xrange(0, 20):
        blocks.append([None, ] * 20)
        for x in xrange(0, 20):
            if level[y][x] == 1:
                blocks[y][x] = Block(PLAYFIELD_PADDING[0] + x * Block.WIDTH, PLAYFIELD_PADDING[1] + y * Block.HEIGHT)
                blockCount += 1

level_number = 1
loadLevel(level_number)

player = Player("Derp")
paddle = Paddle(WINDOW_WIDTH/2 - Block.WIDTH, WINDOW_HEIGHT - 40)
ball = Ball(paddle.rect.x + paddle.rect.width/2 - Ball.RADIUS, paddle.rect.y - Ball.RADIUS * 2)

font = pygame.font.Font("fonts/Xolonium-Regular.otf", 12)


def _update(dt):
    global level_number, scoreLabel, livesLabel, levelLabel
    if blockCount <= 0:
        level_number += 1
        restartLevel(level_number)
    elif player.lives <= 0:
        restartLevel(level_number)

    input(pygame.event.get())
    paddle.update()
    if ball.docked and not ball.dead:
        ball.rect.x = paddle.rect.x + paddle.rect.width/2 - Ball.RADIUS
        ball.rect.y = paddle.rect.y - Ball.RADIUS * 2
    elif player.lives > 0:
        ball.update()

    checkCollision()
    scoreLabel = font.render("SCORE: " + str(player.score), 1, (255, 255, 255))
    livesLabel = font.render("LIVES: " + str(player.lives), 1, (255, 255, 255))
    levelLabel = font.render("LEVEL " + str(level_number), 1, (255, 255, 255))


def checkCollision():
    # ball vs paddle
    if ball.rect.y < paddle.rect.y and pygame.sprite.collide_rect(paddle, ball):
        ball.vy = -1#ball.vy

    # ball vs bottom
    if not ball.dead and ball.rect.y + ball.RADIUS * 2 > WINDOW_HEIGHT:
        player.lives -= 1
        if player.lives < 1:
            ball.dead = True
        else:
            ball.rect.x = paddle.rect.x + paddle.rect.width/2 - Ball.RADIUS
            ball.rect.y = paddle.rect.y - ball.RADIUS * 2
        ball.docked = True

    global blockCount
    # ball vs blocks
    collNum = [0, 0, 0]
    collNumVal = (4, 2, 1)
    blockNumWidth = (WINDOW_WIDTH - PLAYFIELD_PADDING[0] * 2) / Block.WIDTH
    blockNumHeight = 20  # (WINDOW_HEIGHT - playfieldPadding[1] * 2) / 15
    ballblockX = (ball.rect.x - PLAYFIELD_PADDING[0] + ball.RADIUS) / Block.WIDTH
    ballblockY = (ball.rect.y - PLAYFIELD_PADDING[1] + ball.RADIUS) / Block.HEIGHT
    for y in range(ballblockY - 1, ballblockY + 2):
        for x in range(ballblockX - 1, ballblockX + 2):
            if x >= 0 and y >= 0 and x < blockNumWidth and y < blockNumHeight:
                if blocks[y][x] is not None and not blocks[y][x].dead and pygame.sprite.collide_rect(blocks[y][x], ball):
                    blocks[y][x].dead = True
                    blockCount -= 1
                    player.score += 100
                    collNum[y - ballblockY + 1] += collNumVal[x - ballblockX + 1]

    ball.onCollide(collNum)


def restartLevel(newLevelNumber):
    ball.docked = True
    ball.dead = False

    global level, blocks, blockCount

    if newLevelNumber > MAX_LEVEL:
        newLevelNumber = 1

    if level_number < newLevelNumber:
        player.score *= player.lives * 500
    else:
        player.score = 0

    loadLevel(newLevelNumber)

    paddle.rect.x = WINDOW_WIDTH/2 - Block.WIDTH
    paddle.rect.y = WINDOW_HEIGHT - 40
    player.lives = 3


def _draw(interp):
    screen.blit(background, (0, 0))

    screen.blit(border, (0, 0))
    screen.blit(border, (WINDOW_WIDTH - PLAYFIELD_PADDING[0], 0))
    for row in blocks:
        for block in row:
            if block is not None and not block.dead:
                screen.blit(block.image, (block.rect.x, block.rect.y))
    screen.blit(paddle.image, (paddle.rect.x, paddle.rect.y))
    if not ball.dead:
        screen.blit(ball.image, (ball.rect.x, ball.rect.y))
    screen.blit(scoreLabel, (PLAYFIELD_PADDING[0] + 10, 0))
    screen.blit(livesLabel, (PLAYFIELD_PADDING[0] + 150, 0))
    screen.blit(levelLabel, (WINDOW_WIDTH - 100, 0))

    pygame.display.flip()

clock = GameClock(max_ups=60, max_fps=60, update_callback=_update, frame_callback=_draw)

while True:
    clock.tick()

