import glob
import pygame

LEVEL_WIDTH = 640
LEVEL_HEIGHT = 480

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 480

PLAYFIELD_PADDING = (20, 20)
LEVELDIR = "levels/"

MAX_LEVEL = len(glob.glob1(LEVELDIR, "*.lvl"))

BLOCK_NUM_WIDTH = 20
BLOCK_NUM_HEIGHT = 20

MB_LEFT = 1
MB_MIDDLE = 2
MB_RIGHT = 3
MB_WHEEL_UP = 4
MB_WHEEL_DOWN = 5


MENU_COLORS = (pygame.Color("#152642"), pygame.Color("#254373"))
MENU_PADDING = (10, 10)