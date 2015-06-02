from Item import Item
from ImageManager import ImageManager

class ItemLife(Item):
    def __init__(self, x, y):
        Item.__init__(self, x, y)
        self.image = ImageManager.itemLife