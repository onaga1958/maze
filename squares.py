from inventory import Inventory

class Square:
    def __init__(self, message=None):
        self.loot = Inventory()
        self.message = message

    def can_move(self, game, player, direction):
        return None

    def event(self, game, player, event):
        if event == "arrive": 
            if self.loot:
                game.log(player, "Найдены предметы: {}".format(self.loot))
                player.inventory.update(self.loot)
                self.loot = Inventory()
            if self.message:
                game.log(self.message)

class EffectorSquare(Square):
    def __init__(self, effect_class, message=None):
        super(EffectorSquare, self).__init__(message)
        self.effect_class = effect_class

    def event(self, game, player, event):
        super(EffectorSquare, self).event(game, player, event)
        if event == "arrive":
            player.add_effect(game, self.effect_class())

class Exit(Square):
    def __init__(self, direction):
        super(Exit, self).__init__()
        self.direction = direction

    def can_move(self, game, player, direction):
        if direction == self.direction:
            if "сокровище" in player.inventory:
                game.log("Вы вышли из лабиринта. Победа!")
                game.win(player)
            else:
                game.log("Вы уперлись в закрытую дверь")
        return None

class RubberRoom(Square):
    def __init__(self, direction):
        super(RubberRoom, self).__init__()
        self.direction = direction

    def can_move(self, game, player, direction):
        if direction == self.direction:
            game.log("Вы вышли из резиновой комнаты")
            return None
        return True

class Stuff(Square):
    def __init__(self, objects, message=None):
        self.message = message
        self.loot = Inventory(objects)

class Hole(Square):
    def __init__(self, target):
        super(Hole, self).__init__()
        self.target = target

    def event(self, game, player, event):
        super(Hole, self).event(game, player, event)
        if event == "arrive":
            game.log(player, "Вы попали в ДЫРУ.")
            player.position = self.target

class Armory(Square):
    obj = "патрон"
    count = 3

    def event(self, game, player, event):
        super(Armory, self).event(game, player, event)
        if event == "arrive":
            while player.inventory.count(self.obj) < self.count:
                player.inventory.add(self.obj)
            game.log(player, "Вы попали на склад - теперь у вас есть {} x{}".format(self.obj, self.count))

class River(Square):
    def __init__(self, destination):
        super(River, self).__init__()
        self.destination = destination

    def event(self, game, player, event):
        super(River, self).event(game, player, event)
        if event == "start_turn":
            player.position = self.destination
            player.event(game, "arrive")
    
