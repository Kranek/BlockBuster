from Block import Block
from AssetManager import AssetManager


class BlockMultiHit(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y, 2)
        self.image = AssetManager.blocksM[2]

    def onCollide(self):
        if self.type <= 0:
            return self.kill()
        else:
            self.type -= 1
            self.image = AssetManager.blocksM[self.type]
            return False

    def kill(self):
        self.dead = True
        return 400