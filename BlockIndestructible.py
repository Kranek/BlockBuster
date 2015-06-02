from Block import Block
from ImageManager import ImageManager


class BlockIndestructible(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y, 0)
        self.image = ImageManager.blockI

    def onCollide(self):
        return False