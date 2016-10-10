from inventory import Inventory

class Player:         
    def __init__(self, name, position):
        self.start_position = position
        self.position = position
        self.effects = []
        self.inventory = Inventory()
        self.name = name
        self.field = 0
        self.active = True

    def event(self, game, event):
        prevent_default = False
        for effect in self.effects:
            if effect.event(game, self, event):
                prevent_default = True
        return prevent_default

    def die(self, game):
        if self.event(game, "die"):
            return
        game.log(self, "Вы умерли")
        game.field[self.position].loot.update(self.inventory)
        self.inventory = Inventory()
        self.position = self.start_position
        self.field = 0
        self.effects = []

    def add_effect(self, game, effect):
        self.effects.append(effect)
        self.effects[-1].event(game, self, "start")

    def __str__(self):
        return self.name
