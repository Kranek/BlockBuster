

class LevelLoader:

    def __init__(self):
        pass

    @staticmethod
    def load(filename):
        level_arr = []
        with open(filename) as level:
            for row in level:
                level_arr.append(list(int(x) for x in row.strip()))
        for i in xrange(len(level_arr), 20):
            level_arr.append([0 for x in xrange(0, 20)])
        return level_arr