from Block import Block
from AssetManager import AssetManager


class BlockIndestructible(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y, 0)
        self.image = AssetManager.blockI

    def onCollide(self):
        return self.kill()

    def kill(self):
        return False