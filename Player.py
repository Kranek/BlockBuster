"""
This file contains player
"""

class Player(object):
    """
    Player is a container for the name, score and lives
    """
    def __init__(self, name):
        """
        Init with name
        :param name: Player name
        :return:
        """
        self.name = name
        self.score = 0
        self.lives = 3

    def add_points(self, points):
        """
        Used to trigger special events under certain conditions, when adding points
        :param points: Amount of points to add
        :return:
        """
        # add life if there is enough points...
        self.score += points

    def add_lives(self, lives=1):
        """
        Will be used to play extra-life sound (if sounds are going to be added and
        implemented)
        :param lives: Amount of lives to add (usually 1)
        :return:
        """
        self.lives += lives
