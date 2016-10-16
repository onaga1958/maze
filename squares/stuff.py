from .square import Square
from inventory import Inventory

class Stuff(Square):
    def __init__(self, objects, message=None):
        self.message = message
        self.loot = Inventory(objects)


