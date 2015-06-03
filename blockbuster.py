import sys
# import os
import pygame
from pygame.locals import *

from Block import Block
from BlockIndestructible import BlockIndestructible
from BlockMultiHit import BlockMultiHit
from BlockExplosive import BlockExplosive
from LevelLoader import LevelLoader
from ImageManager import ImageManager
from Paddle import Paddle
from Ball import Ball
from Player import Player
from Item import Item
from ItemLife import ItemLife
from Explosion import Explosion
from gameclock import GameClock
from constants import *

pygame.init()
# pygame.display.init()
ImageManager.loadImages()
game_icon = ImageManager.gameIcon  # pygame.image.load('gfx/game_icon.png')
pygame.display.set_caption('BlockBuster')
pygame.display.set_icon(game_icon)
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))



background = ImageManager.background  # pygame.image.load('gfx/background.png')
border = ImageManager.border  # pygame.image.load('gfx/border.png')

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

            elif event.key == K_EQUALS:
                start_level(level_number + 1)
        # else:
        #     print event


def loadLevel(newLevelNumber):
    global level, level_number, blocks, blockCount, items, entities
    loaded_level = LevelLoader.load(LEVELDIR + str(newLevelNumber).zfill(2) + ".lvl")
    level = loaded_level[0]
    items = loaded_level[1]
    level_number = newLevelNumber
    blocks = []
    entities = []
    blockCount = 0
    for y in xrange(0, BLOCK_NUM_HEIGHT):
        blocks.append([None, ] * BLOCK_NUM_WIDTH)
        for x in xrange(0, BLOCK_NUM_WIDTH):
            if level[y][x] == 'i':
                blocks[y][x] = BlockIndestructible(PLAYFIELD_PADDING[0] + x * Block.WIDTH,
                                                   PLAYFIELD_PADDING[1] + y * Block.HEIGHT)
            elif level[y][x] == 'm':
                blocks[y][x] = BlockMultiHit(PLAYFIELD_PADDING[0] + x * Block.WIDTH,
                                             PLAYFIELD_PADDING[1] + y * Block.HEIGHT)
                blockCount += 1
            elif level[y][x] == 'e':
                blocks[y][x] = BlockExplosive(PLAYFIELD_PADDING[0] + x * Block.WIDTH,
                                              PLAYFIELD_PADDING[1] + y * Block.HEIGHT)
                blockCount += 1
            elif level[y][x] != '0':
                blocks[y][x] = Block(PLAYFIELD_PADDING[0] + x * Block.WIDTH, PLAYFIELD_PADDING[1] + y * Block.HEIGHT,
                                     int(level[y][x]) - 1)
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
        # level_number += 1
        start_level(level_number + 1)
    elif player.lives <= 0:
        start_level(level_number)

    input(pygame.event.get())
    paddle.update()
    if ball.docked and not ball.dead:
        ball.rect.x = paddle.rect.x + paddle.rect.width/2 - Ball.RADIUS
        ball.rect.y = paddle.rect.y - Ball.RADIUS * 2
    elif player.lives > 0:
        ball.update()
    for entity in entities:
        if not entity.dead:
            entity.update()

    checkCollision()
    scoreLabel = font.render("SCORE: " + str(player.score), 1, (255, 255, 255))
    livesLabel = font.render("LIVES: " + str(player.lives), 1, (255, 255, 255))
    levelLabel = font.render("LEVEL " + str(level_number), 1, (255, 255, 255))


def block_destruction(block, item, func):
    if item == 1:
        entities.append(ItemLife(block.rect.x, block.rect.y))

    return_v = func()
    if isinstance(block, BlockExplosive):
        rect = block.rect
        entities.append(Explosion(rect.x + rect.width/2 - Explosion.WIDTH/2,
                                  rect.y + rect.height/2 - Explosion.HEIGHT/2))

    if block.dead:
        player.score += return_v
        global blockCount
        blockCount -= 1


def checkCollision():
    # ball vs paddle
    if ball.rect.y < paddle.rect.y and pygame.sprite.collide_rect(paddle, ball):
        ball.vy = -1  # ball.vy

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
    ballblockX = (ball.rect.x - PLAYFIELD_PADDING[0] + ball.RADIUS) / Block.WIDTH
    ballblockY = (ball.rect.y - PLAYFIELD_PADDING[1] + ball.RADIUS) / Block.HEIGHT
    for y in range(ballblockY - 1, ballblockY + 2):
        for x in range(ballblockX - 1, ballblockX + 2):
            # if x >= 0 and y >= 0 and x < BLOCK_NUM_WIDTH and y < BLOCK_NUM_HEIGHT:
            if 0 <= x < BLOCK_NUM_WIDTH and 0 <= y < BLOCK_NUM_HEIGHT:
                if blocks[y][x] is not None and not blocks[y][x].dead and pygame.sprite.collide_rect(blocks[y][x], ball):
                    # if items[y][x] == 1:
                    #     entities.append(ItemLife(blocks[y][x].rect.x, blocks[y][x].rect.y))
                    #
                    # return_v = blocks[y][x].onCollide()
                    # if isinstance(blocks[y][x], BlockExplosive):
                    #     # for col in xrange(y - 1, y + 2):
                    #     #     for row in xrange(x - 1, x + 2):
                    #     #         if blocks[col][row] is not None:
                    #     #             result = blocks[col][row].kill()
                    #     #             if blocks[col][row].dead:
                    #     #                 award_points(player, result)
                    #     rect = blocks[y][x].rect
                    #     entities.append(Explosion(rect.x + rect.width/2 - Explosion.WIDTH/2, rect.y + rect.height/2 - Explosion.HEIGHT/2))
                    #
                    # if blocks[y][x].dead:
                    #     award_points(player, return_v)
                    block_destruction(blocks[y][x], items[y][x], blocks[y][x].onCollide)

                    collNum[y - ballblockY + 1] += collNumVal[x - ballblockX + 1]

    ball.onCollide(collNum)

    # entities
    for entity in entities:
        if not entity.dead:
            # paddle vs items
            if isinstance(entity, ItemLife) and pygame.sprite.collide_rect(paddle, entity):
                entity.dead = True
                player.lives += 1
            # explosion vs blocks
            elif isinstance(entity, Explosion) and entity.state > 0:
                entity_block_x = (entity.rect.x - PLAYFIELD_PADDING[0] + Explosion.WIDTH/2) / Block.WIDTH
                entity_block_y = (entity.rect.y - PLAYFIELD_PADDING[1] + Explosion.HEIGHT/2) / Block.HEIGHT
                for y in xrange(entity_block_y - 1, entity_block_y + 2):
                    for x in xrange(entity_block_x - 1, entity_block_x + 2):
                        if 0 <= x < BLOCK_NUM_WIDTH and 0 <= y < BLOCK_NUM_HEIGHT:
                            if blocks[y][x] is not None and not blocks[y][x].dead:
                                block_destruction(blocks[y][x], items[y][x], blocks[y][x].kill)



def start_level(new_level_num):
    ball.docked = True
    ball.dead = False

    if new_level_num > MAX_LEVEL:
        new_level_num = 1

    if level_number < new_level_num:
        player.score += player.lives * 500
    else:
        player.score = 0

    loadLevel(new_level_num)

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

    for entity in entities:
        if not entity.dead:
            if isinstance(entity, Explosion):
                screen.blit(entity.image, (entity.rect.x, entity.rect.y), (Explosion.WIDTH * entity.state, 0,
                                                                           Explosion.WIDTH, Explosion.HEIGHT))
            else:
                screen.blit(entity.image, (entity.rect.x, entity.rect.y))

    pygame.draw.rect(screen, (0, 0, 0), (PLAYFIELD_PADDING[0], 0, WINDOW_WIDTH - PLAYFIELD_PADDING[0] * 2,
                                         PLAYFIELD_PADDING[1]))

    screen.blit(scoreLabel, (PLAYFIELD_PADDING[0] + 10, 0))
    screen.blit(livesLabel, (PLAYFIELD_PADDING[0] + 150, 0))
    screen.blit(levelLabel, (WINDOW_WIDTH - 100, 0))

    pygame.display.flip()

clock = GameClock(max_ups=60, max_fps=60, update_callback=_update, frame_callback=_draw)

while True:
    clock.tick()

