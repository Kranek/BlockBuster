"""
This file contains Level class, which stores most of the gameplay-related objects and logic
"""
from pygame import sprite, draw, Surface, SRCALPHA
from pygame.locals import KEYDOWN, KEYUP, K_EQUALS, K_1, K_2, K_3, K_4, K_5, K_6, K_SPACE
# K_SPACE, K_1, K_2, K_3, K_4
from Player import Player
from paddle import Paddle
from ball import Ball
from blocks import Block, BlockExplosive, BlockIndestructible, BlockMultiHit
from projectiles import Projectile
from explosion import Explosion
from gamedata import Assets
from LevelLoader import LevelLoader
from items import Item, ItemLife, ItemExpand, ItemLaserGun, ItemShrink, ItemPaddleNano, \
    ItemShrinkMulti, ItemPaddleNanoMulti, ItemAddBlocks
from constants import LEVEL_WIDTH, LEVEL_HEIGHT, LEVELDIR, BLOCK_NUM_WIDTH, BLOCK_NUM_HEIGHT,\
    PLAYFIELD_PADDING, PADDLE_WIDTHS, PADDLE_DEFAULT_WIDTH_INDEX, get_level_count
from random import randint


class Level(object):
    """
    Main Level class, handles most of the gameplay
    """
    def __init__(self, screen, draw_offset, control_set, player_color, finish_game):
        """
        Init with... way too many parameters
        :param screen: Main PyGame surface to draw the objects/UI on
        :param draw_offset: Drawing offset used in multiplayer
        :param control_set: Key-set used to control the Paddle
        :param player_color: Color of the player's Paddle
        :param finish_game: Function passed to the constructor, triggered on
        the game end
        :return:
        """
        self.screen = screen
        self.draw_offset = draw_offset
        self.control_set = control_set
        self.prev_input_x = 0
        self.level_number = 1
        self.block_count = 0
        self.player = Player("Derp")
        self.paddle = Paddle(LEVEL_WIDTH/2 - Paddle.WIDTH/2, LEVEL_HEIGHT - 40,
                             player_color, parent=self, owner=self.player)
        self.ball = Ball(self.paddle.rect.x + Paddle.WIDTH/2 - Ball.RADIUS,
                         self.paddle.rect.y - Ball.RADIUS * 2)
        self.items = None
        self.blocks = []
        self.blocks_surface = None
        self.blocks_surface_dirty = True
        self.entities = []
        self.font = Assets.font
        self.score_label = None
        self.lives_label = None
        self.level_label = None
        self.load_level(self.level_number)
        self.finish_game = finish_game

    def handle_input(self, events):
        """
        Handles incoming input events
        :param events: input events from the main app
        :return:
        """
        BONUS_SPAWN_X = 305
        BONUS_SPAWN_Y = 200
        for event in events:
            if event.type == KEYDOWN:
                if event.key == self.control_set[0]:
                    if self.paddle.vx != 0:
                        self.prev_input_x = 1
                    self.paddle.vx = -1

                elif event.key == self.control_set[2]:
                    if self.paddle.vx != 0:
                        self.prev_input_x = -1
                    self.paddle.vx = 1

                # elif event.key == K_SPACE:
                #     self.paddle.change_size(self.paddle.rect.width+10)

                elif event.key == K_1:
                    # self.add_entity(ItemExpand(BONUS_SPAWN_X, BONUS_SPAWN_Y))
                    self.spawn_item(BONUS_SPAWN_X, BONUS_SPAWN_Y, 1)

                elif event.key == K_2:
                    # self.add_entity(ItemLaserGun(BONUS_SPAWN_X, BONUS_SPAWN_Y))
                    self.spawn_item(BONUS_SPAWN_X, BONUS_SPAWN_Y, 2)

                elif event.key == K_3:
                    # self.add_entity(ItemShrink(BONUS_SPAWN_X, BONUS_SPAWN_Y))
                    self.spawn_item(BONUS_SPAWN_X, BONUS_SPAWN_Y, 3)

                elif event.key == K_4:
                    # self.add_entity(ItemPaddleNano(BONUS_SPAWN_X, BONUS_SPAWN_Y))
                    self.spawn_item(BONUS_SPAWN_X, BONUS_SPAWN_Y, 4)

                elif event.key == K_5:
                    # self.add_entity(ItemLife(BONUS_SPAWN_X, BONUS_SPAWN_Y))
                    self.spawn_item(BONUS_SPAWN_X, BONUS_SPAWN_Y, 5)

                elif event.key == K_6:
                    # self.add_entity(ItemLife(BONUS_SPAWN_X, BONUS_SPAWN_Y))
                    self.spawn_item(BONUS_SPAWN_X, BONUS_SPAWN_Y, 6)

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
                    else:
                        self.paddle.use_attachment()

                elif event.key == K_EQUALS:
                    self.start_level(self.level_number + 1)

    def start_level(self, new_level_num):
        """
        Used to start level, checks the level bounds
        :param new_level_num:
        :return:
        """
        self.ball.docked = True
        self.ball.dead = False

        if new_level_num > get_level_count():
            self.finish_game()
        else:
            if self.level_number < new_level_num:
                self.player.score += self.player.lives * 500
            else:
                self.player.score = 0

            self.load_level(new_level_num)
            self.paddle.change_size(PADDLE_WIDTHS[PADDLE_DEFAULT_WIDTH_INDEX])
            self.paddle.attachments = []
            self.paddle.rect.x = LEVEL_WIDTH/2 - self.paddle.rect.width/2
            self.paddle.rect.y = LEVEL_HEIGHT - 40
            self.player.lives = 3
            self.blocks_surface = Surface((LEVEL_WIDTH, LEVEL_HEIGHT))
            self.blocks_surface_dirty = True

    def load_level(self, new_level_num):
        """
        Parses level from the Character array that is provided by the LevelLoader class
        :param new_level_num: Number of the level, used to construct the filename,
        compute the next level number, and viewed on the UI
        :return:
        """
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
                                              PLAYFIELD_PADDING[1] + y * Block.HEIGHT,
                                              int(level[y][x]) - 1)
                    self.block_count += 1

    def add_entity(self, entity):
        """
        Utility function to add new entities to the level. Later, might search for dead entities
        to replace them instead of expanding the list indefinitely
        :param entity:
        :return:
        """
        self.entities.append(entity)

    def spawn_item(self, x, y, item):
        """
        Function used to spawn items from blocks
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :param item: item to spawn, leave empty to make it randomly selected
        :return:
        """
        if item == 1:
            self.add_entity(ItemLife(x, y))
        elif item == 2:
            self.add_entity(ItemExpand(x, y))
        elif item == 3:
            self.add_entity(ItemShrink(x, y))
        elif item == 4:
            self.add_entity(ItemLaserGun(x, y))
        elif item == 5:
            self.add_entity(ItemPaddleNano(x, y))
        elif item == 6:
            pass
        elif randint(0, 35) == 0:
            item_type = randint(0, 4)
            if item_type == 0:
                dropped_item = ItemLife(x, y)
            elif item_type == 1:
                dropped_item = ItemExpand(x, y)
            elif item_type == 2:
                dropped_item = ItemShrink(x, y)
            elif item_type == 3:
                dropped_item = ItemLaserGun(x, y)
            else:
                dropped_item = ItemPaddleNano(x, y)
            self.add_entity(dropped_item)

    def block_destruction(self, block, item, func):
        """
        Decides what to do with the block, based on the block type (sigh), and performs
        appropriate action
        :param block: Block to operate on
        :param item: If the block has a hard-assigned item in level, it will be spawned
        :param func: Function of the block that returns its points-value
        :return:
        """
        return_v = func()
        if isinstance(block, BlockExplosive):
            rect = block.rect
            self.entities.append(Explosion(rect.x + rect.width/2 - Explosion.WIDTH/2,
                                           rect.y + rect.height/2 - Explosion.HEIGHT/2))

        if block.dead:
            self.player.add_points(return_v)
            self.block_count -= 1
            if not isinstance(block, BlockExplosive):
                self.spawn_item(block.rect.x, block.rect.y, item)
        self.blocks_surface_dirty = True

    def draw(self):
        """
        Method called each frame to (re)draw the objects and UI
        :return:
        """
        self.screen.blit(Assets.background, (self.draw_offset[0], self.draw_offset[1]))

        self.screen.blit(Assets.border, (self.draw_offset[0], self.draw_offset[1]))
        self.screen.blit(Assets.border, (self.draw_offset[0] + LEVEL_WIDTH - PLAYFIELD_PADDING[0],
                                         self.draw_offset[1]))
        if self.blocks_surface_dirty:
            self.blocks_surface = Surface((LEVEL_WIDTH, LEVEL_HEIGHT), SRCALPHA, 32)
            self.blocks_surface = self.blocks_surface.convert_alpha()
            self.blocks_surface_dirty = False
            for row in self.blocks:
                for block in row:
                    if block is not None and not block.dead:
                        block.draw(self.blocks_surface)
        self.screen.blit(self.blocks_surface, self.draw_offset)
        self.paddle.draw(self.screen, self.draw_offset)

        if not self.ball.dead:
            self.ball.draw(self.screen, self.draw_offset)

        # draw entities
        for entity in self.entities:
            if not entity.dead:
                entity.draw(self.screen, self.draw_offset)

        # draw upper bar
        draw.rect(self.screen, (0, 0, 0), (self.draw_offset[0] + PLAYFIELD_PADDING[0], self.draw_offset[1],
                                           LEVEL_WIDTH - PLAYFIELD_PADDING[0] * 2, PLAYFIELD_PADDING[1]))

        self.screen.blit(self.score_label,
                         (self.draw_offset[0] + PLAYFIELD_PADDING[0] + 10, self.draw_offset[1]))
        self.screen.blit(self.lives_label,
                         (self.draw_offset[0] + PLAYFIELD_PADDING[0] + 150, self.draw_offset[1]))
        self.screen.blit(self.level_label,
                         (self.draw_offset[0] + LEVEL_WIDTH - 100, self.draw_offset[1]))

    def update(self):
        """
        Method called each frame, to update the state of entities based on input events and
        previous state of the game
        :return:
        """
        if self.block_count <= 0:
            self.start_level(self.level_number + 1)
        elif self.player.lives <= 0:
            self.start_level(self.level_number)

        self.paddle.update()
        if self.ball.docked and not self.ball.dead:
            self.ball.rect.x = self.paddle.rect.x + self.paddle.rect.width/2 - self.ball.radius
            self.ball.rect.y = self.paddle.rect.y - self.ball.radius * 2
        elif self.player.lives > 0:
            self.ball.update()
        for entity in self.entities:
            if not entity.dead:
                entity.update()

        self.check_collision()
        self.score_label = self.font.render("SCORE: " + str(self.player.score), 1, (255, 255, 255))
        self.lives_label = self.font.render("LIVES: " + str(self.player.lives), 1, (255, 255, 255))
        self.level_label = self.font.render("LEVEL " + str(self.level_number), 1, (255, 255, 255))

    def check_collision(self):
        """
        Called after input handling and movement of the object, to check and solve collisions
        :return:
        """
        # ball vs paddle
        if self.ball.rect.y < self.paddle.rect.y and \
                sprite.collide_rect(self.paddle, self.ball):
            self.ball.vy = -1  # ball.vy

        # ball vs bottom
        if not self.ball.dead and self.ball.rect.y + self.ball.radius * 2 > LEVEL_HEIGHT:
            self.player.lives -= 1
            if self.player.lives < 1:
                self.ball.dead = True
            else:
                self.ball.rect.x = self.paddle.rect.x + self.paddle.rect.width/2 - self.ball.radius
                self.ball.rect.y = self.paddle.rect.y - self.ball.radius * 2
            self.ball.docked = True
            self.paddle.change_size(PADDLE_WIDTHS[PADDLE_DEFAULT_WIDTH_INDEX])
            self.paddle.attachments = []

        # ball vs blocks
        coll_num = [0, 0, 0]
        coll_num_val = (4, 2, 1)
        ball_grid_x = (self.ball.rect.x - PLAYFIELD_PADDING[0] + self.ball.radius) / Block.WIDTH
        ball_grid_y = (self.ball.rect.y - PLAYFIELD_PADDING[1] + self.ball.radius) / Block.HEIGHT
        for y in range(ball_grid_y - 1, ball_grid_y + 2):
            for x in range(ball_grid_x - 1, ball_grid_x + 2):
                if 0 <= x < BLOCK_NUM_WIDTH and 0 <= y < BLOCK_NUM_HEIGHT:
                    if self.blocks[y][x] is not None and not self.blocks[y][x].dead and \
                            sprite.collide_rect(self.blocks[y][x], self.ball):
                        self.block_destruction(self.blocks[y][x],
                                               self.items[y][x], self.blocks[y][x].on_collide)

                        coll_num[y - ball_grid_y + 1] += coll_num_val[x - ball_grid_x + 1]

        self.ball.on_collide(coll_num)

        # entities
        for entity in self.entities:
            if not entity.dead:
                # paddle vs items
                if isinstance(entity, Item) and sprite.collide_rect(self.paddle, entity):
                    entity.on_collect(self.paddle)
                    entity.dead = True
                    # self.player.lives += 1
                # explosion vs blocks
                elif isinstance(entity, Explosion) and entity.state > 0:
                    entity_block_x = (entity.rect.x - PLAYFIELD_PADDING[0] +
                                      Explosion.WIDTH/2) / Block.WIDTH
                    entity_block_y = (entity.rect.y - PLAYFIELD_PADDING[1] +
                                      Explosion.HEIGHT/2) / Block.HEIGHT
                    for y in xrange(entity_block_y - 1, entity_block_y + 2):
                        for x in xrange(entity_block_x - 1, entity_block_x + 2):
                            if 0 <= x < BLOCK_NUM_WIDTH and 0 <= y < BLOCK_NUM_HEIGHT:
                                if self.blocks[y][x] is not None and not self.blocks[y][x].dead:
                                    self.block_destruction(self.blocks[y][x], self.items[y][x],
                                                           self.blocks[y][x].kill)
                elif isinstance(entity, Projectile):
                    entity_block_x = (entity.rect.x - PLAYFIELD_PADDING[0] +
                                      entity.rect.width/2) / Block.WIDTH
                    entity_block_y = (entity.rect.y - PLAYFIELD_PADDING[1] +
                                      entity.rect.height/2) / Block.HEIGHT
                    for y in xrange(entity_block_y - 1, entity_block_y + 2):
                        for x in xrange(entity_block_x - 1, entity_block_x + 2):
                            if 0 <= x < BLOCK_NUM_WIDTH and 0 <= y < BLOCK_NUM_HEIGHT:
                                if self.blocks[y][x] is not None and not self.blocks[y][x].dead \
                                        and sprite.collide_rect(self.blocks[y][x], entity):
                                    self.block_destruction(self.blocks[y][x], self.items[y][x],
                                                           self.blocks[y][x].kill)
                                    entity.on_collide()


class LevelMulti(Level):
    """
    Multiplayer Level variant, handles item spawning differently
    """
    def __init__(self, screen, draw_offset, control_set, player_color, finish_game, disturb_player):
        """
        Init more or less like the main class
        :param screen: Main PyGame surface to draw the objects/UI on
        :param draw_offset: Drawing offset used in multiplayer
        :param control_set: Key-set used to control the Paddle
        :param player_color: Color of the player's Paddle
        :param finish_game: Function passed to the constructor, triggered on
        the game end
        :param disturb_player: Function passed to the level to disturb other players' gameplay
        :return:
        """
        Level.__init__(self, screen, draw_offset, control_set, player_color, finish_game)
        self.player_color = player_color
        self.disturb_player = disturb_player

    def place_random_blocks(self):
        """
        Creates additional random blocks and places them
        :return:
        """
        amount = randint(1, 4)
        for _ in xrange(0, amount):
            x = randint(0, BLOCK_NUM_WIDTH - 1)
            y = randint(0, BLOCK_NUM_HEIGHT - 1)
            new_block = BlockMultiHit(x * Block.WIDTH + PLAYFIELD_PADDING[0], y * Block.HEIGHT + PLAYFIELD_PADDING[1])
            while self.blocks[y][x] is not None or sprite.collide_rect(new_block, self.ball):
                x = randint(0, BLOCK_NUM_WIDTH - 1)
                y = randint(0, BLOCK_NUM_HEIGHT - 1)
                new_block.rect.x = x * Block.WIDTH + PLAYFIELD_PADDING[0]
                new_block.rect.y = y * Block.HEIGHT + PLAYFIELD_PADDING[1]
            self.blocks[y][x] = new_block
            self.block_count += 1
        self.blocks_surface_dirty = True

    def spawn_item(self, x, y, item):
        """
        Function used to spawn items from blocks
        :param x: x coordinate of the play-field
        :param y: y coordinate of the play-field
        :param item: item to spawn, leave empty to make it randomly selected
        :return:
        """
        if item == 1:
            self.add_entity(ItemLife(x, y))
        elif item == 2:
            self.add_entity(ItemExpand(x, y))
        elif item == 3:
            self.add_entity(ItemShrinkMulti(x, y, self))
        elif item == 4:
            self.add_entity(ItemLaserGun(x, y))
        elif item == 5:
            self.add_entity(ItemPaddleNanoMulti(x, y, self))
        elif item == 6:
            self.add_entity(ItemAddBlocks(x, y, self))
        elif randint(0, 25) == 0:
            item_type = randint(0, 5)
            if item_type == 0:
                dropped_item = ItemLife(x, y)
            elif item_type == 1:
                dropped_item = ItemExpand(x, y)
            elif item_type == 2:
                dropped_item = ItemShrinkMulti(x, y, self)
            elif item_type == 3:
                dropped_item = ItemLaserGun(x, y)
            elif item_type == 4:
                dropped_item = ItemPaddleNanoMulti(x, y, self)
            else:
                dropped_item = ItemAddBlocks(x, y, self)
            self.add_entity(dropped_item)
