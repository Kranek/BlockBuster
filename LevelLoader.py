"""
This file contains Level Loader helper class
"""
from constants import BLOCK_NUM_WIDTH, BLOCK_NUM_HEIGHT

class LevelLoader(object):
    """
    Level Loader allows you to load level file. Outputs character array
    """
    def __init__(self):
        pass

    @staticmethod
    def load(filename):
        """
        Loads level from file
        :param filename: Level file name
        :return: Character array
        """
        level_arr = []
        items_arr = []
        with open(filename) as level:
            array_change = False
            for row in level:
                if row == "-\n":
                    array_change = True
                elif not array_change:
                    level_arr.append(list(x for x in row.strip()))
                else:
                    items_arr.append(list(int(x) for x in row.strip()))

        for _ in xrange(len(level_arr), BLOCK_NUM_HEIGHT):
            level_arr.append(['0' for _ in xrange(0, BLOCK_NUM_WIDTH)])

        for _ in xrange(len(items_arr), BLOCK_NUM_HEIGHT):
            items_arr.append([0 for _ in xrange(0, BLOCK_NUM_WIDTH)])

        return level_arr, items_arr

    @staticmethod
    def dummy():
        """
        Dummy method
        :return:
        """
        pass
