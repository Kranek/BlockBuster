import sys
import pygame
from pygame.locals import *
from AssetManager import AssetManager
from LevelLoader import LevelLoader
from Player import Player
from Paddle import Paddle
from Ball import Ball
from Block import Block
from BlockIndestructible import BlockIndestructible
from BlockMultiHit import BlockMultiHit
from BlockExplosive import BlockExplosive
from ItemLife import ItemLife
from Explosion import Explosion
from constants import *
from GameStatePauseMenu import GameStatePauseMenu


class GameStateRunning:

    def __init__(self, context, screen, prev_state, draw_offset, control_set, player_color):
        self.context = context
        self.screen = screen
        # self.background = AssetManager.background
        self.draw_offset = draw_offset
        self.control_set = control_set
        self.prev_input_x = 0
        self.level_number = 1
        self.block_count = 0
        self.player = Player("Derp")
        self.paddle = Paddle(LEVEL_WIDTH/2 - Paddle.WIDTH/2, LEVEL_HEIGHT - 40, player_color)
        self.ball = Ball(self.paddle.rect.x + Paddle.WIDTH/2 - Ball.RADIUS, self.paddle.rect.y - Ball.RADIUS * 2)
        self.items = None
        self.blocks = []
        self.entities = []
        self.font = AssetManager.font
        self.scoreLabel = None
        self.livesLabel = None
        self.levelLabel = None
        self.load_level(self.level_number)
        self.prev_state = prev_state

    def handle_input(self, events):
        for event in events:
            if event.type == QUIT:
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == self.control_set[0]:
                    if self.paddle.vx != 0:
                        self.prev_input_x = 1
                    self.paddle.vx = -1

                elif event.key == self.control_set[2]:
                    if self.paddle.vx != 0:
                        self.prev_input_x = -1
                    self.paddle.vx = 1

                elif event.key == K_ESCAPE:
                    self.context["gamestate"] = GameStatePauseMenu(self.context, self.screen, self)

            elif event.type == KEYUP:
                if event.key == self.control_set[0]:
                    if self.prev_input_x < 0:
                        self.prev_input_x = 0
                    elif self.prev_input_x > 0:
                        self.paddle.vx = 1
                        self.prev_input_x = 0
                    else:
                        self.paddle.vx = 0

                elif event.key == self.control_set[2]:
                    if self.prev_input_x > 0:
                        self.prev_input_x = 0
                    elif self.prev_input_x < 0:
                        self.paddle.vx = -1
                        self.prev_input_x = 0
                    else:
                        self.paddle.vx = 0

                elif event.key == self.control_set[1]:
                    if self.ball.docked:
                        self.ball.docked = False
                        self.ball.vx = 1
                        self.ball.vy = -1

                elif event.key == K_EQUALS:
                    self.start_level(self.level_number + 1)

    def start_level(self, new_level_num):
        self.ball.docked = True
        self.ball.dead = False

        if new_level_num > MAX_LEVEL:
            new_level_num = 1

        if self.level_number < new_level_num:
            self.player.score += self.player.lives * 500
        else:
            self.player.score = 0

        self.load_level(new_level_num)

        self.paddle.rect.x = LEVEL_WIDTH/2 - self.paddle.rect.width/2
        self.paddle.rect.y = LEVEL_HEIGHT - 40
        self.player.lives = 3

    def load_level(self, new_level_num):
        loaded_level = LevelLoader.load(LEVELDIR + str(new_level_num).zfill(2) + ".lvl")
        level = loaded_level[0]
        self.items = loaded_level[1]
        self.level_number = new_level_num
        self.blocks = []
        self.entities = []
        self.block_count = 0
        for y in xrange(0, BLOCK_NUM_HEIGHT):
            self.blocks.append([None, ] * BLOCK_NUM_WIDTH)
            for x in xrange(0, BLOCK_NUM_WIDTH):
                if level[y][x] == 'i':
                    self.blocks[y][x] = BlockIndestructible(PLAYFIELD_PADDING[0] + x * Block.WIDTH,
                                                            PLAYFIELD_PADDING[1] + y * Block.HEIGHT)
                elif level[y][x] == 'm':
                    self.blocks[y][x] = BlockMultiHit(PLAYFIELD_PADDING[0] + x * Block.WIDTH,
                                                      PLAYFIELD_PADDING[1] + y * Block.HEIGHT)
                    self.block_count += 1
                elif level[y][x] == 'e':
                    self.blocks[y][x] = BlockExplosive(PLAYFIELD_PADDING[0] + x * Block.WIDTH,
                                                       PLAYFIELD_PADDING[1] + y * Block.HEIGHT)
                    self.block_count += 1
                elif level[y][x] != '0':
                    self.blocks[y][x] = Block(PLAYFIELD_PADDING[0] + x * Block.WIDTH,
                                              PLAYFIELD_PADDING[1] + y * Block.HEIGHT, int(level[y][x]) - 1)
                    self.block_count += 1

    def block_destruction(self, block, item, func):
        if item == 1:
            self.entities.append(ItemLife(block.rect.x, block.rect.y))

        return_v = func()
        if isinstance(block, BlockExplosive):
            rect = block.rect
            self.entities.append(Explosion(rect.x + rect.width/2 - Explosion.WIDTH/2,
                                           rect.y + rect.height/2 - Explosion.HEIGHT/2))

        if block.dead:
            self.player.score += return_v
            self.block_count -= 1

    def draw(self):
        self.screen.blit(AssetManager.background, (self.draw_offset[0], self.draw_offset[1]))

        self.screen.blit(AssetManager.border, (self.draw_offset[0], self.draw_offset[1]))
        self.screen.blit(AssetManager.border, (self.draw_offset[0] + LEVEL_WIDTH - PLAYFIELD_PADDING[0], self.draw_offset[1]))
        for row in self.blocks:
            for block in row:
                if block is not None and not block.dead:
                    self.screen.blit(block.image, (self.draw_offset[0] + block.rect.x,
                                                   self.draw_offset[1] + block.rect.y))
        self.screen.blit(self.paddle.image, (self.draw_offset[0] + self.paddle.rect.x,
                                             self.draw_offset[1] + self.paddle.rect.y))
        if not self.ball.dead:
            self.screen.blit(self.ball.image, (self.draw_offset[0] + self.ball.rect.x,
                                               self.draw_offset[1] + self.ball.rect.y))

        for entity in self.entities:
            if not entity.dead:
                if isinstance(entity, Explosion):
                    self.screen.blit(entity.image, (self.draw_offset[0] + entity.rect.x,
                                                    self.draw_offset[1] + entity.rect.y),
                                     (Explosion.WIDTH * entity.state, 0, Explosion.WIDTH, Explosion.HEIGHT))
                else:
                    self.screen.blit(entity.image, (self.draw_offset[0] + entity.rect.x,
                                                    self.draw_offset[1] + entity.rect.y))

        pygame.draw.rect(self.screen, (0, 0, 0), (self.draw_offset[0] + PLAYFIELD_PADDING[0], self.draw_offset[1],
                                                  LEVEL_WIDTH - PLAYFIELD_PADDING[0] * 2, PLAYFIELD_PADDING[1]))

        self.screen.blit(self.scoreLabel, (self.draw_offset[0] + PLAYFIELD_PADDING[0] + 10, self.draw_offset[1]))
        self.screen.blit(self.livesLabel, (self.draw_offset[0] + PLAYFIELD_PADDING[0] + 150, self.draw_offset[1]))
        self.screen.blit(self.levelLabel, (self.draw_offset[0] + LEVEL_WIDTH - 100, self.draw_offset[1]))

    def update(self):
        if self.block_count <= 0:
            self.start_level(self.level_number + 1)
        elif self.player.lives <= 0:
            self.start_level(self.level_number)

        self.paddle.update()
        if self.ball.docked and not self.ball.dead:
            self.ball.rect.x = self.paddle.rect.x + self.paddle.rect.width/2 - Ball.RADIUS
            self.ball.rect.y = self.paddle.rect.y - Ball.RADIUS * 2
        elif self.player.lives > 0:
            self.ball.update()
        for entity in self.entities:
            if not entity.dead:
                entity.update()

        self.check_collision()
        self.scoreLabel = self.font.render("SCORE: " + str(self.player.score), 1, (255, 255, 255))
        self.livesLabel = self.font.render("LIVES: " + str(self.player.lives), 1, (255, 255, 255))
        self.levelLabel = self.font.render("LEVEL " + str(self.level_number), 1, (255, 255, 255))

    def check_collision(self):
        # ball vs paddle
        if self.ball.rect.y < self.paddle.rect.y and pygame.sprite.collide_rect(self.paddle, self.ball):
            self.ball.vy = -1  # ball.vy

        # ball vs bottom
        if not self.ball.dead and self.ball.rect.y + self.ball.RADIUS * 2 > LEVEL_HEIGHT:
            self.player.lives -= 1
            if self.player.lives < 1:
                self.ball.dead = True
            else:
                self.ball.rect.x = self.paddle.rect.x + self.paddle.rect.width/2 - Ball.RADIUS
                self.ball.rect.y = self.paddle.rect.y - self.ball.RADIUS * 2
            self.ball.docked = True

        # ball vs blocks
        coll_num = [0, 0, 0]
        coll_num_val = (4, 2, 1)
        ball_grid_x = (self.ball.rect.x - PLAYFIELD_PADDING[0] + self.ball.RADIUS) / Block.WIDTH
        ball_grid_y = (self.ball.rect.y - PLAYFIELD_PADDING[1] + self.ball.RADIUS) / Block.HEIGHT
        for y in range(ball_grid_y - 1, ball_grid_y + 2):
            for x in range(ball_grid_x - 1, ball_grid_x + 2):
                if 0 <= x < BLOCK_NUM_WIDTH and 0 <= y < BLOCK_NUM_HEIGHT:
                    if self.blocks[y][x] is not None and not self.blocks[y][x].dead and \
                            pygame.sprite.collide_rect(self.blocks[y][x], self.ball):
                        self.block_destruction(self.blocks[y][x], self.items[y][x], self.blocks[y][x].onCollide)

                        coll_num[y - ball_grid_y + 1] += coll_num_val[x - ball_grid_x + 1]

        self.ball.onCollide(coll_num)

        # entities
        for entity in self.entities:
            if not entity.dead:
                # paddle vs items
                if isinstance(entity, ItemLife) and pygame.sprite.collide_rect(self.paddle, entity):
                    entity.dead = True
                    self.player.lives += 1
                # explosion vs blocks
                elif isinstance(entity, Explosion) and entity.state > 0:
                    entity_block_x = (entity.rect.x - PLAYFIELD_PADDING[0] + Explosion.WIDTH/2) / Block.WIDTH
                    entity_block_y = (entity.rect.y - PLAYFIELD_PADDING[1] + Explosion.HEIGHT/2) / Block.HEIGHT
                    for y in xrange(entity_block_y - 1, entity_block_y + 2):
                        for x in xrange(entity_block_x - 1, entity_block_x + 2):
                            if 0 <= x < BLOCK_NUM_WIDTH and 0 <= y < BLOCK_NUM_HEIGHT:
                                if self.blocks[y][x] is not None and not self.blocks[y][x].dead:
                                    self.block_destruction(self.blocks[y][x], self.items[y][x], self.blocks[y][x].kill)