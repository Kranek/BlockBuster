from Item import Item
from AssetManager import AssetManager

class ItemLife(Item):
    def __init__(self, x, y):
        Item.__init__(self, x, y)
        self.image = AssetManager.itemLife