from Block import Block
from ImageManager import ImageManager


class BlockExplosive(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y, 0)
        self.image = ImageManager.blockE

    def kill(self):
        self.dead = True
        return False