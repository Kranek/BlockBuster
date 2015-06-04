from Block import Block
from AssetManager import AssetManager


class BlockExplosive(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y, 0)
        self.image = AssetManager.blockE

    def kill(self):
        self.dead = True
        return False