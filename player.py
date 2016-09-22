from inventory import Inventory

class Player:         
    def __init__(self, name, position):
        self.start_position = position
        self.position = position
        self.effects = []
        self.inventory = Inventory()
        self.name = name

    def event(self, game, event):
        prevent_default = False
        for effect in self.effects:
            if effect.event(game, self, event):
                prevent_default = True

    def die(self):
        self.inventory = Inventory()
        self.position = self.start_position

    def __str__(self):
        return self.name
