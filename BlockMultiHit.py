from Block import Block
from ImageManager import ImageManager


class BlockMultiHit(Block):
    def __init__(self, x, y):
        Block.__init__(self, x, y, 2)
        self.image = ImageManager.blocksM[2]

    def onCollide(self):
        if self.type <= 0:
            return self.kill()
        else:
            self.type -= 1
            self.image = ImageManager.blocksM[self.type]
            return False

    def kill(self):
        self.dead = True
        return 400