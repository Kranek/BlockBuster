"""
This file contains Level Editor GameState
"""
import sys
# import pygame
from pygame.locals import QUIT, MOUSEMOTION, MOUSEBUTTONDOWN, MOUSEBUTTONUP, KEYDOWN, K_ESCAPE,\
    K_MINUS, K_KP_MINUS, K_EQUALS, K_KP_PLUS, K_0, K_KP0, K_F5, K_F9
from gamedata import Assets
from blocks import Block
from constants import WINDOW_HEIGHT, BLOCK_NUM_WIDTH, BLOCK_NUM_HEIGHT, MB_LEFT, MB_RIGHT,\
    MB_WHEEL_UP, MB_WHEEL_DOWN, MB_MIDDLE, LEVEL_WIDTH, PLAYFIELD_PADDING
# from GameStateMenu import *
from LevelLoader import LevelLoader
from tkFileDialog import askopenfilename, asksaveasfilename


class GameStateEditor(object):
    """
    Level Editor GameState
    """
    editor_info_padding = (30, WINDOW_HEIGHT - 20)
    editor_help_top_padding = (30, 0)

    def __init__(self, context, screen, prev_state):
        """
        Init with context, main PyGame surface and the previous state
        if you want to be able to go back
        :param context: The field in the main application which contains the current GameState.
        Current GameState has input events pumped into it, is updated and then drawn on the screen.
        Used by the current state to switch to the other GameState
        :param screen: Main PyGame surface to draw the objects/UI on
        :param prev_state: The state to which we will return
        :return:
        """
        self.context = context
        self.screen = screen
        self.prev_state = prev_state
        self.background = Assets.background
        self.border = Assets.border
        self.blocks = []
        self.block_types = dict()
        for i in xrange(0, len(Assets.blocks)):
            self.block_types[str(i + 1)] = Assets.blocks[i]
        self.block_types['e'] = Assets.blockE
        self.block_types['i'] = Assets.blockI
        self.block_types['m'] = Assets.blocksM[len(Assets.blocksM) - 1]
        # self.block_types['0'] = AssetManager.editor_cursor_block
        self.available_block_types = sorted(self.block_types.keys())
        # self.available_block_types.append('0')
        for _ in xrange(0, BLOCK_NUM_HEIGHT):
            self.blocks.append(['0', ] * BLOCK_NUM_WIDTH)
            # for x in xrange(0, BLOCK_NUM_WIDTH):
        self.editor_cursor_block = Assets.editor_cursor_block
        self.editor_cursor_position = (0, 0)
        self.current_block_type = 0
        self.mode_paint = False
        self.mode_erase = False
        self.font = Assets.font
        self.label_current_block_type = self.font.render(
            "Current block:              +/-/mouse wheel to change block type, 0 to reset",
            1, (255, 255, 255))
        self.label_help_top = self.font.render(
            "Esc - Back to menu, F5 - Save, F9 - Load, RMB - Remove block, MMB - Pick block",
            1, (255, 255, 255))
        # print sorted(self.block_types.keys())

    def handle_input(self, events):
        """
        Handles incoming input events
        :param events: input events from the main app
        :return:
        """
        for event in events:
            if event.type == QUIT:
                sys.exit(0)

            elif event.type == MOUSEMOTION:
                if self.is_in_bounds(event.pos):
                    self.editor_cursor_position = self.position_screen_to_grid(event.pos)
                    if self.mode_paint:
                        self.put_block()
                    elif self.mode_erase:
                        self.erase_block()
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == MB_LEFT:
                    if self.is_in_bounds(event.pos):
                        self.put_block()
                    self.mode_paint = True
                    self.mode_erase = False
                elif event.button == MB_RIGHT:
                    if self.is_in_bounds(event.pos):
                        self.erase_block()
                    self.mode_erase = True
                    self.mode_paint = False
                elif event.button == MB_MIDDLE:
                    if self.is_in_bounds(event.pos):
                        self.pick_block()
                elif event.button == MB_WHEEL_DOWN:
                    self.next_block_type()
                elif event.button == MB_WHEEL_UP:
                    self.prev_block_type()
                # print str(self.mode_paint) + " " + str(self.mode_erase)
            elif event.type == MOUSEBUTTONUP:
                self.mode_paint = False
                self.mode_erase = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # from GameStateMenu import GameStateMenu
                    self.context["gamestate"] = self.prev_state
                if event.key == K_MINUS or event.key == K_KP_MINUS:
                    self.prev_block_type()
                elif event.key == K_EQUALS or event.key == K_KP_PLUS:
                    self.next_block_type()
                elif event.key == K_0 or event.key == K_KP0:
                    self.current_block_type = 0
                elif event.key == K_F5:
                    self.save()
                elif event.key == K_F9:
                    self.open()
            # else:
            #     print event

    def prev_block_type(self):
        """
        Range-enforcer, not to go out of block-type list bounds
        :return:
        """
        if self.current_block_type <= 0:
            self.current_block_type = len(self.available_block_types) - 1
        else:
            self.current_block_type -= 1

    def next_block_type(self):
        """
        Range-enforcer, not to go out of block-type list bounds
        :return:
        """
        if self.current_block_type >= len(self.available_block_types) - 1:
            self.current_block_type = 0
        else:
            self.current_block_type += 1

    def draw(self):
        """
        Method called each frame to (re)draw the objects and UI
        :return:
        """
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.border, (0, 0))
        self.screen.blit(self.border, (LEVEL_WIDTH - PLAYFIELD_PADDING[0], 0))
        for y in xrange(0, BLOCK_NUM_HEIGHT):
            for x in xrange(0, BLOCK_NUM_WIDTH):
                if self.blocks[y][x] == '0':
                    pass
                else:
                    self.screen.blit(self.block_types[self.blocks[y][x]],
                                     (PLAYFIELD_PADDING[0] + x * Block.WIDTH,
                                      PLAYFIELD_PADDING[1] + y * Block.HEIGHT))
        self.screen.blit(self.editor_cursor_block,
                         self.position_grid_to_screen(self.editor_cursor_position))
        self.screen.blit(self.label_help_top, self.editor_help_top_padding)
        self.screen.blit(self.label_current_block_type, self.editor_info_padding)
        self.screen.blit(self.block_types[self.available_block_types[self.current_block_type]],
                         (self.editor_info_padding[0] + 100, self.editor_info_padding[1]))
        # print str(self.editor_cursor_position) + " " +
        # str(self.position_grid_to_screen(self.editor_cursor_position))

    def update(self):
        """
        This state does not really need to update any objects, because it operates
        solely on the input events
        :return:
        """
        pass

    def put_block(self):
        """
        Helper function that puts the block on the current Editor Cursor Block position
        :return:
        """
        self.blocks[self.editor_cursor_position[1]][
            self.editor_cursor_position[0]] = self.available_block_types[self.current_block_type]

    def erase_block(self):
        """
        Helper function that removes the block from the current Editor Cursor Block position
        :return:
        """
        self.blocks[self.editor_cursor_position[1]][self.editor_cursor_position[0]] = '0'

    def pick_block(self):
        """
        Helper function that gets the block from the current Editor Cursor Block position
        :return:
        """
        current_block = self.blocks[self.editor_cursor_position[1]][self.editor_cursor_position[0]]
        if current_block in self.available_block_types:
            self.current_block_type = self.available_block_types.index(current_block)

    @staticmethod
    def position_screen_to_grid(vec):
        """
        Helper static function used to calculate mouse position on the block grid
        :param vec: Vector straight from the mouse motion event
        :return:
        """
        pos = ((vec[0] - PLAYFIELD_PADDING[0]) / Block.WIDTH,
               (vec[1] - PLAYFIELD_PADDING[1]) / Block.HEIGHT)
        return pos

    @staticmethod
    def position_grid_to_screen(vec):
        """
        Helper static function used to calculate the block position on the screen
        (from block grid coordinates)
        :param vec: On-Grid Block position vector
        :return:
        """
        return (PLAYFIELD_PADDING[0] + vec[0] * Block.WIDTH,
                PLAYFIELD_PADDING[1] + vec[1] * Block.HEIGHT)

    @staticmethod
    def is_in_bounds(pos):
        """
        Helper static function to ensure we are not trying to read out of bounds index
        from the block grid
        :param pos: Position on the screen, usually straight from the mouse motion event
        :return:
        """
        return PLAYFIELD_PADDING[0] < pos[0] < PLAYFIELD_PADDING[0] +\
            BLOCK_NUM_WIDTH * Block.WIDTH and PLAYFIELD_PADDING[1] < pos[1] <\
            PLAYFIELD_PADDING[1] + BLOCK_NUM_HEIGHT * Block.HEIGHT

    def save(self):
        """
        Method used to save the level, by using Save File dialog
        :return:
        """
        data = ""
        for y in xrange(0, BLOCK_NUM_HEIGHT):
            for x in xrange(0, BLOCK_NUM_WIDTH):
                data += self.blocks[y][x]
            data += '\n'
        print data
        options = {'defaultextension': '.lvl',
                   'filetypes': [('Levels', '.lvl'), ('All files', '*')],
                   'initialdir': 'levels',
                   'initialfile': '',
                   'title': 'Save level'}
        # filename = tkFileDialog.asksaveasfile(**options)
        filename = asksaveasfilename(**options)
        if filename:
            with open(filename, "w") as level:
                level.write(data)

    def open(self):
        """
        Method used to load level, by using Open File dialog
        :return:
        """
        options = {'defaultextension': '.lvl',
                   'filetypes': [('Levels', '.lvl'), ('All files', '*')],
                   'initialdir': 'levels',
                   'initialfile': '',
                   'title': 'Open level'}
        filename = askopenfilename(**options)
        if filename:
            self.blocks = LevelLoader.load(filename)[0]
