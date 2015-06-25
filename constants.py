"""
Constants used in the BlockBuster
"""
import glob
from pygame import Color

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

PADDLE_HEIGHT = 15
PADDLE_WIDTHS = [40, 60, 120, 180]
PADDLE_DEFAULT_WIDTH_INDEX = 1

MENU_COLORS = (Color("#152642"), Color("#254373"))
MENU_PADDING = (10, 10)


def update_level_count():
    """
    Helper function used to refresh level count
    :return:
    """
    global MAX_LEVEL
    MAX_LEVEL = len(glob.glob1(LEVELDIR, "*.lvl"))

def get_level_count():
    """
    Helper function used to get level count
    :return:
    """
    return MAX_LEVEL
