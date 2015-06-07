from constants import *


# noinspection PyUnusedLocal
class LevelLoader:
    def __init__(self):
        pass

    @staticmethod
    def load(filename):
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

        for i in xrange(len(level_arr), BLOCK_NUM_HEIGHT):
            level_arr.append(['0' for x in xrange(0, BLOCK_NUM_WIDTH)])

        for i in xrange(len(items_arr), BLOCK_NUM_HEIGHT):
            items_arr.append([0 for x in xrange(0, BLOCK_NUM_WIDTH)])

        return level_arr, items_arr
